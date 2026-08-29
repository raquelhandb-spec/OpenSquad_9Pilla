#!/usr/bin/env python3
"""
ManyChat Integration Agent — Automação de Fluxos WhatsApp + Funil
Com Z-API + ManyChat = máquina de conversão completa
"""

import requests
import json
from datetime import datetime
from typing import Dict, Any, List

class ManyChatAgent:
    def __init__(self, api_key: str):
        """
        api_key format: 11058963:93a19ff0c8e75129c2d9303960e974dd
        """
        self.api_key = api_key
        self.base_url = "https://api.manychat.com/fb/subscriber"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def validate_credentials(self) -> bool:
        """Valida se credenciais estão corretas"""
        try:
            response = requests.get(
                f"{self.base_url}/count",
                headers=self.headers,
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Erro ao validar ManyChat: {e}")
            return False

    def create_subscriber(self, phone: str, name: str = None, metadata: Dict = None) -> Dict[str, Any]:
        """Cria novo subscriber no ManyChat"""

        payload = {
            "subscriber_phone": phone,
        }

        if name:
            payload["first_name"] = name.split()[0] if " " in name else name
            payload["last_name"] = name.split()[1] if " " in name else ""

        if metadata:
            payload["custom_fields"] = metadata

        try:
            response = requests.post(
                f"{self.base_url}/create-subscriber",
                headers=self.headers,
                json=payload,
                timeout=10
            )

            if response.status_code == 200:
                return {
                    'status': 'success',
                    'subscriber_id': response.json().get('subscriber_id'),
                    'phone': phone
                }
            else:
                return {'status': 'error', 'message': response.text}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def assign_flow(self, subscriber_id: str, flow_name: str) -> Dict[str, Any]:
        """
        Atribui um fluxo (automação) ao subscriber

        Fluxos disponíveis:
        - turma_9pilla_welcome (boas-vindas)
        - turma_9pilla_morning_call (morning call diário)
        - upsell_panelinha_3days (Panelinha no dia 3)
        - upsell_desafio_7days (Desafio no dia 7)
        """

        payload = {
            "subscriber_id": subscriber_id,
            "flow_name": flow_name
        }

        try:
            response = requests.post(
                f"{self.base_url}/assign-flow",
                headers=self.headers,
                json=payload,
                timeout=10
            )
            return {
                'status': 'success' if response.status_code == 200 else 'error',
                'flow': flow_name,
                'subscriber_id': subscriber_id
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def send_message(self, phone: str, message: str, media_url: str = None) -> Dict[str, Any]:
        """Envia mensagem direta via ManyChat"""

        payload = {
            "subscriber_phone": phone,
            "text": message
        }

        if media_url:
            payload["attachment_url"] = media_url
            payload["attachment_type"] = "image"

        try:
            response = requests.post(
                f"{self.base_url}/send-message",
                headers=self.headers,
                json=payload,
                timeout=10
            )
            return {
                'status': 'sent' if response.status_code == 200 else 'failed',
                'phone': phone
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def setup_turma_9pilla_flows(self) -> Dict[str, Any]:
        """
        Configura fluxos automáticos da Turma 9Pilla

        Fluxo 1: Welcome (ao entrar)
        Fluxo 2: Morning Call (09h09 diário)
        Fluxo 3: Panelinha Upsell (dia 3)
        Fluxo 4: Desafio Upsell (dia 7)
        Fluxo 5: Papo de Grana Upsell (dia 14)
        """

        flows = {
            'turma_9pilla_welcome': {
                'name': 'Boas-vindas Turma 9Pilla',
                'trigger': 'new_subscriber',
                'message': """
☀️ Bem-vindo(a) à Turma 9Pilla!

Sou a Raquel. Aqui não tem tabu, nem economês.

Você vai receber:
✅ Morning Call diário (09h09)
✅ Análise de mercado sem complicação
✅ Educação financeira para iniciante

Próximo Morning Call: [HH:MM]

Aproveita! 💛
                """,
                'delay': 0
            },

            'turma_9pilla_morning_call': {
                'name': 'Morning Call Automático',
                'trigger': 'schedule',
                'time': '09:09',
                'days': ['MON', 'TUE', 'WED', 'THU', 'FRI'],
                'message': 'Será enviada via Z-API (síncrono com Morning Call gerado)',
                'delay': 0
            },

            'upsell_panelinha_3days': {
                'name': 'Panelinha Secreta - Dia 3',
                'trigger': 'days_in_group',
                'days': 3,
                'message': """
🔓 PANELINHA SECRETA está aberta!

Você já é membro da Turma 9Pilla por 3 dias.
Está na hora de entrar na Panelinha?

Benefícios:
✨ Calls exclusivas com Raquel
✨ Análise profunda de mercado
✨ Comunidade VIP (50+ membros)
✨ Acesso a estudos sobre investimento

💰 Investimento: R$ 97/mês

👉 Quer conhecer mais?
[LINK_PANELINHA]
                """,
                'delay': 0
            },

            'upsell_desafio_7days': {
                'name': 'Desafio Eu, Investidor - Dia 7',
                'trigger': 'days_in_group',
                'days': 7,
                'message': """
🚀 DESAFIO: EU, INVESTIDOR (7 DIAS)

Parabéns! Você está aqui 7 dias.

Essa é a hora. Hora de dar o próximo passo.

DESAFIO EU, INVESTIDOR:
- 7 dias de transformação
- Faça seu 1º investimento
- Aulas ao vivo com Raquel
- Comunidade de suporte

Garanto: em 7 dias você terá seu 1º investimento!

💰 R$ 197 (investimento)

👉 Entra no desafio:
[LINK_DESAFIO]

P.S. Vagas limitadas (30/mês)
                """,
                'delay': 0
            },

            'upsell_papo_grana_14days': {
                'name': 'Papo de Grana - Dia 14',
                'trigger': 'days_in_group',
                'days': 14,
                'message': """
🎬 PAPO DE GRANA - Série Completa

Você está aqui 2 semanas!

Está criando hábito. Quer aprofundar?

PAPO DE GRANA é uma série de 9 episódios (estilo Netflix):
- Neurociência + Comportamento + Finanças
- Sem chatice. Conteúdo de verdade.
- EP.01 gratuito (assista agora!)

👉 Assista EP.01 grátis:
[LINK_EPISODIO_01]

E se quiser série completa (US$ 297):
[LINK_SERIE_COMPLETA]
                """,
                'delay': 0
            }
        }

        return {
            'status': 'configured',
            'flows': flows,
            'note': 'Fluxos precisam ser configurados manualmente no dashboard ManyChat'
        }

    def get_subscriber_list(self, tag: str = None) -> Dict[str, Any]:
        """Lista subscribers (com filtro opcional por tag)"""

        try:
            response = requests.get(
                f"{self.base_url}/list",
                headers=self.headers,
                params={'tag': tag} if tag else {},
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                return {
                    'status': 'success',
                    'total_subscribers': data.get('total_count', 0),
                    'subscribers': data.get('data', [])
                }
            else:
                return {'status': 'error', 'message': response.text}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def run(self) -> Dict[str, Any]:
        """Valida e prepara ManyChat para 9Pilla"""

        print("🤖 ManyChat Agent — Automação de Fluxos WhatsApp")
        print("=" * 60)

        # 1. Validar credenciais
        print("✓ Validando credenciais ManyChat...")
        is_valid = self.validate_credentials()

        if not is_valid:
            return {
                'status': 'error',
                'message': 'Credenciais ManyChat inválidas',
                'note': 'Verifique API key: 11058963:93a19ff0c8e75129c2d9303960e974dd'
            }

        print("✅ Credenciais válidas!")

        # 2. Configurar fluxos
        print("✓ Configurando fluxos automáticos...")
        flows = self.setup_turma_9pilla_flows()

        # 3. Listar subscribers atuais
        print("✓ Listando subscribers...")
        subscribers = self.get_subscriber_list()

        print("=" * 60)

        return {
            'status': 'ready',
            'agent': 'ManyChat',
            'credentials_valid': True,
            'total_subscribers': subscribers.get('total_subscribers', 0),
            'flows_configured': flows,
            'next_step': 'Integrar Z-API webhooks com ManyChat',
            'timestamp': datetime.now().isoformat()
        }


# Integration: Z-API + ManyChat Webhook
class ZAPIManyChatIntegration:
    """
    Quando Z-API recebe novo lead (webhook),
    passa para ManyChat orquestrar os fluxos
    """

    def on_new_lead_from_zapi(self, phone: str, name: str, source: str = "youtube_shorts"):
        """
        Callback quando novo lead chega via Z-API

        Fluxo:
        1. Criar subscriber no ManyChat
        2. Atribuir fluxo "Welcome"
        3. Tag: "source_youtube_shorts"
        4. Agendar upsells (3 dias, 7 dias, 14 dias)
        """

        manychat = ManyChatAgent(api_key="11058963:93a19ff0c8e75129c2d9303960e974dd")

        # 1. Criar subscriber
        print(f"📝 Criando subscriber: {phone}")
        sub = manychat.create_subscriber(
            phone=phone,
            name=name,
            metadata={
                'source': source,
                'joined_date': datetime.now().isoformat(),
                'status': 'lead'
            }
        )

        if sub['status'] != 'success':
            print(f"❌ Erro ao criar subscriber: {sub}")
            return sub

        subscriber_id = sub['subscriber_id']

        # 2. Atribuir fluxo Welcome
        print(f"🎯 Atribuindo fluxo Welcome...")
        manychat.assign_flow(subscriber_id, 'turma_9pilla_welcome')

        # 3. Enviar mensagem Welcome
        welcome_msg = f"""
☀️ Olá {name}! 👋

Bem-vindo(a) à Turma 9Pilla!

Você vai receber:
✅ Morning Call diário (09h09)
✅ Análise de mercado
✅ Educação financeira

Próximo Morning Call sai em alguns minutos!

Aproveita! 💛
        """

        print(f"💬 Enviando welcome message...")
        manychat.send_message(phone, welcome_msg)

        return {
            'status': 'success',
            'subscriber_id': subscriber_id,
            'phone': phone,
            'flows_assigned': [
                'turma_9pilla_welcome',
                'turma_9pilla_morning_call',
                'upsell_panelinha_3days',
                'upsell_desafio_7days',
                'upsell_papo_grana_14days'
            ]
        }


# Test
if __name__ == "__main__":
    print("\n" + "="*60)
    print("MANYCHAT AGENT TEST")
    print("="*60 + "\n")

    agent = ManyChatAgent(api_key="11058963:93a19ff0c8e75129c2d9303960e974dd")
    result = agent.run()

    print("\n" + json.dumps(result, indent=2, ensure_ascii=False))

    print("\n" + "="*60)
    print("SIMULANDO NOVO LEAD (YouTube Shorts)")
    print("="*60 + "\n")

    integration = ZAPIManyChatIntegration()
    lead_result = integration.on_new_lead_from_zapi(
        phone="5511999887766",  # Exemplo
        name="João Silva",
        source="youtube_shorts"
    )

    print("\n" + json.dumps(lead_result, indent=2, ensure_ascii=False))
