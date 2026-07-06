#!/usr/bin/env node
'use strict';

/**
 * generate-editorial.js — Escreve o Morning Call EDITORIAL do dia, na voz da
 * Raquel, usando o Claude (API) + dados reais do brapi Pro + notícias.
 *
 * É o passo que o pipeline antigo não tinha: um LLM ESCREVE o conteúdo no
 * formato editorial (cabeçalho, intro do café, Termômetro, 3 notícias com
 * análise, Pílula de Sabedoria, assinatura). A "voz" vem de
 * .claude/morning-call/PROMPT-EDITORIAL.md.
 *
 * Env: ANTHROPIC_API_KEY (obrigatório), BRAPI_TOKEN (dados de mercado).
 *
 * Correto-ou-nada: os dados de mercado são buscados e ENTREGUES ao modelo; o
 * modelo é instruído a nunca inventar número. Se ANTHROPIC_API_KEY faltar, sai
 * com erro para o Action cair no fallback (esqueleto).
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

const market = require('./lib/market-data');
const news = require('./lib/news');

const MODEL = 'claude-opus-4-8';
const PROMPT_PATH = path.join(__dirname, '../morning-call/PROMPT-EDITORIAL.md');

function loadConfig() {
  const p = path.join(__dirname, '../config-morning-call.json');
  return fs.existsSync(p) ? JSON.parse(fs.readFileSync(p, 'utf8')) : {};
}

function formatDateISO(d) {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}
function dateExtenso(d) {
  const dias = ['Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado'];
  const meses = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'];
  return `${dias[d.getDay()]}, ${d.getDate()} de ${meses[d.getMonth()]} de ${d.getFullYear()}`;
}

/** Chama a API do Claude (raw HTTPS, no estilo dos outros scripts do projeto). */
function callClaude({ apiKey, system, user }) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({
      model: MODEL,
      max_tokens: 4000,
      system,
      messages: [{ role: 'user', content: user }],
    });
    const req = https.request(
      {
        hostname: 'api.anthropic.com',
        path: '/v1/messages',
        method: 'POST',
        headers: {
          'x-api-key': apiKey,
          'anthropic-version': '2023-06-01',
          'content-type': 'application/json',
          'content-length': Buffer.byteLength(body),
        },
      },
      (res) => {
        let data = '';
        res.on('data', (c) => (data += c));
        res.on('end', () => {
          if (res.statusCode < 200 || res.statusCode >= 300) {
            return reject(new Error(`Claude HTTP ${res.statusCode}: ${data.slice(0, 300)}`));
          }
          try {
            const json = JSON.parse(data);
            const text = (json.content || [])
              .filter((b) => b.type === 'text')
              .map((b) => b.text)
              .join('')
              .trim();
            if (!text) return reject(new Error('Claude retornou resposta vazia.'));
            resolve(text);
          } catch (e) {
            reject(new Error(`Resposta inválida do Claude: ${e.message}`));
          }
        });
      }
    );
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

/** Linha "Nome: valor (±x%)" para o digest de dados entregue ao modelo. */
function line(nome, asset, { unidade = 'R$' } = {}) {
  if (!asset || !Number.isFinite(asset.price)) return `${nome}: (indisponível)`;
  const casas = unidade === 'pts' ? 0 : 2;
  const v = market.brNumber(asset.price, casas);
  const sinal = asset.changePercent >= 0 ? '+' : '';
  const pref = unidade === 'pts' ? '' : unidade + ' ';
  const suf = unidade === 'pts' ? ' pts' : '';
  return `${nome}: ${pref}${v}${suf} (${sinal}${market.brNumber(asset.changePercent, 2)}%)`;
}

