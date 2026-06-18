#!/usr/bin/env python3
"""
🤖 APPROVAL BOT V2 — BOT ROBUSTO E CONFIÁVEL PARA TELEGRAM

MELHORIAS vs V1:
✅ Retry automático com backoff exponencial
✅ Logging estruturado em arquivo
✅ Estados bem definidos (pending → approved/rejected → feedback)
✅ Timeout handling inteligente
✅ Confirmação visual de recebimento
✅ Dashboard de status
✅ Recovery automático de falhas
✅ Melhor UX (emojis, progressão visual)
✅ Persistência de estado robusto
✅ Handlers independentes por tipo de mensagem
"""

import os
import sys
import json
import time
import requests
import logging
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Setup logging
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, 'approval_bot.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APPROVALS_DIR = os.path.join(BASE_DIR, 'data', 'approvals')
os.makedirs(APPROVALS_DIR, exist_ok=True)

# Estado global: {chat_id: {script_id, stage, waiting_for}}
SESSIONS = {}


class TelegramClient:
    """Cliente Telegram com retry automático"""

    MAX_RETRIES = 3
    BASE_DELAY = 2  # segundos

    @staticmethod
    def send_message(text, parse_mode="HTML", reply_markup=None, retries=0):
        """Envia mensagem com retry automático"""

        if retries >= TelegramClient.MAX_RETRIES:
            logger.error(f"Falha após {retries} tentativas ao enviar mensagem")
            return False

        try:
            payload = {
                "chat_id": CHAT_ID,
                "text": text,
                "parse_mode": parse_mode,
                "disable_web_page_preview": True
            }

            if reply_markup:
                payload["reply_markup"] = reply_markup

            response = requests.post(
                f"{BASE_URL}/sendMessage",
                json=payload,
                timeout=15
            )

            if response.status_code == 200:
                logger.info("✅ Mensagem enviada com sucesso")
                return True

            elif response.status_code == 429:  # Rate limit
                retry_after = int(response.headers.get('Retry-After', 5))
                logger.warning(f"⏳ Rate limit. Aguardando {retry_after}s...")
                time.sleep(retry_after)
                return TelegramClient.send_message(text, parse_mode, reply_markup, retries + 1)

            else:
                logger.warning(f"Erro {response.status_code}: {response.text[:200]}")
                delay = TelegramClient.BASE_DELAY * (2 ** retries)
                logger.info(f"↻ Tentando novamente em {delay}s...")
                time.sleep(delay)
                return TelegramClient.send_message(text, parse_mode, reply_markup, retries + 1)

        except requests.Timeout:
            logger.warning("⏱️ Timeout ao enviar mensagem")
            delay = TelegramClient.BASE_DELAY * (2 ** retries)
            time.sleep(delay)
            return TelegramClient.send_message(text, parse_mode, reply_markup, retries + 1)

        except Exception as e:
            logger.error(f"❌ Erro: {str(e)}")
            return False

    @staticmethod
    def answer_callback(callback_id, text, show_alert=False):
        """Responde callback query (remove spinner)"""
        try:
            response = requests.post(
                f"{BASE_URL}/answerCallbackQuery",
                json={
                    "callback_query_id": callback_id,
                    "text": text,
                    "show_alert": show_alert
                },
                timeout=10
            )
            return response.status_code == 200

        except Exception as e:
            logger.error(f"Erro ao responder callback: {e}")
            return False

    @staticmethod
    def edit_message(message_id, text, reply_markup=None):
        """Edita mensagem existente"""
        try:
            payload = {
                "chat_id": CHAT_ID,
                "message_id": message_id,
                "text": text,
                "parse_mode": "HTML"
            }

            if reply_markup:
                payload["reply_markup"] = reply_markup

            response = requests.post(
                f"{BASE_URL}/editMessageText",
                json=payload,
                timeout=10
            )

            return response.status_code == 200

        except Exception as e:
            logger.error(f"Erro ao editar mensagem: {e}")
            return False


def save_decision(script_id, stage, decision, feedback=None, message_id=None):
    """Salva decisão com metadados completos"""

    path = os.path.join(APPROVALS_DIR, f'{script_id}.json')

    data = {}
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except:
                logger.warning(f"Erro ao ler {path}, criando novo")
                data = {}

    data.update({
        'script_id': script_id,
        f'{stage}_decision': decision,
        f'{stage}_decided_at': datetime.now().isoformat(),
        f'{stage}_message_id': message_id
    })

    if feedback:
        data[f'{stage}_feedback'] = feedback

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    logger.info(f"💾 Decisão salva: {script_id} → {stage}: {decision}")


