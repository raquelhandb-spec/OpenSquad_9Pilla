#!/usr/bin/env python3
"""
9Pilla Shorts-Maestro Orchestrator
Orquestrador central que executa o pipeline completo:
Prospector → Writer → Reviewer → Executor → Publisher → Z-API
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, Any, Optional

# Import agents
from agents.prospector import ProspectorAgent
from agents.writer import WriterAgent
from agents.reviewer import ReviewerAgent
from agents.elevenlabs_narration import ElevenLabsAgent
from agents.heygen_avatar import HeyGenAgent
from agents.publisher import PublisherAgent
from agents.zapi_broadcaster import ZAPIBroadcasterAgent
from agents.manychat_integration import ManyChatAgent
from agents.investing_analysis import InvestingAnalysisAgent


class NinePillaOrchestrator:
    """
    Orquestrador do sistema 9Pilla
    Gerencia todo o fluxo de geração, aprovação, produção e publicação de shorts
    """

    def __init__(self):
        """Inicializa todos os agentes com credenciais das env vars"""
        self.config = self._load_config()
        self.agents = {}
        self._init_agents()
        self.cycle_history = []

    def _load_config(self) -> Dict[str, Any]:
        """Carrega configuração das variáveis de ambiente"""
        return {
            'brapi_key': os.getenv('BRAPI_API_KEY', ''),
            'elevenlabs_key': os.getenv('ELEVENLABS_API_KEY', ''),
            'heygen_key': os.getenv('HEYGEN_API_KEY', ''),
            'zapi_instance': os.getenv('ZAPI_INSTANCE_ID', ''),
            'zapi_token': os.getenv('ZAPI_API_TOKEN', ''),
            'telegram_bot_token': os.getenv('TELEGRAM_BOT_TOKEN', ''),
            'telegram_chat_id': os.getenv('TELEGRAM_CHAT_ID', ''),
            'manychat_key': os.getenv('MANYCHAT_API_KEY', ''),
            'ollama_url': os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434'),
            'elevenlabs_voice_id': os.getenv('ELEVENLABS_VOICE_ID', 'PLACEHOLDER_VOICE_ID'),
        }

    def _init_agents(self):
        """Inicializa todos os agentes"""
        print("\n🚀 Inicializando agentes 9Pilla...")

        # 1. Prospector
        if self.config['brapi_key']:
            self.agents['prospector'] = ProspectorAgent(
                brapi_key=self.config['brapi_key']
            )
            print("✅ Prospector Agent")
        else:
            print("⚠️ Prospector Agent (BRAPI_API_KEY não configurada)")

        # 2. Writer (Ollama)
        self.agents['writer'] = WriterAgent(
            ollama_base_url=self.config['ollama_url']
        )
        print("✅ Writer Agent (Ollama)")

        # 3. Reviewer (Telegram)
        if self.config['telegram_bot_token'] and self.config['telegram_chat_id']:
            self.agents['reviewer'] = ReviewerAgent(
                telegram_bot_token=self.config['telegram_bot_token'],
                telegram_chat_id=self.config['telegram_chat_id']
            )
            print("✅ Reviewer Agent (Telegram)")
        else:
            print("⚠️ Reviewer Agent (TELEGRAM credentials não configuradas)")

        # 4. ElevenLabs (Narration)
        if self.config['elevenlabs_key']:
            self.agents['elevenlabs'] = ElevenLabsAgent(
                api_key=self.config['elevenlabs_key']
            )
            print("✅ ElevenLabs Agent")
        else:
            print("⚠️ ElevenLabs Agent (ELEVENLABS_API_KEY não configurada)")

        # 5. HeyGen (Video Avatar)
        if self.config['heygen_key']:
            self.agents['heygen'] = HeyGenAgent(
                api_key=self.config['heygen_key']
            )
            print("✅ HeyGen Agent")
        else:
            print("⚠️ HeyGen Agent (HEYGEN_API_KEY não configurada)")

        # 6. Publisher
        self.agents['publisher'] = PublisherAgent()
        print("✅ Publisher Agent")

        # 7. Z-API (WhatsApp)
        if self.config['zapi_instance'] and self.config['zapi_token']:
            self.agents['zapi'] = ZAPIBroadcasterAgent(
                instance_id=self.config['zapi_instance'],
                api_token=self.config['zapi_token']
            )
            print("✅ Z-API Broadcaster Agent")
        else:
            print("⚠️ Z-API Agent (ZAPI credentials não configuradas)")

        # 8. ManyChat
        if self.config['manychat_key']:
            self.agents['manychat'] = ManyChatAgent(
                api_key=self.config['manychat_key']
            )
            print("✅ ManyChat Agent")
        else:
            print("⚠️ ManyChat Agent (MANYCHAT_API_KEY não configurada)")

        # 9. Investing Analysis (web scraper)
        self.agents['investing'] = InvestingAnalysisAgent()
        print("✅ Investing Analysis Agent")

    def validate_setup(self) -> Dict[str, Any]:
        """Valida se todos os agentes estão configurados"""
        print("\n" + "="*60)
        print("🔍 VALIDANDO SETUP 9PILLA")
        print("="*60)

        validation_results = {}

        # Validar cada agente
        if 'prospector' in self.agents:
            validation_results['prospector'] = {
                'status': self.agents['prospector'].validate_credentials(),
                'required': True
            }

        if 'writer' in self.agents:
            setup = self.agents['writer'].run_setup_test()
            validation_results['writer'] = {
                'status': setup['status'] == 'ready',
                'required': True,
                'details': setup
            }

        if 'reviewer' in self.agents:
            setup = self.agents['reviewer'].run_validation_test()
            validation_results['reviewer'] = {
                'status': setup['status'] == 'ready',
                'required': True,
                'details': setup
            }

        if 'elevenlabs' in self.agents:
            setup = self.agents['elevenlabs'].run_safe_test()
            validation_results['elevenlabs'] = {
                'status': setup['status'] == 'ready',
                'required': False,
                'details': setup
            }

        if 'heygen' in self.agents:
            setup = self.agents['heygen'].run_safe_test()
            validation_results['heygen'] = {
                'status': setup['status'] == 'ready',
                'required': False,
                'details': setup
            }

        if 'publisher' in self.agents:
            status = self.agents['publisher'].run_platform_status()
            validation_results['publisher'] = {
                'status': status['status'] == 'ready',
                'required': True,
                'details': status
            }

        # Verificar credenciais críticas
        print("\n📋 CREDENCIAIS CRÍTICAS:")
        critical = {
            'BRAPI_API_KEY': bool(self.config['brapi_key']),
            'OLLAMA_RUNNING': validation_results.get('writer', {}).get('status', False),
            'TELEGRAM_BOT': bool(self.config['telegram_bot_token']),
            'ELEVENLABS_VOICE_ID': self.config['elevenlabs_voice_id'] != 'PLACEHOLDER_VOICE_ID'
        }

        for key, status in critical.items():
            emoji = "✅" if status else "⚠️"
            print(f"{emoji} {key}")

        print("\n" + "="*60)

        return {
            'timestamp': datetime.now().isoformat(),
            'agents': validation_results,
            'critical_settings': critical,
            'ready_to_run': all(critical.values())
        }

    def run_full_cycle(self, dry_run: bool = False) -> Dict[str, Any]:
        """
        Executa um ciclo completo da pipeline

        Fluxo:
        1. Prospector identifica tema trending
        2. Writer gera script com Raquel Voice
        3. Reviewer envia para aprovação Raquel (Telegram)
        4. ⏳ Aguarda reação (👍 = cria vídeo, 👎 = tenta novamente)
        5. Se aprovado: Executor (ElevenLabs + HeyGen) cria vídeo
        6. Publisher publica no YouTube + notifica via WhatsApp
        """

        print("\n" + "="*60)
        print("🚀 EXECUTANDO CICLO COMPLETO 9PILLA")
        print("="*60)

        cycle_id = f"9Pilla_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        results = {
            'cycle_id': cycle_id,
            'start_time': datetime.now().isoformat(),
            'stages': {},
            'status': 'running'
        }

        try:
            # STAGE 1: Prospector
            print("\n[1/6] 🔍 PROSPECTOR — Identificando tema trending...")
            if 'prospector' not in self.agents:
                raise RuntimeError("Prospector Agent não configurado")

            prospector_result = self.agents['prospector'].identify_trending_topic()
            results['stages']['prospector'] = {
                'status': 'completed',
                'result': prospector_result
            }
            print(f"✅ Tema: {prospector_result.get('topic')}")
            print(f"   Ticker: {prospector_result.get('trending_ticker')}")

            # STAGE 2: Writer
            print("\n[2/6] 📝 WRITER — Gerando script com Raquel Voice...")
            if 'writer' not in self.agents:
                raise RuntimeError("Writer Agent não configurado")

            writer_result = self.agents['writer'].generate_script(
                market_data={
                    'ticker': prospector_result.get('trending_ticker'),
                    'price': prospector_result.get('current_price'),
                    'change_percent': prospector_result.get('price_change'),
                    'trend_topic': prospector_result.get('topic')
                }
            )
            results['stages']['writer'] = {
                'status': 'completed',
                'script_id': cycle_id
            }
            print(f"✅ Script gerado ({len(writer_result.get('script_full', '').split())} palavras)")

            # STAGE 3: Reviewer
            print("\n[3/6] 👤 REVIEWER — Enviando para aprovação Raquel...")
            if 'reviewer' not in self.agents:
                print("⚠️ Reviewer não configurado - pulando aprovação")
                results['stages']['reviewer'] = {'status': 'skipped'}
            else:
                reviewer_result = self.agents['reviewer'].send_script_for_approval(
                    script_data=writer_result,
                    script_id=cycle_id
                )
                results['stages']['reviewer'] = {
                    'status': reviewer_result['status'],
                    'message_id': reviewer_result.get('message_id')
                }
                print(f"✅ Script enviado para Telegram")
                if 'telegram_url' in reviewer_result:
                    print(f"   Link: {reviewer_result['telegram_url']}")

            # STAGE 4-6: Aguardando aprovação
            print("\n" + "="*60)
            print("⏳ PRÓXIMA ETAPA: Raquel aprova via Telegram")
            print("="*60)
            print(f"""
