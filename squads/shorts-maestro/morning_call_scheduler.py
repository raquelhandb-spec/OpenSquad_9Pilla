#!/usr/bin/env python3
"""
⏰ MORNING CALL AUTOMÁTICO — 09:09 TODOS OS DIAS

Roda automáticamente via Windows Task Scheduler
Horário: 09:09 todos os dias
Função: Gera Morning Call, salva, envia para aprovação

Setup Windows (execute UMA VEZ):
    python morning_call_scheduler.py --setup

Depois Task Scheduler cuida de rodar diariamente!
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Adicionar path para imports
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from agents.prospector import ProspectorAgent
from agents.market_analyst import MarketAnalystAgent
from agents.expectation_tracker import ExpectationTrackerAgent
from agents.writer import WriterAgent
from approval_bot import send_for_approval

KNOWN_TICKERS = {'petr4': 'PETR4', 'vale3': 'VALE3', 'itub4': 'ITUB4',
                 'b3sa3': 'B3SA3', 'ibov': '^BVSP'}
OUTPUT_DIR = os.path.join(BASE_DIR, 'data', 'morning_calls')
os.makedirs(OUTPUT_DIR, exist_ok=True)

LOG_FILE = os.path.join(BASE_DIR, 'logs', 'morning_call_scheduler.log')
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)


def log(msg):
    """Log para arquivo e console"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_msg = f"[{timestamp}] {msg}"
    print(log_msg)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_msg + '\n')


def run_morning_call():
    """Executa pipeline completo do Morning Call"""
    try:
        log("=" * 70)
        log("🚀 MORNING CALL AUTOMÁTICO INICIADO")
        log("=" * 70)

        mc_id = f"MC_{datetime.now().strftime('%Y%m%d')}"

        # 1. Prospector
        log("[1/5] 🔍 Buscando dados reais (Brapi)...")
        prospector = ProspectorAgent(brapi_key=os.getenv('BRAPI_API_KEY', ''))
        prosp = prospector.run()
        market_data = prosp.get('market_data', {})
        top_topic = prosp.get('top_topic', {})

        movers = [(k, abs(v.get('change_pct', 0))) for k, v in market_data.items()
                  if k in KNOWN_TICKERS]
        focus_ticker = KNOWN_TICKERS[max(movers, key=lambda x: x[1])[0]] if movers else 'IBOV'
        log(f"   ✅ Ativo em foco: {focus_ticker}")

        # 2. Analyst
        log("[2/5] 🧠 Analista lendo macro, geopolítica e fluxo...")
        analyst = MarketAnalystAgent()
        analysis = analyst.analyze(
            ticker=focus_ticker,
            market_data=market_data,
            news_context=top_topic.get('title', '')
        )
        if analysis.get('status') != 'completed':
            log(f"   ❌ Analista falhou: {analysis.get('message')}")
            return False

        # 3. Tracker
        log("[3/5] 🔍 Conferindo expectativa de ontem...")
        tracker = ExpectationTrackerAgent()
        review = tracker.review_yesterday(today_market=market_data)
        review_text = review.get('review_text') if review.get('status') == 'completed' else None
        if review_text:
            log("   ✅ Bloco [CONFERE?] gerado")
        tracker.save_expectations(analysis=analysis, market_snapshot=market_data)

        # 4. Writer
        log("[4/5] 📝 Escrevendo Morning Call...")
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
            log(f"   ❌ Writer falhou: {mc.get('message')}")
            return False

        # 5. Salvar
        out_path = os.path.join(OUTPUT_DIR, f'{mc_id}.txt')
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(mc['script_full'])
        log(f"   💾 Salvo em: {out_path}")

        # 6. Enviar para aprovação
        log("[5/5] 📱 Enviando para aprovação...")
        ok = send_for_approval(mc['script_full'], mc_id, stage="mc")

        if ok:
            log("✅ MORNING CALL ENVIADO PARA APROVAÇÃO NO TELEGRAM!")
        else:
            log("⚠️ Falha ao enviar para Telegram, mas arquivo está salvo")

        log("=" * 70)
        log("✅ MORNING CALL AUTOMÁTICO CONCLUÍDO!")
        log("=" * 70)
        return True

    except Exception as e:
        log(f"❌ ERRO: {str(e)}")
        import traceback
        log(traceback.format_exc())
        return False


def setup_windows_task():
    """Setup automático para Windows Task Scheduler"""
    print("\n" + "=" * 70)
    print("⏰ SETUP: MORNING CALL AUTOMÁTICO NO WINDOWS")
    print("=" * 70)
    print("""
Para automatizar o Morning Call às 09:09 todos os dias:

1. Abra Task Scheduler (Agendador de Tarefas)
   - Windows + R → taskschd.msc → Enter

2. Clique em "Criar Tarefa Básica"

3. Preenchimento:
   Nome: Morning Call 9Pilla
   Descrição: Gera Morning Call automáticamente todos os dias às 09:09

4. Gatilho: Clique "Novo..."
   - Tipo: Diariamente
   - Hora: 09:09
   - Recorrência: Todos os dias

5. Ação: Clique "Novo..."
   - Programa: python.exe
   - Argumentos: C:\\seu\\caminho\\morning_call_scheduler.py --run
   - Iniciar em: C:\\seu\\caminho\\

6. Condições:
   ☑ Executar apenas se o usuário estiver conectado
   ☑ Executar com privilégios mais elevados

7. Configurações:
   ☑ Permitir na demanda
   ☑ Se a tarefa não terminar em 24 horas, forçar encerramento

Logs: data/morning_calls/morning_call_scheduler.log
    """)
    print("=" * 70)


if __name__ == "__main__":
    if '--setup' in sys.argv:
        setup_windows_task()
    elif '--run' in sys.argv:
        run_morning_call()
    else:
        print("USO:")
        print("  python morning_call_scheduler.py --setup    (primeira vez)")
        print("  python morning_call_scheduler.py --run      (rodar agora)")
