#!/usr/bin/env node
'use strict';

/**
 * publish-if-approved.js — 09:09 BRT.
 * Confere se a Raquel respondeu SIM no WhatsApp (depois das ~08:15). Se sim,
 * injeta os dados reais frescos e PUBLICA na Turma 9Pilla. Se não, não publica
 * e avisa a Raquel.
 *
 * Env: ZAPI_*, ZAPI_PHONE_RAQUEL, ZAPI_GROUP_JID, BRAPI_TOKEN (opcional).
 *
 * Correto-ou-nada: se os dados reais não confirmarem, ABORTA (não publica).
 */

const market = require('./lib/market-data');
const content = require('./lib/content');
const zapi = require('./lib/zapi');

const APPROVAL_WINDOW_MS = 3 * 60 * 60 * 1000; // últimas 3h cobrem 08:15→09:09

async function main() {
  const phone = process.env.ZAPI_PHONE_RAQUEL;
  const group = process.env.ZAPI_GROUP_JID;
  if (!phone) throw new Error('ZAPI_PHONE_RAQUEL não definido.');
  if (!group) throw new Error('ZAPI_GROUP_JID não definido.');

  // 1) A Raquel aprovou na janela?
  const since = Date.now() - APPROVAL_WINDOW_MS;
  const { approved, matched } = await zapi.approvalReceivedSince(phone, since);
  if (!approved) {
    console.log('⏸️  Sem aprovação da Raquel até 09:09. NÃO publiquei.');
    await zapi.sendText(
      phone,
      '⏸️ Não recebi seu *SIM* até 09:09, então não publiquei a Morning Call na Turma. Se ainda quiser, me avisa.'
    );
    process.exit(0);
  }
  console.log(`✅ Aprovação detectada ("${matched}"). Publicando na Turma...`);

  // 2) Dados reais frescos + injeta no conteúdo do dia
  const { content: raw } = content.readForDate(new Date());
  const data = await market.fetchMorningCallData({ token: process.env.BRAPI_TOKEN });
  const block = market.formatMarketBlock(data);
  const message = content.toWhatsApp(content.injectMarketBlock(raw, block));

  // 3) Publica no grupo
  const res = await zapi.sendText(group, message);
  console.log('✅ Morning Call publicada na Turma 9Pilla!', res.messageId || res.id || '');
  await zapi.sendText(phone, '✅ Publiquei a Morning Call na Turma 9Pilla agora (09:09).');
  process.exit(0);
}

main().catch(async (err) => {
  console.error('❌ Falha ao publicar:', err.message);
  try {
    if (process.env.ZAPI_PHONE_RAQUEL) {
      await zapi.sendText(
        process.env.ZAPI_PHONE_RAQUEL,
        `⚠️ Tentei publicar a Morning Call e falhei: ${err.message}. NÃO publiquei nada na Turma.`
      );
    }
  } catch (_) {}
  process.exit(1);
});
