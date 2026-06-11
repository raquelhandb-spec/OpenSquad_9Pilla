#!/usr/bin/env python3
"""
🤖 APPROVAL BOT — Bot de Aprovação 9Pilla (roda na máquina LOCAL da Raquel)

Por que este arquivo existe:
O servidor remoto não alcança o Telegram (rede bloqueada). E um bot precisa
de um programa RODANDO para escutar os cliques. Este é esse programa.

COMO USAR (Windows):
    python approval_bot.py              → inicia o bot escutando
    python approval_bot.py --send-test  → envia script de teste com botões

O bot envia scripts com BOTÕES (✅ APROVAR / ❌ REJEITAR), muito mais
confiável que reação de emoji. Quando a Raquel clica:
- ✅ APROVAR  → bot confirma na hora e salva decisão em data/approvals/
- ❌ REJEITAR → bot pede feedback, Raquel responde com texto, tudo salvo

As decisões salvas em data/approvals/{script_id}.json são lidas pelo
orchestrator para liberar (ou não) a etapa HeyGen (US$ 0,30).
"""

import os
import sys
import json
import time
import requests
from datetime import datetime

# Carregar .env da mesma pasta
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))
except ImportError:
    pass  # .env opcional se as variáveis já estiverem no ambiente

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APPROVALS_DIR = os.path.join(BASE_DIR, 'data', 'approvals')
os.makedirs(APPROVALS_DIR, exist_ok=True)

# Estado: aguardando feedback de rejeição? {chat_id: script_id}
pending_feedback = {}


# ─────────────────────────────────────────────────────────────────
# ENVIO COM BOTÕES
# ─────────────────────────────────────────────────────────────────

def send_for_approval(script_text: str, script_id: str, stage: str = "script") -> bool:
    """
    Envia script/vídeo para aprovação com botões inline.
    stage: "script" (estágio 1) ou "video" (estágio 2)
    """
    titulo = "📝 NOVO SCRIPT PARA APROVAÇÃO" if stage == "script" else "🎬 VÍDEO PRONTO PARA APROVAÇÃO"
    custo = "Se APROVAR → avatar HeyGen será criado (~US$ 0,30)" if stage == "script" \
        else "Se APROVAR → vídeo será publicado no YouTube + WhatsApp"

    message = f"""{titulo}

📌 ID: {script_id}
⏰ {datetime.now().strftime('%d/%m/%Y %H:%M')}

━━━━━━━━━━━━━━━━━━━━━━━

{script_text}

━━━━━━━━━━━━━━━━━━━━━━━

⚠️ {custo}
Se REJEITAR → zero gasto, e você pode mandar feedback"""

    keyboard = {
        "inline_keyboard": [[
            {"text": "✅ APROVAR", "callback_data": f"approve:{stage}:{script_id}"},
            {"text": "❌ REJEITAR", "callback_data": f"reject:{stage}:{script_id}"}
        ]]
    }

    r = requests.post(f"{BASE_URL}/sendMessage", json={
        "chat_id": CHAT_ID,
        "text": message[:4000],  # limite Telegram 4096
        "reply_markup": keyboard
    }, timeout=15)

    if r.status_code == 200:
        print(f"✅ Enviado para aprovação: {script_id} (estágio: {stage})")
        return True
    print(f"❌ Erro ao enviar: {r.status_code} {r.text[:200]}")
    return False


# ─────────────────────────────────────────────────────────────────
# DECISÕES
# ─────────────────────────────────────────────────────────────────

def save_decision(script_id: str, stage: str, decision: str, feedback: str = None):
    """Salva decisão em data/approvals/{script_id}.json (lido pelo orchestrator)"""
    path = os.path.join(APPROVALS_DIR, f'{script_id}.json')

    data = {}
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

    data.setdefault('script_id', script_id)
    data[f'{stage}_decision'] = decision
    data[f'{stage}_decided_at'] = datetime.now().isoformat()
    if feedback:
        data[f'{stage}_feedback'] = feedback

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"💾 Decisão salva: {script_id} → {stage}: {decision}" + (f" (feedback: {feedback[:50]}...)" if feedback else ""))


def reply(chat_id, text):
    requests.post(f"{BASE_URL}/sendMessage", json={"chat_id": chat_id, "text": text}, timeout=15)


# ─────────────────────────────────────────────────────────────────
# LISTENER (o programa que faltava!)
# ─────────────────────────────────────────────────────────────────

