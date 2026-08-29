#!/usr/bin/env python3
"""
🌍 DATA COLLECTOR ÉPICO — Coleta dados de TODAS as fontes globais
Executar na Windows da Raquel (tem internet completa)

COMO USAR:
    python data_collector_epic.py

Coleta:
    ✅ Brapi: PETR4, VALE3, IBOV, USD-BRL, Brent
    ✅ Bolsas globais: S&P500, VIX, FTSE, Nikkei, Hang Seng
    ✅ Commodities: Ouro, Prata, Cobre
    ✅ Crypto: Bitcoin, Ethereum (opcional)
    ✅ Análise: Salva tudo em JSON estruturado para Claude analisar

Output: data_epic_{timestamp}.json — pronto para Git Push
"""

import os
import sys
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))

BRAPI_KEY = os.getenv('BRAPI_API_KEY', '')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, 'data', 'epic_collection')
os.makedirs(OUTPUT_DIR, exist_ok=True)

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_file = os.path.join(OUTPUT_DIR, f'data_epic_{timestamp}.json')

data = {
    'timestamp': datetime.now().isoformat(),
    'data_br': {},
    'bolsas_globais': {},
    'commodities': {},
    'crypto': {},
    'analise_geopolitica': {}
}


def coletar_brapi():
    """Coleta dados brasileiros via Brapi"""
    print("\n🇧🇷 COLETANDO DADOS BRASIL (Brapi)...")
    try:
        # Cotação de ativos
        tickers = ['PETR4', 'VALE3', 'ITUB4', 'B3SA3', '^BVSP']
        headers = {'Authorization': f'Bearer {BRAPI_KEY}'} if BRAPI_KEY else {}

        for ticker in tickers:
            try:
                r = requests.get(
                    f'https://brapi.dev/api/v2/quote/{ticker}',
                    headers=headers,
                    timeout=10
                )
                if r.status_code == 200:
                    result = r.json()
                    if 'results' in result and result['results']:
                        quote = result['results'][0]
                        data['data_br'][ticker] = {
                            'price': quote.get('regularMarketPrice'),
                            'change': quote.get('regularMarketChange'),
                            'change_pct': quote.get('regularMarketChangePercent'),
                            'high_52w': quote.get('fiftyTwoWeekHigh'),
                            'low_52w': quote.get('fiftyTwoWeekLow'),
                            'volume': quote.get('regularMarketVolume'),
                            'market_cap': quote.get('marketCap')
                        }
                        print(f"  ✅ {ticker}: R$ {quote.get('regularMarketPrice')} ({quote.get('regularMarketChangePercent'):+.2f}%)")
            except Exception as e:
                print(f"  ⚠️ {ticker}: Erro ({str(e)[:50]})")

        # USD-BRL
        try:
            r = requests.get(
                'https://brapi.dev/api/v2/currency?currency=USD-BRL',
                headers=headers,
                timeout=10
            )
            if r.status_code == 200:
                result = r.json()
                if 'results' in result and result['results']:
                    usd = result['results'][0]
                    data['data_br']['USD_BRL'] = {
                        'bid': usd.get('bid'),
                        'ask': usd.get('ask'),
                        'price': (usd.get('bid', 0) + usd.get('ask', 0)) / 2
                    }
                    print(f"  ✅ USD-BRL: R$ {data['data_br']['USD_BRL']['price']:.4f}")
        except Exception as e:
            print(f"  ⚠️ USD-BRL: Erro ({str(e)[:50]})")

        # Brent (petróleo)
        try:
            r = requests.get(
                'https://brapi.dev/api/v2/quote/BRENT',
                headers=headers,
                timeout=10
            )
            if r.status_code == 200:
                result = r.json()
                if 'results' in result and result['results']:
                    brent = result['results'][0]
                    data['data_br']['BRENT'] = {
                        'price': brent.get('regularMarketPrice'),
                        'change': brent.get('regularMarketChange'),
                        'change_pct': brent.get('regularMarketChangePercent')
                    }
                    print(f"  ✅ Brent: US$ {brent.get('regularMarketPrice')} ({brent.get('regularMarketChangePercent'):+.2f}%)")
        except Exception as e:
            print(f"  ⚠️ Brent: Erro ({str(e)[:50]})")

    except Exception as e:
        print(f"  ❌ Erro geral Brapi: {e}")


