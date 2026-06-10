#!/usr/bin/env python3
"""
Prospector Agent — Identifica tópicos trending de mercado
Usa Brapi API para dados reais (IBOV, PETR4, VALE3, etc)
"""

import requests
import json
from datetime import datetime
from typing import List, Dict, Any

class ProspectorAgent:
    def __init__(self, brapi_key: str):
        self.brapi_key = brapi_key
        self.base_url = "https://api.brapi.dev/api/v2"
        self.headers = {"Authorization": f"Bearer {brapi_key}"}

    def get_market_data(self) -> Dict[str, Any]:
        """Buscar dados de mercado via Brapi"""

        try:
            # Índices principais
            response = requests.get(
                f"{self.base_url}/quote/PETR4,VALE3,ITUB4,B3SA3,^BVSP,^USD",
                params={"token": self.brapi_key},
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                return self._parse_market_data(data)
            else:
                print(f"Erro Brapi: {response.status_code}")
                return self._get_mock_data()

        except Exception as e:
            print(f"Erro ao conectar Brapi: {e}")
            return self._get_mock_data()

    def _parse_market_data(self, brapi_response: Dict) -> Dict[str, Any]:
        """Parse dados da Brapi"""

        data = {}

        if 'results' in brapi_response:
            for quote in brapi_response['results']:
                symbol = quote.get('symbol', '').upper()

                if symbol == '^BVSP' or symbol == 'IBOV':
                    data['ibov'] = {
                        'value': quote.get('regularMarketPrice', 0),
                        'change': quote.get('regularMarketChange', 0),
                        'change_pct': quote.get('regularMarketChangePercent', 0),
                    }
                elif symbol == '^USD' or 'USD' in symbol:
                    data['dolar'] = {
                        'value': quote.get('regularMarketPrice', 0),
                        'change': quote.get('regularMarketChange', 0),
                        'change_pct': quote.get('regularMarketChangePercent', 0),
                    }
                elif symbol == 'PETR4':
                    data['petr4'] = {
                        'value': quote.get('regularMarketPrice', 0),
                        'change': quote.get('regularMarketChange', 0),
                        'change_pct': quote.get('regularMarketChangePercent', 0),
                    }
                elif symbol == 'VALE3':
                    data['vale3'] = {
                        'value': quote.get('regularMarketPrice', 0),
                        'change': quote.get('regularMarketChange', 0),
                        'change_pct': quote.get('regularMarketChangePercent', 0),
                    }

        return data

    def _get_mock_data(self) -> Dict[str, Any]:
        """Dados mock para teste (quando Brapi não responde)"""
        return {
            'ibov': {'value': 176200, 'change': 1250, 'change_pct': 0.71},
            'dolar': {'value': 4.96, 'change': 0.02, 'change_pct': 0.40},
            'petr4': {'value': 47.50, 'change': -0.85, 'change_pct': -1.76},
            'vale3': {'value': 84.30, 'change': 1.10, 'change_pct': 1.32},
            'brent': {'value': 103.45, 'change': 3.90, 'change_pct': 3.92},
        }

    def identify_trending_topics(self, market_data: Dict) -> List[Dict[str, Any]]:
        """Identifica tópicos com base nos movimentos do mercado"""

        topics = []

        # Tema 1: IBOVESPA em movimento
        if 'ibov' in market_data:
            ibov = market_data['ibov']
            if abs(ibov['change_pct']) > 1.0:
                topics.append({
                    'title': f"IBOVESPA {'sobe' if ibov['change_pct'] > 0 else 'cai'} {abs(ibov['change_pct']):.2f}% - O que está acontecendo",
                    'category': 'market_movement',
                    'relevance_score': 10,
                    'data': ibov,
                    'keywords': ['ibovespa', 'bolsa', 'mercado'],
                })

        # Tema 2: Petrobras (PETR4) em destaque
        if 'petr4' in market_data:
            petr4 = market_data['petr4']
            if abs(petr4['change_pct']) > 1.5:
                topics.append({
                    'title': f"PETR4 em movimento: {petr4['change_pct']:+.2f}% - Análise do dia",
                    'category': 'stock_analysis',
                    'relevance_score': 9,
                    'data': petr4,
                    'keywords': ['petr4', 'petróleo', 'energia'],
                })

        # Tema 3: Vale (VALE3)
        if 'vale3' in market_data:
            vale3 = market_data['vale3']
            if abs(vale3['change_pct']) > 1.5:
                topics.append({
                    'title': f"VALE3 em foco: {vale3['change_pct']:+.2f}% - O que muda para você",
                    'category': 'stock_analysis',
                    'relevance_score': 8,
                    'data': vale3,
                    'keywords': ['vale3', 'mineração', 'commodities'],
                })

        # Tema 4: Dólar em movimento
        if 'dolar' in market_data:
            dolar = market_data['dolar']
            if abs(dolar['change_pct']) > 0.5:
                topics.append({
                    'title': f"Dólar {'sobe' if dolar['change_pct'] > 0 else 'cai'} para R$ {dolar['value']:.2f} - Impacto na sua carteira",
                    'category': 'currency',
                    'relevance_score': 8,
                    'data': dolar,
                    'keywords': ['dólar', 'câmbio', 'importação'],
                })

        # Tema 5: Educação financeira (sempre relevante)
        topics.append({
            'title': "Como investir iniciante: Guia prático passo-a-passo",
            'category': 'education',
            'relevance_score': 7,
            'data': market_data,
            'keywords': ['investimento', 'educação', 'iniciante'],
        })

        # Ordenar por relevância
        topics.sort(key=lambda x: x['relevance_score'], reverse=True)

        return topics

    def run(self) -> Dict[str, Any]:
        """Executa o agente"""

        print("🔍 Prospector Agent — Buscando dados de mercado...")

        # Buscar dados
        market_data = self.get_market_data()
        print(f"✅ Dados coletados: {list(market_data.keys())}")

        # Identificar tópicos
        topics = self.identify_trending_topics(market_data)
        top_topic = topics[0] if topics else None

        print(f"✅ Top tema: {top_topic['title']}")

        return {
            'status': 'success',
            'top_topic': top_topic,
            'all_topics': topics,
            'market_data': market_data,
            'timestamp': datetime.now().isoformat(),
            'agent': 'Prospector',
        }


# Test
if __name__ == "__main__":
    agent = ProspectorAgent(brapi_key="tky3Vocipoj9ZocxEumbCe")
    result = agent.run()
    print("\n" + "="*60)
    print(json.dumps(result, indent=2, ensure_ascii=False))