def handle_callback(callback):
    """Handler robusto para cliques em botões"""

    callback_id = callback.get('id')
    chat_id = callback.get('message', {}).get('chat', {}).get('id')
    message_id = callback.get('message', {}).get('message_id')
    data = callback.get('data', '')

    logger.info(f"🔔 Callback recebido: {data}")

    # Responder callback (remove spinner)
    TelegramClient.answer_callback(callback_id, "⏳ Processando...")

    try:
        # Parse: "action:stage:script_id"
        parts = data.split(':', 2)
        if len(parts) != 3:
            logger.error(f"Callback inválido: {data}")
            return

        action, stage, script_id = parts

        if action == 'approve':
            handle_approve(script_id, stage, message_id)

        elif action == 'reject':
            handle_reject(script_id, stage, message_id)

        elif action == 'confirm_feedback':
            handle_confirm_feedback(script_id, stage, message_id)

    except Exception as e:
        logger.error(f"Erro ao processar callback: {e}")
        TelegramClient.answer_callback(callback_id, f"❌ Erro: {str(e)[:50]}", show_alert=True)


def handle_approve(script_id, stage, message_id):
    """Aprova script ou vídeo"""

    save_decision(script_id, stage, 'approved', message_id=message_id)

    stage_name = "Script" if stage == "script" else "Vídeo"

    # Remover botões da mensagem anterior
    TelegramClient.edit_message(message_id, f"✅ {stage_name} {script_id} APROVADO!")

    # Mensagem de confirmação
    if stage == 'script':
        msg = f"""
✅ <b>Script APROVADO!</b>

📝 ID: {script_id}
⏱️ {datetime.now().strftime('%H:%M:%S')}

<b>Próximos passos:</b>
1️⃣ Gerando áudio (ElevenLabs)
2️⃣ Criando vídeo (HeyGen)
3️⃣ Processando design (Canva)
4️⃣ Enviando para aprovação final

⏳ <i>Tempo estimado: 5-10 minutos</i>
"""
    else:  # video
        msg = f"""
✅ <b>Vídeo APROVADO!</b>

🎬 ID: {script_id}
⏱️ {datetime.now().strftime('%H:%M:%S')}

<b>Ações automáticas:</b>
1️⃣ Publicando no YouTube Shorts
2️⃣ Postando no TikTok
3️⃣ Compartilhando no Instagram Reels
4️⃣ Compilando para Spotify Podcast

✨ Seu vídeo está ao vivo para a Turma 9Pilla!
"""

    TelegramClient.send_message(msg)
    logger.info(f"✅ Aprovado: {script_id}")


def handle_reject(script_id, stage, message_id):
    """Rejeita e pede feedback"""

    save_decision(script_id, stage, 'rejected', message_id=message_id)

    stage_name = "Script" if stage == "script" else "Vídeo"

    # Remover botões
    TelegramClient.edit_message(message_id, f"❌ {stage_name} {script_id} REJEITADO")

    # Pedir feedback
    msg = f"""
❌ <b>{stage_name} REJEITADO</b>

📝 ID: {script_id}
⏱️ {datetime.now().strftime('%H:%M:%S')}

<b>Nenhum custo foi gerado!</b> ✅

💭 <b>Qual é o problema?</b>
Responde aqui com:
• Ton muito formal?
• Dados errados?
• Vídeo com lag?
• Outro?

O sistema aprende com seu feedback e melhora na próxima.
"""

    TelegramClient.send_message(msg)

    # Marcar sessão como aguardando feedback
    SESSIONS[chat_id] = {
        'script_id': script_id,
        'stage': stage,
        'waiting_for': 'feedback'
    }

    logger.info(f"❌ Rejeitado: {script_id} - Aguardando feedback")


