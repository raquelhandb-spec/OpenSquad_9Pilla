#!/usr/bin/env node
'use strict';

/**
 * generate-editorial.js — Escreve o Morning Call EDITORIAL do dia como um
 * ANALISTA SÊNIOR: faz o dever de casa (pesquisa web em Investing/InfoMoney para
 * o Brasil e Bloomberg para o global), monta um Termômetro rico com dados reais,
 * e escreve na voz da Raquel — SEM citar fontes.
 *
 * Como funciona:
 *  1) Busca números precisos (brapi Pro para B3/câmbio + Yahoo para índices EUA,
 *     futuros, VIX, ouro, bitcoin). Tudo best-effort: o que não vier, o modelo
 *     pesquisa.
 *  2) Chama o Claude (claude-opus-4-8) com as ferramentas web_search + web_fetch
 *     e o PROMPT-EDITORIAL.md como voz/estrutura. O modelo pesquisa o calendário
 *     econômico e as notícias do dia nas fontes certas.
 *
 * Env: ANTHROPIC_API_KEY (obrigatório), BRAPI_TOKEN (dados de mercado).
 * Correto-ou-nada: o modelo é instruído a nunca inventar número nem evento.
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

const market = require('./lib/market-data');
const content = require('./lib/content');

const MODEL = 'claude-opus-4-8';
const PROMPT_PATH = path.join(__dirname, '../morning-call/PROMPT-EDITORIAL.md');
const MAX_TOOL_TURNS = 8; // pause_turn: continua a pesquisa server-side

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

/** Uma requisição à Messages API do Claude (raw HTTPS). Retorna o JSON. */
function anthropicRequest(apiKey, payload) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify(payload);
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
        timeout: 240000,
      },
      (res) => {
        let data = '';
        res.on('data', (c) => (data += c));
        res.on('end', () => {
          if (res.statusCode < 200 || res.statusCode >= 300) {
            return reject(new Error(`Claude HTTP ${res.statusCode}: ${data.slice(0, 400)}`));
          }
          try { resolve(JSON.parse(data)); }
          catch (e) { reject(new Error(`Resposta inválida do Claude: ${e.message}`)); }
        });
      }
    );
    req.on('timeout', () => req.destroy(new Error('Timeout na API do Claude')));
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

/**
 * Chama o Claude com ferramentas de pesquisa web, resolvendo o loop de
 * server-tools (stop_reason "pause_turn") até a resposta final.
 */
async function callClaudeResearch({ apiKey, system, user }) {
  const tools = [
    { type: 'web_search_20260209', name: 'web_search' },
    { type: 'web_fetch_20260209', name: 'web_fetch' },
  ];
  let messages = [{ role: 'user', content: user }];

  for (let turn = 0; turn < MAX_TOOL_TURNS; turn++) {
    const res = await anthropicRequest(apiKey, {
      model: MODEL,
      max_tokens: 8000,
      system,
      tools,
      messages,
    });
    if (res.stop_reason === 'pause_turn') {
      // Server-tool loop atingiu o limite; reenvia com o parcial para continuar.
      messages = messages.concat([{ role: 'assistant', content: res.content }]);
      continue;
    }
    const text = (res.content || [])
      .filter((b) => b.type === 'text')
      .map((b) => b.text)
      .join('')
      .trim();
    if (!text) throw new Error(`Claude terminou sem texto (stop_reason: ${res.stop_reason}).`);
    return text;
  }
  throw new Error('Pesquisa web não convergiu (pause_turn demais).');
}

/** Linha "Nome: valor (±x%)" para o digest de dados entregue ao modelo. */
function line(nome, asset, unidade) {
  if (!asset || !Number.isFinite(asset.price)) return null;
  const casas = unidade === 'pts' ? 0 : 2;
  const v = market.brNumber(asset.price, casas);
  const sinal = asset.changePercent >= 0 ? '+' : '';
  const pref = unidade === 'pts' || !unidade ? '' : unidade + ' ';
  const suf = unidade === 'pts' ? ' pts' : '';
  return `- ${nome}: ${pref}${v}${suf} (${sinal}${market.brNumber(asset.changePercent, 2)}%)`;
}

/** Busca um símbolo no Yahoo, best-effort (null se falhar). */
async function yh(symbol) {
  try { return await market.fetchQuoteYahoo(symbol); } catch (_) { return null; }
}

