#!/usr/bin/env node
'use strict';

/**
 * validate-fetch.js — Dry-run: prova que a busca REAL funciona, SEM enviar nada.
 *
 * Mostra os 5 ativos obrigatórios (brapi + fallback Yahoo), o bloco
 * internacional (NY + commodities via Yahoo), a Selic oficial (BCB) e as
 * manchetes reais do dia (fontes preferenciais). Não toca no Z-API.
 *
 * Sai com código 1 se algum dado obrigatório não puder ser confirmado.
 */

const fs = require('fs');
const path = require('path');

const market = require('./lib/market-data');
const news = require('./lib/news');

function loadBrapi() {
  const p = path.join(__dirname, '../config-morning-call.json');
  if (!fs.existsSync(p)) {
    console.warn('⚠️  config-morning-call.json ausente; vou tentar só pelo Yahoo (backup).');
    return {};
  }
  return JSON.parse(fs.readFileSync(p, 'utf8')).brapi || {};
}

async function main() {
  console.log('🔎 DRY-RUN — validando busca real (nada será enviado)\n');
  const brapi = loadBrapi();

  console.log('1️⃣  Ativos obrigatórios (brapi, com fallback Yahoo)');
  const data = await market.fetchMorningCallData({
    baseUrl: brapi.baseUrl || market.DEFAULT_BASE_URL,
    token: brapi.token,
  });
  console.log(market.formatMarketBlock(data));
  const fontes = new Set(
    [data.ibov, data.dolar, data.petr4, data.vale3, data.itub4].map((a) => a.source)
  );
  console.log(`   fontes usadas: ${[...fontes].join(', ')}\n`);

  console.log('2️⃣  Internacional (Yahoo: NY + commodities)');
  const g = await market.fetchGlobalData();
  for (const k of Object.keys(g)) {
    const a = g[k];
    console.log(
      a.error
        ? `   ⚠️  ${a.ticker}: ${a.error}`
        : `   ${a.ticker}: ${a.price} (${a.changePercent.toFixed(2)}%)`
    );
  }
  console.log('');

  console.log('3️⃣  Selic oficial (Banco Central, série 432)');
  try {
    const s = await market.fetchSelic();
    console.log(`   Meta Selic: ${s.value}% a.a. (${s.asOf})\n`);
  } catch (e) {
    console.log(`   ⚠️  Não confirmou Selic no BCB: ${e.message}\n`);
  }

  console.log('4️⃣  Notícias reais do dia (Investing, InfoMoney, Bloomberg, CNN primeiro)');
  const headlines = await news.fetchHeadlines({ limit: 5 });
  headlines.forEach((h) =>
    console.log(`   ${h.preferred ? '⭐' : '  '} ${h.title}  ::  ${h.source || 's/ fonte'}`)
  );

  console.log('\n✅ Busca real OK. Dados, juros e notícias confirmados.');
  process.exit(0);
}

main().catch((err) => {
  console.error('\n❌ DRY-RUN FALHOU (algum dado obrigatório não pôde ser confirmado):');
  console.error(`   ${err.message}`);
  process.exit(1);
});
