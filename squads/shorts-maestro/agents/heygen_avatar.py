#!/usr/bin/env python3
"""
HeyGen Integration Agent — Avatar Video Creation (CUSTO-OTIMIZADO)

⚠️ ESTRATÉGIA DE ECONOMIA:
- Avatar criado APENAS após aprovação do Reviewer Agent
- Nunca gasta créditos em vídeos rejeitados
- Máxima eficiência de tokens
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional

class HeyGenAgent:
    def __init__(self, api_key: str):
        """
        api_key: sk_V2_hgu_kkX2jmyuQzW_9R8ocwO4rBLzHX0mrIyQwKAJWLAGrJjW

        ⚠️ US$ 15 em créditos - usar com sabedoria!
        """
        self.api_key = api_key
        self.base_url = "https://api.heygen.com/v1"
        self.headers = {
            "X-Api-Key": api_key,
            "Content-Type": "application/json"
        }
        self.max_retries = 3
        self.retry_delay = 2

    def validate_credentials(self) -> bool:
        """Valida se credenciais estão corretas"""
        try:
            response = requests.get(
                f"{self.base_url}/avatars.list",
                headers=self.headers,
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            print(f"⚠️ Erro validação HeyGen: {e}")
            return False

    def list_available_avatars(self) -> Dict[str, Any]:
        """Lista avatares disponíveis para usar"""
        try:
            response = requests.get(
                f"{self.base_url}/avatars.list",
                headers=self.headers,
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                avatars = data.get('data', {}).get('avatars', [])

                return {
                    'status': 'success',
                    'total_avatars': len(avatars),
                    'avatars': [
                        {
                            'avatar_id': av.get('avatar_id'),
                            'name': av.get('avatar_name'),
                            'preview_image_url': av.get('preview_image_url')
                        }
                        for av in avatars
                    ]
                }
            else:
                return {'status': 'error', 'message': response.text}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def get_video_generation_status(self, video_id: str) -> Dict[str, Any]:
        """Consulta status de um vídeo em geração"""
        try:
            response = requests.get(
                f"{self.base_url}/video_status.get",
                headers=self.headers,
                params={'video_id': video_id},
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                video_data = data.get('data', {})

                return {
                    'status': 'success',
                    'video_id': video_id,
                    'status': video_data.get('status'),  # 'processing', 'completed', 'failed'
                    'video_url': video_data.get('video_url'),
                    'progress': video_data.get('progress', 0),
                    'error': video_data.get('error_message', None)
                }
            else:
                return {'status': 'error', 'message': response.text}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def create_avatar_video_with_retries(
        self,
        script_text: str,
        avatar_id: str,
        video_title: str = None
    ) -> Dict[str, Any]:
        """
        Cria vídeo com avatar - com retry automático

        ⚠️ IMPORTANTE: APENAS chamar após aprovação do Reviewer Agent!

        Args:
            script_text: Texto a ser narrado
            avatar_id: Avatar a usar (ex: "Avatar_1")
            video_title: Título do vídeo (para rastreamento)

        Returns:
            Dict com video_id, status, etc
        """

        if not video_title:
            video_title = f"9Pilla_Shorts_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        payload = {
            "video_inputs": [
                {
                    "character": {
                        "type": "AVATAR",
                        "avatar_id": avatar_id
                    },
                    "voice": {
                        "type": "TEXT",
                        "input_text": script_text,
                        "language": "pt-BR"
                    },
                    "actions": [
                        {
                            "type": "TALK",
                            "duration": len(script_text.split()) * 0.4  # ~0.4s por palavra
                        }
                    ]
                }
            ],
            "video_title": video_title,
            "test": False  # ⚠️ Usar True para TESTAR sem gastar créditos
        }

        print(f"\n🎬 HeyGen — Criando avatar video")
        print(f"   Título: {video_title}")
        print(f"   Avatar: {avatar_id}")
        print(f"   Texto: {script_text[:100]}...")
        print(f"   ⚠️ ATENÇÃO: Isso vai usar créditos!\n")

        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    f"{self.base_url}/video.generate",
                    headers=self.headers,
                    json=payload,
                    timeout=30
                )

                if response.status_code == 200:
                    data = response.json()
                    video_id = data.get('data', {}).get('video_id')

                    return {
                        'status': 'created',
                        'video_id': video_id,
                        'title': video_title,
                        'avatar_id': avatar_id,
                        'created_at': datetime.now().isoformat(),
                        'note': '⏳ Processando... (pode levar 2-5 min)',
                        'next_step': f'Monitore com: heygen.wait_for_video("{video_id}")'
                    }

                elif response.status_code == 429:  # Rate limit
                    print(f"⚠️ Rate limit (tentativa {attempt+1}/{self.max_retries})")
                    if attempt < self.max_retries - 1:
                        wait_time = self.retry_delay * (2 ** attempt)
                        print(f"   Aguardando {wait_time}s...\n")
                        time.sleep(wait_time)
                        continue
                    else:
                        return {
                            'status': 'error',
                            'message': 'Rate limit excedido após 3 tentativas',
                            'recommendation': 'Tente novamente em alguns minutos'
                        }
                else:
                    return {
                        'status': 'error',
                        'message': response.text,
                        'status_code': response.status_code
                    }

            except Exception as e:
                print(f"❌ Erro na tentativa {attempt+1}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                else:
                    return {'status': 'error', 'message': str(e)}

        return {'status': 'error', 'message': 'Falha após múltiplas tentativas'}

    def wait_for_video_completion(
        self,
        video_id: str,
        max_wait_seconds: int = 600
    ) -> Dict[str, Any]:
        """
        Aguarda conclusão do vídeo (polling)

        Args:
            video_id: ID do vídeo
            max_wait_seconds: Máximo de segundos a esperar (default 10 min)
        """

        print(f"\n⏳ Aguardando conclusão do vídeo {video_id}")
        print(f"   Timeout: {max_wait_seconds}s\n")

        start_time = time.time()
        poll_interval = 5  # 5 segundos entre polls

        while (time.time() - start_time) < max_wait_seconds:
            status = self.get_video_generation_status(video_id)

            if status['status'] != 'success':
                print(f"❌ Erro ao consultar: {status['message']}")
                return status

            video_status = status.get('status')

            if video_status == 'completed':
                print(f"✅ Vídeo pronto!")
                return {
                    'status': 'completed',
                    'video_id': video_id,
                    'video_url': status.get('video_url'),
                    'ready_for_publisher': True
                }

            elif video_status == 'failed':
                print(f"❌ Geração falhou: {status.get('error')}")
                return {
                    'status': 'failed',
                    'video_id': video_id,
                    'error': status.get('error')
                }

            else:  # 'processing' ou outro status
                progress = status.get('progress', 0)
                print(f"   Status: {video_status} (Progresso: {progress}%)")
                time.sleep(poll_interval)

        return {
            'status': 'timeout',
            'video_id': video_id,
            'message': f'Timeout após {max_wait_seconds}s'
        }

    def run_safe_test(self) -> Dict[str, Any]:
        """
        Teste SEGURO sem gastar créditos

        Valida credenciais e lista avatares disponíveis
        """

        print("🧪 HeyGen — Teste Seguro (SEM gastar créditos)")
        print("=" * 60)

        # 1. Validar credenciais
        print("✓ Validando credenciais...")
        is_valid = self.validate_credentials()

        if not is_valid:
            return {
                'status': 'error',
                'message': 'Credenciais HeyGen inválidas'
            }

        print("✅ Credenciais válidas!\n")

        # 2. Listar avatares
        print("✓ Listando avatares disponíveis...")
        avatars = self.list_available_avatars()

        print("=" * 60)

        return {
            'status': 'ready',
            'credentials_valid': True,
            'avatars_available': avatars,
            'next_step': 'Aguardar aprovação de script (Reviewer) → Então criar avatar',
            'cost_warning': '⚠️ US$ 15 em créditos. Use com sabedoria!'
        }


# FLUXO OTIMIZADO: Só cria avatar após aprovação
class OptimizedAvatarCreationFlow:
    """
    Fluxo que economiza créditos:
    1. Script gerado (Writer)
    2. Enviado para aprovação (Reviewer)
    3. ✅ SE APROVADO → APENAS ENTÃO cria avatar (HeyGen)
    4. SE REJEITADO → cancela (não gasta créditos!)
    """

    def __init__(self, heygen_api_key: str):
        self.heygen = HeyGenAgent(api_key=heygen_api_key)

    def on_script_approved_by_reviewer(
        self,
        script: Dict[str, Any],
        avatar_id: str,
        video_title: str
    ) -> Dict[str, Any]:
        """
        CALLBACK: Chamado quando Reviewer aprova o script

        Agora SIM é seguro gastar créditos em avatar!
        """

        # Concatenar partes do script
        full_text = f"""
{script.get('hook', '')}