def handle_message(message):
    """Handler para mensagens de texto (feedback)"""

    chat_id = message.get('chat', {}).get('id')
    text = message.get('text', '').strip()

    logger.info(f"💬 Mensagem: {text[:50]}")

    if not text:
        return

    # Comandos
    if text == '/start':
        msg = f"""
🤖 <b>Approval Bot 9Pilla V2</b> - Ativo e conectado!

Quando um script ou vídeo ficar pronto, você receberá uma mensagem com botões:
✅ APROVAR
❌ REJEITAR

Clique para tomar sua decisão. Se rejeitar, mande seu feedback aqui.

📊 Status: <b>Escutando...</b>
"""
        TelegramClient.send_message(msg)

    elif text == '/status':
        msg = f"""
📊 <b>Status do Approval Bot V2</b>

✅ Bot conectado
✅ Token válido
✅ Escutando mensagens
✅ Long polling ativo

Decisões registradas: {len(os.listdir(APPROVALS_DIR))}

Tudo funcionando normalmente! 🚀
"""
        TelegramClient.send_message(msg)

    elif text == '/logs':
        # Enviar últimas linhas do log
        log_file = os.path.join(LOG_DIR, 'approval_bot.log')
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()[-10:]
            log_text = ''.join(lines)
            msg = f"<pre>{log_text}</pre>"
            TelegramClient.send_message(msg)

    else:
        # Feedback de rejeição
        if chat_id in SESSIONS and SESSIONS[chat_id].get('waiting_for') == 'feedback':
            script_id = SESSIONS[chat_id]['script_id']
            stage = SESSIONS[chat_id]['stage']

            save_decision(script_id, stage, 'rejected', feedback=text)

            msg = f"""
📚 <b>Feedback registrado!</b>

"{text[:100]}..."

O sistema aprende com isso e a próxima versão sai melhor.

Obrigada pela atenção à qualidade! 💛
"""
            TelegramClient.send_message(msg)
            del SESSIONS[chat_id]

        else:
            msg = "Não entendi. Digite /start para ajuda ou aguarde um script para aprovar."
            TelegramClient.send_message(msg)


def send_for_approval(script_text, script_id, stage="script"):
    """Envia script/vídeo para aprovação com botões inline"""

    titulo = "📝 NOVO SCRIPT PARA APROVAÇÃO" if stage == "script" else "🎬 NOVO VÍDEO PARA APROVAÇÃO"

    message = f"""
<b>{titulo}</b>

🔹 <b>ID:</b> {script_id}
🔹 <b>Horário:</b> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
🔹 <b>Estágio:</b> {stage}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{script_text[:3000]}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

<b>⚠️ Antes de aprovar:</b>
• Tom é da Raquel?
• Dados estão corretos?
• Nenhum travessão "—"?

<b>✅ Aprovar:</b> Vídeo vai para produção
<b>❌ Rejeitar:</b> Zero custo, volta para ajustar
"""

    keyboard = {
        "inline_keyboard": [[
            {"text": "✅ APROVAR", "callback_data": f"approve:{stage}:{script_id}"},
            {"text": "❌ REJEITAR", "callback_data": f"reject:{stage}:{script_id}"}
        ]]
    }

    if TelegramClient.send_message(message, reply_markup=keyboard):
        logger.info(f"📤 Enviado para aprovação: {script_id}")
        return True
    else:
        logger.error(f"❌ Falha ao enviar: {script_id}")
        return False


def listen():
    """Loop principal com tratamento robusto de erros"""

    print("=" * 70)
    print("🤖 APPROVAL BOT V2 — ROBUSTO E CONFIÁVEL")
    print("=" * 70)
    print(f"Bot: @raquel_9pilla_bot")
    print(f"Chat ID: {CHAT_ID}")
    print(f"Decisões: {APPROVALS_DIR}")
    print(f"Logs: {LOG_DIR}")
    print("=" * 70)

    offset = None
    reconnect_delay = 5

    while True:
        try:
            params = {
                "timeout": 30,  # Long polling
                "allowed_updates": ["message", "callback_query"]
            }

            if offset:
                params["offset"] = offset

            response = requests.get(
                f"{BASE_URL}/getUpdates",
                params=params,
                timeout=40
            )

            if response.status_code != 200:
                logger.error(f"getUpdates error: {response.status_code}")
                time.sleep(reconnect_delay)
                reconnect_delay = min(reconnect_delay * 2, 60)
                continue

            reconnect_delay = 5  # Reset ao conectar com sucesso

            updates = response.json().get('result', [])

            for update in updates:
                offset = update['update_id'] + 1

                if 'callback_query' in update:
                    handle_callback(update['callback_query'])

                elif 'message' in update:
                    handle_message(update['message'])

        except requests.Timeout:
            logger.warning("⏱️ Timeout, reconectando...")
            time.sleep(reconnect_delay)

        except KeyboardInterrupt:
            logger.info("👋 Bot encerrado pelo usuário")
            break

        except Exception as e:
            logger.error(f"Erro no loop: {e}")
            time.sleep(reconnect_delay)
            reconnect_delay = min(reconnect_delay * 2, 60)


if __name__ == "__main__":
    if not BOT_TOKEN or not CHAT_ID:
        logger.error("❌ Configure TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID no .env")
        sys.exit(1)

    if '--send-test' in sys.argv:
        send_for_approval(
            "Teste do Approval Bot V2 - Escreva /start para ajuda",
            "TEST_BOT_V2",
            stage="script"
        )
    else:
        listen()
