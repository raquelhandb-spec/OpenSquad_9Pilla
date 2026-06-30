#!/usr/bin/env node
'use strict';

/**
 * generate-morning-call.js — Cria o Morning Call do dia com DADOS e NOTÍCIAS REAIS.
 *
 * MUDANÇA CRÍTICA vs versão antiga:
 *  - ANTES: notícias e números ficavam HARDCODED no script (texto fixo que saía
 *    igual todo dia: "Ibovespa 197 mil pontos", "dólar R$ 4,99", "Copom 28-29 abril").
 *    Isso é fabricação de dado.
 *  - AGORA: busca os 5 ativos reais no brapi e manchetes reais do dia (Investing,
 *    InfoMoney, Bloomberg, CNN). Se o dado real não vier, ABORTA — não inventa.
 *
 * O arquivo gerado tem o bloco de mercado delimitado por
 * <!--MERCADO:START--> ... <!--MERCADO:END--> para que o send-morning-call.js
 * possa reinjetar os números frescos às 09h09.
 *
 * Roda em ambiente com internet (GitHub Action / online). Requer brapi.token
 * em .claude/config-morning-call.json.
 */

const fs = require('fs');
const path = require('path');

const market = require('./lib/market-data');
const news = require('./lib/news');

function loadConfig() {
  const configPath = path.join(__dirname, '../config-morning-call.json');
  if (!fs.existsSync(configPath)) {
    throw new Error(
      `config-morning-call.json não encontrado em ${configPath}. ` +
        'Configure brapi.token (no Action vem do secret BRAPI_TOKEN).'
    );
  }
  return JSON.parse(fs.readFileSync(configPath, 'utf8'));
}

function formatDateISO(date) {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, '0');
  const d = String(date.getDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

function formatDateBR(date) {
  return date.toLocaleDateString('pt-BR');
}

function getDayName(date) {
  const days = [
    'Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado',
  ];
  return days[date.getDay()];
}

/** Formata as manchetes reais em bullets com a fonte citada. */
function formatNews(headlines) {
  return headlines
    .map((h) => {
      const src = h.source ? ` _(${h.source})_` : '';
      return `• ${h.title}${src}`;
    })
    .join('\n');
}

async function main() {
  const now = new Date();
  const dateStr = formatDateISO(now);
  console.log(`🌅 Gerando Morning Call de ${formatDateBR(now)}...\n`);

  const config = loadConfig();
  const brapi = config.brapi || {};

  // 1) Dados reais (correto-ou-nada)
  console.log('1️⃣  Buscando dados reais no brapi...');
  const data = await market.fetchMorningCallData({
    baseUrl: brapi.baseUrl || market.DEFAULT_BASE_URL,
    token: brapi.token,
  });
  const marketBlock = market.formatMarketBlock(data);
  console.log(marketBlock + '\n');

  // 2) Notícias reais do dia (Investing, InfoMoney, Bloomberg, CNN)
  console.log('2️⃣  Buscando notícias reais do dia...');
  const headlines = await news.fetchHeadlines({ limit: 4 });
  headlines.forEach((h) => console.log(`   • ${h.title} (${h.source || 's/ fonte'})`));
  console.log('');

  // 2.5) Enriquecimento (brapi pago): destaques do pregão. Best-effort.
  const topMovers = await market.fetchTopMovers({
    baseUrl: brapi.baseUrl || market.DEFAULT_BASE_URL,
    token: brapi.token,
  });
  const destaquesBlock = market.formatTopMovers(topMovers);
  const destaquesSection = destaquesBlock
    ? `\n📊 DESTAQUES DO PREGÃO\n${destaquesBlock}\n`
    : '';

  // 3) Monta o conteúdo (bloco de mercado delimitado para reinjeção)
  const body = `Bom dia, Turma! 🌅

━━━━━━━━━━━━━━━━━━━━
📊 MERCADO AGORA
━━━━━━━━━━━━━━━━━━━━
<!--MERCADO:START-->
${marketBlock}
<!--MERCADO:END-->
━━━━━━━━━━━━━━━━━━━━
${destaquesSection}
🌎 O QUE ACONTECEU

${formatNews(headlines)}

🎯 SUA AÇÃO DE HOJE

Revise sua carteira com calma. Quem constrói patrimônio não corre atrás de barulho: lê o cenário, respira e age com método.

Dinheiro não é destino. É a jornada para a LIBERDADE. 🌱

⚠️ Conteúdo educativo e informativo. Não é recomendação de investimento. Decisões são de responsabilidade do investidor. Investimentos envolvem riscos. CVM Resolução 20/2021.`;

  const fullContent = `<!-- Morning Call 9Pilla | ${getDayName(now)}, ${formatDateBR(now)} | gerado com dados/notícias reais -->
${body}
`;

  const contentPath = path.join(
    __dirname,
    '../../content/morning-call',
    `${dateStr}.md`
  );
  fs.mkdirSync(path.dirname(contentPath), { recursive: true });
  fs.writeFileSync(contentPath, fullContent, 'utf8');

  console.log(`3️⃣  ✅ Arquivo salvo: ${contentPath}`);
  console.log('   Dados: brapi (reais). Notícias: RSS fontes preferenciais (reais).');
  console.log('   Pronto para revisão/aprovação da Raquel antes do envio 09h09.');
  process.exit(0);
}

main().catch((err) => {
  console.error('\n❌ GERAÇÃO ABORTADA (não criei conteúdo com dado inventado):');
  console.error(`   ${err.message}`);
  process.exit(1);
});
