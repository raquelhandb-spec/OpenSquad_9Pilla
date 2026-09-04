'use strict';

/**
 * content.js — Helpers de conteúdo do Morning Call (ler arquivo, injetar
 * dados frescos no bloco MERCADO e converter para texto de WhatsApp).
 * Usado por notify-telegram.js e generate-morning-call.js.
 */

const fs = require('fs');
const path = require('path');

const MARKER_START = '<!--MERCADO:START-->';
const MARKER_END = '<!--MERCADO:END-->';

function formatDateISO(date = new Date()) {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, '0');
  const d = String(date.getDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

function contentPathFor(date = new Date(), suffix = '') {
  return path.join(__dirname, '../../../content/morning-call', `${formatDateISO(date)}${suffix}.md`);
}

/**
 * Decide a EDIÇÃO (Morning Call de manhã x Giro de tarde) e o caminho do
 * arquivo, a partir do horário de Brasília — MESMA regra usada por
 * generate-editorial.js. Fonte única de verdade: o Morning Call (manhã)
 * sempre grava no arquivo "puro" da data (arquivo histórico do dia); o Giro
 * grava num arquivo com sufixo "-giro-HHhMM", pra NUNCA sobrescrever o
 * Morning Call do mesmo dia (foi o que aconteceu em 03/09, antes deste fix).
 */
function resolveEdicao(now = new Date()) {
  const brt = new Date(now.getTime() - 3 * 3600 * 1000);
  const brtHour = brt.getUTCHours();
  const brtMin = brt.getUTCMinutes();
  const isGiro = brtHour >= 12;
  const horaAtual = `${String(brtHour).padStart(2, '0')}h${String(brtMin).padStart(2, '0')}`;
  const suffix = isGiro ? `-giro-${horaAtual}` : '';
  return { isGiro, brt, brtHour, brtMin, horaAtual, suffix, path: contentPathFor(now, suffix) };
}

function readForDate(date = new Date()) {
  const p = contentPathFor(date);
  if (!fs.existsSync(p)) {
    throw new Error(`Morning Call do dia não encontrado: ${p}`);
  }
  return { content: fs.readFileSync(p, 'utf8'), contentPath: p };
}

/**
 * Acha o arquivo de hoje escrito MAIS RECENTEMENTE (maior mtime). Usado no
 * lugar de recalcular resolveEdicao(now) pra LER: o Giro grava o HHhMM exato
 * no nome do arquivo, mas generate-editorial.js e notify-telegram.js rodam
 * como processos SEPARADOS no mesmo job — a chamada ao Claude leva minutos,
 * então o minuto pode mudar entre "gerar" e "notificar", e o nome recalculado
 * não bate mais com o arquivo real no disco (foi o que quebrou o Giro das
 * 14h36: notify calculou 14h38). Por mtime nunca erra, porque o checkout é
 * sempre fresco no início do job — só o arquivo recém-escrito é mais novo.
 */
function findLatestEditionFile(now = new Date()) {
  const dateStr = formatDateISO(now);
  const dir = path.join(__dirname, '../../../content/morning-call');
  if (!fs.existsSync(dir)) return null;
  const candidatos = fs
    .readdirSync(dir)
    .filter((f) => f.startsWith(dateStr) && f.endsWith('.md'))
    .map((f) => {
      const p = path.join(dir, f);
      return { path: p, mtime: fs.statSync(p).mtimeMs };
    })
    .sort((a, b) => b.mtime - a.mtime);
  return candidatos.length ? candidatos[0].path : null;
}

/**
 * Lê o arquivo da EDIÇÃO ATUAL (Morning Call ou Giro, conforme o horário de
 * agora). Usado pelo notify-telegram.js pra sempre enviar o que acabou de
 * ser gerado no mesmo job — nunca um arquivo de outra edição do mesmo dia.
 */
function readForNow(now = new Date()) {
  const p = findLatestEditionFile(now);
  if (!p || !fs.existsSync(p)) {
    throw new Error(`Morning Call/Giro de agora não encontrado (nenhum arquivo de hoje no disco).`);
  }
  return { content: fs.readFileSync(p, 'utf8'), contentPath: p };
}

/** Substitui o bloco entre os marcadores pelos dados frescos. Aborta se ausentes. */
function injectMarketBlock(content, marketBlock) {
  const s = content.indexOf(MARKER_START);
  const e = content.indexOf(MARKER_END);
  if (s === -1 || e === -1 || e < s) {
    throw new Error(
      'Arquivo sem bloco de mercado (<!--MERCADO:START--> ... <!--MERCADO:END-->). ' +
        'Não envio conteúdo cujo dado eu não consiga validar.'
    );
  }
  return `${content.slice(0, s + MARKER_START.length)}\n${marketBlock}\n${content.slice(e)}`;
}

// Frases de BASTIDOR/DESCULPA que NUNCA podem chegar à Turma. Se um parágrafo
// contém qualquer uma, ele é removido inteiro. É o cinto de segurança contra o
// modelo vazar o "pensamento" ou pedir desculpa por dado que não veio.
const META_MARKERS = [
  /dever de casa/i,
  /\bé futura\b/i,
  /buscas?\b[^.\n]*\b(retorn|volt|vier|vazi|não)/i,
  /pesquisa web|ferramentas? web|web[_ ]?search/i,
  /não (consigo|pude|vou|consegui|posso)\s+(confirmar|inventar|fabricar|chutar)/i,
  /não me trouxe/i,
  /dado real ou nada/i,
  /(regra inegociável|fiel à regra|seguindo a regra)/i,
  /vou (pesquisar|usar exatamente|construir o morning|fazer o dever|tratar)/i,
  /nesta sess(ã|a)o/i,
  /(não chuta|inventa indicador|inventar (um )?(evento|indicador|número|manchete|fato))/i,
  /prefiro te dizer com honestidade/i,
  /horário errado/i,
  /omit(ir|o|indo)\b[^.\n]*\b(linha|seção|item|agenda)/i,
];

// Palavras que denunciam um DADO-FANTASMA: uma linha de termômetro ("Rótulo:
// valor") que descreve a direção em vez de trazer o número real. Regra da casa:
// dado real (com número) ou nada. Nunca "em alta, acompanhando o à vista".
const FILLER_VALOR = /(em alta|em baixa|acompanhando|est[aá]ve(l|is)|sem varia|no (positivo|negativo)|misto|levemente|de leve|para (cima|baixo)|firme|pressionad|indispon[ií]vel|a confirmar|sob revis)/i;

/** É uma linha de termômetro "Rótulo: <descrição sem número>" (dado-fantasma)? */
function isFillerDataLine(line) {
  const t = line.trim();
  if (t.length === 0 || t.length > 70) return false;
  // "Rótulo curto: valor" — o rótulo pode ter número (DI 10 anos, S&P 500).
  const m = t.match(/^[*_]*[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ0-9 ()/.&-]{0,30}:\s*(.+)$/);
  if (!m) return false;
  const valor = m[1];
  if (/\d/.test(valor)) return false; // valor tem número -> dado real, mantém
  return FILLER_VALOR.test(valor);
}

/** Um bloco é "só cabeçalho de seção" (título sem corpo)? */
function isHeaderOnly(block) {
  if (block.includes('\n')) return false;
  const t = block.trim();
  if (t.length === 0 || t.length > 80) return false;
  if (/^\*{1,2}[^*]+\*{1,2}$/.test(t)) return true; // ex: **Notícias do dia**
  if (/^[🌡️📅📰💊🗓️📊]/u.test(t)) return true; // ex: 📅 **Calendário...**
  return false;
}

/**
 * Remove qualquer preâmbulo/meta-comentário do editorial: corta tudo antes do
 * cabeçalho e descarta parágrafos de bastidor/desculpa. Se uma seção (ex:
 * 📅 Calendário) ficar só com o título porque o corpo era desculpa, o título
 * também sai. A Turma recebe só o Morning Call, limpo.
 *
 * @param {string} expectedEmoji — '☕' (Morning Call) ou '🔄' (Giro). Se dado,
 * corta EXATAMENTE nesse emoji e ignora o outro — evita o bug onde o modelo
 * escreve os dois emoji juntos ("☕ 🔄 *Giro 9Pilla*") e o corte errado escolhe
 * o emoji da edição ERRADA por aparecer primeiro. Sem o parâmetro, mantém o
 * comportamento antigo (corta no que aparecer primeiro, dos dois).
 */
function stripMeta(text, expectedEmoji) {
  let t = String(text || '');
  // Corta o preâmbulo antes do cabeçalho da edição (Morning Call ☕ ou Giro 🔄).
  const emojisParaChecar = expectedEmoji ? [expectedEmoji] : ['☕', '🔄'];
  const idxs = emojisParaChecar.map((e) => t.indexOf(e)).filter((n) => n > 0);
  if (idxs.length) t = t.slice(Math.min(...idxs));
  // Se sobrar o emoji da OUTRA edição colado na linha do cabeçalho (ex: "🔄
  // *Giro 9Pilla* ☕"), remove — a linha do cabeçalho é só da edição de hoje.
  if (expectedEmoji) {
    const outroEmoji = expectedEmoji === '☕' ? '🔄' : '☕';
    const linhas = t.split('\n');
    if (linhas[0] && linhas[0].includes(outroEmoji)) {
      linhas[0] = linhas[0].split(outroEmoji).join('').replace(/\s{2,}/g, ' ').trim();
      t = linhas.join('\n');
    }
  }
  const blocks = t.split(/\n{2,}/).map((b) => b.replace(/\s+$/g, '')).filter((b) => b.trim() !== '');
  const meta = blocks.map((b) => META_MARKERS.some((re) => re.test(b)));
  const keep = blocks.map((b, idx) => {
    if (meta[idx]) return false;
    if (isHeaderOnly(b)) {
      let j = idx + 1;
      while (j < blocks.length && meta[j]) j++;
      if (j >= blocks.length || isHeaderOnly(blocks[j])) return false; // título órfão
    }
    return true;
  });
  // Passo final, linha a linha: remove dados-fantasma (linha de termômetro que
  // descreve direção sem número — "Ibovespa futuro: em alta, acompanhando...").
  const limpo = blocks
    .filter((_, idx) => keep[idx])
    .join('\n\n')
    .split('\n')
    .filter((ln) => !isFillerDataLine(ln))
    .join('\n');
  return limpo.replace(/\n{3,}/g, '\n\n').trim();
}

/**
 * Cinto de segurança: o Giro NÃO tem Píllula de Sabedoria (só o Morning Call
 * de manhã). Se o modelo incluir por engano, remove o bloco 💊 e tudo até o
 * CTA de fechamento ("chegou até aqui" / "Grande beijo"), preservando o
 * fechamento e a assinatura. Sem efeito se incluiPillula=true ou se a seção
 * já não existir.
 */
function stripPillulaSeAusente(text, incluiPillula) {
  if (incluiPillula) return text;
  const blocks = text.split(/\n{2,}/);
  const startIdx = blocks.findIndex((b) => /^💊/u.test(b.trim()));
  if (startIdx === -1) return text;
  let endIdx = blocks.length;
  for (let i = startIdx + 1; i < blocks.length; i++) {
    if (/chegou até aqui|^Grande beijo/i.test(blocks[i])) { endIdx = i; break; }
  }
  return blocks
    .filter((_, i) => i < startIdx || i >= endIdx)
    .join('\n\n')
    .trim();
}

/** Limpa markdown/chrome para a mensagem do WhatsApp. */
function toWhatsApp(content) {
  return content
    .replace(/<!--[\s\S]*?-->/g, '')
    .replace(/^#{1,6}\s*/gm, '')
    .replace(/\*\*(.*?)\*\*/g, '*$1*')
    .replace(/^\s*---\s*$/gm, '')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

module.exports = {
  MARKER_START,
  MARKER_END,
  formatDateISO,
  contentPathFor,
  resolveEdicao,
  readForDate,
  readForNow,
  stripPillulaSeAusente,
  injectMarketBlock,
  toWhatsApp,
  stripMeta,
};
