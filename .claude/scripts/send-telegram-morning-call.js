#!/usr/bin/env node

/**
 * send-telegram-morning-call.js
 * Envia Morning Call para Telegram de Raquel (aprovação antes de 09h09)
 *
 * Uso:
 *   node ./.claude/scripts/send-telegram-morning-call.js \
 *     --file content/morning-call/2026-06-24.md \
 *     --bot-token YOUR_BOT_TOKEN \
 *     --chat-id YOUR_CHAT_ID
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

// Parse arguments
const args = process.argv.slice(2);
let filePath = null;
let botToken = null;
let chatId = null;

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--file') filePath = args[i + 1];
  if (args[i] === '--bot-token') botToken = args[i + 1];
  if (args[i] === '--chat-id') chatId = args[i + 1];
}

// Validação
if (!filePath || !botToken || !chatId) {
  console.error('❌ Uso: node send-telegram-morning-call.js --file <path> --bot-token <token> --chat-id <id>');
  process.exit(1);
}

// Ler arquivo
if (!fs.existsSync(filePath)) {
  console.error(`❌ Arquivo não encontrado: ${filePath}`);
  process.exit(1);
}

const content = fs.readFileSync(filePath, 'utf-8');

// Preparar mensagem
const message = `📱 **MORNING CALL 9PILLA** (Aguardando Aprovação)

${content}

---
*Clique em ✅ para aprovar e publicar às 09h09*
*Ou responda com revisões necessárias*`;

// Enviar para Telegram
const url = `https://api.telegram.org/bot${botToken}/sendMessage`;

const postData = JSON.stringify({
  chat_id: chatId,
  text: message,
  parse_mode: 'Markdown',
  disable_web_page_preview: true
});

const options = {
  hostname: 'api.telegram.org',
  path: `/bot${botToken}/sendMessage`,
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': Buffer.byteLength(postData)
  }
};

const req = https.request(options, (res) => {
  let data = '';

  res.on('data', (chunk) => {
    data += chunk;
  });

  res.on('end', () => {
    try {
      const response = JSON.parse(data);

      if (response.ok) {
        console.log('✅ Morning Call enviado ao Telegram com sucesso!');
        console.log(`📱 Mensagem ID: ${response.result.message_id}`);
        console.log(`⏰ Aguardando aprovação de Raquel...`);
      } else {
        console.error(`❌ Erro ao enviar: ${response.description}`);
        process.exit(1);
      }
    } catch (e) {
      console.error('❌ Erro ao processar resposta:', e.message);
      process.exit(1);
    }
  });
});

req.on('error', (e) => {
  console.error(`❌ Erro de conexão: ${e.message}`);
  process.exit(1);
});

req.write(postData);
req.end();
