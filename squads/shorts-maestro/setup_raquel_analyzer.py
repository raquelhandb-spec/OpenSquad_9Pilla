#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 SETUP RAQUEL ANALYZER — Análise exata do seu setup profissional
Médias: SMA 20 (curto), SMA 45 (médio), SMA 200 (longo)
Timeframes: 5min (intraday) + Diário (tendência)
Cenários dinâmicos com cruzamento de sinais
"""

import os
import sys
import json
import requests
import numpy as np
from datetime import datetime, timedelta
from dotenv import load_dotenv
from typing import Dict, List, Any

# Fix encoding para Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))

BRAPI_KEY = os.getenv('BRAPI_API_KEY', '')
BASE_URL = "https://brapi.dev/api"
HEADERS = {"Authorization": f"Bearer {BRAPI_KEY}"}

class SetupRaquelAnalyzer:
    """Análise usando EXATAMENTE o setup profissional da Raquel"""

    def __init__(self, symbol: str):
        self.symbol = symbol
        self.data_5min = []
        self.data_daily = []
        self.prices_5min = []
        self.prices_daily = []

    def fetch_intraday_data(self) -> bool:
        """Busca dados de 5 minutos (últimas 24h)"""
        print(f"\n📥 Buscando dados 5min para {self.symbol}...")

        try:
            # BRAPI: tentar buscar com interval 5min
            response = requests.get(
                f"{BASE_URL}/quote/{self.symbol}",
                params={
                    "range": "1d",
                    "interval": "5m"
                },
                headers=HEADERS,
                timeout=15
            )

            if response.status_code == 200:
                result = response.json()
                if 'results' in result and result['results']:
                    self.data_5min = sorted(
                        result['results'],
                        key=lambda x: x.get('date', x.get('timestamp', 0))
                    )
                    self.prices_5min = [x.get('close', x.get('regularMarketPrice', 0)) for x in self.data_5min]
                    print(f"✅ {len(self.data_5min)} candles de 5min obtidos")
                    return True
            else:
                print(f"⚠️ BRAPI não suporta 5min (erro {response.status_code})")
                print("   Usando dados diários como fallback")
                return self.fetch_daily_data()

        except Exception as e:
            print(f"⚠️ Erro: {e}")
            return False

    def fetch_daily_data(self) -> bool:
        """Busca dados diários (últimos 2 anos)"""
        print(f"\n📥 Buscando dados diários para {self.symbol}...")

        try:
            response = requests.get(
                f"{BASE_URL}/quote/{self.symbol}",
                params={
                    "range": "2y",
                    "interval": "1d"
                },
                headers=HEADERS,
                timeout=15
            )

            if response.status_code == 200:
                result = response.json()
                if 'results' in result and result['results']:
                    self.data_daily = sorted(
                        result['results'],
                        key=lambda x: x.get('date', x.get('timestamp', 0))
                    )
                    self.prices_daily = [x.get('close', x.get('regularMarketPrice', 0)) for x in self.data_daily]
                    print(f"✅ {len(self.data_daily)} candles diários obtidos")
                    return True
            else:
                print(f"❌ Erro {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Erro: {e}")
            return False

    def calculate_sma(self, prices: List[float], period: int) -> List[float]:
        """Calcula SMA com período específico"""
        if len(prices) < period:
            return []
        return [np.mean(prices[i-period:i]) for i in range(period, len(prices)+1)]

    def analyze_timeframe(self, prices: List[float], timeframe: str) -> Dict[str, Any]:
        """Analisa um timeframe com as 3 médias de Raquel"""

        if not prices or len(prices) < 2:
            return {}

        # Calcular as 3 médias (usar mínimo disponível)
        sma_20_period = min(20, len(prices))
        sma_45_period = min(45, len(prices))
        sma_200_period = min(200, len(prices))

        sma_20 = self.calculate_sma(prices, sma_20_period) if sma_20_period > 0 else []
        sma_45 = self.calculate_sma(prices, sma_45_period) if sma_45_period > 0 else []
        sma_200 = self.calculate_sma(prices, sma_200_period) if sma_200_period > 0 else []

        current_price = prices[-1]
        prev_price = prices[-2] if len(prices) > 1 else current_price

        # Últimos valores das médias
        last_sma_20 = sma_20[-1] if sma_20 else current_price
        last_sma_45 = sma_45[-1] if sma_45 else current_price
        last_sma_200 = sma_200[-1] if sma_200 else current_price

        # Determinar tendência
        trend = self._determine_trend(current_price, last_sma_20, last_sma_45, last_sma_200)

        # Cruzamentos de médias (sinais de mudança de tendência)
        crossovers = self._detect_crossovers(sma_20, sma_45, sma_200)

        return {
            'timeframe': timeframe,
            'current_price': current_price,
            'change': current_price - prev_price,
            'change_pct': ((current_price - prev_price) / prev_price * 100) if prev_price > 0 else 0,
            'sma_20': round(last_sma_20, 2),
            'sma_45': round(last_sma_45, 2),
            'sma_200': round(last_sma_200, 2),
            'trend': trend,
            'position_vs_20': self._position(current_price, last_sma_20),
            'position_vs_45': self._position(current_price, last_sma_45),
            'position_vs_200': self._position(current_price, last_sma_200),
            'crossovers': crossovers,
        }

    def _determine_trend(self, price: float, sma_20: float, sma_45: float, sma_200: float) -> str:
        """Determina tendência: ALTA, BAIXA ou LATERAL"""

        if price > sma_20 > sma_45 > sma_200:
            return "🔺 ALTA FORTE (preço > SMA20 > SMA45 > SMA200)"
        elif price > sma_45 and sma_20 > sma_45:
            return "🔼 ALTA (preço acima de SMA45)"
        elif price > sma_200 and price < sma_45:
            return "➡️ LATERAL ALTA (entre SMA45 e SMA200)"
        elif price < sma_20 < sma_45 < sma_200:
            return "🔻 BAIXA FORTE (preço < SMA20 < SMA45 < SMA200)"
        elif price < sma_45 and sma_20 < sma_45:
            return "🔽 BAIXA (preço abaixo de SMA45)"
        elif price < sma_200 and price > sma_45:
            return "➡️ LATERAL BAIXA (entre SMA45 e SMA200)"
        else:
            return "➡️ LATERAL (sem tendência clara)"

    def _position(self, price: float, sma: float) -> str:
        """Posição do preço em relação à média"""
        if price > sma:
            diff_pct = ((price - sma) / sma * 100)
            return f"ACIMA (+{diff_pct:.2f}%)"
        elif price < sma:
            diff_pct = ((sma - price) / sma * 100)
            return f"ABAIXO (-{diff_pct:.2f}%)"
        else:
            return "NO PREÇO"

    def _detect_crossovers(self, sma_20: List[float], sma_45: List[float], sma_200: List[float]) -> List[str]:
        """Detecta cruzamentos entre médias (sinais de mudança)"""
        crossovers = []

        if len(sma_20) < 2 or len(sma_45) < 2:
            return crossovers

        # Cruzamento SMA20 vs SMA45
        if sma_20[-2] < sma_45[-2] and sma_20[-1] > sma_45[-1]:
            crossovers.append("🔄 SMA20 cruzou acima de SMA45 (SINAL DE ALTA)")
        elif sma_20[-2] > sma_45[-2] and sma_20[-1] < sma_45[-1]:
            crossovers.append("🔄 SMA20 cruzou abaixo de SMA45 (SINAL DE BAIXA)")

        # Cruzamento SMA45 vs SMA200
        if len(sma_200) >= 2:
            if sma_45[-2] < sma_200[-2] and sma_45[-1] > sma_200[-1]:
                crossovers.append("🔄 SMA45 cruzou acima de SMA200 (SINAL DE ALTA FORTE)")
            elif sma_45[-2] > sma_200[-2] and sma_45[-1] < sma_200[-1]:
                crossovers.append("🔄 SMA45 cruzou abaixo de SMA200 (SINAL DE BAIXA FORTE)")

        return crossovers

    def build_scenarios(self, analysis_5min: Dict, analysis_daily: Dict) -> Dict[str, str]:
        """Constrói CENÁRIOS dinâmicos baseado no cruzamento dos timeframes"""

        if not analysis_5min or not analysis_daily:
            return {}

        trend_5min = analysis_5min.get('trend', '')
        trend_daily = analysis_daily.get('trend', '')

        scenarios = {}

        # CENÁRIO 1: Tendências alinhadas (5min + daily = mesma direção)
        if '🔺' in trend_daily or '🔼' in trend_daily:  # Daily em ALTA
            if '🔺' in trend_5min or '🔼' in trend_5min:  # 5min também em ALTA
                scenarios['Cenário Otimista'] = """
                ✅ CENÁRIO OTIMISTA (COMPRA)
                • Daily em ALTA: preço acima de todas as médias
                • 5min também em ALTA: confirmação intraday
                • Sinal: ENTRADA COMPRADA
                • Alvo: Primeira resistência técnica
                • Stop: Abaixo da SMA20
                """
            elif '🔽' in trend_5min or '🔻' in trend_5min:  # 5min em BAIXA
                scenarios['Cenário Divergência'] = """
                ⚠️ CENÁRIO DIVERGÊNCIA (CAUTELA)
                • Daily em ALTA (tendência de médio prazo)
                • Mas 5min em BAIXA (pullback intraday)
                • Sinal: ESPERAR VOLTA DA SMA20
                • Se 5min voltar à alta = ENTRADA COMPRADA FORTE
                • Se 5min continuar baixa = ESPERAR PRÓXIMA OPORTUNIDADE
                """

        elif '🔻' in trend_daily or '🔽' in trend_daily:  # Daily em BAIXA
            if '🔻' in trend_5min or '🔽' in trend_5min:  # 5min também em BAIXA
                scenarios['Cenário Pessimista'] = """
                ❌ CENÁRIO PESSIMISTA (VENDA)
                • Daily em BAIXA: preço abaixo de todas as médias
                • 5min também em BAIXA: confirmação intraday
                • Sinal: ENTRADA VENDIDA
                • Alvo: Primeira suporte técnico
                • Stop: Acima da SMA20
                """
            elif '🔺' in trend_5min or '🔼' in trend_5min:  # 5min em ALTA
                scenarios['Cenário Rally Dentro Baixa'] = """
                ⚠️ CENÁRIO RALLY DENTRO DE QUEDA (TRAP)
                • Daily em BAIXA (tendência de queda)
                • Mas 5min em ALTA (bounce intraday)
                • Sinal: CUIDADO COM COMPRA AQUI
                • Provável: Trampolin / Armadilha de alta
                • Se 5min quebrar SMA45 para baixo = VENDA
                """

        else:  # Daily LATERAL
            scenarios['Cenário Congestão'] = f"""
            ➡️ CENÁRIO LATERAL (CONGESTÃO)
            • Daily em LATERAL: preço oscilando sem tendência clara
            • 5min: {trend_5min}
            • Sinal: OPERAR SUPORTE/RESISTÊNCIA LOCAIS
            • Compra: se tocar suporte da congestão
            • Venda: se tocar resistência da congestão
            • Stop: Fora dos limites laterais
            """

        # Adicionar crossovers como alertas
        crossovers_5min = analysis_5min.get('crossovers', [])
        crossovers_daily = analysis_daily.get('crossovers', [])

        if crossovers_daily:
            scenarios['Alerta'] = f"""
            🚨 ALERTA IMPORTANTE
            {chr(10).join(crossovers_daily)}
            → Possível mudança de tendência de MÉDIO PRAZO
            → Monitor atentamente para confirmação em 5min
            """

        return scenarios

    def print_analysis(self):
        """Imprime análise completa"""

        # Buscar dados
        has_5min = self.fetch_intraday_data()
        has_daily = self.fetch_daily_data()

        if not has_daily:
            print(f"❌ Não foi possível buscar dados")
            return

        print("\n" + "=" * 100)
        print(f"🎯 SETUP RAQUEL — {self.symbol}")
        print("=" * 100)

        # Análise diária
        analysis_daily = self.analyze_timeframe(self.prices_daily, "DIÁRIO (tendência)")

        if not analysis_daily:
            print("❌ Não consegui gerar análise (dados insuficientes)")
            return

        print(f"\n📊 TIMEFRAME DIÁRIO (Tendência de Médio/Longo Prazo)")
        print("-" * 100)
        print(f"Preço: R$ {analysis_daily['current_price']:.2f} ({analysis_daily['change_pct']:+.2f}%)")
        print(f"\nMédias Móveis:")
        print(f"  SMA 20: R$ {analysis_daily['sma_20']:.2f} → {analysis_daily['position_vs_20']}")
        print(f"  SMA 45: R$ {analysis_daily['sma_45']:.2f} → {analysis_daily['position_vs_45']}")
        print(f"  SMA 200: R$ {analysis_daily['sma_200']:.2f} → {analysis_daily['position_vs_200']}")
        print(f"\n🔄 Tendência: {analysis_daily['trend']}")

        if analysis_daily.get('crossovers'):
            print(f"\n⚠️ Cruzamentos detectados:")
            for crossover in analysis_daily['crossovers']:
                print(f"  {crossover}")

        # Análise de 5 minutos (se disponível)
        analysis_5min = {}
        if has_5min and self.prices_5min:
            analysis_5min = self.analyze_timeframe(self.prices_5min, "5 MINUTOS (intraday)")

            print(f"\n\n📊 TIMEFRAME 5 MINUTOS (Operações Intraday)")
            print("-" * 100)
            print(f"Preço: R$ {analysis_5min['current_price']:.2f} ({analysis_5min['change_pct']:+.2f}%)")
            print(f"\nMédias Móveis:")
            print(f"  SMA 20: R$ {analysis_5min['sma_20']:.2f} → {analysis_5min['position_vs_20']}")
            print(f"  SMA 45: R$ {analysis_5min['sma_45']:.2f} → {analysis_5min['position_vs_45']}")
            print(f"  SMA 200: R$ {analysis_5min['sma_200']:.2f} → {analysis_5min['position_vs_200']}")
            print(f"\n🔄 Tendência: {analysis_5min['trend']}")

            if analysis_5min.get('crossovers'):
                print(f"\n⚠️ Cruzamentos detectados:")
                for crossover in analysis_5min['crossovers']:
                    print(f"  {crossover}")

        # Cenários dinâmicos
        if analysis_5min:
            scenarios = self.build_scenarios(analysis_5min, analysis_daily)
        else:
            scenarios = self.build_scenarios(analysis_daily, analysis_daily)

        print(f"\n\n🎯 CENÁRIOS DINÂMICOS (O que fazer agora)")
        print("=" * 100)

        for scenario_name, scenario_desc in scenarios.items():
            print(scenario_desc)
            print()

        print("=" * 100)
        print("✅ ANÁLISE CONCLUÍDA")
        print("=" * 100)

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    symbols = ['PETR4', 'VALE3', 'ITUB4']

    for symbol in symbols:
        analyzer = SetupRaquelAnalyzer(symbol)
        analyzer.print_analysis()
        print("\n\n")
