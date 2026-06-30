'use strict';

/**
 * news.js — Manchetes REAIS do dia (Google News RSS, pt-BR).
 *
 * Regra de ouro: NOTÍCIA REAL OU NADA.
 * Busca manchetes de fontes financeiras via RSS público (sem chave).
 * Se não conseguir manchetes reais, LANÇA erro — nunca inventa notícia.
 *
 * O RSS traz título + fonte + data. A curadoria/voz fica para a etapa
 * de redação (Nina) e a aprovação da Raquel; aqui garantimos que o
 * insumo é real e do dia.
 */

const https = require('https');

const REQUEST_TIMEOUT_MS = 15000;

function getText(url) {
  return new Promise((resolve, reject) => {
    const req = https.get(
      url,
      {
        timeout: REQUEST_TIMEOUT_MS,
        headers: {
          'User-Agent':
            'Mozilla/5.0 (compatible; 9PillaMorningCall/1.0; +https://9pilla.link)',
          Accept: 'application/rss+xml, application/xml, text/xml',
        },
      },
      (res) => {
        // Segue redirecionamento simples
        if (
          res.statusCode >= 300 &&
          res.statusCode < 400 &&
          res.headers.location
        ) {
          return resolve(getText(res.headers.location));
        }
        let data = '';
        res.on('data', (chunk) => (data += chunk));
        res.on('end', () => {
          if (res.statusCode < 200 || res.statusCode >= 300) {
            return reject(
              new Error(`HTTP ${res.statusCode} ao buscar notícias (${url})`)
            );
          }
          resolve(data);
        });
      }
    );
    req.on('timeout', () => req.destroy(new Error('Timeout ao buscar notícias')));
    req.on('error', reject);
  });
}

function decodeEntities(s) {
  return s
    .replace(/<!\[CDATA\[(.*?)\]\]>/gs, '$1')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&#(\d+);/g, (_, n) => String.fromCharCode(Number(n)))
    .trim();
}

/** Extrai itens {title, source, pubDate} de um RSS. */
function parseRssItems(xml) {
  const items = [];
  const blocks = xml.split(/<item>/i).slice(1);
  for (const block of blocks) {
    const body = block.split(/<\/item>/i)[0];
    const titleMatch = body.match(/<title>(.*?)<\/title>/s);
    const sourceMatch = body.match(/<source[^>]*>(.*?)<\/source>/s);
    const dateMatch = body.match(/<pubDate>(.*?)<\/pubDate>/s);
    if (!titleMatch) continue;
    let title = decodeEntities(titleMatch[1]);
    let source = sourceMatch ? decodeEntities(sourceMatch[1]) : '';
    // Google News costuma anexar " - Fonte" no fim do título
    if (!source) {
      const dash = title.lastIndexOf(' - ');
      if (dash > 0) {
        source = title.slice(dash + 3).trim();
        title = title.slice(0, dash).trim();
      }
    } else {
      const suffix = ` - ${source}`;
      if (title.endsWith(suffix)) title = title.slice(0, -suffix.length).trim();
    }
    items.push({
      title,
      source,
      pubDate: dateMatch ? decodeEntities(dateMatch[1]) : '',
    });
  }
  return items;
}

// Fontes preferenciais de referência (a pedido da Raquel).
// Domínios usados tanto no filtro do RSS quanto para priorizar resultados.
const PREFERRED_SOURCES = [
  { name: 'Investing.com', domain: 'investing.com' },
  { name: 'InfoMoney', domain: 'infomoney.com.br' },
  { name: 'Bloomberg Línea', domain: 'bloomberglinea.com.br' },
  { name: 'CNN Brasil', domain: 'cnnbrasil.com.br' },
];

function isPreferred(item) {
  const hay = `${item.source} ${item.title}`.toLowerCase();
  return PREFERRED_SOURCES.some(
    (s) =>
      hay.includes(s.name.toLowerCase()) ||
      hay.includes(s.domain.toLowerCase())
  );
}

/**
 * Busca manchetes reais do dia sobre mercado financeiro brasileiro,
 * priorizando Investing, InfoMoney, Bloomberg e CNN.
 *
 * Estratégia:
 *  1) Faz uma busca restrita às fontes preferenciais (site:...).
 *  2) Faz uma busca ampla como complemento/garantia.
 *  3) Junta, deduplica, coloca as fontes preferenciais primeiro.
 *
 * @param {object} opts
 * @param {string} [opts.query] termo base de busca
 * @param {number} [opts.limit] quantas manchetes retornar
 * @returns {Promise<Array<{title,source,pubDate,preferred:boolean}>>}
 * @throws se não conseguir nenhuma manchete real.
 */
async function fetchHeadlines({
  query = 'Ibovespa mercado financeiro bolsa dólar',
  limit = 5,
} = {}) {
  const siteFilter = PREFERRED_SOURCES.map((s) => `site:${s.domain}`).join(' OR ');
  const queries = [
    `${query} (${siteFilter})`, // 1) restrito às fontes preferenciais
    query, // 2) busca ampla de complemento
  ];

  const collected = [];
  for (const q of queries) {
    const url =
      'https://news.google.com/rss/search?q=' +
      encodeURIComponent(q) +
      '&hl=pt-BR&gl=BR&ceid=BR:pt-419';
    try {
      const xml = await getText(url);
      for (const item of parseRssItems(xml)) {
        if (item.title) collected.push(item);
      }
    } catch (e) {
      // Uma das buscas pode falhar; seguimos com a outra.
      console.warn(`⚠️  Falha numa busca de notícias (${q.slice(0, 40)}...): ${e.message}`);
    }
  }

  if (collected.length === 0) {
    throw new Error(
      'Nenhuma manchete real encontrada no RSS. Abortando (não inventamos notícia).'
    );
  }

  // Deduplica por título e marca/prioriza fontes preferenciais.
  const seen = new Set();
  const unique = [];
  for (const item of collected) {
    const key = item.title.toLowerCase();
    if (seen.has(key)) continue;
    seen.add(key);
    unique.push({ ...item, preferred: isPreferred(item) });
  }
  unique.sort((a, b) => Number(b.preferred) - Number(a.preferred));

  return unique.slice(0, limit);
}

module.exports = { fetchHeadlines, parseRssItems, PREFERRED_SOURCES };