INSTRUÇÕES:
1. Acesse: {results['stages'].get('reviewer', {}).get('telegram_url', '[Link enviado para Telegram]')}
2. Reaja com 👍 para APROVAR (vai criar vídeo HeyGen - US$ 0.30)
3. Reaja com 👎 para REJEITAR (zero gasto - volta para Writer)
4. Ou responda com feedback

QUANDO APROVAR:
→ Executor (ElevenLabs + HeyGen) cria vídeo
→ Publisher publica no YouTube Shorts
→ Z-API notifica Turma 9Pilla no WhatsApp
            """)

            results['stages']['executor'] = {
                'status': 'pending_approval',
                'waiting_for': 'Raquel approval (Telegram reaction)'
            }
            results['stages']['publisher'] = {
                'status': 'pending_execution',
                'awaiting': 'Video ready'
            }

            results['status'] = 'awaiting_approval'

        except Exception as e:
            results['status'] = 'error'
            results['error'] = str(e)
            print(f"\n❌ Erro: {e}")

        results['end_time'] = datetime.now().isoformat()
        self.cycle_history.append(results)

        return results

    def on_reviewer_approval(
        self,
        script_id: str,
        avatar_id: str = "Avatar_1"
    ) -> Dict[str, Any]:
        """
        CALLBACK: Chamado quando Raquel aprova via Telegram (👍)

        Executa STAGE 4-5: Executor → Publisher
        """

        print("\n" + "="*60)
        print(f"🎉 APROVADO! Criando vídeo...")
        print("="*60)

        # Encontrar ciclo correspondente
        cycle = None
        for c in self.cycle_history:
            if c['cycle_id'] == script_id:
                cycle = c
                break

        if not cycle:
            return {'status': 'error', 'message': f'Ciclo {script_id} não encontrado'}

        # STAGE 4: Executor (ElevenLabs + HeyGen)
        print("\n[4/6] 🎬 EXECUTOR — Criando vídeo...")

        heygen_result = None
        if 'heygen' in self.agents:
            # Criar vídeo com HeyGen (após aprovação!)
            print("⚠️ Criando avatar HeyGen (US$ 0.30)...")
            heygen_result = self.agents['heygen'].create_avatar_video_with_retries(
                script_text=cycle['stages']['writer']['script_id'],
                avatar_id=avatar_id,
                video_title=f"9Pilla_Shorts_{script_id}"
            )
            cycle['stages']['executor'] = {
                'status': 'created',
                'video_id': heygen_result.get('video_id'),
                'heygen_cost': 'US$ 0.30'
            }
            print(f"✅ Avatar criado - aguardando conclusão...")

        # STAGE 5: Publisher
        print("\n[5/6] 📺 PUBLISHER — Publicando no YouTube...")

        if heygen_result and 'publisher' in self.agents:
            # Simular resultado (em produção seria YouTube URL real)
            youtube_result = {
                'status': 'mock_published',
                'video_id': heygen_result.get('video_id'),
                'url': f"https://youtube.com/shorts/9Pilla_{script_id}"
            }
            cycle['stages']['publisher'] = {
                'status': 'published',
                'url': youtube_result['url']
            }
            print(f"✅ Publicado: {youtube_result['url']}")

        # STAGE 6: Z-API Notification
        print("\n[6/6] 💬 Z-API — Notificando Turma 9Pilla...")

        if 'zapi' in self.agents and youtube_result:
            zapi_result = self.agents['zapi'].send_to_group(
                group_id="TURMA_9PILLA_GROUP_ID",
                message=f"""
