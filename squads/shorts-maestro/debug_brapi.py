#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 DEBUG BRAPI — Vê exatamente o que BRAPI está retornando
"""

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))

BRAPI_KEY = os.getenv('BRAPI_API_KEY', '')
BASE_URL = "https://brapi.dev/api"
HEADERS = {"Authorization": f"Bearer {BRAPI_KEY}"}

print("=" * 100)
print("🔍 DEBUG BRAPI")
print("=" * 100)

# ============================================================================
# TEST 1: Quote simples (sem parâmetros)
# ============================================================================

print("\n[TEST 1] GET /quote/PETR4 (SEM parâmetros)")
print("-" * 100)

try:
    response = requests.get(
        f"{BASE_URL}/quote/PETR4",
        headers=HEADERS,
        timeout=10
    )

    print(f"Status: {response.status_code}")
    print(f"Response:")
    data = response.json()
    print(json.dumps(data, indent=2, ensure_ascii=False))

except Exception as e:
    print(f"❌ Erro: {e}")

# ============================================================================
# TEST 2: Quote com range e interval
# ============================================================================

print("\n[TEST 2] GET /quote/PETR4?range=2y&interval=1d (COM parâmetros)")
print("-" * 100)

try:
    response = requests.get(
        f"{BASE_URL}/quote/PETR4",
        params={
            "range": "2y",
            "interval": "1d"
        },
        headers=HEADERS,
        timeout=10
    )

    print(f"Status: {response.status_code}")
    print(f"Response (primeiros 50 resultados):")
    data = response.json()

    if 'results' in data:
        print(f"Total de resultados: {len(data['results'])}")
        print("\nPrimeiro resultado:")
        if data['results']:
            print(json.dumps(data['results'][0], indent=2, ensure_ascii=False))
    else:
        print(json.dumps(data, indent=2, ensure_ascii=False))

except Exception as e:
    print(f"❌ Erro: {e}")

# ============================================================================
# TEST 3: Tentar /quote/list
# ============================================================================

print("\n[TEST 3] GET /quote/list (listar quotes)")
print("-" * 100)

try:
    response = requests.get(
        f"{BASE_URL}/quote/list",
        headers=HEADERS,
        timeout=10
    )

    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Disponível: {data.get('status', 'N/A')}")
        print(f"Total: {len(data.get('stocks', []))}")
    else:
        print(f"Response: {response.text[:500]}")

except Exception as e:
    print(f"❌ Erro: {e}")

# ============================================================================
# TEST 4: Verificar estrutura de dados
# ============================================================================

print("\n[TEST 4] Estrutura esperada dos dados")
print("-" * 100)

print("""
BRAPI retorna dados com estrutura:
{
  "results": [
    {
      "symbol": "PETR4",
      "regularMarketPrice": 41.18,
      "regularMarketChange": -0.60,
      "regularMarketChangePercent": -1.39,
      "regularMarketOpen": 41.78,
      "regularMarketHigh": 41.85,
      "regularMarketLow": 40.95,
      "regularMarketVolume": 123456,
      "timestamp": 1686614400,
      "close": 41.18,
      "open": 41.78,
      "high": 41.85,
      "low": 40.95,
      ...
    }
  ]
}

OU com histórico:
{
  "results": [
    {
      "timestamp": 1686614400,
      "open": 41.00,
      "high": 41.50,
      "low": 40.95,
      "close": 41.18,
      "volume": 123456
    },
    ...
  ]
}
""")

print("\n" + "=" * 100)
print("✅ Se você vê muitos resultados em TEST 2, o problema pode ser:")
print("   1. Script não está processando corretamente")
print("   2. Precisa ajustar o parsing dos dados")
print("=" * 100)
