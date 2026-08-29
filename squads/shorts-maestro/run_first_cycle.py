import os
import json

# Set all credentials
os.environ['BRAPI_API_KEY'] = 'tky3Vocipoj9ZocxEumbCe'
os.environ['ELEVENLABS_API_KEY'] = 'sk_2e12b95dc92a231055f4e9d4f275ae9fab83940d59b26a3e'
os.environ['ELEVENLABS_VOICE_ID'] = '0r2zCQO0vO1jOfWbm7N7'
os.environ['HEYGEN_API_KEY'] = 'sk_V2_hgu_kkX2jmyuQzW_9R8ocwO4rBLzHX0mrIyQwKAJWLAGrJjW'
os.environ['HEYGEN_AVATAR_ID'] = '351538dd8eea417882a312681f2168d9'
os.environ['ZAPI_INSTANCE_ID'] = '3F11BDD3D23071C40CFC9EED2DF277BD'
os.environ['ZAPI_API_TOKEN'] = 'D06BC58B1E9B2833DB10EBF3'
os.environ['TELEGRAM_BOT_TOKEN'] = '8371953023:AAH8zJBO9hc0n_Z0x5D_f630piy31brCGXc'
os.environ['TELEGRAM_CHAT_ID'] = '7686120986'
os.environ['MANYCHAT_API_KEY'] = '11058963:93a19ff0c8e75129c2d9303960e974dd'

from agents.prospector import ProspectorAgent
from agents.writer import WriterAgent
from agents.reviewer import ReviewerAgent
from agents.zapi_broadcaster import ZAPIBroadcasterAgent

print("\n🚀 INICIANDO PRIMEIRO CICLO 9PILLA!\n")

# Step 1: Prospector
print("[1/3] 🔍 PROSPECTOR - Buscando tema trending...")
prospector = ProspectorAgent(brapi_key='tky3Vocipoj9ZocxEumbCe')
market_data = prospector.run()
print(f"✅ Tema: {market_data.get('topic', 'N/A')}")
print(f"   Ticker: {market_data.get('trending_ticker', 'N/A')}\n")

# Step 2: Writer
print("[2/3] 📝 WRITER - Gerando script com Raquel Voice...")
writer = WriterAgent(ollama_base_url="http://localhost:11434")
script = writer.generate_script(
    market_data={
        'ticker': market_data.get('trending_ticker', 'IBOV'),
        'price': market_data.get('current_price'),
        'change_percent': market_data.get('price_change'),
        'trend_topic': market_data.get('topic', 'Tema de mercado')
    }
)
print(f"✅ Script gerado! ({len(script.get('script_full', '').split())} palavras)\n")

# Step 3: Reviewer
print("[3/3] 📱 REVIEWER - Enviando para Telegram...")
reviewer = ReviewerAgent(
    telegram_bot_token='8371953023:AAH8zJBO9hc0n_Z0x5D_f630piy31brCGXc',
    telegram_chat_id='7686120986'
)
script_id = f"{market_data.get('trending_ticker', 'IBOV')}_{pd.Timestamp.now().strftime('%Y%m%d')}"

try:
    result = reviewer.send_script_for_approval(script, script_id)
    print(f"✅ Script enviado para Telegram!")
    print(f"   Telegram URL: {result.get('telegram_url', 'N/A')}\n")
except Exception as e:
    print(f"⚠️ Erro ao enviar: {e}\n")

print("=" * 60)
print("🎉 CICLO INICIADO!")
print("=" * 60)
print(f"\n📱 PRÓXIMO PASSO:")
print(f"1. Abra seu Telegram")
print(f"2. Vá para: @raquel_9pilla_bot")
print(f"3. Você receberá o SCRIPT em segundos")
print(f"4. Reaja com 👍 para APROVAR")
print(f"5. Vídeo será criado automaticamente!")
print(f"\nSeu Chat ID: 7686120986")
print(f"Bot: @raquel_9pilla_bot\n")