async function buildDigest({ baseUrl, token }) {
  const out = [];

  // Núcleo B3 + câmbio + commodities (brapi principal, Yahoo backup) — correto-ou-nada
  const d = await market.fetchMorningCallData({ baseUrl, token });
  const b3 = [
    line('Ibovespa', d.ibov, 'pts'),
    line('BOVA11', d.bova11, 'R$'),
    line('PETR4', d.petr4, 'R$'),
    line('VALE3', d.vale3, 'R$'),
    line('ITUB4 (Itaú)', d.itub4, 'R$'),
    line('Dólar (USD/BRL)', d.dolar, 'R$'),
    line('Petróleo Brent', d.brent, 'US$'),
    line('Petróleo WTI', d.wti, 'US$'),
  ].filter(Boolean);
  out.push('NÚMEROS PRECISOS (use exatamente estes):', ...b3);

  // Extras via Yahoo (best-effort). O modelo pesquisa os que faltarem.
  const extras = [
    ['Banco do Brasil (BBAS3)', 'BBAS3.SA', 'R$'],
    ['Bradesco (BBDC4)', 'BBDC4.SA', 'R$'],
    ['S&P 500', '^GSPC', 'pts'],
    ['S&P 500 futuro', 'ES=F', 'pts'],
    ['Dow Jones', '^DJI', 'pts'],
    ['Dow Jones futuro', 'YM=F', 'pts'],
    ['Nasdaq', '^IXIC', 'pts'],
    ['Nasdaq futuro', 'NQ=F', 'pts'],
    ['VIX', '^VIX', ''],
    ['Ouro', 'GC=F', 'US$'],
    ['Bitcoin', 'BTC-USD', 'US$'],
  ];
  const results = await Promise.all(extras.map(([, sym]) => yh(sym)));
  extras.forEach(([nome, , unidade], i) => {
    const l = line(nome, results[i], unidade);
    if (l) out.push(l);
  });

  out.push(
    '',
    'AINDA FALTA (pesquise nas fontes certas e confirme): Ibovespa futuro, ' +
      'DI Brasil 10 anos, e qualquer item acima que não veio. Calendário econômico ' +
      'de hoje e as notícias do dia também são dever de casa.'
  );
  return out.join('\n');
}

async function main() {
  // Remove QUALQUER espaço em branco (inclui \n/\r/espaço que o copiar-colar do
  // secret pode deixar) — senão o header x-api-key é recusado pelo Node.
  const apiKey = (process.env.ANTHROPIC_API_KEY || '').replace(/\s/g, '');
  if (!apiKey) throw new Error('ANTHROPIC_API_KEY não definido (editorial requer o Claude).');

  const now = new Date();
  const cfg = loadConfig();
  const baseUrl = (cfg.brapi && cfg.brapi.baseUrl) || market.DEFAULT_BASE_URL;
  const token = cfg.brapi && cfg.brapi.token;

  console.log('1️⃣  Buscando números precisos (brapi + Yahoo)...');
  let digest = '';
  try { digest = await buildDigest({ baseUrl, token }); }
  catch (e) { console.warn('⚠️  Digest parcial:', e.message); }
  console.log(digest + '\n');

  const system = fs.readFileSync(PROMPT_PATH, 'utf8');
  const user =
    `A data de HOJE é ${dateExtenso(now)}. Essa data é REAL e ATUAL — NÃO é futura. ` +
    `As ferramentas web_search/web_fetch retornam informação atual: USE-AS e ` +
    `CONFIE nos resultados.\n\n` +
    `DEVER DE CASA (faça ANTES de escrever, pesquisando de verdade):\n` +
    `1) Calendário econômico de HOJE, por horário — pesquise em Investing Brasil ` +
    `(calendário econômico) e InfoMoney. Se conseguir confirmar os horários, inclua ` +
    `a seção 📅. Se NÃO conseguir confirmar, OMITA a seção 📅 inteira em silêncio ` +
    `(sem título, sem parágrafo, SEM pedir desculpa) — nunca escreva que a agenda ` +
    `"não veio".\n` +
    `2) Notícias que movem o mercado HOJE — Brasil (Investing/InfoMoney) e global ` +
    `(Bloomberg). Fatos, nomes e números reais e atuais.\n` +
    `3) Complete o Termômetro que faltou (Ibovespa futuro, DI 10 anos) com dado real; ` +
    `o que não confirmar, apenas omita a linha.\n\n` +
    `NÚMEROS JÁ BUSCADOS (use exatamente, não invente):\n${digest || '(nenhum — pesquise tudo)'}\n\n` +
    `REGRAS DE SAÍDA (críticas):\n` +
    `- Responda APENAS com o Morning Call final. NADA antes, NADA depois.\n` +
    `- NUNCA escreva comentários sobre o seu processo, sobre a busca, sobre a data ` +
    `ser futura, sobre o que você "vai fazer" ou "fez". Isso é PROIBIDO no texto.\n` +
    `- O texto começa DIRETO no cabeçalho "☕ *Morning Call 9Pilla*".\n` +
    `- Se depois de pesquisar de verdade um item não vier, OMITA a linha/seção em ` +
    `silêncio (sem explicar). NUNCA escreva um parágrafo pedindo desculpa por dado ` +
    `que faltou.\n` +
    `- NUNCA cite fontes no texto. Formate para WhatsApp: títulos e destaques em ` +
    `*negrito* com asterisco simples.`;

  console.log('2️⃣  Fazendo o dever de casa e escrevendo (Claude + pesquisa web)...');
  let texto = await callClaudeResearch({ apiKey, system, user });

  // Cinto de segurança: corta qualquer preâmbulo antes do ☕ e remove parágrafos
  // de bastidor/desculpa (ex: "as buscas vieram vazias", "a data é futura"). Se
  // uma seção ficar só com o título, o título também sai. A Turma recebe limpo.
  texto = content.stripMeta(texto);

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