def coletar_bolsas_globais():
    """Coleta índices globais (S&P500, VIX, FTSE, Nikkei, Hang Seng)"""
    print("\n🌎 COLETANDO BOLSAS GLOBAIS...")

    # Tickers globais via Brapi ou Yahoo Finance
    tickers_globais = {
        'SPY': 'S&P 500 (SPY)',
        'VIX': 'VIX (Índice do Medo)',
        'FTSE': 'FTSE 100 (Londres)',
        'N225': 'Nikkei 225 (Tóquio)',
        'HSI': 'Hang Seng (Hong Kong)'
    }

    brapi_key = os.getenv('BRAPI_API_KEY', '')
    headers = {'Authorization': f'Bearer {brapi_key}'} if brapi_key else {}

    for ticker, nome in tickers_globais.items():
        try:
            r = requests.get(
                f'https://brapi.dev/api/v2/quote/{ticker}',
                headers=headers,
                timeout=10
            )
            if r.status_code == 200:
                result = r.json()
                if 'results' in result and result['results']:
                    quote = result['results'][0]
                    data['bolsas_globais'][ticker] = {
                        'nome': nome,
                        'price': quote.get('regularMarketPrice'),
                        'change': quote.get('regularMarketChange'),
                        'change_pct': quote.get('regularMarketChangePercent'),
                        'volume': quote.get('regularMarketVolume')
                    }
                    print(f"  ✅ {nome}: {quote.get('regularMarketPrice')} ({quote.get('regularMarketChangePercent'):+.2f}%)")
        except Exception as e:
            print(f"  ⚠️ {nome} ({ticker}): Erro ({str(e)[:50]})")


def coletar_commodities():
    """Coleta preços de commodities (Ouro, Prata, Cobre)"""
    print("\n⛏️ COLETANDO COMMODITIES...")

    commodities = {
        'GOLD': 'Ouro (por onça)',
        'SILVER': 'Prata (por onça)',
        'COPPER': 'Cobre (por libra)'
    }

    brapi_key = os.getenv('BRAPI_API_KEY', '')
    headers = {'Authorization': f'Bearer {brapi_key}'} if brapi_key else {}

    for ticker, nome in commodities.items():
        try:
            r = requests.get(
                f'https://brapi.dev/api/v2/quote/{ticker}',
                headers=headers,
                timeout=10
            )
            if r.status_code == 200:
                result = r.json()
                if 'results' in result and result['results']:
                    quote = result['results'][0]
                    data['commodities'][ticker] = {
                        'nome': nome,
                        'price': quote.get('regularMarketPrice'),
                        'change_pct': quote.get('regularMarketChangePercent')
                    }
                    print(f"  ✅ {nome}: US$ {quote.get('regularMarketPrice')} ({quote.get('regularMarketChangePercent'):+.2f}%)")
        except Exception as e:
            print(f"  ⚠️ {nome} ({ticker}): Erro ({str(e)[:50]})")


