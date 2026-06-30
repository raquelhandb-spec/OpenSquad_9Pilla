#!/usr/bin/env node
'use strict';

/**
 * send-morning-call.js — Envio do Morning Call via Z-API (roda 09h09 seg-sex)
 *
 * MUDANÇA CRÍTICA vs versão antiga:
 *  - ANTES: buscava o brapi, imprimia no log e DESCARTAVA. Enviava o texto
 *    estático do .md (dado escrito à mão / desatualizado).
 *  - AGORA: busca o brapi de verdade e INJETA os números reais no bloco
 *    "MERCADO AGORA" do .md, imediatamente antes de enviar. Se o brapi não
 *    confirmar os 5 ativos, ABORTA o envio (correto-ou-nada). A Turma nunca
 *    recebe dado errado.
 *
 * Fail-safe: aborta (exit 1) se faltar arquivo, faltar o bloco de mercado,
 * ou se qualquer ativo do brapi falhar.
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

const market = require('./lib/market-data');

const MARKER_START = '<!--MERCADO:START-->';
const MARKER_END = '<!--MERCADO:END-->';

function loadConfig() {
  const configPath = path.join(__dirname, '../config-morning-call.json');
  if (!fs.existsSync(configPath)) {
    throw new Error(
      `config-morning-call.json não encontrado em ${configPath}. ` +
        'No GitHub Action ele é criado a partir dos secrets.'
    );
  }
  return JSON.parse(fs.readFileSync(configPath, 'utf8'));
}

function formatDate(date) {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, '0');
  const d = String(date.getDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

function isBusinessDay(date) {
  const day = date.getDay();
  return day >= 1 && day <= 5;
}

function readMorningCallContent(date) {
  const dateStr = formatDate(date);
  const contentPath = path.join(
    __dirname,
    '../../content/morning-call',
    `${dateStr}.md`
  );
  if (!fs.existsSync(contentPath)) {
    throw new Error(`Morning Call do dia não encontrado: ${contentPath}`);
  }
  return { content: fs.readFileSync(contentPath, 'utf8'), contentPath };
}

/**
 * Substitui o bloco entre os marcadores pelos dados reais e frescos.
 * Aborta se os marcadores não existirem (arquivo não validável).
 */
function injectMarketBlock(content, marketBlock) {
  const startIdx = content.indexOf(MARKER_START);
  const endIdx = content.indexOf(MARKER_END);
  if (startIdx === -1 || endIdx === -1 || endIdx < startIdx) {
    throw new Error(
      'Arquivo sem bloco de mercado delimitado (<!--MERCADO:START--> ... ' +
        '<!--MERCADO:END-->). Gere o Morning Call com generate-morning-call.js. ' +
        'Não envio conteúdo cujo dado eu não consiga validar.'
    );
  }
  const before = content.slice(0, startIdx + MARKER_START.length);
  const after = content.slice(endIdx);
  return `${before}\n${marketBlock}\n${after}`;
}

/** Limpa o markdown/chrome para a mensagem do WhatsApp. */
function toWhatsApp(content) {
  return content
    .replace(/<!--[\s\S]*?-->/g, '') // remove comentários/marcadores
    .replace(/^#{1,6}\s*/gm, '') // remove headers markdown
    .replace(/\*\*(.*?)\*\*/g, '*$1*') // **bold** -> *bold* (WhatsApp)
    .replace(/^\s*---\s*$/gm, '') // remove linhas "---"
    .replace(/\n{3,}/g, '\n\n') // colapsa linhas em branco
    .trim();
}

function sendViaZAPI(zapi, messageText) {
  return new Promise((resolve, reject) => {
    const postData = JSON.stringify({
      phone: zapi.groupJid,
      message: messageText,
    });
    const url = new URL(zapi.apiUrl);
    const options = {
      hostname: url.hostname,
      port: 443,
      path: url.pathname + url.search,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData),
        'Client-Token': zapi.clientToken, // Client-Token no header (não na URL)
      },
    };
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (c) => (data += c));
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve({ statusCode: res.statusCode, response: data });
        } else {
          reject(new Error(`Z-API status ${res.statusCode}: ${data}`));
        }
      });
    });
    req.on('error', reject);
    req.write(postData);
    req.end();
  });
}

async function main() {
  const now = new Date();
  console.log(`[${now.toISOString()}] Envio Morning Call — data ${formatDate(now)}`);

  if (!isBusinessDay(now)) {
    console.log('⏭️  Não é dia útil (seg-sex). Nada a enviar.');
    process.exit(0);
  }

  const config = loadConfig();
  const zapi = config['z-api'];
  const brapi = config.brapi || {};

  // 1) Lê o conteúdo aprovado do dia
  console.log('📖 Lendo conteúdo aprovado do dia...');
  const { content } = readMorningCallContent(now);

  // 2) Busca dados REAIS e frescos. Se falhar, aborta (não envia).
  console.log('📊 Buscando dados reais no brapi (correto-ou-nada)...');
  const data = await market.fetchMorningCallData({
    baseUrl: brapi.baseUrl || market.DEFAULT_BASE_URL,
    token: brapi.token,
  });
  [data.ibov, data.dolar, data.petr4, data.vale3, data.itub4].forEach((a) => {
    console.log(`   ${a.ticker}: ${a.price} (${a.changePercent}%)`);
  });

  // 3) Injeta os números reais no bloco MERCADO AGORA
  const marketBlock = market.formatMarketBlock(data);
  const withFreshData = injectMarketBlock(content, marketBlock);

  // 4) Converte para WhatsApp e envia
  const messageText = toWhatsApp(withFreshData);
  console.log('📤 Enviando via Z-API...');
  const result = await sendViaZAPI(zapi, messageText);

  console.log('✅ Morning Call enviado com dados reais!');
  console.log(`   Status: ${result.statusCode}`);
  process.exit(0);
}

main().catch((err) => {
  console.error('\n❌ ENVIO ABORTADO (nada foi enviado pra Turma):');
  console.error(`   ${err.message}`);
  process.exit(1);
});