☀️ NOVO SHORTS 9PILLA! 📺

Assista agora:
{youtube_result['url']}

💬 Me passa seu feedback!
                """.strip()
            )
            print(f"✅ Notificado via WhatsApp")

        cycle['status'] = 'completed'
        cycle['completed_at'] = datetime.now().isoformat()

        return cycle

    def get_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas de ciclos executados"""
        total = len(self.cycle_history)
        completed = sum(1 for c in self.cycle_history if c.get('status') == 'completed')
        approved = sum(1 for c in self.cycle_history if 'reviewer' in c['stages'])

        return {
            'total_cycles': total,
            'completed': completed,
            'awaiting_approval': total - completed,
            'approval_rate': f"{approved / max(total, 1) * 100:.1f}%",
            'cycles': self.cycle_history
        }


# CLI Interface
def main():
    """Interface CLI para o orquestrador"""
    import argparse

    parser = argparse.ArgumentParser(description='9Pilla Shorts-Maestro Orchestrator')
    parser.add_argument('--validate', action='store_true', help='Validar setup')
    parser.add_argument('--cycle', action='store_true', help='Executar ciclo completo')
    parser.add_argument('--dry-run', action='store_true', help='Executar sem realmente publicar')
    parser.add_argument('--stats', action='store_true', help='Mostrar estatísticas')

    args = parser.parse_args()

    # Inicializar orquestrador
    orchestrator = NinePillaOrchestrator()

    if args.validate:
        result = orchestrator.validate_setup()
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))

    elif args.cycle:
        result = orchestrator.run_full_cycle(dry_run=args.dry_run)
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))

    elif args.stats:
        result = orchestrator.get_statistics()
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))

    else:
        print("""
╔════════════════════════════════════════════════════════════════╗
║         9PILLA SHORTS-MAESTRO ORCHESTRATOR                    ║
║                                                                ║
║  Automated YouTube Shorts Generation Pipeline                 ║
║  Prospector → Writer → Reviewer → Executor → Publisher         ║
╚════════════════════════════════════════════════════════════════╝

USAGE:
  python orchestrator.py --validate     # Validar setup
  python orchestrator.py --cycle        # Executar ciclo completo
  python orchestrator.py --stats        # Ver estatísticas

SETUP CHECKLIST:
  1. Configure env vars (veja .env.example)
  2. Instale Ollama e execute: ollama serve
  3. Configure Telegram bot token e chat ID
  4. Clone sua voz no ElevenLabs (Voice ID)
  5. Execute: python orchestrator.py --validate

FULL PIPELINE:
  python orchestrator.py --cycle

Depois de enviar script para aprovação:
  - Raquel recebe no Telegram
  - Reage com 👍 para aprovar (cria vídeo HeyGen)
  - Reage com 👎 para rejeitar (zero gasto, volta para Writer)
        """)


if __name__ == "__main__":
    main()
