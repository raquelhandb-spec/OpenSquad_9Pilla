#!/usr/bin/env python3
"""
☕ MORNING CALL 9PILLA — Gerador diário em TEXTO (formato padrão)

Estratégia da Raquel (11/06/2026):
- TEXTO todo dia (WhatsApp/Blog), custo ~US$ 0,02
- Vídeo HeyGen só 1-2x por semana
- Áudio ocasional, com aprovação

Fluxo:
1. Prospector busca dados reais (Brapi)
2. Analyst lê macro + geopolítica + fluxo (com histórico)
3. Tracker revisa a expectativa de ontem (bloco [CONFERE?])
4. Writer gera o Morning Call completo em texto
5. Envia para Telegram com botões ✅/❌
6. Aprovado → texto pronto para colar no WhatsApp (Turma 9Pilla)

USO (na máquina da Raquel):
    python morning_call.py
"""

import os
import sys
import json
from datetime import datetime

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))

from agents.prospector import ProspectorAgent
from agents.market_analyst import MarketAnalystAgent
from agents.expectation_tracker import ExpectationTrackerAgent
from agents.writer import WriterAgent
from approval_bot import send_for_approval

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

KNOWN_TICKERS = {'petr4': 'PETR4', 'vale3': 'VALE3', 'itub4': 'ITUB4',
                 'b3sa3': 'B3SA3', 'ibov': '^BVSP'}


def main():
    print("="*60)
    print(f"☕ MORNING CALL 9PILLA — {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("="*60)

    mc_id = f"MC_{datetime.now().strftime('%Y%m%d')}"

    # 1. Dados reais do mercado
    print("\n[1/5] 🔍 Buscando dados reais (Brapi)...")
    prospector = ProspectorAgent(brapi_key=os.getenv('BRAPI_API_KEY', ''))
    prosp = prospector.run()
    market_data = prosp.get('market_data', {})
    top_topic = prosp.get('top_topic', {})

    # Ticker em foco: o ativo que mais se mexeu no dia
    movers = [(k, abs(v.get('change_pct', 0))) for k, v in market_data.items()
              if k in KNOWN_TICKERS]
    focus_ticker = KNOWN_TICKERS[max(movers, key=lambda x: x[1])[0]] if movers else 'IBOV'
    print(f"   Ativo em foco: {focus_ticker}")

    # 2. Análise profissional
    print("\n[2/5] 🧠 Analista lendo macro, geopolítica e fluxo...")
    analyst = MarketAnalystAgent()
    analysis = analyst.analyze(
        ticker=focus_ticker,
        market_data=market_data,
        news_context=top_topic.get('title', '')
    )
    if analysis.get('status') != 'completed':
        print(f"❌ Analista falhou: {analysis.get('message')}")
        sys.exit(1)

    # 3. Accountability: revisar ontem + salvar hoje
    print("\n[3/5] 🔍 Conferindo a expectativa de ontem...")
    tracker = ExpectationTrackerAgent()
    review = tracker.review_yesterday(today_market=market_data)
    review_text = review.get('review_text') if review.get('status') == 'completed' else None
    if review_text:
        print("   ✅ Bloco [CONFERE?] gerado")
    tracker.save_expectations(analysis=analysis, market_snapshot=market_data)

    # 4. Escrever o Morning Call
    print("\n[4/5] 📝 Escrevendo Morning Call com a voz da Raquel...")
    writer = WriterAgent()
    ticker_key = focus_ticker.lower().replace('^bvsp', 'ibov')
    focus_data = market_data.get(ticker_key, {})
    mc = writer.generate_script(
        market_data={
            'ticker': focus_ticker,
            'change_percent': focus_data.get('change_pct', 0),
            'trend_topic': top_topic.get('title', 'Mercado hoje'),
            'full_market': market_data
        },
        analyst_insights=analysis,
        video_format='morning_call',
        yesterday_review=review_text
    )

    if mc.get('status') != 'generated':
        print(f"❌ Writer falhou: {mc.get('message')}")
        sys.exit(1)

    # Salvar localmente
    out_path = os.path.join(OUTPUT_DIR, f'{mc_id}.md')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(mc['script_full'])
    print(f"   💾 Salvo em: {out_path}")

    # 5. Enviar para aprovação no Telegram
    print("\n[5/5] 📱 Enviando para aprovação no Telegram...")
    ok = send_for_approval(mc['script_full'], mc_id, stage="mc")

    if ok:
        print("\n" + "="*60)
        print("✅ MORNING CALL ENVIADO PARA SEU TELEGRAM!")
        print("="*60)
        print("""
PRÓXIMOS PASSOS:
1. Garanta que o approval_bot.py está rodando (outra janela)
2. Leia o Morning Call no Telegram
3. ✅ APROVAR → texto pronto, é só colar no WhatsApp da Turma
4. ❌ REJEITAR → mande o feedback, e rode de novo

Custo deste Morning Call: ~US$ 0,03 (texto, sem HeyGen) 💛
        """)
    else:
        print("\n⚠️ Falha no envio Telegram. O texto está salvo em:")
        print(f"   {out_path}")


if __name__ == "__main__":
    main()
