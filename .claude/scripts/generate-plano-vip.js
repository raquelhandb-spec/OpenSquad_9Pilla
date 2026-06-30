#!/usr/bin/env node
'use strict';

/**
 * generate-plano-vip.js — Gera o "Plano VIP do Dia" (exclusivo VIP 9Pilla).
 *
 * Diferente do Morning Call (gratuito, macro): o Plano VIP é mais operacional.
 * Traz os 8 ativos reais + uma leitura curta do dia + lembrete de gestão.
 * Os setups específicos de opções a Raquel manda ao vivo quando opera.
 *
 * Dados reais (brapi + fallback Yahoo). Correto-ou-nada: aborta se faltar.
 * Salva em content/vip/YYYY-MM-DD.md com o bloco MERCADO delimitado, pronto
 * pra reinjeção/envio (mesmo padrão do Morning Call).
 */

const fs = require('fs');
const path = require('path');
const market = require('./lib/market-data');

function dateISO(d = new Date()) {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const dd = String(d.getDate()).padStart(2, '0');
  return `${y}-${m}-${dd}`;
}

function dateBR(d = new Date()) {
  return d.toLocaleDateString('pt-BR');
}

/** Leitura automática e honesta a partir dos dados (sem chutar setup). */
function leituraDoDia(data) {
  const ibovUp = data.ibov.changePercent >= 0;
  const dolarUp = data.dolar.changePercent >= 0;
  const oilDown = data.brent.changePercent < 0;
  const partes = [];
  partes.push(
    ibovUp
      ? 'Ibovespa no positivo, viés mais construtivo pra bolsa hoje.'
      : 'Ibovespa no negativo, dia pede mais cautela na ponta comprada.'
  );
  partes.push(
    dolarUp
      ? 'Dólar firme, fica de olho no impacto em exportadoras e na inflação.'
      : 'Dólar comportado, alívio pro humor doméstico.'
  );
  if (oilDown) partes.push('Petróleo em queda pesa em Petrobras no curto prazo.');
  else partes.push('Petróleo firme, atenção em Petrobras.');
  return partes.join(' ');
}

async function main() {
  const now = new Date();
  console.log(`🎯 Gerando Plano VIP do Dia — ${dateBR(now)}`);

  const data = await market.fetchMorningCallData({ token: process.env.BRAPI_TOKEN });
  const block = market.formatMarketBlock(data);

  const body = `🎯 *PLANO VIP DO DIA* — ${dateBR(now)}
_Exclusivo VIP 9Pilla. Recebido em primeira mão._

📊 *MERCADO AGORA*
<!--MERCADO:START-->
${block}
<!--MERCADO:END-->

🧭 *Leitura do dia*
${leituraDoDia(data)}

🛡️ *Lembrete de gestão*
Antes de qualquer entrada: defina o risco máximo aceitável e o ponto de saída. Operação boa é a que você sabe quanto pode perder antes de começar.

As minhas operações de opções, com a tese, eu mando ao vivo aqui no grupo conforme eu monto e desmonto. Fica de olho.

Dinheiro não é destino. É a jornada para a LIBERDADE.

⚠️ Conteúdo educativo, não é recomendação. CVM Res. 20/2021.`;

  const outDir = path.join(__dirname, '../../content/vip');
  fs.mkdirSync(outDir, { recursive: true });
  const outPath = path.join(outDir, `${dateISO(now)}.md`);
  fs.writeFileSync(outPath, `<!-- Plano VIP do Dia | ${dateBR(now)} | dados reais -->\n${body}\n`, 'utf8');

  console.log('✅ Plano VIP gerado:', outPath);
  console.log(block);
  process.exit(0);
}

main().catch((err) => {
  console.error('❌ Geração do Plano VIP abortada (dado não confirmado):', err.message);
  process.exit(1);
});
