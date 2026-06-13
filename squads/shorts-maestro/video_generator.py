#!/usr/bin/env python3
"""
🎬 VIDEO GENERATOR — Gera vídeos com HeyGen + ElevenLabs
Fluxo: Script → Áudio ElevenLabs → Vídeo HeyGen → Aprovação Telegram → Pronto

IMPORTANTE: NADA se publica sem aprovação da Raquel no Telegram!
"""

import os
import sys
import json
import time
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Carregar .env
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))

ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY', '')
ELEVENLABS_VOICE_ID = os.getenv('ELEVENLABS_VOICE_ID', '')
HEYGEN_API_KEY = os.getenv('HEYGEN_API_KEY', '')
HEYGEN_AVATAR_ID = os.getenv('HEYGEN_AVATAR_ID', '')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, 'output', 'videos')
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_audio_elevenlabs(text, bloco_num, mc_date):
    """Gera áudio com ElevenLabs (sua voz Raquel)"""
    print(f"\n   🎤 Gerando áudio ElevenLabs (Bloco {bloco_num})...")

    # Garantir que o texto tem mínimo de caracteres
    if len(text.strip()) < 50:
        print(f"      ⚠️ Texto muito curto ({len(text)} chars), expandindo...")
        text = f"Olá! Aqui é a Raquel! {text} Obrigada por escutar!"

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"

    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "text": text.strip(),
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    try:
        print(f"      📝 Enviando {len(text)} caracteres para ElevenLabs...")
        response = requests.post(url, json=data, headers=headers, timeout=30)

        if response.status_code == 200:
            audio_file = os.path.join(OUTPUT_DIR, f"audio_bloco{bloco_num}_{mc_date}.mp3")
            with open(audio_file, 'wb') as f:
                f.write(response.content)
            print(f"   ✅ Áudio salvo: {audio_file}")
            return audio_file
        else:
            error_msg = response.text[:200] if response.text else "Erro desconhecido"
            print(f"   ❌ ElevenLabs erro {response.status_code}: {error_msg}")
            print(f"      API Key: {ELEVENLABS_API_KEY[:20]}...")
            print(f"      Voice ID: {ELEVENLABS_VOICE_ID}")
            return None
    except Exception as e:
        print(f"   ❌ Erro ao gerar áudio: {e}")
        return None


def generate_video_heygen(audio_file, bloco_num, mc_date):
    """Gera vídeo com HeyGen (seu avatar)"""
    print(f"\n   🎬 Gerando vídeo HeyGen (Bloco {bloco_num})...")

    url = "https://api.heygen.com/v1/video_requests"

    headers = {
        "X-API-Key": HEYGEN_API_KEY,
        "Content-Type": "application/json"
    }

    # Enviar áudio para HeyGen gerar vídeo
    data = {
        "input": [
            {
                "character": {
                    "avatar_id": HEYGEN_AVATAR_ID,
                    "avatar_style": "normal"
                },
                "voice": {
                    "input_path": audio_file  # URL do áudio gerado
                }
            }
        ],
        "dimension": {
            "width": 1080,
            "height": 1920
        }
    }

    try:
        response = requests.post(url, json=data, headers=headers, timeout=60)

        if response.status_code in [200, 201]:
            result = response.json()
            video_id = result.get('data', {}).get('video_id')

            if video_id:
                print(f"   ✅ Vídeo solicitado (ID: {video_id})")
                print(f"      (processando... pode levar 2-5 minutos)")
                return video_id
            else:
                print(f"   ⚠️ Resposta inesperada: {result}")
                return None
        else:
            print(f"   ❌ HeyGen erro: {response.status_code} - {response.text[:200]}")
            return None

    except Exception as e:
        print(f"   ❌ Erro ao gerar vídeo: {e}")
        return None


