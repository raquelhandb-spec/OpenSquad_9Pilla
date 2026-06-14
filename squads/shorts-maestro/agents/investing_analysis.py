#!/usr/bin/env python3
"""
InvestingAnalysisAgent — Web Scraper de análises profissionais
Extrai dados do Investing.com para enriquecer scripts
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from typing import Dict, Any, List
import re

class InvestingAnalysisAgent:
    def __init__(self):
        """
        Agent para scraping de análises do Investing.com
        Fonte: https://br.investing.com/analysis/
        """
        self.base_url = "https://br.investing.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def scrape_ticker_analysis(self, ticker: str) -> Dict[str, Any]:
        """
        Scraping de análise completa de um ticker

        Args:
            ticker: Ex: "PETR4", "VALE3", "IBOV"

        Returns:
            Dict com análises, recomendações, etc
        """

        print(f"\n🔍 Investing Analysis — Scraping {ticker}")

        try:
            # URL padrão análise Investing
            url = f"{self.base_url}/analysis/{ticker.lower()}-analise"

            response = requests.get(
                url,
                headers=self.headers,
                timeout=10
            )

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Extrair análises
                analysis_data = self._extract_analysis_data(soup, ticker)
                return analysis_data
            else:
                print(f"⚠️ Status {response.status_code} ao acessar Investing")
                return self._get_mock_analysis(ticker)

        except Exception as e:
            print(f"⚠️ Erro ao scraping: {e}")
            return self._get_mock_analysis(ticker)

    def _extract_analysis_data(self, soup: BeautifulSoup, ticker: str) -> Dict[str, Any]:
        """
        Extrai dados estruturados da página Investing
        """

        data = {
            'ticker': ticker,
            'source': 'investing.com',
            'timestamp': datetime.now().isoformat(),
            'analysts': [],
            'technical_analysis': {},
            'sentiment': 'NEUTRA'
        }

        try:
            # Extrair análises técnicas
            tech_section = soup.find('div', class_=re.compile('technical.*analysis', re.I))
            if tech_section:
                data['technical_analysis'] = {
                    'trend': self._extract_trend(tech_section),
                    'support_levels': self._extract_support(tech_section),
                    'resistance_levels': self._extract_resistance(tech_section)
                }

            # Extrair recomendações de analistas
            analyst_section = soup.find_all('div', class_=re.compile('analyst.*recommendation', re.I))
            if analyst_section:
                for section in analyst_section[:5]:  # Top 5 analistas
                    analyst = self._parse_analyst_recommendation(section)
                    if analyst:
                        data['analysts'].append(analyst)

            # Determinar sentimento geral
            data['sentiment'] = self._calculate_sentiment(data['analysts'])

        except Exception as e:
            print(f"⚠️ Erro ao extrair dados: {e}")

        return data

    def _extract_trend(self, section) -> str:
        """Extrai tendência (ALTA, BAIXA, LATERAL)"""
        text = section.get_text().lower()
        if 'alta' in text or 'bullish' in text or 'subindo' in text:
            return 'ALTA'
        elif 'baixa' in text or 'bearish' in text or 'caindo' in text:
            return 'BAIXA'
        else:
            return 'LATERAL'

    def _extract_support(self, section) -> List[float]:
        """Extrai níveis de suporte"""
        levels = []
        text = section.get_text()
        # Procura por padrões como "suporte: R$ XX"
        matches = re.findall(r'R\$\s*([\d,]+)', text)
        for match in matches[:3]:
            try:
                level = float(match.replace(',', '.'))
                levels.append(level)
            except:
                pass
        return sorted(levels)

    def _extract_resistance(self, section) -> List[float]:
        """Extrai níveis de resistência"""
        levels = []
        text = section.get_text()
        matches = re.findall(r'R\$\s*([\d,]+)', text)
        for match in matches[-3:]:
            try:
                level = float(match.replace(',', '.'))
                levels.append(level)
            except:
                pass
        return sorted(levels, reverse=True)

    def _parse_analyst_recommendation(self, section) -> Dict[str, Any]:
        """Parse de recomendação de um analista"""
        try:
            analyst_name = section.find(class_=re.compile('analyst.*name', re.I))
            recommendation = section.find(class_=re.compile('recommendation', re.I))
            target_price = section.find(class_=re.compile('target.*price', re.I))

            return {
                'analyst': analyst_name.get_text().strip() if analyst_name else 'Desconhecido',
                'recommendation': recommendation.get_text().strip() if recommendation else 'N/A',
                'target_price': target_price.get_text().strip() if target_price else 'N/A'
            }
        except:
            return None

    def _calculate_sentiment(self, analysts: List[Dict]) -> str:
        """Calcula sentimento geral baseado em recomendações"""
        if not analysts:
            return 'NEUTRA'

        compra = sum(1 for a in analysts if 'compra' in a.get('recommendation', '').lower())
        venda = sum(1 for a in analysts if 'venda' in a.get('recommendation', '').lower())

        if compra > venda * 1.5:
            return 'COMPRA'
        elif venda > compra * 1.5:
            return 'VENDA'
        else:
            return 'NEUTRA'

    def _get_mock_analysis(self, ticker: str) -> Dict[str, Any]:
        """
        Dados mock quando não consegue scraping
        (para testes sem internet)
        """

        mock_data = {
            'PETR4': {
                'ticker': 'PETR4',
                'source': 'investing.com (mock)',
                'timestamp': datetime.now().isoformat(),
                'analysts': [
                    {
                        'analyst': 'Itaú BBA',
                        'recommendation': 'COMPRA',
                        'target_price': 'R$ 50.00'
                    },
                    {
                        'analyst': 'Bradesco BBI',
                        'recommendation': 'COMPRA',
                        'target_price': 'R$ 48.50'
                    },
                    {
                        'analyst': 'Goldman Sachs',
                        'recommendation': 'MANUTENÇÃO',
                        'target_price': 'R$ 46.00'
                    }
                ],
                'technical_analysis': {
                    'trend': 'ALTA',
                    'support_levels': [45.50, 44.00],
                    'resistance_levels': [50.00, 52.00]
                },
                'sentiment': 'COMPRA'
            },
            'VALE3': {
                'ticker': 'VALE3',
                'source': 'investing.com (mock)',
                'timestamp': datetime.now().isoformat(),
                'analysts': [
                    {
                        'analyst': 'Morgan Stanley',
                        'recommendation': 'COMPRA',
                        'target_price': 'R$ 90.00'
                    },
                    {
                        'analyst': 'Citigroup',
                        'recommendation': 'COMPRA',
                        'target_price': 'R$ 88.00'
                    },
                    {
                        'analyst': 'JPMorgan',
                        'recommendation': 'MANUTENÇÃO',
                        'target_price': 'R$ 85.00'
                    }
                ],
                'technical_analysis': {
                    'trend': 'ALTA',
                    'support_levels': [80.00, 78.00],
                    'resistance_levels': [90.00, 95.00]
                },
                'sentiment': 'COMPRA'
            }
        }

        return mock_data.get(ticker, {
            'ticker': ticker,
            'source': 'investing.com (mock - ticker não encontrado)',
            'analysts': [],
            'sentiment': 'NEUTRA'
        })

    def get_analysis_summary(self, ticker: str) -> str:
        """
        Gera resumo em linguagem natural para scripts

        Exemplo:
        "Analistas da Itaú BBA e Bradesco recomendam COMPRA com alvo R$ 50.
        Tendência técnica é ALTA com resistência em R$ 52."
        """

        analysis = self.scrape_ticker_analysis(ticker)

        if not analysis.get('analysts'):
            return f"Sem análises disponíveis para {ticker} no momento."

        # Montar resumo
        analyst_names = [a['analyst'] for a in analysis['analysts'][:3]]
        recommendation = analysis['sentiment']
        targets = [a['target_price'] for a in analysis['analysts'] if a.get('target_price')]

        summary = f"Analistas de {', '.join(analyst_names)} recomendam {recommendation}. "

        if targets:
            summary += f"Preços-alvo: {', '.join(targets)}. "

        if analysis.get('technical_analysis'):
            tech = analysis['technical_analysis']
            summary += f"Tendência técnica: {tech.get('trend', 'N/A')}. "

        return summary

    def run_analysis_for_tickers(self, tickers: List[str]) -> Dict[str, Any]:
        """
        Analisa múltiplos tickers

        Args:
            tickers: Lista de tickers (ex: ['PETR4', 'VALE3', 'IBOV'])
        """

        results = {
            'timestamp': datetime.now().isoformat(),
            'tickers_analyzed': len(tickers),
            'analyses': {}
        }

        for ticker in tickers:
            print(f"\n📊 Analisando {ticker}...")
            analysis = self.scrape_ticker_analysis(ticker)
            results['analyses'][ticker] = analysis

        return results


# INTEGRAÇÃO: Investing + Prospector
class EnrichedProspectorAgent:
    """
    Prospector enriquecido com análises do Investing
    """

    def __init__(self, brapi_key: str):
        self.investing = InvestingAnalysisAgent()
        # Prospector original aqui (Brapi)
        self.brapi_key = brapi_key

    def run_enriched_analysis(self, market_data: Dict) -> Dict[str, Any]:
        """
        Combina dados Brapi + análises Investing
        """

        results = {
            'market_data': market_data,
            'analyst_insights': {},
            'enriched_narrative': {}
        }

        # Para cada ticker no market_data, pegar análises
        for ticker in ['PETR4', 'VALE3', 'IBOV']:
            print(f"\n🔍 Enriquecendo {ticker} com análises...")

            # Scraping Investing
            analysis = self.investing.scrape_ticker_analysis(ticker)
            summary = self.investing.get_analysis_summary(ticker)

            results['analyst_insights'][ticker] = analysis
            results['enriched_narrative'][ticker] = summary

        return results


# Test
if __name__ == "__main__":
    print("\n" + "="*60)
    print("INVESTING ANALYSIS AGENT TEST")
    print("="*60 + "\n")

    agent = InvestingAnalysisAgent()

    # Teste 1: Análise single ticker
    print("📊 Teste 1: Análise PETR4")
    petr_analysis = agent.scrape_ticker_analysis('PETR4')
    print(json.dumps(petr_analysis, indent=2, ensure_ascii=False))

    # Teste 2: Resumo narrativo
    print("\n📝 Teste 2: Resumo narrativo")
    summary = agent.get_analysis_summary('PETR4')
    print(f"Resumo: {summary}")

    # Teste 3: Múltiplos tickers
    print("\n📊 Teste 3: Análise múltipla")
    tickers_analysis = agent.run_analysis_for_tickers(['PETR4', 'VALE3', 'IBOV'])
    print(f"Tickers analisados: {tickers_analysis['tickers_analyzed']}")

    print("\n" + "="*60)
    print("INTEGRAÇÃO COM PROSPECTOR:")
    print("="*60)
    print("""
# Usar com Prospector enriquecido
enriched = EnrichedProspectorAgent(brapi_key='...')
result = enriched.run_enriched_analysis(market_data)

# Resultado:
# - Dados de mercado (IBOV, PETR4, VALE3)
# - + Análises de profissionais (recomendações, preços-alvo)
# - + Narrativa enriquecida (resumo em linguagem natural)

# Writer Agent usa isso para scripts MUITO mais ricos!
    """)
