#!/usr/bin/env python3
"""
🔍 BRAPI EXPLORER — Descobre e testa TODOS os endpoints do BRAPI
Cria documentação completa de como usar cada endpoint
"""

import requests
import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))

BRAPI_KEY = os.getenv('BRAPI_API_KEY', '')
BASE_URL = "https://brapi.dev/api"
HEADERS = {"Authorization": f"Bearer {BRAPI_KEY}"}

print("=" * 80)
print("🔍 BRAPI EXPLORER — Testando TODOS os endpoints disponíveis")
print("=" * 80)
print(f"API Key: {BRAPI_KEY[:20]}...")
print()

# ============================================================================
# ENDPOINT 1: QUOTE (Cotações em tempo real)
# ============================================================================
print("\n[1/8] QUOTE — Cotações em tempo real (ações, índices)")
print("-" * 80)

try:
    # Teste: múltiplas ações de uma vez
    response = requests.get(
        f"{BASE_URL}/quote/PETR4,VALE3,ITUB4,B3SA3,^BVSP,GGBR4,MGLU3,ABEV3",
        headers=HEADERS,
        timeout=10
    )

    if response.status_code == 200:
        data = response.json()
        print("✅ Funcionando!")
        print(f"   Endpoint: GET /quote/SYMBOL1,SYMBOL2,...")
        print(f"   Dados retornados por ação:")

        if 'results' in data and data['results']:
            sample = data['results'][0]
            print(f"      - symbol: {sample.get('symbol')}")
            print(f"      - regularMarketPrice: {sample.get('regularMarketPrice')}")
            print(f"      - regularMarketChange: {sample.get('regularMarketChange')}")
            print(f"      - regularMarketChangePercent: {sample.get('regularMarketChangePercent')}")
            print(f"      - marketCap: {sample.get('marketCap')}")
            print(f"      - preMarketPrice: {sample.get('preMarketPrice')}")
            print(f"      - postMarketPrice: {sample.get('postMarketPrice')}")
            print(f"      - volume: {sample.get('volume')}")
            print(f"      - fifty2WeekHigh: {sample.get('fiftyTwoWeekHigh')}")
            print(f"      - fifty2WeekLow: {sample.get('fiftyTwoWeekLow')}")
    else:
        print(f"❌ Erro {response.status_code}")

except Exception as e:
    print(f"❌ Erro: {e}")

# ============================================================================
# ENDPOINT 2: CURRENCY (Moedas e pares de câmbio)
# ============================================================================
print("\n[2/8] CURRENCY — Cotação de moedas (USD-BRL, EUR-BRL, etc)")
print("-" * 80)

