#!/usr/bin/env python3
"""
Teste direto do Telegram - execute isso no seu computador local!
Isso contorna a restrição de rede do servidor remoto.
"""

import requests
from datetime import datetime

# Suas credenciais do Telegram
TELEGRAM_BOT_TOKEN = "8371953023:AAH8zJBO9hc0n_Z0x5D_f630piy31brCGXc"
TELEGRAM_CHAT_ID = "7686120986"

# Script para enviar
SCRIPT_CONTENT = """Bom dia, bom dia! Aqui é Raquel. Já pegou seu café? ☕

📊 TERMÔMETRO DO DIA
💵 Dólar: R$ 5,03
📈 Ibovespa: 174.197
🛢️ Petróleo Brent: US$ 95,45
🏦 PETR4 em movimento: -1.76% - Análise do dia

PETR4 está em 📉 queda hoje. Por quê? Porque o petróleo internacional caiu e isso afeta Petrobras.

Isso pode parecer um número só, mas afeta seu bolso de três formas diferentes. Vou explicar.

A primeira conexão é direta: preço da ação muda, seu patrimônio muda. Simples.
A segunda é no bolso pela inflação.
A terceira é nas oportunidades que você deixa passar.

Lição do dia: Não é coincidência. Quando PETR4 cai, sempre tem um contexto.
Pode ser geopolítica, pode ser balanço, pode ser sentimento do mercado.
O importante é você entender a conexão.

Continue nos acompanhando para as próximas análises! Disclaimer: Conteúdo educacional apenas."""

def send_telegram_message():
    """Envia mensagem de teste para seu Telegram"""

    base_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

    message_text = f"""📝 NOVO SCRIPT PARA APROVAÇÃO

🎯 Ticker: PETR4
⏰ Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}
📌 ID: 9Pilla_TESTE_20260611

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{SCRIPT_CONTENT}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ RESPONDA:
👍 APROVA (use a reação 👍)
👎 REJEITA (use a reação 👎)
💬 Feedback: Responda a essa mensagem

⚠️ PROTEÇÃO ORÇAMENTO:
Se REJEITAR → Nenhum crédito HeyGen gasto ✅
Se APROVAR → Avatar será criado (~US$ 0.30) ⚡"""

    try:
        print("📨 Enviando mensagem para Telegram...")
        print(f"   Bot Token: {TELEGRAM_BOT_TOKEN[:20]}...")
        print(f"   Chat ID: {TELEGRAM_CHAT_ID}")

        response = requests.post(
            f"{base_url}/sendMessage",
            json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message_text,
                "parse_mode": "HTML"
            },
            timeout=10
        )

        print(f"\n📊 Resposta do Telegram: Status {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            message_id = data['result']['message_id']
            print(f"✅ SUCESSO! Mensagem enviada!")
            print(f"   Message ID: {message_id}")
            print(f"\n🎉 Vá para seu Telegram e procure a mensagem!")
            print(f"   Bot: @raquel_9pilla_bot")
            return True
        else:
            print(f"❌ Erro: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Erro ao enviar: {e}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("🤖 TESTE DIRETO DO TELEGRAM")
    print("="*60)

    success = send_telegram_message()

    if success:
        print("\n" + "="*60)
        print("Próximas etapas:")
        print("1. Abra o Telegram")
        print("2. Vá para @raquel_9pilla_bot")
        print("3. Reaja com 👍 para APROVAR o script")
        print("="*60)