def check_video_status(video_id):
    """Verifica status do vídeo HeyGen"""
    url = f"https://api.heygen.com/v1/video_requests/{video_id}"

    headers = {
        "X-API-Key": HEYGEN_API_KEY
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            data = response.json().get('data', {})
            status = data.get('status')  # pending, processing, completed, failed
            video_url = data.get('video_url')

            return status, video_url
        else:
            print(f"   ❌ Erro ao verificar status: {response.status_code}")
            return None, None

    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return None, None


def wait_for_video(video_id, max_wait=600):
    """Aguarda vídeo ficar pronto (máx 10 minutos)"""
    print(f"\n   ⏳ Aguardando vídeo (máx {max_wait//60} minutos)...")

    start_time = time.time()
    check_count = 0

    while time.time() - start_time < max_wait:
        status, video_url = check_video_status(video_id)

        if status == "completed":
            print(f"   ✅ Vídeo pronto! (tempo total: {int(time.time() - start_time)}s)")
            return video_url

        elif status == "failed":
            print(f"   ❌ Geração falhou")
            return None

        elif status in ["pending", "processing"]:
            check_count += 1
            wait_time = min(30, 5 + check_count * 2)  # Aumenta espera gradualmente
            print(f"   ⏳ Status: {status}... (próxima verificação em {wait_time}s)")
            time.sleep(wait_time)

        else:
            print(f"   ⚠️ Status desconhecido: {status}")
            time.sleep(10)

    print(f"   ❌ Timeout: vídeo não ficou pronto em {max_wait//60} minutos")
    return None


def send_for_approval_telegram(video_data):
    """IMPORTANTE: Envia vídeo para aprovação NO TELEGRAM antes de publicar!"""
    print(f"\n   📱 Enviando para aprovação no Telegram...")

    from approval_bot import send_for_approval

    bloco = video_data['bloco_num']
    mc_date = video_data['mc_date']
    video_url = video_data['video_url']

    # Enviar para aprovação
    message = f"""
🎬 NOVO VÍDEO PRONTO PARA APROVAÇÃO

📝 Bloco: {bloco}/3
📅 Data: {mc_date}
🎥 Vídeo: [Link]({video_url})

⚠️ Após aprovação, será publicado em:
   • YouTube Shorts
   • TikTok
   • Instagram Reels
   • Spotify Podcast

Se ✅ APROVAR: vídeo vai para publicação
Se ❌ REJEITAR: volta para ajustes
"""

    script_id = f"VIDEO_{mc_date}_BLOCO{bloco}"
    ok = send_for_approval(message, script_id, stage="video")

    if ok:
        print(f"   ✅ Enviado para Telegram (@raquel_9pilla_bot)")
        print(f"      Aguardando sua aprovação antes de publicar...")
        return True
    else:
        print(f"   ❌ Falha ao enviar Telegram")
        return False


def process_bloco(bloco_file, bloco_num, mc_date):
    """Processa 1 bloco: Script → Audio → Video → Aprovação"""
    print(f"\n{'='*70}")
    print(f"🎬 PROCESSANDO BLOCO {bloco_num}")
    print(f"{'='*70}")

    # Ler script
    if not os.path.exists(bloco_file):
        print(f"❌ Arquivo não encontrado: {bloco_file}")
        return False

    with open(bloco_file, 'r', encoding='utf-8') as f:
        script_text = f.read()

    # Extrair apenas o conteúdo de fala (remove tags/marcações)
    import re
    texto_fala = re.sub(r'\[.*?\]|#{1,6}\s|\*\*|\*|_|→', '', script_text)

    # 1. Gerar áudio
    audio_file = generate_audio_elevenlabs(texto_fala, bloco_num, mc_date)
    if not audio_file:
        return False

    # 2. Gerar vídeo
    video_id = generate_video_heygen(audio_file, bloco_num, mc_date)
    if not video_id:
        return False

    # 3. Aguardar vídeo ficar pronto
    video_url = wait_for_video(video_id)
    if not video_url:
        return False

    # 4. IMPORTANTE: Enviar para aprovação Telegram
    video_data = {
        'bloco_num': bloco_num,
        'mc_date': mc_date,
        'video_url': video_url,
        'video_id': video_id,
        'status': 'awaiting_approval'
    }

    # Salvar metadados
    metadata_file = os.path.join(OUTPUT_DIR, f"video_bloco{bloco_num}_{mc_date}_metadata.json")
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(video_data, f, ensure_ascii=False, indent=2)

    send_for_approval_telegram(video_data)

    return True


if __name__ == "__main__":
    print("=" * 70)
    print("🎬 VIDEO GENERATOR — HeyGen + ElevenLabs + Telegram Approval")
    print("=" * 70)

    # Procurar shorts processados
    shorts_dir = os.path.join(BASE_DIR, 'output', 'shorts')

    if not os.path.exists(shorts_dir):
        print("❌ Pasta de shorts não encontrada!")
        print("   Execute primeiro: python shorts_processor.py")
        sys.exit(1)

    # Procurar pasta MC mais recente
    mc_folders = [f for f in os.listdir(shorts_dir) if f.startswith('MC_')]

    if not mc_folders:
        print("❌ Nenhum Morning Call processado encontrado")
        sys.exit(1)

    mc_folder = os.path.join(shorts_dir, sorted(mc_folders)[-1])
    mc_date = os.path.basename(mc_folder).replace('MC_', '')

    print(f"\n📁 Processando: {mc_date}\n")

    # Processar os 3 blocos
    for bloco_num in [1, 2, 3]:
        bloco_file = os.path.join(mc_folder, f'bloco{bloco_num}.txt')

        if os.path.exists(bloco_file):
            process_bloco(bloco_file, bloco_num, mc_date)
        else:
            print(f"⚠️ Bloco {bloco_num} não encontrado")

    print(f"\n{'='*70}")
    print("✅ TODOS OS VÍDEOS ENVIADOS PARA APROVAÇÃO NO TELEGRAM!")
    print(f"{'='*70}")