async function buildDigest({ baseUrl, token }) {
  const linhas = [];

  // 8 ativos obrigatórios (brapi + Yahoo) — correto-ou-nada
  const d = await market.fetchMorningCallData({ baseUrl, token });
  linhas.push('MERCADO BRASIL / COMMODITIES:');
  linhas.push('- ' + line('Ibovespa', d.ibov, { unidade: 'pts' }));
  linhas.push('- ' + line('BOVA11', d.bova11));
  linhas.push('- ' + line('PETR4', d.petr4));
  linhas.push('- ' + line('VALE3', d.vale3));
  linhas.push('- ' + line('ITUB4', d.itub4));
  linhas.push('- ' + line('Dólar (USD/BRL)', d.dolar));
  linhas.push('- ' + line('Petróleo Brent', d.brent, { unidade: 'US$' }));
  linhas.push('- ' + line('Petróleo WTI', d.wti, { unidade: 'US$' }));

  // Índices americanos (Yahoo) — best-effort
  const us = {};
  await Promise.all(
    [['S&P 500', '^GSPC'], ['Nasdaq', '^IXIC'], ['Dow Jones', '^DJI']].map(async ([nome, sym]) => {
      try { us[nome] = await market.fetchQuoteYahoo(sym); } catch (_) {}
    })
  );
  const usLinhas = Object.entries(us).map(([nome, a]) => '- ' + line(nome, a, { unidade: 'pts' }));
  if (usLinhas.length) { linhas.push('', 'MERCADO EUA:', ...usLinhas); }

  // Termômetro macro (Selic/CDI/IPCA/juro real) — best-effort
  const macro = await market.fetchMacro({ baseUrl, token });
  const term = market.formatTermometro(macro);
  if (term) linhas.push('', 'MACRO:', term);

  // Destaques do pregão — best-effort
  const tm = await market.fetchTopMovers({ baseUrl, token });
  const dest = market.formatTopMovers(tm);
  if (dest) linhas.push('', 'DESTAQUES DO PREGÃO:', dest);

  // Notícias reais do dia
  let headlines = [];
  try { headlines = await news.fetchHeadlines({ limit: 6 }); } catch (_) {}
  if (headlines.length) {
    linhas.push('', 'NOTÍCIAS REAIS DE HOJE (use as mais relevantes, cite a fonte):');
    headlines.forEach((h) => linhas.push(`- ${h.title}${h.source ? ` (${h.source})` : ''}`));
  }

  return linhas.join('\n');
}

async function main() {
  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) throw new Error('ANTHROPIC_API_KEY não definido (editorial requer o Claude).');

  const now = new Date();
  const cfg = loadConfig();
  const baseUrl = (cfg.brapi && cfg.brapi.baseUrl) || market.DEFAULT_BASE_URL;
  const token = cfg.brapi && cfg.brapi.token;

  console.log('1️⃣  Buscando dados reais (brapi + índices EUA + notícias)...');
  const digest = await buildDigest({ baseUrl, token });
  console.log(digest + '\n');

  const system = fs.readFileSync(PROMPT_PATH, 'utf8');
  const user =
    `Hoje é ${dateExtenso(now)}.\n\n` +
    `Dados reais de hoje (NÃO invente nenhum número; use exatamente estes, ` +
    `e a referência de fechamento quando fizer sentido):\n\n${digest}\n\n` +
    `Escreva o Morning Call editorial de HOJE seguindo EXATAMENTE a estrutura e a ` +
    `voz definidas. Responda APENAS com o texto final do Morning Call, pronto para ` +
    `copiar e colar — sem comentários seus, sem markdown de bloco de código.`;

  console.log('2️⃣  Escrevendo o editorial na voz da Raquel (Claude)...');
  const texto = await callClaude({ apiKey, system, user });

  const outPath = path.join(__dirname, '../../content/morning-call', `${formatDateISO(now)}.md`);
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  fs.writeFileSync(outPath, texto + '\n', 'utf8');
  console.log(`3️⃣  ✅ Editorial salvo: ${outPath}`);
  process.exit(0);
}

main().catch((err) => {
  console.error('❌ Falha ao gerar o editorial:', err.message);
  process.exit(1);
});
