'use strict';

/**
 * market-data.js — Módulo único de dados de mercado.
 *
 * Regra de ouro: DADO REAL OU NADA. Nunca preenche valor "plausível".
 *
 * Fontes (com fallback automático, correto-ou-nada):
 *  1) brapi.dev   — ações B3 e índice (^BVSP); dólar via /v2/currency
 *  2) Yahoo Finance (query1.finance.yahoo.com) — BACKUP sem token; cobre
 *     também NY (^GSPC, ^IXIC, ^DJI) e commodities (BZ=F Brent, CL=F WTI)
 *  3) Banco Central (API SGS, série 432) — Meta Selic OFICIAL
 *
 * Se um ativo obrigatório falhar em TODAS as fontes, LANÇA erro. Quem chama
 * aborta, e o pipeline nunca envia dado errado pra Turma.
 */

const https = require('https');

const DEFAULT_BASE_URL = 'https://brapi.dev/api';
const YAHOO_BASE = 'https://query1.finance.yahoo.com/v8/finance/chart/';
const BCB_SELIC_URL =
  'https://api.bcb.gov.br/dados/serie/bcdados.sgs.432/dados/ultimos/1?formato=json';
const REQUEST_TIMEOUT_MS = 15000;
const UA =
  'Mozilla/5.0 (compatible; 9PillaMorningCall/1.0; +https://9pilla.link)';

/** GET genérico que devolve JSON, ou lança erro com status/corpo. */
function getJson(url, headers = {}) {
  return new Promise((resolve, reject) => {
    const req = https.get(
      url,
      { timeout: REQUEST_TIMEOUT_MS, headers: { 'User-Agent': UA, ...headers } },
      (res) => {
        let data = '';
        res.on('data', (chunk) => (data += chunk));
        res.on('end', () => {
          if (res.statusCode < 200 || res.statusCode >= 300) {
            return reject(
              new Error(`HTTP ${res.statusCode} em ${url} :: ${data.slice(0, 160)}`)
            );
          }
          try {
            resolve(JSON.parse(data));
          } catch (e) {
            reject(new Error(`Resposta não-JSON em ${url}: ${e.message}`));
          }
        });
      }
    );
    req.on('timeout', () => req.destroy(new Error(`Timeout em ${url}`)));
    req.on('error', reject);
  });
}

function isFiniteNumber(v) {
  return typeof v === 'number' && Number.isFinite(v);
}

/* ---------------- Fonte 1: brapi ---------------- */

async function fetchQuoteBrapi(baseUrl, token, ticker) {
  const url = `${baseUrl}/quote/${encodeURIComponent(ticker)}?token=${token}`;
  const json = await getJson(url, { Authorization: `Bearer ${token}` });
  const q = json && json.results && json.results[0];
  if (!q) throw new Error(`brapi sem resultado para ${ticker}`);
  const price = Number(q.regularMarketPrice);
  const changePercent = Number(q.regularMarketChangePercent);
  if (!isFiniteNumber(price) || !isFiniteNumber(changePercent)) {
    throw new Error(`brapi dados inválidos para ${ticker}`);
  }
  return { price, changePercent, asOf: q.regularMarketTime || null, source: 'brapi' };
}

async function fetchCurrencyBrapi(baseUrl, token, pair = 'USD-BRL') {
  const url = `${baseUrl}/v2/currency?currency=${encodeURIComponent(pair)}&token=${token}`;
  const json = await getJson(url, { Authorization: `Bearer ${token}` });
  const c = json && json.currency && json.currency[0];
  if (!c) throw new Error(`brapi sem resultado para ${pair}`);
  const price = Number(c.bidPrice);
  const changePercent = Number(c.percentageChange);
  if (!isFiniteNumber(price) || !isFiniteNumber(changePercent)) {
    throw new Error(`brapi dados inválidos para ${pair}`);
  }
  return { price, changePercent, asOf: c.updatedAtDate || null, source: 'brapi' };
}

/* ---------------- Fonte 2: Yahoo Finance (backup, sem token) ---------------- */

async function fetchQuoteYahoo(symbol) {
  const url = `${YAHOO_BASE}${encodeURIComponent(symbol)}?interval=1d&range=1d`;
  const json = await getJson(url);
  const meta = json && json.chart && json.chart.result && json.chart.result[0]
    && json.chart.result[0].meta;
  if (!meta) throw new Error(`Yahoo sem resultado para ${symbol}`);
  const price = Number(meta.regularMarketPrice);
  const prev = Number(meta.chartPreviousClose ?? meta.previousClose);
  if (!isFiniteNumber(price) || !isFiniteNumber(prev) || prev === 0) {
    throw new Error(`Yahoo dados inválidos para ${symbol}`);
  }
  const changePercent = ((price - prev) / prev) * 100;
  return { price, changePercent, asOf: meta.regularMarketTime || null, source: 'yahoo' };
}

/* ---------------- Fonte 3: Banco Central (Selic oficial) ---------------- */

/** Meta Selic vigente (% a.a.), direto da API SGS do BCB (série 432). */
async function fetchSelic() {
  const json = await getJson(BCB_SELIC_URL);
  const row = Array.isArray(json) && json[json.length - 1];
  if (!row || row.valor == null) throw new Error('BCB sem dado de Selic');
  const value = Number(String(row.valor).replace(',', '.'));
  if (!isFiniteNumber(value)) throw new Error('BCB Selic inválida');
  return { value, asOf: row.data || null, source: 'bcb' };
}

