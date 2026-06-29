'use strict';

/**
 * zapi.js — Cliente mínimo do Z-API (WhatsApp).
 *
 * Endpoints (confirmados na doc Z-API):
 *  - Enviar texto:  POST /instances/{id}/token/{token}/send-text
 *      header: Client-Token; body: { phone, message }
 *      (phone serve tanto p/ pessoa quanto p/ grupo — basta o JID/ID do grupo)
 *  - Ler mensagens: GET  /instances/{id}/token/{token}/chat-messages/{phone}
 *      header: Client-Token; retorna mensagens da conversa
 *
 * Credenciais vêm de variáveis de ambiente (GitHub Secrets), nunca do código:
 *   ZAPI_INSTANCE_ID, ZAPI_TOKEN, ZAPI_CLIENT_TOKEN
 */

const https = require('https');

const BASE = 'https://api.z-api.io';
const TIMEOUT_MS = 20000;

function cfg() {
  const id = process.env.ZAPI_INSTANCE_ID;
  const token = process.env.ZAPI_TOKEN;
  const clientToken = process.env.ZAPI_CLIENT_TOKEN;
  if (!id || !token || !clientToken) {
    throw new Error(
      'Z-API não configurado. Defina ZAPI_INSTANCE_ID, ZAPI_TOKEN e ZAPI_CLIENT_TOKEN (GitHub Secrets).'
    );
  }
  return { id, token, clientToken };
}

function request(method, path, { clientToken, body } = {}) {
  return new Promise((resolve, reject) => {
    const url = new URL(`${BASE}${path}`);
    const payload = body ? JSON.stringify(body) : null;
    const options = {
      method,
      hostname: url.hostname,
      path: url.pathname + url.search,
      headers: {
        Accept: 'application/json',
        'Client-Token': clientToken,
        ...(payload
          ? { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(payload) }
          : {}),
      },
      timeout: TIMEOUT_MS,
    };
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (c) => (data += c));
      res.on('end', () => {
        if (res.statusCode < 200 || res.statusCode >= 300) {
          return reject(new Error(`Z-API HTTP ${res.statusCode}: ${data.slice(0, 200)}`));
        }
        try {
          resolve(data ? JSON.parse(data) : {});
        } catch (e) {
          reject(new Error(`Z-API resposta não-JSON: ${e.message}`));
        }
      });
    });
    req.on('timeout', () => req.destroy(new Error('Z-API timeout')));
    req.on('error', reject);
    if (payload) req.write(payload);
    req.end();
  });
}

/** Envia texto para uma pessoa ou grupo (phone = número OU id do grupo). */
async function sendText(phone, message) {
  const { id, token, clientToken } = cfg();
  return request('POST', `/instances/${id}/token/${token}/send-text`, {
    clientToken,
    body: { phone, message },
  });
}

/** Lê as últimas mensagens de uma conversa. */
async function getChatMessages(phone, amount = 30) {
  const { id, token, clientToken } = cfg();
  const path = `/instances/${id}/token/${token}/chat-messages/${encodeURIComponent(phone)}?amount=${amount}`;
  return request('GET', path, { clientToken });
}

/** Normaliza o texto de uma mensagem (Z-API varia o formato). */
function messageText(m) {
  if (!m) return '';
  if (typeof m.text === 'string') return m.text;
  if (m.text && typeof m.text.message === 'string') return m.text.message;
  if (typeof m.message === 'string') return m.message;
  if (typeof m.body === 'string') return m.body;
  return '';
}

/** Timestamp (ms) da mensagem, tolerando segundos vs ms. */
function messageTime(m) {
  const t = Number(m.momment ?? m.moment ?? m.timestamp ?? m.messageTimestamp ?? 0);
  if (!Number.isFinite(t) || t === 0) return 0;
  return t < 1e12 ? t * 1000 : t; // segundos -> ms
}

const APPROVE_RE = /\b(sim|ok|aprovo|aprovado|aprovada|publica(r)?|pode)\b|👍|✅/i;

/**
 * Verifica se a Raquel aprovou (mensagem recebida DELA depois de `sinceMs`).
 * @returns {Promise<{approved:boolean, matched?:string}>}
 */
async function approvalReceivedSince(phone, sinceMs) {
  const res = await getChatMessages(phone, 40);
  const list = Array.isArray(res) ? res : res.messages || res.data || [];
  for (const m of list) {
    if (m.fromMe === true) continue; // só conta resposta dela
    if (messageTime(m) < sinceMs) continue;
    const txt = messageText(m);
    if (APPROVE_RE.test(txt)) return { approved: true, matched: txt.slice(0, 60) };
  }
  return { approved: false };
}

module.exports = { sendText, getChatMessages, approvalReceivedSince, messageText, messageTime };
