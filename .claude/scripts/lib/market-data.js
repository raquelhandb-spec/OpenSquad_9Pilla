'use strict';

/**
 * market-data.js — Módulo único de dados de mercado (brapi.dev)
 *
 * Regra de ouro: DADO REAL OU NADA.
 * - Ações e índice (^BVSP): GET /api/quote/{ticker}
 *     campos: regularMarketPrice, regularMarketChangePercent
 * - Dólar (USD/BRL):        GET /api/v2/currency?currency=USD-BRL
 *     campos: bidPrice, percentageChange
 *
 * Se qualquer ativo obrigatório não puder ser confirmado, este módulo
 * LANÇA erro. Nunca preenche valor "plausível" no lugar. Quem chama
 * decide abortar (e o pipeline nunca envia dado errado pra Turma).
 */

const https = require('https');

const DEFAULT_BASE_URL = 'https://brapi.dev/api';
const REQUEST_TIMEOUT_MS = 15000;

/** Faz GET e devolve JSON, ou lança erro com status/corpo. */
function getJson(url, token) {
  return new Promise((resolve, reject) => {
    const options = {
      timeout: REQUEST_TIMEOUT_MS,
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    };
    const req = https.get(url, options, (res) => {
      let data = '';
      res.on('data', (chunk) => (data += chunk));
      res.on('end', () => {
        if (res.statusCode < 200 || res.statusCode >= 300) {
          return reject(
            new Error(`HTTP ${res.statusCode} em ${url} :: ${data.slice(0, 200)}`)
          );
        }
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(new Error(`Resposta não-JSON em ${url}: ${e.message}`));
        }
      });
    });
    req.on('timeout', () => {
      req.destroy(new Error(`Timeout (${REQUEST_TIMEOUT_MS}ms) em ${url}`));
    });
    req.on('error', reject);
  });
}

function isFiniteNumber(v) {
  return typeof v === 'number' && Number.isFinite(v);
}

/**
 * Busca uma ação ou índice no endpoint /quote.
 * @returns {Promise<{ticker, price:number, changePercent:number, asOf:?string}>}
 * @throws se o ativo não vier com preço e variação numéricos.
 */
async function fetchQuote(baseUrl, token, ticker) {
  const url = `${baseUrl}/quote/${encodeURIComponent(ticker)}?token=${token}`;
  const json = await getJson(url, token);
  const q = json && json.results && json.results[0];
  if (!q) throw new Error(`Sem resultado para ${ticker} em /quote`);
  const price = Number(q.regularMarketPrice);
  const changePercent = Number(q.regularMarketChangePercent);
  if (!isFiniteNumber(price) || !isFiniteNumber(changePercent)) {
    throw new Error(
      `Dados inválidos para ${ticker}: price=${q.regularMarketPrice} change=${q.regularMarketChangePercent}`
    );
  }
  return {
    ticker,
    price,
    changePercent,
    asOf: q.regularMarketTime || null,
  };
}

/**
 * Busca a cotação de moeda no endpoint /v2/currency (campos diferentes!).
 * @returns {Promise<{ticker, price:number, changePercent:number, asOf:?string}>}
 */
async function fetchCurrency(baseUrl, token, pair = 'USD-BRL', label = 'Dólar') {
  const url = `${baseUrl}/v2/currency?currency=${encodeURIComponent(pair)}&token=${token}`;
  const json = await getJson(url, token);
  const c = json && json.currency && json.currency[0];
  if (!c) throw new Error(`Sem resultado para ${pair} em /v2/currency`);
  const price = Number(c.bidPrice);
  const changePercent = Number(c.percentageChange);
  if (!isFiniteNumber(price) || !isFiniteNumber(changePercent)) {
    throw new Error(
      `Dados inválidos para ${pair}: bidPrice=${c.bidPrice} percentageChange=${c.percentageChange}`
    );
  }
  return {
    ticker: label,
    price,
    changePercent,
    asOf: c.updatedAtDate || null,
  };
}

/**
 * Busca os 5 ativos obrigatórios do Morning Call.
 * IBOV (^BVSP), Dólar (USD-BRL), PETR4, VALE3, ITUB4.
 * Lança erro se QUALQUER um falhar — correto-ou-nada.
 *
 * @returns {Promise<{ibov,dolar,petr4,vale3,itub4}>} cada um {ticker,price,changePercent,asOf}
 */
async function fetchMorningCallData({ baseUrl = DEFAULT_BASE_URL, token } = {}) {
  if (!token || token === '') {
    throw new Error(
      'BRAPI token ausente. Configure config-morning-call.json (brapi.token) ou o secret BRAPI_TOKEN.'
    );
  }

  // Roda em paralelo, mas exige que TODOS retornem.
  const [ibov, petr4, vale3, itub4, dolar] = await Promise.all([
    fetchQuote(baseUrl, token, '^BVSP'),
    fetchQuote(baseUrl, token, 'PETR4'),
    fetchQuote(baseUrl, token, 'VALE3'),
    fetchQuote(baseUrl, token, 'ITUB4'),
    fetchCurrency(baseUrl, token, 'USD-BRL', 'Dólar'),
  ]);

  // Rótulos amigáveis
  ibov.ticker = 'IBOV';
  return { ibov, dolar, petr4, vale3, itub4 };
}

/* ---------- Formatação pt-BR ---------- */

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

/** Linha do índice em PONTOS (não R$). Ex: "🟢 IBOV: 173.295 pts (+0,76%)" */
function formatIndexLine(asset) {
  return `${emojiFor(asset.changePercent)} ${asset.ticker}: ${brNumber(asset.price, 0)} pts (${signed(asset.changePercent)})`;
}

/** Linha de preço em R$. Ex: "🔴 PETR4: R$ 38,07 (-0,99%)" */
function formatPriceLine(asset, decimals = 2) {
  return `${emojiFor(asset.changePercent)} ${asset.ticker}: R$ ${brNumber(asset.price, decimals)} (${signed(asset.changePercent)})`;
}

/**
 * Monta o bloco "MERCADO AGORA" a partir de dados REAIS.
 * @param {object} data resultado de fetchMorningCallData
 */
function formatMarketBlock(data) {
  const lines = [
    formatIndexLine(data.ibov),
    formatPriceLine(data.dolar, 2),
    formatPriceLine(data.petr4, 2),
    formatPriceLine(data.vale3, 2),
    formatPriceLine(data.itub4, 2),
  ];
  return lines.join('\n');
}

module.exports = {
  DEFAULT_BASE_URL,
  fetchQuote,
  fetchCurrency,
  fetchMorningCallData,
  formatMarketBlock,
  formatIndexLine,
  formatPriceLine,
  brNumber,
};
