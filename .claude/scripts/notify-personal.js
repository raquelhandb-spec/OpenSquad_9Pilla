#!/usr/bin/env node
'use strict';

/**
 * notify-personal.js — 08:15 BRT.
 * Lê a Morning Call do dia (já gerada), injeta os dados reais frescos e
 * envia no WhatsApp PESSOAL da Raquel pedindo aprovação. Não publica no grupo.
 *
 * Env: ZAPI_INSTANCE_ID, ZAPI_TOKEN, ZAPI_CLIENT_TOKEN, ZAPI_PHONE_RAQUEL,
 *      BRAPI_TOKEN (opcional; sem ele usa Yahoo).
 *
 * Correto-ou-nada: se os dados reais não confirmarem, ABORTA e avisa a Raquel.
 */

const market = require('./lib/market-data');
const content = require('./lib/content');
const zapi = require('./lib/zapi');

async function main() {
  const phone = process.env.ZAPI_PHONE_RAQUEL;
  if (!phone) throw new Error('ZAPI_PHONE_RAQUEL não definido.');

  const { content: raw } = content.readForDate(new Date());

  // Dados reais e frescos (brapi + fallback Yahoo). Aborta se faltar.
  const data = await market.fetchMorningCallData({ token: process.env.BRAPI_TOKEN });
  const block = market.formatMarketBlock(data);
  const withData = content.injectMarketBlock(raw, block);

  const message =
    content.toWhatsApp(withData) +
    '\n\n——\n✅ Responda *SIM* até 09:05 para eu publicar na Turma 9Pilla às 09:09.';

  const res = await zapi.sendText(phone, message);
  console.log('✅ Morning Call enviada ao WhatsApp da Raquel para aprovação.');
  console.log('   messageId:', res.messageId || res.id || '(ok)');
  process.exit(0);
}

main().catch(async (err) => {
  console.error('❌ Falha ao preparar/enviar para aprovação:', err.message);
  try {
    if (process.env.ZAPI_PHONE_RAQUEL) {
      await zapi.sendText(
        process.env.ZAPI_PHONE_RAQUEL,
        `⚠️ Não consegui montar a Morning Call de hoje com dado confirmado: ${err.message}. Não publiquei nada.`
      );
    }
  } catch (_) {}
  process.exit(1);
});
