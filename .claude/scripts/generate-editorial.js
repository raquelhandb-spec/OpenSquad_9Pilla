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
  // ATENÇÃO: índices À VISTA em NÍVEL de fechamento. Nasdaq à vista é o
  // Composite (^IXIC, ~26 mil). Os FUTUROS vêm numa linha separada, só como
  // DIREÇÃO (%), pra NUNCA misturar o nível do Composite com o do Nasdaq-100.
  const extras = [
    ['Banco do Brasil (BBAS3)', 'BBAS3.SA', 'R$'],
    ['Bradesco (BBDC4)', 'BBDC4.SA', 'R$'],
    ['S&P 500', '^GSPC', 'pts'],
    ['Dow Jones', '^DJI', 'pts'],
    ['Nasdaq (Composite)', '^IXIC', 'pts'],
    ['VIX', '^VIX', ''],
    ['Ouro', 'GC=F', 'US$'],
    ['Bitcoin', 'BTC-USD', 'US$'],
  ];
  const results = await Promise.all(extras.map(([, sym]) => yh(sym)));
  extras.forEach(([nome, , unidade], i) => {
    const l = line(nome, results[i], unidade);
    if (l) out.push(l);
  });

  // Futuros de Nova York: SÓ a direção (variação %), numa linha única. Assim a
  // gente dá a prévia do pré-mercado sem comparar nível de índices diferentes.
  const futuros = [
    ['S&P 500', 'ES=F'],
    ['Dow Jones', 'YM=F'],
    ['Nasdaq', 'NQ=F'],
  ];
  const futResults = await Promise.all(futuros.map(([, sym]) => yh(sym)));
  const futPartes = futuros
    .map(([nome], i) => {
      const a = futResults[i];
      if (!a || !Number.isFinite(a.changePercent)) return null;
      const sinal = a.changePercent >= 0 ? '+' : '';
      return `${nome} ${sinal}${market.brNumber(a.changePercent, 2)}%`;
    })
    .filter(Boolean);
  if (futPartes.length) {
    out.push(`- Futuros de NY (prévia, só a direção): ${futPartes.join(', ')}`);
  }

  // Ibovespa futuro (IND) e DI 10 anos (curva DI1) direto do brapi Pro —
  // SINCRONIZADOS com o mercado. Best-effort: o que não vier é omitido.
  const [ibovFut, di10] = await Promise.all([
    market.fetchIbovFuturo({ baseUrl, token }).catch(() => null),
    market.fetchDI10y({ baseUrl, token }).catch(() => null),
  ]);
  if (ibovFut && Number.isFinite(ibovFut.price)) {
    const sinal = ibovFut.changePercent >= 0 ? '+' : '';
    const varTxt = Number.isFinite(ibovFut.changePercent)
      ? ` (${sinal}${market.brNumber(ibovFut.changePercent, 2)}%)`
      : '';
    out.push(`- Ibovespa futuro: ${market.brNumber(ibovFut.price, 0)} pts${varTxt}`);
  }
  if (di10 && Number.isFinite(di10.rate)) {
    out.push(`- DI Brasil 10 anos: ${market.brNumber(di10.rate, 2)}% ao ano`);
  }

  out.push(
    '',
    'REGRA DO TERMÔMETRO: mostre os índices dos EUA em NÍVEL de fechamento (o ' +
      'Nasdaq é o Composite, ~26 mil). Para os futuros, use SÓ a linha "Futuros de ' +
      'NY" acima (direção em %). NUNCA escreva algo como "Nasdaq 26.214 | futuro ' +
      '29.172" — isso compara índices diferentes e é dado errado.',
    '',
    'IBOV FUTURO E DI 10 ANOS: use SOMENTE se aparecerem como linha acima (vêm do ' +
      'brapi, sincronizados). Se NÃO estiverem acima, OMITA essas linhas — é ' +
      'PROIBIDO buscá-los na web ou estimar, porque número solto não bate com o ' +
      'à vista (dado errado). Melhor a linha não existir.',
    '',
    'DEVER DE CASA (pesquise nas fontes certas): apenas o Calendário econômico de ' +
      'hoje e as notícias do dia. Os números do termômetro já estão todos acima.'
  );
  return out.join('\n');
}

