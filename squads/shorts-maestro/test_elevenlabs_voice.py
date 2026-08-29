#!/usr/bin/env python3
"""
🎤 TEST ELEVENLABS VOICE — Valida qual voice usar
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))

ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY', '')
ELEVENLABS_VOICE_ID = os.getenv('ELEVENLABS_VOICE_ID', '')

print("=" * 100)
print("🎤 ELEVENLABS VOICE TEST")
print("=" * 100)

# ============================================================================
# TEST 1: Testar sua voz clonada
# ============================================================================

print(f"\n[TEST 1/3] Testando sua voz clonada: {ELEVENLABS_VOICE_ID}")
print("-" * 100)

if not ELEVENLABS_VOICE_ID:
    print("❌ ELEVENLABS_VOICE_ID não configurado no .env")
else:
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": "Olá, meu nome é Raquel. Este é um teste de voz.",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)

        if response.status_code == 200:
            print(f"✅ SUA VOZ FUNCIONA PERFEITAMENTE!")
            print(f"   Voice ID: {ELEVENLABS_VOICE_ID}")
            print(f"   Audio gerado: {len(response.content)} bytes")
        else:
            print(f"❌ Erro {response.status_code}")
            error_detail = response.json().get('detail', {})
            print(f"   Mensagem: {error_detail.get('message', response.text[:200])}")
            print(f"   Status: {error_detail.get('status', 'desconhecido')}")

    except Exception as e:
        print(f"❌ Erro: {e}")

# ============================================================================
# TEST 2: Listar voices disponíveis
# ============================================================================

print(f"\n[TEST 2/3] Listando voices disponíveis no ElevenLabs")
print("-" * 100)

try:
    url = "https://api.elevenlabs.io/v1/voices"
    headers = {"xi-api-key": ELEVENLABS_API_KEY}
    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code == 200:
        voices = response.json().get('voices', [])
        print(f"✅ {len(voices)} voices disponíveis:\n")

        # Mostrar primeiros 5
        for i, voice in enumerate(voices[:5], 1):
            print(f"{i}. {voice.get('name')}")
            print(f"   ID: {voice.get('voice_id')}")
            print(f"   Descrição: {voice.get('labels', {}).get('accent', 'N/A')}")
            print()

        # Procurar por voices customizados (sua voz clonada)
        custom = [v for v in voices if 'custom' in v.get('labels', {})]
        if custom:
            print(f"\n🎯 VOICES CLONADOS/CUSTOMIZADOS:")
            for voice in custom:
                print(f"   • {voice.get('name')} — ID: {voice.get('voice_id')}")
        else:
            print(f"⚠️ Nenhum voice customizado encontrado")

    else:
        print(f"❌ Erro ao listar voices: {response.status_code}")

except Exception as e:
    print(f"❌ Erro: {e}")

# ============================================================================
# TEST 3: Testar voice padrão
# ============================================================================

print(f"\n[TEST 3/3] Testando voice padrão (fallback)")
print("-" * 100)

default_voice_id = "21m00Tcm4TlvDq8ikWAM"  # "Rachel" — voice padrão feminino

url = f"https://api.elevenlabs.io/v1/text-to-speech/{default_voice_id}"
headers = {
    "xi-api-key": ELEVENLABS_API_KEY,
    "Content-Type": "application/json"
}
data = {
    "text": "Teste com voice padrão.",
    "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.75
    }
}

try:
    response = requests.post(url, json=data, headers=headers, timeout=10)

    if response.status_code == 200:
        print(f"✅ VOICE PADRÃO FUNCIONA!")
        print(f"   Voice: Rachel (ID: {default_voice_id})")
        print(f"   Audio gerado: {len(response.content)} bytes")
    else:
        print(f"❌ Erro: {response.status_code}")

except Exception as e:
    print(f"❌ Erro: {e}")

# ============================================================================
# RECOMENDAÇÃO FINAL
# ============================================================================

print(f"\n" + "=" * 100)
print("💡 RECOMENDAÇÃO")
print("=" * 100)

print("""
SE SUA VOZ CLONADA NÃO FUNCIONAR:

Use este voice padrão no .env:
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM

Ou acesse https://elevenlabs.io/voice-lab para:
1. Confirmar que sua voz foi criada corretamente
2. Copiar o Voice ID correto
3. Verificar se está com status "Ready"

Depois rode este teste novamente!
""")

print("=" * 100)