{script.get('delivery', '')}

{script.get('punchline', '')}
        """.strip()

        print("\n" + "🎉 " * 20)
        print("✅ SCRIPT APROVADO POR RAQUEL!")
        print("🎉 " * 20)
        print(f"\n🎬 Criando avatar video...\n")

        # Criar avatar (agora sim, script foi aprovado)
        result = self.heygen.create_avatar_video_with_retries(
            script_text=full_text,
            avatar_id=avatar_id,
            video_title=video_title
        )

        if result['status'] == 'created':
            print(f"✅ Avatar criado! Video ID: {result['video_id']}")
            print(f"⏳ Aguardando conclusão...\n")

            # Aguardar conclusão
            final_result = self.heygen.wait_for_video_completion(
                video_id=result['video_id']
            )

            return {
                'status': 'avatar_ready',
                'video_id': result['video_id'],
                'video_url': final_result.get('video_url'),
                'ready_for_publisher': True
            }
        else:
            return result


# Test
if __name__ == "__main__":
    print("\n" + "="*60)
    print("HEYGEN AGENT TEST")
    print("="*60 + "\n")

    agent = HeyGenAgent(api_key="sk_V2_hgu_kkX2jmyuQzW_9R8ocwO4rBLzHX0mrIyQwKAJWLAGrJjW")
    result = agent.run_safe_test()

    print("\n" + json.dumps(result, indent=2, ensure_ascii=False))

    print("\n" + "="*60)
    print("GUIA DE USO:")
    print("="*60)
    print("""
⚠️ IMPORTANTE: HeyGen custa créditos!

FLUXO CORRETO:
1. Script gerado pelo Writer
2. Enviado para Raquel aprovar (Reviewer)
3. ✅ SE APROVADO → ENTÃO criar avatar
4. ❌ SE REJEITADO → NÃO gastar créditos!

PARA CRIAR AVATAR:
```python
flow = OptimizedAvatarCreationFlow(api_key)
flow.on_script_approved_by_reviewer(
    script={...},
    avatar_id="Avatar_1",
    video_title="9Pilla_Shorts_..."
)
```

Isso garante:
✅ Zero gasto em vídeos rejeitados
✅ Máxima eficiência dos US$ 15
✅ Só gasta quando script está PRONTO
    """)
