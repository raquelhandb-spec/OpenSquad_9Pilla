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
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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
from agents.market_analyst import MarketAnalystAgent
from agents.expectation_tracker import ExpectationTrackerAgent


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
            'elevenlabs_voice_id': os.getenv('ELEVENLABS_VOICE_ID', '0r2zCQO0vO1jOfWbm7N7'),
            'heygen_key': os.getenv('HEYGEN_API_KEY', ''),
            'heygen_avatar_id': os.getenv('HEYGEN_AVATAR_ID', '351538dd8eea417882a312681f2168d9'),
            'zapi_instance': os.getenv('ZAPI_INSTANCE_ID', ''),
            'zapi_token': os.getenv('ZAPI_API_TOKEN', ''),
            'telegram_bot_token': os.getenv('TELEGRAM_BOT_TOKEN', ''),
            'telegram_chat_id': os.getenv('TELEGRAM_CHAT_ID', ''),
            'manychat_key': os.getenv('MANYCHAT_API_KEY', ''),
            'anthropic_key': os.getenv('ANTHROPIC_API_KEY', ''),
            'claude_model': os.getenv('CLAUDE_MODEL', 'claude-sonnet-4-6'),
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

        # 2. Writer (Claude API — migrado de Ollama em 11/06/2026)
        if self.config['anthropic_key']:
            self.agents['writer'] = WriterAgent(
                claude_api_key=self.config['anthropic_key'],
                model=self.config['claude_model']
            )
            print(f"✅ Writer Agent (Claude — {self.config['claude_model']})")
        else:
            print("⚠️ Writer Agent (ANTHROPIC_API_KEY não configurada)")

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

        # 10. Market Analyst (macro + geopolítica + fluxo, com histórico Brapi)
        if self.config['anthropic_key']:
            self.agents['analyst'] = MarketAnalystAgent(
                brapi_key=self.config['brapi_key'],
                claude_api_key=self.config['anthropic_key'],
                model=self.config['claude_model']
            )
            print("✅ Market Analyst Agent (macro/geopolítica/fluxo)")
        else:
            print("⚠️ Market Analyst Agent (ANTHROPIC_API_KEY não configurada)")

        # 11. Expectation Tracker (accountability: revisa ontem vs hoje)
        if self.config['anthropic_key']:
            self.agents['tracker'] = ExpectationTrackerAgent(
                claude_api_key=self.config['anthropic_key'],
                model=self.config['claude_model']
            )
            print("✅ Expectation Tracker Agent (revisão diária)")

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
            'CLAUDE_API': validation_results.get('writer', {}).get('status', False),
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

            prospector_result = self.agents['prospector'].run()
            results['stages']['prospector'] = {
                'status': 'completed',
                'result': prospector_result
            }
            top_topic = prospector_result.get('top_topic', {})
            print(f"✅ Tema: {top_topic.get('title', 'N/A')}")
            market_data = prospector_result.get('market_data', {})

            # STAGE 2: Writer
            print("\n[2/6] 📝 WRITER — Gerando script com Raquel Voice...")
            if 'writer' not in self.agents:
                raise RuntimeError("Writer Agent não configurado")

            # Preparar dados do tópico para o Writer
            top_topic = prospector_result.get('top_topic', {})
            ticker_data = top_topic.get('data', {})

            # Extrair ticker limpo das keywords (ex: 'petr4' → 'PETR4')
            keywords = top_topic.get('keywords', [])
            clean_ticker = keywords[0].upper() if keywords else 'IBOV'

            # Se o tema não é um ativo real (ex: tema educação → "INVESTIMENTO"),
            # usar para análise o ativo que mais se mexeu no dia
            KNOWN_TICKERS = {'PETR4', 'VALE3', 'ITUB4', 'B3SA3', 'IBOV', '^BVSP'}
            if clean_ticker not in KNOWN_TICKERS:
                TICKER_MAP = {'petr4': 'PETR4', 'vale3': 'VALE3', 'itub4': 'ITUB4',
                              'b3sa3': 'B3SA3', 'ibov': '^BVSP'}
                movers = [(k, abs(v.get('change_pct', 0))) for k, v in market_data.items()
                          if k in TICKER_MAP]
                if movers:
                    top_mover = max(movers, key=lambda x: x[1])[0]
                    clean_ticker = TICKER_MAP[top_mover]
                    print(f"   ℹ️ Tema sem ticker próprio. Analista usará o ativo mais movimentado: {clean_ticker}")

            # STAGE 1.5: Market Analyst (macro + geopolítica + fluxo)
            analyst_result = None
            if 'analyst' in self.agents:
                print("\n[1.5/6] 🧠 ANALYST — Leitura macro, geopolítica e fluxo...")
                analyst_result = self.agents['analyst'].analyze(
                    ticker=clean_ticker,
                    market_data=market_data,
                    news_context=top_topic.get('title', '')
                )
                results['stages']['analyst'] = {
                    'status': analyst_result.get('status'),
                    'technical_stats': analyst_result.get('technical_stats', {})
                }
                if analyst_result.get('status') != 'completed':
                    print(f"⚠️ Analyst indisponível, Writer seguirá sem análise profunda")
                    analyst_result = None

            # STAGE 1.6: Expectation Tracker (accountability loop)
            yesterday_review_text = None
            if 'tracker' in self.agents:
                # Revisar o que foi dito ontem contra os dados de hoje
                review = self.agents['tracker'].review_yesterday(today_market=market_data)
                if review.get('status') == 'completed':
                    yesterday_review_text = review['review_text']
                    results['stages']['tracker_review'] = {
                        'status': 'completed',
                        'reviewed_date': review['reviewed_date']
                    }
                # Salvar a expectativa de HOJE para revisão amanhã
                if analyst_result:
                    self.agents['tracker'].save_expectations(
                        analysis=analyst_result,
                        market_snapshot=market_data
                    )

            writer_result = self.agents['writer'].generate_script(
                market_data={
                    'ticker': clean_ticker,
                    'price': ticker_data.get('value', 0),
                    'change_percent': ticker_data.get('change_pct', 0),
                    'trend_topic': top_topic.get('title', 'Notícia de mercado'),
                    'full_market': market_data
                },
                analyst_insights=analyst_result,
                yesterday_review=yesterday_review_text
            )

            if writer_result.get('status') == 'error':
                raise RuntimeError(f"Writer falhou: {writer_result.get('message')}")

            results['stages']['writer'] = {
                'status': 'completed',
                'script_id': cycle_id,
                'script': writer_result.get('script_full', '')
            }
            script_word_count = len(writer_result.get('script_full', '').split())
            print(f"✅ Script gerado ({script_word_count} palavras)")

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
                    'status': reviewer_result.get('status'),
                    'message_id': reviewer_result.get('message_id'),
                    'script_id': reviewer_result.get('script_id')
                }
                print(f"✅ Script enviado para Telegram")
                if 'telegram_url' in reviewer_result:
                    print(f"   Link: {reviewer_result.get('telegram_url')}")

            # STAGE 4-6: Aguardando aprovação
            print("\n" + "="*60)
            print("⏳ PRÓXIMA ETAPA: Raquel aprova via Telegram")
            print("="*60)
            print(f"""
INSTRUÇÕES:
1. Garanta que o approval_bot.py está rodando em outra janela:
   python approval_bot.py
2. Abra o Telegram (@raquel_9pilla_bot)
3. Clique no botão ✅ APROVAR (vai criar vídeo HeyGen - US$ 0.30)
   ou no botão ❌ REJEITAR (zero gasto + você pode mandar feedback)

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
        avatar_id: str = None
    ) -> Dict[str, Any]:
        """
        CALLBACK: Chamado quando Raquel aprova via Telegram (👍)

        Executa STAGE 4-5: Executor → Publisher
        """

        print("\n" + "="*60)
        print(f"🎉 APROVADO! Criando vídeo...")
        print("="*60)

        # Usar avatar ID configurado se não fornecido
        if not avatar_id:
            avatar_id = self.config.get('heygen_avatar_id', '351538dd8eea417882a312681f2168d9')

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
            print(f"⚠️ Criando avatar HeyGen com seu avatar realista (US$ 0.30)...")
            print(f"   Avatar ID: {avatar_id}")
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
