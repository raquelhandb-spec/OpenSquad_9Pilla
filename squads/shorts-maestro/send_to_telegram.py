import requests
import json
from datetime import datetime

TELEGRAM_TOKEN = '8371953023:AAH8zJBO9hc0n_Z0x5D_f630piy31brCGXc'
CHAT_ID = '7686120986'

message_text = """
📝 NOVO SCRIPT PARA APROVAÇÃO (TEST)

🎯 Ticker: PETR4
⏰ Data: 10/06/2026 20:01
📌 ID: TEST_PETR4_20260610

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Bom dia, bom dia! Aqui é Raquel! ☕

📊 TERMÔMETRO DO DIA
💵 Dólar: R$ 5,03
📈 Ibovespa: 174.197
🛢️ Petróleo Brent: US$ 95,45
🏦 PETR4: 📉 queda 1.76%

PETR4 está caindo hoje. Sabe por quê? Porque o petróleo internacional desabou!

Quando o Brent cai, Petrobras cai junto. É assim que funciona.

O interessante é entender A CONEXÃO: preço do petróleo → Petrobras cai → seu patrimônio (se você tem PETR4) muda.

Lição do dia: Não é coincidência! Sempre tem contexto!

Continue nos acompanhando! Disclaimer: Conteúdo educacional apenas.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ RESPONDA:
👍 APROVA (próximo: criar vídeo)
👎 REJEITA (feedback?)
"""

print("📤 Enviando para Telegram...")
response = requests.post(
    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
    json={
        "chat_id": CHAT_ID,
        "text": message_text
    }
)

if response.status_code == 200:
    print("✅ SCRIPT ENVIADO PARA SEU TELEGRAM!")
    print(f"   Bot: @raquel_9pilla_bot")
    print(f"   Chat ID: {CHAT_ID}")
    print("\n🎉 VERIFIQUE SEU TELEGRAM AGORA!")
    print("   Você vai receber a mensagem em SEGUNDOS!")
    print("\n👉 Reaja com 👍 para APROVAR o script!")
else:
    print(f"❌ Erro: {response.status_code}")
    print(response.text)

