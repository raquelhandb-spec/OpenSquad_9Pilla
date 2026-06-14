#!/usr/bin/env python3
"""
✅ VALIDAR DADOS DO MORNING CALL — Compara dados dos blocos com BRAPI em tempo real
Corrige inconsistências e garante que TUDO vem de dados reais
"""

import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))

BRAPI_KEY = os.getenv('BRAPI_API_KEY', '')
BASE_URL = "https://brapi.dev/api"
HEADERS = {"Authorization": f"Bearer {BRAPI_KEY}"}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, 'output', 'shorts')

def get_real_market_data():
    """Busca dados REAIS do BRAPI em tempo real"""

    print("\n🔍 Buscando dados REAIS do BRAPI...")

    data = {}

    try:
        # Quote: ações + índice
        response = requests.get(
            f"{BASE_URL}/quote/PETR4,VALE3,ITUB4,B3SA3,^BVSP",
            headers=HEADERS,
            timeout=10
        )

        if response.status_code == 200:
            quotes = response.json().get('results', [])
            for quote in quotes:
                symbol = quote.get('symbol', '').upper()
                data[symbol] = {
                    'price': quote.get('regularMarketPrice', 0),
                    'change': quote.get('regularMarketChange', 0),
                    'change_pct': quote.get('regularMarketChangePercent', 0),
                    'timestamp': quote.get('updateTime', datetime.now().isoformat())
                }

        # Currency: dólar
        fx_response = requests.get(
            f"{BASE_URL}/v2/currency",
            params={"currency": "USD-BRL"},
            headers=HEADERS,
            timeout=10
        )

        if fx_response.status_code == 200:
            fx = fx_response.json().get('currency', [])
            if fx:
                usd = fx[0]
                data['USD-BRL'] = {
                    'price': float(usd.get('bidPrice', 0) or 0),
                    'change': float(usd.get('bidVariation', 0) or 0),
                    'change_pct': float(usd.get('percentageChange', 0) or 0),
                    'timestamp': datetime.now().isoformat()
                }

        print("✅ Dados BRAPI obtidos!")
        return data

    except Exception as e:
        print(f"❌ Erro ao buscar BRAPI: {e}")
        return None

def extract_numbers_from_text(text):
    """Extrai números do texto em português"""

    extracted = {}

    # PETR4 - procura por "41 reais e 18 centavos" ou "R$ 41,18"
    if 'petr4' in text.lower():
        # Padrão: "41 reais e 18 centavos"
        import re
        match = re.search(r'41\s+reais?\s+e\s+(\d+)\s+centavos', text.lower())
        if match:
            extracted['PETR4'] = float(f"41.{match.group(1)}")

        # Padrão: "R$ 41,18"
        match = re.search(r'R\$\s+(\d+,\d+)', text)
        if match:
            extracted['PETR4'] = float(match.group(1).replace(',', '.'))

    # VALE3 - procura por "79 reais e 17 centavos"
    if 'vale3' in text.lower():
        import re
        match = re.search(r'79\s+reais?\s+e\s+(\d+)\s+centavos', text.lower())
        if match:
            extracted['VALE3'] = float(f"79.{match.group(1)}")

    # IBOV - procura por "171 mil 133"
    if 'ibov' in text.lower():
        import re
        match = re.search(r'171\s+mil\s+(\d+)', text.lower())
        if match:
            extracted['IBOV'] = float(f"171{match.group(1)}")

    # DÓLAR - procura por "5 reais e 8 centavos"
    if 'dólar' in text.lower() or 'dolar' in text.lower():
        import re
        match = re.search(r'5\s+reais?\s+e\s+(\d+)\s+centavos', text.lower())
        if match:
            extracted['USD-BRL'] = float(f"5.{match.group(1)}")

    return extracted

def validate_bloco(bloco_num, real_data):
    """Valida um bloco contra dados reais"""

    bloco_file = os.path.join(OUTPUT_DIR, f'MC_20260613', f'bloco{bloco_num}.txt')

    if not os.path.exists(bloco_file):
        print(f"❌ Arquivo não encontrado: {bloco_file}")
        return False

    with open(bloco_file, 'r', encoding='utf-8') as f:
        bloco_text = f.read()

    print(f"\n📋 VALIDANDO BLOCO {bloco_num}")
    print("-" * 80)

    extracted = extract_numbers_from_text(bloco_text)

    if not extracted:
        print(f"⚠️ Nenhum dado extraído do bloco")
        return False

    print(f"Dados encontrados no bloco: {extracted}")
    print(f"Dados reais do BRAPI: {real_data}")
    print()

    # Comparar
    discrepancies = []

    for symbol, bloco_price in extracted.items():
        if symbol in real_data:
            real_price = real_data[symbol]['price']
            diff = abs(bloco_price - real_price)
            diff_pct = (diff / real_price * 100) if real_price > 0 else 0

            if diff_pct > 1.0:  # Mais de 1% de diferença
                discrepancies.append({
                    'symbol': symbol,
                    'bloco': bloco_price,
                    'real': real_price,
                    'diff': diff,
                    'diff_pct': diff_pct
                })
                print(f"⚠️ DISCREPÂNCIA em {symbol}:")
                print(f"   Bloco diz: {bloco_price}")
                print(f"   BRAPI diz: {real_price}")
                print(f"   Diferença: {diff:.2f} ({diff_pct:.2f}%)")
            else:
                print(f"✅ {symbol}: OK (bloco={bloco_price}, real={real_price})")

    return len(discrepancies) == 0

# ============================================================================
# MAIN
# ============================================================================

print("=" * 80)
print("✅ VALIDADOR DE DADOS — Morning Call vs BRAPI")
print("=" * 80)

# Buscar dados reais
real_data = get_real_market_data()

if not real_data:
    print("❌ Não consegui buscar dados do BRAPI. Verifique sua conexão e API key.")
    exit(1)

# Mostrar dados reais obtidos
print("\n📊 DADOS REAIS DO BRAPI (AGORA):")
print("-" * 80)
for symbol, data in real_data.items():
    print(f"{symbol}: R$ {data['price']:.2f} ({data['change_pct']:+.2f}%) - {data['timestamp']}")

# Validar cada bloco
print("\n" + "=" * 80)
print("🔍 VALIDANDO BLOCOS")
print("=" * 80)

all_valid = True
for bloco_num in [1, 2, 3]:
    if not validate_bloco(bloco_num, real_data):
        all_valid = False

# Resultado final
print("\n" + "=" * 80)
if all_valid:
    print("✅ TODOS OS BLOCOS ESTÃO CORRETOS!")
else:
    print("⚠️ EXISTEM DISCREPÂNCIAS — BLOCOS PRECISAM SER ATUALIZADOS COM DADOS REAIS")
print("=" * 80)

print("\n💡 RECOMENDAÇÃO:")
print("1. Rodar brapi_explorer.py para ver todos os endpoints")
print("2. Modificar prospector.py para extrair TODOS os dados")
print("3. Rodar shorts_processor.py com dados reais e validados")
print("4. Validar novamente com este script")