def coletar_crypto():
    """Coleta preços de Bitcoin e Ethereum (opcional)"""
    print("\n₿ COLETANDO CRYPTO (Bitcoin, Ethereum)...")

    try:
        # Bitcoin via CoinGecko (free API, sem auth)
        r = requests.get(
            'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd,brl&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true',
            timeout=10
        )
        if r.status_code == 200:
            prices = r.json()
            if 'bitcoin' in prices:
                data['crypto']['BTC'] = {
                    'price_usd': prices['bitcoin'].get('usd'),
                    'price_brl': prices['bitcoin'].get('brl'),
                    'change_24h': prices['bitcoin'].get('usd_24h_change')
                }
                print(f"  ✅ Bitcoin: US$ {prices['bitcoin'].get('usd'):,.0f} ({prices['bitcoin'].get('usd_24h_change'):+.2f}%)")
            if 'ethereum' in prices:
                data['crypto']['ETH'] = {
                    'price_usd': prices['ethereum'].get('usd'),
                    'price_brl': prices['ethereum'].get('brl'),
                    'change_24h': prices['ethereum'].get('usd_24h_change')
                }
                print(f"  ✅ Ethereum: US$ {prices['ethereum'].get('usd'):,.0f} ({prices['ethereum'].get('usd_24h_change'):+.2f}%)")
    except Exception as e:
        print(f"  ⚠️ Crypto: Erro ({str(e)[:50]})")


def adicionar_contexto_geopolitico():
    """Adiciona contexto geopolítico (Trump, negociações, etc.)"""
    print("\n🌐 CONTEXTO GEOPOLÍTICO...")

    data['analise_geopolitica'] = {
        'trump_negociacoes': {
            'evento': 'Trump anuncia momentos finais de negociações de paz',
            'impacto_esperado': 'Redução de tensões geopolíticas → petróleo pode cair → flight-to-safety reduz → mercados emergentes ganham apetite',
            'horario_noticia': '~03:00 UTC (ontem/hoje madrugada)'
        },
        'oriente_medio': {
            'status': 'Tensões elevadas, petróleo reagindo',
            'proxy': 'BRENT acima de US$ 100'
        },
        'brasil': {
            'risco_politico': 'PETR4 pode sofrer com pressão por intervenção em combustíveis se Brent ficar alto',
            'selic': '14,50% ao ano',
            'inflacao': 'IPCA acima de 5%, teto em 4,50%'
        }
    }

    print(f"  ✅ Trump: Negociações em momento final")
    print(f"  ✅ Impacto esperado: Alívio geopolítico → redução de risco")


def salvar_dados():
    """Salva todos os dados em JSON estruturado"""
    print(f"\n💾 SALVANDO DADOS...")

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"✅ ARQUIVO SALVO: {output_file}")
        print(f"   Tamanho: {os.path.getsize(output_file)} bytes")
        print(f"\n📊 RESUMO COLETADO:")
        print(f"   • Ativos Brasil: {len(data['data_br'])} (PETR4, VALE3, IBOV, USD, Brent)")
        print(f"   • Bolsas Globais: {len(data['bolsas_globais'])} (S&P500, VIX, FTSE, Nikkei, Hang Seng)")
        print(f"   • Commodities: {len(data['commodities'])} (Ouro, Prata, Cobre)")
        print(f"   • Crypto: {len(data['crypto'])} (Bitcoin, Ethereum)")
        print(f"\n🚀 PRÓXIMO PASSO:")
        print(f"   git add {output_file}")
        print(f"   git commit -m 'Coleta de dados épica para Morning Call 12/06/2026'")
        print(f"   git push")

        return True
    except Exception as e:
        print(f"❌ Erro ao salvar: {e}")
        return False


def main():
    print("="*70)
    print("🌍 DATA COLLECTOR ÉPICO — 12/06/2026 — 03:35 MADRUGADA")
    print("="*70)

    coletar_brapi()
    coletar_bolsas_globais()
    coletar_commodities()
    coletar_crypto()
    adicionar_contexto_geopolitico()

    if salvar_dados():
        print("\n" + "="*70)
        print("✅ COLETA COMPLETA! Dados prontos para análise épica.")
        print("="*70)
    else:
        print("\n❌ Erro na coleta. Verifique conexão e credenciais.")
        sys.exit(1)


if __name__ == "__main__":
    main()
