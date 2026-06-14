#!/usr/bin/env python3
"""
ElevenLabs Integration Agent — Narração IA com voz Raquel
Gera áudio a partir de scripts (para YouTube Shorts + Podcast)
"""

import requests
import json
from datetime import datetime
from typing import Dict, Any, Optional
import io

class ElevenLabsAgent:
    def __init__(self, api_key: str, voice_id: str = None):
        """
        api_key: sk_2e12b95dc92a231055f4e9d4f275ae9fab83940d59b26a3e
        voice_id: SERÁ PREENCHIDO PELA RAQUEL APÓS CLONAR VOZ

        Placeholder para voice_id:
        - Ao clonar voz em https://elevenlabs.io/voice-lab
        - Copiar o Voice ID
        - Passar para Raquel informar
        """
        self.api_key = api_key
        self.voice_id = voice_id or "PLACEHOLDER_VOICE_ID"  # SERÁ SUBSTITUÍDO
        self.base_url = "https://api.elevenlabs.io/v1"
        self.headers = {
            "xi-api-key": api_key,
            "Content-Type": "application/json"
        }

    def validate_credentials(self) -> bool:
        """Valida credenciais ElevenLabs"""
        try:
            response = requests.get(
                f"{self.base_url}/voices",
                headers=self.headers,
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            print(f"⚠️ Validação ElevenLabs: {e}")
            return False

    def list_voices(self) -> Dict[str, Any]:
        """Lista todas as vozes disponíveis"""
        try:
            response = requests.get(
                f"{self.base_url}/voices",
                headers=self.headers,
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                voices = data.get('voices', [])
                return {
                    'status': 'success',
                    'total_voices': len(voices),
                    'voices': [
                        {
                            'voice_id': v.get('voice_id'),
                            'name': v.get('name'),
                            'category': v.get('category', 'unknown')
                        }
                        for v in voices
                    ]
                }
            else:
                return {'status': 'error', 'message': response.text}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def generate_speech(
        self,
        text: str,
        voice_id: str = None,
        model_id: str = "eleven_monolingual_v2",
        stability: float = 0.5,
        similarity_boost: float = 0.75
    ) -> Dict[str, Any]:
        """
        Gera áudio a partir de texto

        Args:
            text: Texto para narração
            voice_id: Voice ID (usa a clonada da Raquel se não especificar)
            model_id: eleven_monolingual_v2 (português) ou eleven_multilingual_v2
            stability: 0.0-1.0 (mais estável = menos natural)
            similarity_boost: 0.0-1.0 (mais similar = mais natural)

        Returns:
            Dict com status e caminho do arquivo MP3
        """

        if voice_id is None:
            voice_id = self.voice_id

        # Se ainda for placeholder, avisar
        if voice_id == "PLACEHOLDER_VOICE_ID":
            return {
                'status': 'error',
                'message': 'Voice ID da Raquel ainda não foi configurado!',
                'instruction': 'Raquel precisa: 1) Clonar voz em ElevenLabs, 2) Passar o Voice ID'
            }

        payload = {
            "text": text,
            "model_id": model_id,
            "voice_settings": {
                "stability": stability,
                "similarity_boost": similarity_boost
            }
        }

        try:
            response = requests.post(
                f"{self.base_url}/text-to-speech/{voice_id}",
                headers=self.headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                # Salvar áudio
                audio_path = f"/tmp/narration_{datetime.now().timestamp()}.mp3"
                with open(audio_path, 'wb') as f:
                    f.write(response.content)

                return {
                    'status': 'success',
                    'audio_path': audio_path,
                    'audio_size_bytes': len(response.content),
                    'voice_id': voice_id,
                    'model': model_id
                }
            else:
                return {
                    'status': 'error',
                    'message': response.text,
                    'status_code': response.status_code
                }

        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

    def get_voice_settings(self, voice_id: str = None) -> Dict[str, Any]:
        """Obtém configurações de uma voz"""

        if voice_id is None:
            voice_id = self.voice_id

        try:
            response = requests.get(
                f"{self.base_url}/voices/{voice_id}/settings",
                headers=self.headers,
                timeout=10
            )

            if response.status_code == 200:
                return {
                    'status': 'success',
                    'settings': response.json()
                }
            else:
                return {'status': 'error', 'message': response.text}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def set_voice_settings(
        self,
        stability: float = 0.5,
        similarity_boost: float = 0.75,
        voice_id: str = None
    ) -> Dict[str, Any]:
        """Configura as settings da voz"""

        if voice_id is None:
            voice_id = self.voice_id

        payload = {
            "stability": stability,
            "similarity_boost": similarity_boost
        }

        try:
            response = requests.post(
                f"{self.base_url}/voices/{voice_id}/settings/edit",
                headers=self.headers,
                json=payload,
                timeout=10
            )

            return {
                'status': 'success' if response.status_code == 200 else 'error',
                'stability': stability,
                'similarity_boost': similarity_boost
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def run_narration_test(self, test_text: str = None) -> Dict[str, Any]:
        """Testa narração com texto de exemplo"""

        if test_text is None:
            test_text = """
Olá! Eu sou a Raquel, criadora da 9Pilla.
Aqui a gente fala de dinheiro sem tabu, sem economês.
Seu próximo passo? Educação financeira de verdade.
            """

        print("🎙️ ElevenLabs Agent — Teste de Narração")
        print("=" * 60)

        # Gerar áudio
        result = self.generate_speech(test_text)

        if result['status'] == 'error':
            print(f"❌ Erro: {result['message']}")
            if 'instruction' in result:
                print(f"ℹ️ {result['instruction']}")
        else:
            print(f"✅ Áudio gerado com sucesso!")
            print(f"   Caminho: {result['audio_path']}")
            print(f"   Tamanho: {result['audio_size_bytes']} bytes")

        print("=" * 60)
        return result


# Pipeline: Script → Narração (para Writer Agent)
class WriterToNarrationPipeline:
    """
    Converte scripts do Writer Agent em áudio via ElevenLabs
    """

    def __init__(self, elevenlabs_api_key: str, voice_id: str):
        self.elevenlabs = ElevenLabsAgent(
            api_key=elevenlabs_api_key,
            voice_id=voice_id
        )

    def process_script(self, script: Dict[str, Any]) -> Dict[str, Any]:
        """
        Converte script estruturado em áudio

        Input (do Writer Agent):
        {
            'topic': 'Petróleo acima de US$ 100',
            'hook': '...',
            'delivery': '...',
            'punchline': '...',
        }

        Output:
        {
            'audio_path': '/tmp/...',
            'duration_seconds': 47,
            'ready_for_video': True
        }
        """

        # Concatenar partes do script
        full_text = f"""
{script.get('hook', '')}

{script.get('delivery', '')}

{script.get('punchline', '')}
        """.strip()

        # Gerar narração
        result = self.elevenlabs.generate_speech(full_text)

        if result['status'] == 'success':
            return {
                'status': 'success',
                'audio_path': result['audio_path'],
                'topic': script.get('topic'),
                'ready_for_executor': True
            }
        else:
            return {
                'status': 'error',
                'message': result['message']
            }


# Test
if __name__ == "__main__":
    print("\n" + "="*60)
    print("ELEVENLABS AGENT TEST")
    print("="*60 + "\n")

    # Criar agente (com placeholder voice_id)
    agent = ElevenLabsAgent(api_key="sk_2e12b95dc92a231055f4e9d4f275ae9fab83940d59b26a3e")

    # Teste 1: Validar credenciais
    print("1️⃣ Validando credenciais...")
    is_valid = agent.validate_credentials()
    print(f"   Status: {'✅ Válida' if is_valid else '⚠️ Falhou (network restriction)'}\n")

    # Teste 2: Listar vozes (quando tiver acesso)
    print("2️⃣ Listando vozes disponíveis...")
    voices = agent.list_voices()
    print(f"   Status: {voices.get('status')}\n")

    # Teste 3: Teste de narração
    print("3️⃣ Teste de narração (espera Raquel passar Voice ID)...")
    test_result = agent.run_narration_test()

    print("\n" + "="*60)
    print("INSTRUÇÕES PARA RAQUEL")
    print("="*60)
    print("""
1. Acesse: https://elevenlabs.io/voice-lab
2. Clique em "Clone Voice"
3. Grave sua voz (10-30 segundos falando)
4. Dê um nome (ex: "Raquel 9Pilla")
5. Copie o VOICE ID que aparecerá
6. ME PASSE: "Minha voz se chama: [NOME] e o Voice ID é: [ID]"

Exemplo:
   "Minha voz se chama: Raquel 9Pilla e o Voice ID é: abc123def456"

PRONTO! A gente ativa em tudo e toca o butão!
    """)
