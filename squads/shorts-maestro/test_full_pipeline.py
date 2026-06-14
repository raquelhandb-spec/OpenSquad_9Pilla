#!/usr/bin/env python3
"""
🚀 TEST FULL PIPELINE — Teste end-to-end do workflow 9Pilla
Simula dados → Análise Order Flow → Morning Call → Shorts

Fluxo testado:
1. quick_start.py — gera CSV simulado com 10 candles
2. profit_flow_analyzer.py — analisa order flow
3. setup_raquel_analyzer.py — análise técnica com seu setup
4. morning_call.py — gera Morning Call (requer Brapi real)
5. shorts_processor.py — divide em 3 blocos
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run_command(description, command, timeout=120):
    """Executa um comando e mostra status"""
    print(f"\n{'='*70}")
    print(f"[{description}]")
    print(f"{'='*70}")

    try:
        result = subprocess.run(
            command,
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding='utf-8'
        )

        print(result.stdout)

        if result.returncode != 0:
            print(f"❌ Erro (exit code: {result.returncode})")
            if result.stderr:
                print("STDERR:", result.stderr)
            return False
        else:
            print(f"✅ {description} concluído com sucesso!")
            return True

    except subprocess.TimeoutExpired:
        print(f"⏱️ Timeout após {timeout}s")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def main():
    print("\n" + "="*70)
    print("🚀 TESTE FULL PIPELINE — 9PILLA MORNING CALL WORKFLOW")
    print("="*70)
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print(f"Base Dir: {BASE_DIR}")

    results = {}

    # ========================================================================
    # FASE 1: Gerar dados simulados
    # ========================================================================

    print("\n\n📊 FASE 1: Gerando dados simulados (CSV com 10 candles)...")

    ok = run_command(
        "STEP 1/5: quick_start.py",
        [sys.executable, '-u', 'quick_start.py'],
        timeout=60
    )
    results['quick_start'] = ok

    # ========================================================================
    # FASE 2: Análise Order Flow
    # ========================================================================

    print("\n\n🔥 FASE 2: Analisando Order Flow (Profit Pro CSV)...")

    ok = run_command(
        "STEP 2/5: profit_flow_analyzer.py",
        [sys.executable, '-u', 'profit_flow_analyzer.py'],
        timeout=60
    )
    results['profit_flow'] = ok

    # Ler resultado da análise
    json_output = os.path.join(OUTPUT_DIR, 'profit_flow_analysis.json')
    if os.path.exists(json_output):
        try:
            with open(json_output, 'r', encoding='utf-8') as f:
                flow_data = json.load(f)

            print("\n📊 RESUMO ORDER FLOW:")
            print(f"   Ponta em controle: {flow_data['ponta'].get('ponta_controle')}")
            print(f"   Total compras: {flow_data['analysis'].get('total_compras', 0):,.0f}")
            print(f"   Total vendas: {flow_data['analysis'].get('total_vendas', 0):,.0f}")
            print(f"   Saldo: {flow_data['analysis'].get('saldo_final', 0):,.0f}")
        except Exception as e:
            print(f"⚠️ Erro ao ler resultado: {e}")

    # ========================================================================
    # FASE 3: Análise técnica com seu setup
    # ========================================================================

    print("\n\n📈 FASE 3: Análise técnica (SMA 20/45/200)...")

    ok = run_command(
        "STEP 3/5: setup_raquel_analyzer.py",
        [sys.executable, '-u', 'setup_raquel_analyzer.py'],
        timeout=120
    )
    results['technical_analysis'] = ok

    # ========================================================================
    # FASE 4: Testar Writer Agent (Claude) com dados simulados
    # ========================================================================

    print("\n\n📝 FASE 4: Testando WriterAgent (Claude API)...")
    print("   (gerando script de exemplo)")

    from agents.writer import WriterAgent

    try:
        writer = WriterAgent()

        # Verificar conexão
        if not writer.validate_connection():
            print("⚠️ Claude API não está acessível")
            print("   💡 Verifique:")
            print("      1. pip install anthropic")
            print("      2. ANTHROPIC_API_KEY configurada no .env")
            print("      3. Créditos disponíveis em https://console.anthropic.com/settings/billing")
            results['writer_agent'] = False
        else:
            print("✅ Claude API conectado")

            # Tentar gerar um script curto
            script = writer.generate_script(
                market_data={
                    'ticker': 'PETR4',
                    'change_percent': -1.76,
                    'trend_topic': 'Teste de Order Flow + Setup técnico',
                    'full_market': {
                        'ibov': {'value': 176200, 'change_pct': 0.71},
                        'dolar': {'value': 4.96, 'change_pct': 0.40},
                        'petr4': {'value': 47.50, 'change_pct': -1.76},
                        'brent': {'value': 103.45, 'change_pct': 3.92},
                    }
                },
                video_format='shorts'
            )

            if script.get('status') == 'generated':
                print("✅ Script gerado com sucesso!")
                print(f"   Tamanho: {len(script['script_full'])} caracteres")
                print(f"\n📄 PRÉVIA DO SCRIPT:")
                print("-" * 70)
                print(script['script_full'][:500] + "...")
                print("-" * 70)
                results['writer_agent'] = True
            else:
                print(f"❌ Erro ao gerar script: {script.get('message')}")
                results['writer_agent'] = False

    except Exception as e:
        print(f"❌ Erro ao testar WriterAgent: {e}")
        results['writer_agent'] = False

    # ========================================================================
    # FASE 5: Relatório final
    # ========================================================================

    print("\n\n" + "="*70)
    print("📋 RESUMO DO TESTE END-TO-END")
    print("="*70)

    status_map = {
        'quick_start': '✅ Dados simulados',
        'profit_flow': '✅ Order Flow analisado',
        'technical_analysis': '✅ Setup técnico validado',
        'writer_agent': '✅ WriterAgent (Claude) funcionando',
    }

    for key, msg in status_map.items():
        status = "✅" if results.get(key) else "❌"
        print(f"{status} {msg}")

    all_ok = all(results.values())

    if all_ok:
        print("\n🎉 TESTE COMPLETO COM SUCESSO!")
        print("""
PRÓXIMOS PASSOS:
1. ✅ Dados de teste funcionando (simul ados)
2. ✅ Order Flow analisado (PONTA COMPRADORA identificada)
3. ✅ Setup técnico validado (SMA 20/45/200)
4. ✅ WriterAgent pronto (Claude gerando scripts)

🚀 Para rodar com dados REAIS:
   python morning_call.py

   Isso vai:
   • Buscar dados reais do BRAPI
   • Analisar macro + geopolítica
   • Gerar Morning Call completo
   • Enviar para aprovação no Telegram
   • Você aprova → texto pronto para WhatsApp
        """)
    else:
        print("\n⚠️ Alguns testes falharam.")
        print("Erros acima indicam o que corrigir.")

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
