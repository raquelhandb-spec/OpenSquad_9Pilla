'use strict';

/**
 * market-data.js — Módulo único de dados de mercado.
 *
 * Regra de ouro: DADO REAL OU NADA. Nunca preenche valor "plausível".
 *
 * Ativos obrigatórios do Morning Call (definidos pela Raquel):
 *   IBOV (^BVSP), BOVA11, PETR4, VALE3, ITUB4, Dólar (USD-BRL),
 *   Petróleo Brent (BZ=F) e WTI (CL=F) enquanto a guerra não estiver resolvida.
 *
 * Fontes (com fallback automático, correto-ou-nada):
 *  1) brapi.dev   — ações B3 e índice (^BVSP); dólar via /v2/currency
 *  2) Yahoo Finance (query1.finance.yahoo.com) — BACKUP sem token; ÚNICA
 *     fonte de Brent/WTI (commodities) e cobre NY se precisar
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
  const meta =
    json && json.chart && json.chart.result && json.chart.result[0] &&
    json.chart.result[0].meta;
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

async function fetchSelic() {
  const json = await getJson(BCB_SELIC_URL);
  const row = Array.isArray(json) && json[json.length - 1];
  if (!row || row.valor == null) throw new Error('BCB sem dado de Selic');
  const value = Number(String(row.valor).replace(',', '.'));
  if (!isFiniteNumber(value)) throw new Error('BCB Selic inválida');
  return { value, asOf: row.data || null, source: 'bcb' };
}

/* ---------------- Enriquecimento (brapi pago): destaques do pregão ---------------- */

/**
 * Maiores altas e baixas do dia via /quote/list (requer brapi pago).
 * Best-effort: se falhar, retorna null (NUNCA derruba o Morning Call).
 */
async function fetchTopMovers({ baseUrl = DEFAULT_BASE_URL, token, n = 3 } = {}) {
  if (!token) return null; // recurso do brapi pago
  async function side(order) {
    const url = `${baseUrl}/quote/list?type=stock&sortBy=change&sortOrder=${order}&limit=${n}&token=${token}`;
    const json = await getJson(url, { Authorization: `Bearer ${token}` });
    const list = (json && json.stocks) || [];
    return list
      .slice(0, n)
      .map((s) => ({ ticker: s.stock, change: Number(s.change), close: Number(s.close) }))
      .filter((x) => isFiniteNumber(x.change));
  }
  try {
    const [altas, baixas] = await Promise.all([side('desc'), side('asc')]);
    if (!altas.length && !baixas.length) return null;
    return { altas, baixas };
  } catch (e) {
    console.warn('⚠️  Destaques do pregão indisponíveis (brapi):', e.message);
    return null;
  }
}

/* ---------------- Orquestração com fallback ---------------- */

async function withFallback(label, primary, fallback) {
  try {
    return await primary();
  } catch (e1) {
    try {
      const r = await fallback();
      console.warn(`⚠️  ${label}: fonte principal falhou (${e1.message}). Usei backup.`);
      return r;
    } catch (e2) {
      throw new Error(
        `${label} não pôde ser confirmado em nenhuma fonte. principal: ${e1.message} | backup: ${e2.message}`
      );
    }
  }
}

const noBrapi = () => Promise.reject(new Error('sem token brapi'));

/**
 * Busca os 8 ativos obrigatórios do Morning Call.
 * brapi principal (B3) + Yahoo backup; Brent/WTI só via Yahoo.
 * Lança erro se QUALQUER um falhar (correto-ou-nada).
 */
