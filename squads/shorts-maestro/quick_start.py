#!/usr/bin/env python3
"""
🚀 QUICK START — Teste completo em 5 minutos
Simula dados, roda análises, mostra o workflow funcionando
"""

import os
import csv
import subprocess
import sys
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 100)
print("🚀 QUICK START — TESTE COMPLETO DO WORKFLOW")
print("=" * 100)

# ============================================================================
# STEP 1: Criar CSV de teste (simulando dados do Profit Pro)
# ============================================================================

print("\n[STEP 1/4] 📊 Criando dados de teste...")
print("-" * 100)

csv_file = os.path.join(OUTPUT_DIR, 'profit_export.csv')

# Dados simulados realistas
test_data = [
    ('2026-06-14', '09:30', 41.00, 41.10, 40.95, 41.05, 12500),
    ('2026-06-14', '09:35', 41.05, 41.20, 41.00, 41.18, 14300),
    ('2026-06-14', '09:40', 41.18, 41.25, 41.10, 41.22, 11200),
    ('2026-06-14', '09:45', 41.22, 41.35, 41.15, 41.30, 15800),  # Grande compra
    ('2026-06-14', '09:50', 41.30, 41.40, 41.20, 41.35, 13500),
    ('2026-06-14', '09:55', 41.35, 41.30, 41.10, 41.15, 16200),  # Venda forte
    ('2026-06-14', '10:00', 41.15, 41.20, 40.95, 41.10, 14100),
    ('2026-06-14', '10:05', 41.10, 41.28, 41.05, 41.25, 12800),
    ('2026-06-14', '10:10', 41.25, 41.45, 41.20, 41.40, 18900),  # Grande compra 2
    ('2026-06-14', '10:15', 41.40, 41.50, 41.30, 41.45, 15600),
]

try:
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Data', 'Hora', 'Abertura', 'Máxima', 'Mínima', 'Fechamento', 'Volume'])
        writer.writerows(test_data)

    print(f"✅ CSV criado: {csv_file}")
    print(f"   {len(test_data)} candles simulados")
    print(f"   Período: 2026-06-14 09:30 a 10:15")

except Exception as e:
    print(f"❌ Erro ao criar CSV: {e}")
    sys.exit(1)

# ============================================================================
# STEP 2: Rodar análise de Order Flow
# ============================================================================

print("\n[STEP 2/4] 🔥 Analisando Order Flow...")
print("-" * 100)

try:
    result = subprocess.run(
        [sys.executable, 'profit_flow_analyzer.py'],
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
        timeout=30
    )

    if result.returncode == 0:
        print("✅ Análise concluída!")
        print("\nSaída:")
        print(result.stdout)
    else:
        print("❌ Erro na análise")
        print(result.stderr)

except Exception as e:
    print(f"❌ Erro ao rodar análise: {e}")

# ============================================================================
# STEP 3: Rodar análise técnica com seu setup
# ============================================================================

print("\n[STEP 3/4] 📈 Analisando seu setup técnico...")
print("-" * 100)

print("""
Para puxar dados REAIS do BRAPI (último ano):

python setup_raquel_analyzer.py

Isso vai:
✅ Conectar ao BRAPI
✅ Buscar dados de PETR4, VALE3, ITUB4
✅ Calcular SMA 20, 45, 200
✅ Mostrar tendências nos 2 timeframes
✅ Gerar 5 cenários dinâmicos

Roda esse comando agora na sua máquina!
""")

# ============================================================================
# STEP 4: Próximas etapas
# ============================================================================

print("\n[STEP 4/4] 🎯 Próximas etapas...")
print("-" * 100)

print("""
PARA FAZER DE VERDADE (com dados reais):

1️⃣ NO PROFIT PRO:
   • Abra Ferramentas → Editor de Estratégias
   • Copie o script de GUIA-NTSL-ORDER-FLOW.md
   • Rode durante a bolsa amanhã (09:30-16:00)
   • Exporte dados em: output/profit_export.csv

2️⃣ NO PYTHON:
   python profit_flow_analyzer.py    # Analisa Order Flow
   python setup_raquel_analyzer.py   # Analisa seu setup técnico

3️⃣ INTEGRAR COM MORNING CALL:
   • Writer Agent recebe dados de Order Flow + Setup técnico
   • Gera Morning Call baseado em dados REAIS
   • Você aprova no Telegram
   • Publica no YouTube/TikTok/Instagram

📖 DOCUMENTAÇÃO COMPLETA:
   • GUIA-NTSL-ORDER-FLOW.md — Como usar Profit Pro
   • profit_flow_analyzer.py — Processa dados
   • setup_raquel_analyzer.py — Análise técnica
   • PROFIT-PRO-INTEGRATION.md — Pipeline completo

🚀 Tudo pronto! Sua revolução 9Pilla começa agora!
""")

print("=" * 100)
print("✅ QUICK START CONCLUÍDO")
print("=" * 100)
print("\n💡 Próximo passo: python setup_raquel_analyzer.py")
print("   (Para puxar dados REAIS do BRAPI)")
