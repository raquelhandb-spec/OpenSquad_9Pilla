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

function contentPathFor(date = new Date()) {
  return path.join(__dirname, '../../../content/morning-call', `${formatDateISO(date)}.md`);
}

function readForDate(date = new Date()) {
  const p = contentPathFor(date);
  if (!fs.existsSync(p)) {
    throw new Error(`Morning Call do dia não encontrado: ${p}`);
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
  readForDate,
  injectMarketBlock,
  toWhatsApp,
};
