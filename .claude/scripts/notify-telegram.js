#!/usr/bin/env node
'use strict';

/**
 * notify-telegram.js — 07:45 BRT.
 * Lê a Morning Call do dia (já gerada), injeta os dados reais frescos e
 * envia no TELEGRAM PESSOAL da Raquel, pronta para copiar e colar na Turma.
 *
 * Não publica em grupo nenhum: a Raquel copia e cola manualmente às 09:09.
 *
 * Env: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID_RAQUEL,
 *      BRAPI_TOKEN (para os números de mercado; sem ele usa Yahoo como fallback).
 *
 * Correto-ou-nada: se os dados reais não confirmarem, ABORTA e avisa a Raquel.
 */

const https = require('https');

const market = require('./lib/market-data');
const content = require('./lib/content');

/** Envia uma mensagem de texto puro (sem parse_mode) via Telegram Bot API. */
function sendTelegram(botToken, chatId, text) {
  return new Promise((resolve, reject) => {
    const postData = JSON.stringify({
      chat_id: chatId,
      text,
      disable_web_page_preview: true,
    });

    const options = {
      hostname: 'api.telegram.org',
      path: `/bot${botToken}/sendMessage`,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData),
      },
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => (data += chunk));
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          if (parsed.ok) return resolve(parsed.result);
          reject(new Error(parsed.description || 'Telegram respondeu não-ok'));
        } catch (e) {
          reject(new Error(`Resposta inválida do Telegram: ${e.message}`));
        }
      });
    });
    req.on('error', reject);
    req.write(postData);
    req.end();
  });
}

async function main() {
  const botToken = process.env.TELEGRAM_BOT_TOKEN;
  const chatId = process.env.TELEGRAM_CHAT_ID_RAQUEL;
  if (!botToken) throw new Error('TELEGRAM_BOT_TOKEN não definido.');
  if (!chatId) throw new Error('TELEGRAM_CHAT_ID_RAQUEL não definido.');

  const { content: raw } = content.readForDate(new Date());

  // Dados reais e frescos (brapi + fallback Yahoo). Aborta se faltar.
  const data = await market.fetchMorningCallData({ token: process.env.BRAPI_TOKEN });
  const block = market.formatMarketBlock(data);
  const withData = content.injectMarketBlock(raw, block);

  // Texto já no formato do WhatsApp (negrito com * simples), pronto para copiar.
  const morningCall = content.toWhatsApp(withData);

  const header =
    '🌅 *Morning Call de hoje — pronta para copiar*\n' +
    'Confira e cole na Turma 9Pilla às 09:09 👇\n' +
    '━━━━━━━━━━━━━━━━━━━━\n\n';

  // Envia numa mensagem só o cabeçalho + o conteúdo, para copiar tudo de uma vez.
  await sendTelegram(botToken, chatId, header + morningCall);

  console.log('✅ Morning Call enviada ao seu Telegram, pronta para copiar.');
  process.exit(0);
}

main().catch(async (err) => {
  console.error('❌ Falha ao preparar/enviar para o Telegram:', err.message);
  try {
    const botToken = process.env.TELEGRAM_BOT_TOKEN;
    const chatId = process.env.TELEGRAM_CHAT_ID_RAQUEL;
    if (botToken && chatId) {
      await sendTelegram(
        botToken,
        chatId,
        `⚠️ Não consegui montar a Morning Call de hoje com dado confirmado: ${err.message}. ` +
          'Não enviei nada pronto — melhor conferir manualmente.'
      );
    }
  } catch (_) {}
  process.exit(1);
});