async function main() {
  // Remove QUALQUER espaço em branco (inclui \n/\r/espaço que o copiar-colar do
  // secret pode deixar) — senão o header x-api-key é recusado pelo Node.
  const apiKey = (process.env.ANTHROPIC_API_KEY || '').replace(/\s/g, '');
  if (!apiKey) throw new Error('ANTHROPIC_API_KEY não definido (editorial requer o Claude).');

  const now = new Date();
  // Horário de Brasília (UTC-3): decide a EDIÇÃO. Manhã = Morning Call (☕, 09h09);
  // meio-dia em diante = Giro 9Pilla (🔄, hora atual), um resumo intraday/tarde.
  const brt = new Date(now.getTime() - 3 * 3600 * 1000);
  const brtHour = brt.getUTCHours();
  const brtMin = brt.getUTCMinutes();
  const isGiro = brtHour >= 12;
  const horaAtual = `${String(brtHour).padStart(2, '0')}h${String(brtMin).padStart(2, '0')}`;
  const edicao = isGiro
    ? {
        emoji: '🔄',
        cabecalho: `🔄 *Giro 9Pilla*`,
        hora: horaAtual,
        aberturaGuia:
          'Abertura de TARDE, sem "bom dia" nem café da manhã. Algo como "Oi, ' +
          'Turma 9Pilla, passando pro giro da tarde" — o pregão ainda está aberto ' +
          '(a B3 fecha por volta das 17h/18h), então fale de mercado EM ANDAMENTO ' +
          'nesta tarde, ancorando no que o dia teve de mais forte.',
        termometroNota: `(cotações desta tarde, ${horaAtual}, pregão em andamento)`,
      }
    : {
        emoji: '☕',
        cabecalho: `☕ *Morning Call 9Pilla*`,
        hora: '09h09',
        aberturaGuia:
          'Abertura calorosa de manhã: "Bom dia, Turma 9Pilla" + o ritual do café, ' +
          'lugar tranquilo, ancorada no que o dia tem de real.',
        termometroNota:
          '(fechamento do pregão anterior e cotações em andamento nesta manhã)',
      };

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
    `A data de HOJE é ${dateExtenso(brt)}. Essa data é REAL e ATUAL — NÃO é futura. ` +
    `As ferramentas web_search/web_fetch retornam informação atual: USE-AS e ` +
    `CONFIE nos resultados.\n\n` +
    `EDIÇÃO DE HOJE (siga à risca):\n` +
    `- Cabeçalho EXATO (primeira linha): "${edicao.cabecalho}"\n` +
    `- Segunda linha: "${dateExtenso(brt)} | ${edicao.hora}"\n` +
    `- Abertura: ${edicao.aberturaGuia}\n` +
    `- Nota do Termômetro: use "${edicao.termometroNota}".\n` +
    `- O RESTO (Termômetro, notícias, Píllula, fechamento, assinatura, disclaimer ` +
    `CVM) é IGUAL ao padrão. Só o cabeçalho, a hora e a abertura mudam.\n\n` +
    `DEVER DE CASA (faça ANTES de escrever, pesquisando de verdade):\n` +
    `1) Calendário econômico de HOJE, por horário — pesquise em Investing Brasil ` +
    `(calendário econômico) e InfoMoney. Se conseguir confirmar os horários, inclua ` +
    `a seção 📅. Se NÃO conseguir confirmar, OMITA a seção 📅 inteira em silêncio ` +
    `(sem título, sem parágrafo, SEM pedir desculpa) — nunca escreva que a agenda ` +
    `"não veio".\n` +
    `2) Notícias que movem o mercado HOJE — Brasil (Investing/InfoMoney) e global ` +
    `(Bloomberg). Fatos, nomes e números reais e atuais.\n` +
    `3) NÃO pesquise Ibovespa futuro nem DI 10 anos na web: use SÓ os números ` +
    `abaixo (vêm do brapi, sincronizados). Se não estiverem abaixo, OMITA essas ` +
    `linhas. Toda linha do termômetro tem número real, ou não existe — nunca ` +
    `descrição sem número ("em alta", "a confirmar").\n\n` +
    `NÚMEROS JÁ BUSCADOS (use exatamente, não invente):\n${digest || '(nenhum — pesquise tudo)'}\n\n` +
    `REGRAS DE SAÍDA (críticas):\n` +
    `- Responda APENAS com o texto final da edição. NADA antes, NADA depois.\n` +
    `- NUNCA escreva comentários sobre o seu processo, sobre a busca, sobre a data ` +
    `ser futura, sobre o que você "vai fazer" ou "fez". Isso é PROIBIDO no texto.\n` +
    `- O texto começa DIRETO no cabeçalho "${edicao.cabecalho}".\n` +
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
