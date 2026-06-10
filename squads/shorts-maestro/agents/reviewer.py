#!/usr/bin/env python3
"""
ReviewerAgent — Human-in-the-Loop Script Approval via Telegram
Sends scripts to Raquel for approval, collects feedback, prevents wasteful HeyGen spending
"""

import requests
import json
from datetime import datetime
from typing import Dict, Any, Optional, List

class ReviewerAgent:
    def __init__(self, telegram_bot_token: str, telegram_chat_id: str):
        """
        Args:
            telegram_bot_token: Token do bot Telegram (@BotFather)
            telegram_chat_id: Chat ID de Raquel para receber scripts

        ⚠️ SETUP REQUIRED:
        1. Criar bot: https://t.me/BotFather
        2. Copiar token: sk_...
        3. Enviar /start ao bot
        4. Executar: curl https://api.telegram.org/bot{token}/getUpdates
        5. Encontrar chat_id e salvar
        """
        self.telegram_bot_token = telegram_bot_token
        self.telegram_chat_id = telegram_chat_id
        self.base_url = f"https://api.telegram.org/bot{telegram_bot_token}"
        self.headers = {"Content-Type": "application/json"}

        # Store approval status (em produção, seria DB)
        self.approvals_db = {}

    def validate_credentials(self) -> bool:
        """Valida se Telegram bot está funcional"""
        try:
            response = requests.get(
                f"{self.base_url}/getMe",
                headers=self.headers,
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            print(f"⚠️ Erro validação Telegram: {e}")
            return False

    def send_script_for_approval(
        self,
        script_data: Dict[str, Any],
        script_id: str
    ) -> Dict[str, Any]:
        """
        Envia script para aprovação de Raquel via Telegram

        Args:
            script_data: Dict com script_full, market_data, etc
            script_id: ID único do script (para rastreamento)

        Returns:
            Dict com status e message_id
        """

        ticker = script_data.get('market_data', {}).get('ticker', 'IBOV')
        full_script = script_data.get('script_full', '')

        # Formatar mensagem Telegram
        message_text = f"""📝 NOVO SCRIPT PARA APROVAÇÃO

🎯 Ticker: {ticker}
⏰ Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}
📌 ID: {script_id}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{full_script}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ RESPONDA:
👍 APROVA (use a reação 👍)
👎 REJEITA (use a reação 👎)
💬 Feedback: Responda a essa mensagem

⚠️ PROTEÇÃO ORÇAMENTO:
Se REJEITAR → Nenhum crédito HeyGen gasto ✅
Se APROVAR → Avatar será criado (~US$ 0.30) ⚡
"""

        print(f"\n📨 Enviando script {script_id} para aprovação Telegram...")
        print(f"   Ticker: {ticker}")
        print(f"   Chat ID: {self.telegram_chat_id}")

        try:
            response = requests.post(
                f"{self.base_url}/sendMessage",
                headers=self.headers,
                json={
                    "chat_id": self.telegram_chat_id,
                    "text": message_text,
                    "parse_mode": "HTML"
                },
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                message_id = data['result']['message_id']

                # Registrar no DB local
                self.approvals_db[script_id] = {
                    'message_id': message_id,
                    'sent_at': datetime.now().isoformat(),
                    'status': 'pending',
                    'ticker': ticker,
                    'script_data': script_data
                }

                return {
                    'status': 'sent',
                    'script_id': script_id,
                    'message_id': message_id,
                    'telegram_url': f"https://t.me/c/{self.telegram_chat_id}/{message_id}",
                    'next_step': 'Aguardando reação de Raquel...'
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

    def check_approval_status(self, script_id: str) -> Dict[str, Any]:
        """Verifica status de aprovação de um script"""

        if script_id not in self.approvals_db:
            return {
                'status': 'not_found',
                'script_id': script_id,
                'message': 'Script não encontrado na fila de aprovação'
            }

        approval = self.approvals_db[script_id]
        message_id = approval['message_id']

        # Em produção, consultaria Telegram API para reações
        # Por enquanto, retorna status pendente
        return {
            'status': approval['status'],
            'script_id': script_id,
            'message_id': message_id,
            'sent_at': approval['sent_at'],
            'ticker': approval['ticker'],
            'awaiting_feedback': True,
            'note': 'Em produção: use Telegram Bot API para monitorar reações'
        }

    def mark_approved(
        self,
        script_id: str,
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Marca script como aprovado (quando Raquel reagir com 👍)
        Trigger para criar avatar no HeyGen

        ⚠️ A PARTIR DAQUI: Gasta créditos HeyGen!
        """

        if script_id not in self.approvals_db:
            return {
                'status': 'error',
                'message': f'Script {script_id} não encontrado'
            }

        approval = self.approvals_db[script_id]
        approval['status'] = 'approved'
        approval['approved_at'] = datetime.now().isoformat()
        approval['notes'] = notes

        script_data = approval['script_data']

        return {
            'status': 'approved',
            'script_id': script_id,
            'approved_at': approval['approved_at'],
            'ticker': approval['ticker'],
            'script_data': script_data,
            'next_step': '🚀 CRIAR AVATAR NO HEYGEN (vai gastar créditos!)',
            'warning': '⚠️ A partir daqui, US$ 0.30 será debitado dos créditos HeyGen'
        }

    def mark_rejected(
        self,
        script_id: str,
        feedback: str = "Rejeitar e tentar novamente"
    ) -> Dict[str, Any]:
        """
        Marca script como rejeitado (quando Raquel reagir com 👎)
        ✅ Nenhum crédito HeyGen gasto!
        """

        if script_id not in self.approvals_db:
            return {
                'status': 'error',
                'message': f'Script {script_id} não encontrado'
            }

        approval = self.approvals_db[script_id]
        approval['status'] = 'rejected'
        approval['rejected_at'] = datetime.now().isoformat()
        approval['feedback'] = feedback

        return {
            'status': 'rejected',
            'script_id': script_id,
            'rejected_at': approval['rejected_at'],
            'ticker': approval['ticker'],
            'feedback': feedback,
            'heygen_cost': 'R$ 0 (script rejeitado) ✅',
            'next_step': '🔄 Writer vai aprender com feedback e tentar novamente',
            'safety_win': 'Proteção de orçamento ativada - Zero gasto em script ruim!'
        }

    def get_approval_history(self) -> Dict[str, Any]:
        """Retorna histórico de aprovações/rejeições"""

        approved = [s for s in self.approvals_db.values() if s['status'] == 'approved']
        rejected = [s for s in self.approvals_db.values() if s['status'] == 'rejected']
        pending = [s for s in self.approvals_db.values() if s['status'] == 'pending']

        return {
            'total_submitted': len(self.approvals_db),
            'approved_count': len(approved),
            'rejected_count': len(rejected),
            'pending_count': len(pending),
            'approval_rate': f"{len(approved) / max(len(self.approvals_db), 1) * 100:.1f}%",
            'history': {
                'approved': approved,
                'rejected': rejected,
                'pending': pending
            }
        }

    def run_validation_test(self) -> Dict[str, Any]:
        """Testa conexão Telegram"""

        print("🧪 ReviewerAgent — Teste de Setup")
        print("=" * 60)

        is_valid = self.validate_credentials()

        if is_valid:
            print("✅ Telegram bot conectado com sucesso!")
        else:
            print("⚠️ Telegram bot não está configurado")
            print("\n📋 SETUP RÁPIDO:")
            print("1. Vá para: https://t.me/BotFather")
            print("2. Crie novo bot: /newbot")
            print("3. Copie o token")
            print("4. Configure em environment vars")
            print("5. Teste novamente\n")

        print("=" * 60)

        return {
            'status': 'ready' if is_valid else 'needs_setup',
            'telegram_connected': is_valid,
            'chat_id': self.telegram_chat_id,
            'approval_workflow': 'Telegram Bot API',
            'setup_guide': 'https://core.telegram.org/bots'
        }


# INTEGRAÇÃO: Writer → Reviewer → Executor
class WriterToReviewerToExecutorPipeline:
    """
    Fluxo completo: Writer → Reviewer → Executor

    1. Writer gera script ✅
    2. Reviewer envia para Raquel aprova
    3. SE APROVADO → Executor cria vídeo
    4. SE REJEITADO → Voltar para Writer (learn from feedback)
    """

    def __init__(
        self,
        reviewer_agent: ReviewerAgent,
        heygen_agent: Optional[Any] = None  # Será importado quando necessário
    ):
        self.reviewer = reviewer_agent
        self.heygen_agent = heygen_agent

    def submit_script_for_approval_and_execute(
        self,
        writer_output: Dict[str, Any],
        script_id: str
    ) -> Dict[str, Any]:
        """
        Workflow completo: Submete para aprovação e aguarda feedback

        Retorna: Dados prontos para HeyGen APENAS se aprovado
        """

        print("\n📝 → 👤 → 🎬 Pipeline: Writer → Reviewer → Executor")

        # 1. Enviar para aprovação
        approval_result = self.reviewer.send_script_for_approval(
            script_data=writer_output,
            script_id=script_id
        )

        if approval_result['status'] != 'sent':
            return {
                'status': 'approval_failed',
                'message': 'Não conseguiu enviar para Telegram'
            }

        print(f"\n✅ Script enviado para Raquel!")
        print(f"   Aguardando reação (👍 aprova, 👎 rejeita)")
        print(f"   Link: {approval_result.get('telegram_url')}")

        # 2. Aguardar aprovação (em produção, seria webhook)
        return {
            'status': 'awaiting_approval',
            'script_id': script_id,
            'message_id': approval_result['message_id'],
            'workflow_state': 'reviewer',
            'next_step': 'Raquel aprova via Telegram (reação 👍) → Executor cria vídeo'
        }

    def on_script_approved(
        self,
        script_id: str,
        avatar_id: str = "Avatar_1"
    ) -> Dict[str, Any]:
        """
        CALLBACK: Chamado quando Raquel aprova via Telegram (👍)

        Agora É SEGURO gastar créditos HeyGen!
        """

        print(f"\n🎉 SCRIPT {script_id} APROVADO POR RAQUEL!")

        # 1. Marcar como aprovado no Reviewer
        approval = self.reviewer.mark_approved(script_id)

        if not self.heygen_agent:
            return {
                'status': 'approved_awaiting_heygen',
                'script_id': script_id,
                'message': 'HeyGen agent não configurado ainda',
                'next_step': 'Importar HeyGenAgent e criar vídeo'
            }

        # 2. AGORA: Criar avatar (gastar créditos)
        script_data = approval['script_data']

        from heygen_avatar import OptimizedAvatarCreationFlow

        flow = OptimizedAvatarCreationFlow(
            heygen_api_key=self.heygen_agent.api_key
        )

        result = flow.on_script_approved_by_reviewer(
            script=script_data['script_sections'],
            avatar_id=avatar_id,
            video_title=f"9Pilla_Shorts_{script_id}"
        )

        return {
            'status': 'creating_avatar',
            'script_id': script_id,
            'heygen_result': result,
            'workflow_state': 'executor',
            'next_step': 'HeyGen processando vídeo (2-5 min)...'
        }

    def on_script_rejected(
        self,
        script_id: str,
        feedback: str
    ) -> Dict[str, Any]:
        """
        CALLBACK: Chamado quando Raquel rejeita via Telegram (👎)

        ✅ NENHUM GASTO! Voltar para Writer com feedback.
        """

        print(f"\n📝 SCRIPT {script_id} REJEITADO POR RAQUEL (Feedback: {feedback})")
        print(f"   ✅ Proteção de créditos HeyGen: R$ 0 gasto")

        # Marcar como rejeitado
        rejection = self.reviewer.mark_rejected(script_id, feedback)

        return {
            'status': 'rejected',
            'script_id': script_id,
            'feedback': feedback,
            'heygen_cost_avoided': 'US$ 0.30',
            'next_step': '🔄 Writer aprende com feedback e gera novo script',
            'workflow_state': 'writer_retry',
            'protection': 'Budget protection ativada - evitou gasto desnecessário!'
        }


# Test
if __name__ == "__main__":
    print("\n" + "="*60)
    print("REVIEWER AGENT TEST")
    print("="*60 + "\n")

    # Setup mock (em produção, viriam de env vars ou Telegram)
    TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
    TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"

    reviewer = ReviewerAgent(
        telegram_bot_token=TELEGRAM_BOT_TOKEN,
        telegram_chat_id=TELEGRAM_CHAT_ID
    )

    # Teste 1: Validar setup
    print("📋 Teste 1: Setup Telegram")
    setup = reviewer.run_validation_test()
    print(json.dumps(setup, indent=2, ensure_ascii=False))

    # Teste 2: Enviar script para aprovação
    print("\n📝 Teste 2: Enviar script para aprovação")

    mock_script = {
        'script_full': """Bom dia! Aqui é Raquel...

📊 TERMÔMETRO DO DIA
💵 Dólar: R$ 5,03
📈 Ibov: 174.197
🛢️ Petróleo: US$ 95,45

PETR4 caiu 1.76% hoje por causa da queda do petróleo...

A lição é: Sempre tem contexto por trás dos números.

Continue nos acompanhando! 🚀""",
        'market_data': {
            'ticker': 'PETR4',
            'price': 27.50,
            'change_percent': -1.76
        },
        'status': 'generated'
    }

    script_id = f"PETR4_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    approval = reviewer.send_script_for_approval(
        script_data=mock_script,
        script_id=script_id
    )

    print(json.dumps(approval, indent=2, ensure_ascii=False))

    print("\n" + "="*60)
    print("WORKFLOW USAGE:")
    print("="*60)
    print("""
# 1. Writer gera script
writer = WriterAgent()
script = writer.generate_script(market_data)

# 2. Enviar para Reviewer
reviewer = ReviewerAgent(bot_token, chat_id)
script_id = f"PETR4_{datetime.now()}"
reviewer.send_script_for_approval(script, script_id)

# 3. Raquel aprova via Telegram (👍)
# Webhook detecta reação e chama:
pipeline.on_script_approved(script_id)

# 4. Avatar criado automaticamente
# HeyGen gasta US$ 0.30 ✅ (só porque foi aprovado!)

# OU Raquel rejeita via Telegram (👎)
# Webhook detecta reação e chama:
pipeline.on_script_rejected(script_id, "Muito fast")

# ✅ Zero gasto! Voltar para Writer com feedback.
    """)