try:
    # Teste: múltiplas moedas
    currencies = ["USD-BRL", "EUR-BRL", "GBP-BRL", "JPY-BRL"]

    for curr in currencies:
        response = requests.get(
            f"{BASE_URL}/v2/currency",
            params={"currency": curr},
            headers=HEADERS,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            if 'currency' in data and data['currency']:
                fx = data['currency'][0]
                print(f"✅ {curr}:")
                print(f"   - bidPrice: {fx.get('bidPrice')}")
                print(f"   - askPrice: {fx.get('askPrice')}")
                print(f"   - bidVariation: {fx.get('bidVariation')}")
                print(f"   - percentageChange: {fx.get('percentageChange')}")
        else:
            print(f"❌ {curr}: Erro {response.status_code}")

except Exception as e:
    print(f"❌ Erro: {e}")

# ============================================================================
# ENDPOINT 3: HISTORICAL (Dados históricos)
# ============================================================================
print("\n[3/8] HISTORICAL — Dados históricos (OHLCV)")
print("-" * 80)

try:
    # Teste: últimos 30 dias de PETR4
    response = requests.get(
        f"{BASE_URL}/quote/PETR4",
        params={
            "range": "1mo",  # 1 mês
            "interval": "1d"  # diário
        },
        headers=HEADERS,
        timeout=10
    )

    if response.status_code == 200:
        data = response.json()
        print("✅ Funcionando!")
        print(f"   Endpoint: GET /quote/SYMBOL?range=1mo&interval=1d")
        print(f"   Ranges disponíveis: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, max")
        print(f"   Intervals: 1d, 1wk, 1mo")

        if 'results' in data and data['results']:
            sample = data['results'][0]
            print(f"   Dados por candle OHLCV:")
            print(f"      - open: {sample.get('open')}")
            print(f"      - high: {sample.get('high')}")
            print(f"      - low: {sample.get('low')}")
            print(f"      - close: {sample.get('close')}")
            print(f"      - volume: {sample.get('volume')}")
            print(f"      - timestamp: {sample.get('timestamp')}")
    else:
        print(f"❌ Erro {response.status_code}")

except Exception as e:
    print(f"❌ Erro: {e}")

# ============================================================================
# ENDPOINT 4: STOCKS (Lista de todas as ações)
# ============================================================================
print("\n[4/8] STOCKS — Lista de todas as ações da bolsa")
print("-" * 80)

try:
    response = requests.get(
        f"{BASE_URL}/stocks",
        headers=HEADERS,
        timeout=10
    )

    if response.status_code == 200:
        data = response.json()
        print("✅ Funcionando!")
        print(f"   Endpoint: GET /stocks")
        print(f"   Total de ações: {len(data.get('stocks', []))}")
        if data.get('stocks'):
            print(f"   Exemplo de ação: {data['stocks'][0]}")
    else:
        print(f"❌ Erro {response.status_code}")

except Exception as e:
    print(f"❌ Erro: {e}")

# ============================================================================
# ENDPOINT 5: SEARCH (Busca por ação/empresa)
# ============================================================================
print("\n[5/8] SEARCH — Buscar ação por nome ou código")
print("-" * 80)

try:
    response = requests.get(
        f"{BASE_URL}/search",
        params={"q": "petrobras"},  # Buscar por "petrobras"
        headers=HEADERS,
        timeout=10
    )

    if response.status_code == 200:
        data = response.json()
        print("✅ Funcionando!")
        print(f"   Endpoint: GET /search?q=QUERY")
        print(f"   Resultados para 'petrobras':")
        if 'stocks' in data:
            for stock in data['stocks'][:3]:
                print(f"      - {stock.get('symbol')}: {stock.get('name')}")
    else:
        print(f"❌ Erro {response.status_code}")

except Exception as e:
    print(f"❌ Erro: {e}")

# ============================================================================
# ENDPOINT 6: COMPANY INFO (Informações da empresa)
# ============================================================================
print("\n[6/8] COMPANY INFO — Informações completas da empresa")
print("-" * 80)

try:
    response = requests.get(
        f"{BASE_URL}/quote/PETR4",
        headers=HEADERS,
        timeout=10
    )

    if response.status_code == 200:
        data = response.json()
        if 'results' in data and data['results']:
            company = data['results'][0]
            print("✅ Funcionando!")
            print(f"   Dados da empresa disponíveis:")
            print(f"      - longName: {company.get('longName')}")
            print(f"      - sector: {company.get('sector')}")
            print(f"      - industry: {company.get('industry')}")
            print(f"      - website: {company.get('website')}")
            print(f"      - marketCap: {company.get('marketCap')}")
            print(f"      - priceAvg50: {company.get('priceAvg50')}")
            print(f"      - priceAvg200: {company.get('priceAvg200')}")
            print(f"      - eps: {company.get('eps')}")
            print(f"      - pe: {company.get('pe')}")
            print(f"      - dividendYield: {company.get('dividendYield')}")
    else:
        print(f"❌ Erro {response.status_code}")

except Exception as e:
    print(f"❌ Erro: {e}")

# ============================================================================
# ENDPOINT 7: AVAILABLE ENDPOINTS (Descubra o que há)
# ============================================================================
print("\n[7/8] AVAILABLE ENDPOINTS — Ver todos os endpoints")
print("-" * 80)

try:
    response = requests.get(
        f"{BASE_URL}/",
        headers=HEADERS,
        timeout=10
    )

    if response.status_code == 200:
        print("✅ Endpoints documentados:")
        print("   /quote/{symbol} — Cotação em tempo real")
        print("   /quote/{symbol}?range=1mo&interval=1d — Dados históricos")
        print("   /v2/currency?currency=USD-BRL — Cotação de moedas")
        print("   /stocks — Lista de todas as ações")
        print("   /search?q=query — Buscar ação")
        print("   /available — Símbolos disponíveis")
    else:
        print(f"❌ Erro {response.status_code}")

except Exception as e:
    print(f"❌ Erro: {e}")

# ============================================================================
# ENDPOINT 8: BRENT (Preço do petróleo Brent)
# ============================================================================
print("\n[8/8] COMMODITIES — Petróleo Brent e outras commodities")
print("-" * 80)

try:
    # Tentar buscar via quote normal
    response = requests.get(
        f"{BASE_URL}/quote/BRENT",
        headers=HEADERS,
        timeout=10
    )

    if response.status_code == 200:
        print("✅ Brent disponível!")
        data = response.json()
        if 'results' in data and data['results']:
            brent = data['results'][0]
            print(f"   - Preço: US$ {brent.get('regularMarketPrice')}")
            print(f"   - Variação: {brent.get('regularMarketChange')}")
    else:
        print(f"⚠️ Brent não encontrado no quote, tentando via search...")

except Exception as e:
    print(f"⚠️ Erro: {e}")

# ============================================================================
# RESUMO E RECOMENDAÇÕES
# ============================================================================
print("\n" + "=" * 80)
print("📋 RESUMO — O que usar para o Morning Call")
print("=" * 80)

print("""
PARA CADA BLOCO DO MORNING CALL, USE:

1. TERMÔMETRO (Mercado em geral):
   - GET /quote/^BVSP,PETR4,VALE3,DOLAR
   - Retorna: price, change, change_pct em tempo real
   - Use: regularMarketPrice, regularMarketChangePercent

2. ATIVOS PRINCIPAIS:
   - GET /quote/PETR4,VALE3,ITUB4,B3SA3
   - Máximo 5-6 ações por request
   - Dados: marketCap, volume, pe, dividendYield

3. INDICADORES TÉCNICOS:
   - GET /quote/PETR4?range=1mo&interval=1d
   - Retorna: open, high, low, close, volume (últimos 30 dias)
   - Use para identificar suporte/resistência

4. ANÁLISE COMPARATIVA:
   - GET /quote/SYMBOL?range=1y
   - Veja variação de 52 semanas (fifty2WeekHigh/Low)
   - Compare com preço de hoje

5. MOEDAS:
   - GET /v2/currency?currency=USD-BRL,EUR-BRL
   - Impacto no portfolio de brasileiros

DADOS REAIS PARA O SEU PÚBLICO:
- Sempre valide data/hora (timestamp)
- Use dados atualizados (não cache de 24h)
- Combine QUOTE (hoje) + HISTORICAL (tendência)
- Sempre cite a fonte: "Dados de X horário BRAPI"

""")

print("=" * 80)
print("✅ EXPLORER FINALIZADO")
print("=" * 80)
print("\nPróximo passo: Modificar prospector.py e writer.py para usar TODOS esses dados!")