/* ---------------- Orquestração com fallback ---------------- */

async function withFallback(label, primary, fallback) {
  try {
    return await primary();
  } catch (e1) {
    try {
      const r = await fallback();
      console.warn(`⚠️  ${label}: brapi falhou (${e1.message}). Usei Yahoo como backup.`);
      return r;
    } catch (e2) {
      throw new Error(
        `${label} não pôde ser confirmado em nenhuma fonte. brapi: ${e1.message} | yahoo: ${e2.message}`
      );
    }
  }
}

/**
 * Busca os 5 ativos obrigatórios do Morning Call, com brapi + fallback Yahoo.
 * Lança erro se QUALQUER um falhar em ambas as fontes (correto-ou-nada).
 */
async function fetchMorningCallData({ baseUrl = DEFAULT_BASE_URL, token } = {}) {
  const useBrapi = !!token && token !== '';

  const ibovP = withFallback(
    'IBOV',
    () => (useBrapi ? fetchQuoteBrapi(baseUrl, token, '^BVSP') : Promise.reject(new Error('sem token brapi'))),
    () => fetchQuoteYahoo('^BVSP')
  );
  const petrP = withFallback(
    'PETR4',
    () => (useBrapi ? fetchQuoteBrapi(baseUrl, token, 'PETR4') : Promise.reject(new Error('sem token brapi'))),
    () => fetchQuoteYahoo('PETR4.SA')
  );
  const valeP = withFallback(
    'VALE3',
    () => (useBrapi ? fetchQuoteBrapi(baseUrl, token, 'VALE3') : Promise.reject(new Error('sem token brapi'))),
    () => fetchQuoteYahoo('VALE3.SA')
  );
  const itubP = withFallback(
    'ITUB4',
    () => (useBrapi ? fetchQuoteBrapi(baseUrl, token, 'ITUB4') : Promise.reject(new Error('sem token brapi'))),
    () => fetchQuoteYahoo('ITUB4.SA')
  );
  const dolarP = withFallback(
    'Dólar',
    () => (useBrapi ? fetchCurrencyBrapi(baseUrl, token, 'USD-BRL') : Promise.reject(new Error('sem token brapi'))),
    () => fetchQuoteYahoo('BRL=X')
  );

  const [ibov, petr4, vale3, itub4, dolar] = await Promise.all([
    ibovP, petrP, valeP, itubP, dolarP,
  ]);

  return {
    ibov: { ticker: 'IBOV', ...ibov },
    dolar: { ticker: 'Dólar', ...dolar },
    petr4: { ticker: 'PETR4', ...petr4 },
    vale3: { ticker: 'VALE3', ...vale3 },
    itub4: { ticker: 'ITUB4', ...itub4 },
  };
}

/**
 * Bloco internacional (NY + commodities), só via Yahoo (brapi não cobre bem).
 * Não é obrigatório: se falhar, retorna o que conseguiu e marca os ausentes.
 */
async function fetchGlobalData() {
  const symbols = [
    ['sp500', '^GSPC', 'S&P 500'],
    ['nasdaq', '^IXIC', 'Nasdaq'],
    ['dow', '^DJI', 'Dow Jones'],
    ['brent', 'BZ=F', 'Petróleo Brent'],
    ['wti', 'CL=F', 'Petróleo WTI'],
  ];
  const out = {};
  await Promise.all(
    symbols.map(async ([key, sym, label]) => {
      try {
        out[key] = { ticker: label, ...(await fetchQuoteYahoo(sym)) };
      } catch (e) {
        out[key] = { ticker: label, error: e.message };
      }
    })
  );
  return out;
}

/* ---------------- Formatação pt-BR ---------------- */

function brNumber(value, decimals) {
  return value.toLocaleString('pt-BR', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
}

function emojiFor(changePercent) {
  return changePercent >= 0 ? '🟢' : '🔴';
}

function signed(changePercent) {
  const s = changePercent >= 0 ? '+' : '';
  return `${s}${brNumber(changePercent, 2)}%`;
}

/** Linha de índice em PONTOS. Ex: "🟢 IBOV: 173.295 pts (+0,76%)" */
function formatIndexLine(asset) {
  return `${emojiFor(asset.changePercent)} ${asset.ticker}: ${brNumber(asset.price, 0)} pts (${signed(asset.changePercent)})`;
}

/** Linha de preço em R$. Ex: "🔴 PETR4: R$ 38,07 (-0,99%)" */
function formatPriceLine(asset, decimals = 2) {
  return `${emojiFor(asset.changePercent)} ${asset.ticker}: R$ ${brNumber(asset.price, decimals)} (${signed(asset.changePercent)})`;
}

function formatMarketBlock(data) {
  return [
    formatIndexLine(data.ibov),
    formatPriceLine(data.dolar, 2),
    formatPriceLine(data.petr4, 2),
    formatPriceLine(data.vale3, 2),
    formatPriceLine(data.itub4, 2),
  ].join('\n');
}

module.exports = {
  DEFAULT_BASE_URL,
  fetchMorningCallData,
  fetchGlobalData,
  fetchSelic,
  fetchQuoteYahoo,
  formatMarketBlock,
  formatIndexLine,
  formatPriceLine,
  brNumber,
};