async function fetchMorningCallData({ baseUrl = DEFAULT_BASE_URL, token } = {}) {
  const useBrapi = !!token && token !== '';
  const brapiQuote = (t) => (useBrapi ? () => fetchQuoteBrapi(baseUrl, token, t) : noBrapi);

  const jobs = {
    ibov: withFallback('IBOV', brapiQuote('^BVSP'), () => fetchQuoteYahoo('^BVSP')),
    bova11: withFallback('BOVA11', brapiQuote('BOVA11'), () => fetchQuoteYahoo('BOVA11.SA')),
    petr4: withFallback('PETR4', brapiQuote('PETR4'), () => fetchQuoteYahoo('PETR4.SA')),
    vale3: withFallback('VALE3', brapiQuote('VALE3'), () => fetchQuoteYahoo('VALE3.SA')),
    itub4: withFallback('ITUB4', brapiQuote('ITUB4'), () => fetchQuoteYahoo('ITUB4.SA')),
    dolar: withFallback(
      'Dólar',
      useBrapi ? () => fetchCurrencyBrapi(baseUrl, token, 'USD-BRL') : noBrapi,
      () => fetchQuoteYahoo('BRL=X')
    ),
    brent: withFallback('Brent', () => fetchQuoteYahoo('BZ=F'), () => fetchQuoteYahoo('BZ=F')),
    wti: withFallback('WTI', () => fetchQuoteYahoo('CL=F'), () => fetchQuoteYahoo('CL=F')),
  };

  const keys = Object.keys(jobs);
  const results = await Promise.all(keys.map((k) => jobs[k]));
  const out = {};
  const labels = {
    ibov: 'IBOV', bova11: 'BOVA11', petr4: 'PETR4', vale3: 'VALE3',
    itub4: 'ITUB4', dolar: 'Dólar', brent: 'Petróleo Brent', wti: 'Petróleo WTI',
  };
  keys.forEach((k, i) => (out[k] = { ticker: labels[k], ...results[i] }));
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

/** Índice em PONTOS. Ex: "🟢 IBOV: 173.295 pts (+0,76%)" */
function formatIndexLine(asset) {
  return `${emojiFor(asset.changePercent)} ${asset.ticker}: ${brNumber(asset.price, 0)} pts (${signed(asset.changePercent)})`;
}

/** Preço em R$. Ex: "🔴 PETR4: R$ 38,07 (-0,99%)" */
function formatPriceLine(asset, decimals = 2) {
  return `${emojiFor(asset.changePercent)} ${asset.ticker}: R$ ${brNumber(asset.price, decimals)} (${signed(asset.changePercent)})`;
}

/** Preço em US$ (commodities). Ex: "🔴 Petróleo Brent: US$ 72,52 (-1,20%)" */
function formatUsdLine(asset, decimals = 2) {
  return `${emojiFor(asset.changePercent)} ${asset.ticker}: US$ ${brNumber(asset.price, decimals)} (${signed(asset.changePercent)})`;
}

/** Formata os destaques do pregão (maiores altas/baixas). Vazio se null. */
function formatTopMovers(tm) {
  if (!tm) return '';
  const fmt = (m) => `${m.ticker} ${signed(m.change)}`;
  const altas = tm.altas.map(fmt).join(', ');
  const baixas = tm.baixas.map(fmt).join(', ');
  return `📈 Maiores altas: ${altas}\n📉 Maiores baixas: ${baixas}`;
}

/** Monta o bloco "MERCADO AGORA" com os 8 ativos, na ordem da Raquel. */
function formatMarketBlock(data) {
  return [
    formatIndexLine(data.ibov),
    formatPriceLine(data.bova11, 2),
    formatPriceLine(data.petr4, 2),
    formatPriceLine(data.vale3, 2),
    formatPriceLine(data.itub4, 2),
    formatPriceLine(data.dolar, 2),
    formatUsdLine(data.brent, 2),
    formatUsdLine(data.wti, 2),
  ].join('\n');
}

module.exports = {
  DEFAULT_BASE_URL,
  fetchMorningCallData,
  fetchSelic,
  fetchTopMovers,
  fetchQuoteYahoo,
  formatMarketBlock,
  formatTopMovers,
  formatIndexLine,
  formatPriceLine,
  formatUsdLine,
  brNumber,
};
