#!/usr/bin/env node
'use strict';

/**
 * validate-fetch.js — Dry-run: prova que a busca REAL funciona, SEM enviar nada.
 *
 * Busca os 5 ativos no brapi e as manchetes reais do dia (fontes preferenciais)
 * e imprime tudo. Não toca no Z-API. Usado para validar o pipeline antes de
 * confiar no envio automático das 09h09.
 *
 * Sai com código 1 se qualquer dado real não puder ser confirmado.
 */

const fs = require('fs');
const path = require('path');

const market = require('./lib/market-data');
const news = require('./lib/news');

function loadBrapi() {
  const configPath = path.join(__dirname, '../config-morning-call.json');
  if (!fs.existsSync(configPath)) {
    throw new Error(
      `config-morning-call.json não encontrado (${configPath}). ` +
        'No Action ele é criado a partir do secret BRAPI_TOKEN.'
    );
  }
  return (JSON.parse(fs.readFileSync(configPath, 'utf8')).brapi) || {};
}

async function main() {
  console.log('🔎 DRY-RUN — validando busca real (nada será enviado)\n');

  const brapi = loadBrapi();

  console.log('1️⃣  brapi — 5 ativos obrigatórios');
  const data = await market.fetchMorningCallData({
    baseUrl: brapi.baseUrl || market.DEFAULT_BASE_URL,
    token: brapi.token,
  });
  console.log(market.formatMarketBlock(data));
  console.log('');

  console.log('2️⃣  Notícias reais do dia (Investing, InfoMoney, Bloomberg, CNN primeiro)');
  const headlines = await news.fetchHeadlines({ limit: 5 });
  headlines.forEach((h) =>
    console.log(`   ${h.preferred ? '⭐' : '  '} ${h.title}  ::  ${h.source || 's/ fonte'}`)
  );
  console.log('');

  console.log('✅ Busca real OK. Dados e notícias confirmados — pipeline pronto.');
  process.exit(0);
}

main().catch((err) => {
  console.error('\n❌ DRY-RUN FALHOU (algum dado real não pôde ser confirmado):');
  console.error(`   ${err.message}`);
  process.exit(1);
});