def handle_callback(callback):
    """Processa clique nos botões"""
    callback_id = callback['id']
    chat_id = callback['message']['chat']['id']
    message_id = callback['message']['message_id']
    data = callback.get('data', '')

    # Confirmar recebimento do clique (tira o "reloginho" do Telegram)
    requests.post(f"{BASE_URL}/answerCallbackQuery", json={
        "callback_query_id": callback_id, "text": "Recebido! 👍"
    }, timeout=15)

    try:
        action, stage, script_id = data.split(':', 2)
    except ValueError:
        return

    # Remover botões da mensagem original (evita clique duplo)
    requests.post(f"{BASE_URL}/editMessageReplyMarkup", json={
        "chat_id": chat_id, "message_id": message_id,
        "reply_markup": {"inline_keyboard": []}
    }, timeout=15)

    stage_name = "Script" if stage == "script" else "Vídeo"

    if action == 'approve':
        save_decision(script_id, stage, 'approved')
        if stage == 'script':
            reply(chat_id,
                  f"✅ {stage_name} {script_id} APROVADO!\n\n"
                  f"Próximo passo: gerar narração (ElevenLabs) e avatar (HeyGen ~US$ 0,30).\n"
                  f"Quando o vídeo ficar pronto, ele chega aqui para a aprovação final. 🎬")
        else:
            reply(chat_id,
                  f"✅ Vídeo {script_id} APROVADO!\n\n"
                  f"Publicando no YouTube Shorts e avisando a Turma 9Pilla no WhatsApp. 🚀")

    elif action == 'reject':
        save_decision(script_id, stage, 'rejected')
        pending_feedback[chat_id] = script_id + ':' + stage
        reply(chat_id,
              f"❌ {stage_name} {script_id} REJEITADO. Zero gasto! ✅\n\n"
              f"Me conta o que não gostou? Responde aqui mesmo com o motivo "
              f"(ex: 'tom muito formal', 'número errado'). O sistema aprende com seu feedback. 📚")


def handle_message(message):
    """Processa mensagens de texto (feedback de rejeição)"""
    chat_id = message['chat']['id']
    text = message.get('text', '')

    if not text:
        return

    if chat_id in pending_feedback:
        script_stage = pending_feedback.pop(chat_id)
        script_id, stage = script_stage.rsplit(':', 1)
        save_decision(script_id, stage, 'rejected', feedback=text)
        reply(chat_id,
              f"📚 Feedback anotado! Obrigada, Raquel.\n\n"
              f"\"{text[:200]}\"\n\n"
              f"Isso vai pro arquivo de aprendizado e o próximo script sai melhor. 💛")
    elif text == '/start':
        reply(chat_id,
              "🤖 Bot de Aprovação 9Pilla ativo!\n\n"
              "Quando um script ou vídeo ficar pronto, ele chega aqui com botões "
              "✅ APROVAR / ❌ REJEITAR. É só clicar!")
    elif text == '/status':
        files = os.listdir(APPROVALS_DIR) if os.path.exists(APPROVALS_DIR) else []
        reply(chat_id, f"📊 Decisões registradas: {len(files)}\nBot rodando normalmente. ✅")


def listen():
    """Loop principal: escuta cliques e mensagens (long polling)"""
    print("="*60)
    print("🤖 BOT DE APROVAÇÃO 9PILLA — ESCUTANDO")
    print("="*60)
    print(f"   Bot: @raquel_9pilla_bot")
    print(f"   Decisões salvas em: {APPROVALS_DIR}")
    print("   Deixe esta janela ABERTA. Ctrl+C para parar.")
    print("="*60)

    offset = None
    while True:
        try:
            params = {"timeout": 30}
            if offset:
                params["offset"] = offset

            r = requests.get(f"{BASE_URL}/getUpdates", params=params, timeout=40)
            if r.status_code != 200:
                print(f"⚠️ getUpdates: {r.status_code}. Tentando de novo em 5s...")
                time.sleep(5)
                continue

            for update in r.json().get('result', []):
                offset = update['update_id'] + 1
                if 'callback_query' in update:
                    handle_callback(update['callback_query'])
                elif 'message' in update:
                    handle_message(update['message'])

        except KeyboardInterrupt:
            print("\n👋 Bot encerrado.")
            break
        except Exception as e:
            print(f"⚠️ Erro no loop: {e}. Reconectando em 5s...")
            time.sleep(5)


# ─────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if not BOT_TOKEN or not CHAT_ID:
        print("❌ Configure TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID no .env")
        sys.exit(1)

    if '--send-test' in sys.argv:
        # Enviar o último script gerado (ou um exemplo) com botões
        script_path = os.path.join(BASE_DIR, 'output', 'script_atual.json')
        if os.path.exists(script_path):
            with open(script_path, 'r', encoding='utf-8') as f:
                script_data = json.load(f)
            texto = script_data.get('script_full', 'Script de teste 9Pilla')
            sid = f"9Pilla_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        else:
            texto = "Bom dia, bom dia! Aqui é a Raquel! ☕ Este é um teste dos botões de aprovação."
            sid = "TESTE_BOTOES"
        send_for_approval(texto, sid, stage="script")
        print("\nAgora rode sem --send-test para escutar os cliques:")
        print("   python approval_bot.py")
    else:
        listen()
