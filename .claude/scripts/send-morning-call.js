#!/usr/bin/env node

/**
 * Script de envio do Morning Call via Z-API
 * Executa automaticamente seg-sex às 09h09
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

// Configurações Z-API
const Z_API_CONFIG = {
  instanceId: '3F11BDD3D23071C40CFC9EED2DF277BD',
  token: 'D06BC58B1E9B2833DB10EBF3',
  clientToken: 'Fa5f350a5afc04288905bf0ea9692a1ffS',
  groupJid: '120363407926604570-group',
  apiUrl: 'https://api.z-api.io/instances/3F11BDD3D23071C40CFC9EED2DF277BD/token/D06BC58B1E9B2833DB10EBF3/send-text'
};

/**
 * Formata data como YYYY-MM-DD
 */
function formatDate(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

/**
 * Verifica se é dia útil (seg-sex)
 */
function isBusinessDay(date = new Date()) {
  const day = date.getDay();
  return day >= 1 && day <= 5; // 1 = seg, 5 = sex
}

/**
 * Lê o conteúdo do Morning Call do dia
 */
function readMorningCallContent(date) {
  const dateStr = formatDate(date);
  const contentPath = path.join(
    __dirname,
    '../../content/morning-call',
    `${dateStr}.md`
  );

  if (!fs.existsSync(contentPath)) {
    throw new Error(
      `Arquivo de Morning Call não encontrado: ${contentPath}`
    );
  }

  return fs.readFileSync(contentPath, 'utf8');
}

/**
 * Envia mensagem via Z-API
 */
function sendViaZAPI(content) {
  return new Promise((resolve, reject) => {
    const postData = JSON.stringify({
      phone: Z_API_CONFIG.groupJid,
      message: content,
      clientToken: Z_API_CONFIG.clientToken
    });

    const url = new URL(Z_API_CONFIG.apiUrl);
    const options = {
      hostname: url.hostname,
      port: 443,
      path: url.pathname + url.search,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData),
        'Client-Token': Z_API_CONFIG.clientToken
      }
    };

    const req = https.request(options, (res) => {
      let data = '';

      res.on('data', (chunk) => {
        data += chunk;
      });

      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve({
            success: true,
            statusCode: res.statusCode,
            response: data
          });
        } else {
          reject(new Error(
            `Z-API retornou status ${res.statusCode}: ${data}`
          ));
        }
      });
    });

    req.on('error', reject);
    req.write(postData);
    req.end();
  });
}

/**
 * Função principal
 */
async function main() {
  const now = new Date();
  const dateStr = formatDate(now);

  console.log(`[${now.toISOString()}] Iniciando envio do Morning Call...`);
  console.log(`Data: ${dateStr}`);

  // Verifica se é dia útil
  if (!isBusinessDay(now)) {
    console.log('❌ Não é dia útil (seg-sex). Cancelando envio.');
    process.exit(0);
  }

  try {
    // Lê conteúdo
    console.log('📖 Lendo conteúdo...');
    const content = readMorningCallContent(now);

    // Envia via Z-API
    console.log('📤 Enviando via Z-API...');
    const result = await sendViaZAPI(content);

    console.log('✅ Morning Call enviado com sucesso!');
    console.log(`Status: ${result.statusCode}`);
    console.log(`Response: ${result.response}`);

    process.exit(0);
  } catch (error) {
    console.error('❌ Erro ao enviar Morning Call:');
    console.error(error.message);
    process.exit(1);
  }
}

main();
