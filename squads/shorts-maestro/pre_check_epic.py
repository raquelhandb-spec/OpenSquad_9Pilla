#!/usr/bin/env python3
"""
✅ PRE-CHECK ÉPICO — Valida tudo antes de rodar data_collector_epic.py
"""

import os
import sys
import requests
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))

print("="*70)
print("✅ PRE-CHECK PARA COLETA ÉPICA")
print("="*70)

# Check 1: Python version
print("\n[1/5] Python version...")
if sys.version_info >= (3, 8):
    print(f"  ✅ Python {sys.version.split()[0]} OK")
else:
    print(f"  ❌ Python 3.8+ necessário (você tem {sys.version})")
    sys.exit(1)

# Check 2: Módulos
print("\n[2/5] Módulos necessários...")
modulos = ['requests', 'dotenv']
for mod in modulos:
    try:
        __import__(mod)
        print(f"  ✅ {mod} OK")
    except ImportError:
        print(f"  ❌ {mod} NÃO INSTALADO")
        print(f"     Rode: python -m pip install {mod}")
        sys.exit(1)

# Check 3: .env
print("\n[3/5] Arquivo .env...")
env_path = os.path.join(BASE_DIR, '.env')
if os.path.exists(env_path):
    print(f"  ✅ .env encontrado ({os.path.getsize(env_path)} bytes)")
    brapi_key = os.getenv('BRAPI_API_KEY', '')
    if brapi_key:
        print(f"  ✅ BRAPI_API_KEY configurada")
    else:
        print(f"  ⚠️ BRAPI_API_KEY vazia (opcional, coleta parcial)")
else:
    print(f"  ⚠️ .env não encontrado (usando variáveis de ambiente)")

# Check 4: Conectividade
print("\n[4/5] Teste de conectividade...")

urls = [
    ("Brapi", "https://brapi.dev/api/v2/quote/PETR4"),
    ("CoinGecko", "https://api.coingecko.com/api/v3/simple/price"),
    ("Google DNS", "https://8.8.8.8/")
]

for nome, url in urls:
    try:
        r = requests.head(url, timeout=5, allow_redirects=False)
        print(f"  ✅ {nome}: Acessível")
    except requests.exceptions.Timeout:
        print(f"  ⚠️ {nome}: Timeout (conexão lenta)")
    except Exception as e:
        print(f"  ⚠️ {nome}: {str(e)[:40]}")

# Check 5: Diretórios
print("\n[5/5] Diretórios necessários...")
data_dir = os.path.join(BASE_DIR, 'data', 'epic_collection')
os.makedirs(data_dir, exist_ok=True)
print(f"  ✅ {data_dir} pronto")

print("\n" + "="*70)
print("✅ PRE-CHECK COMPLETO! Você está pronto para rodar:")
print("   python data_collector_epic.py")
print("="*70)
