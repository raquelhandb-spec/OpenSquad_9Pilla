#!/usr/bin/env python3
"""
📊 TECHNICAL ANALYZER — Análise técnica com 5+ anos de dados
Calcula indicadores, padrões, suporte/resistência, ciclos
SÓ DADOS. SÓ FATOS. SEM OPINIÃO.
"""

import os
import json
import requests
import numpy as np
from datetime import datetime, timedelta
from dotenv import load_dotenv
from typing import Dict, List, Any

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))

BRAPI_KEY = os.getenv('BRAPI_API_KEY', '')
BASE_URL = "https://brapi.dev/api"
HEADERS = {"Authorization": f"Bearer {BRAPI_KEY}"}

class TechnicalAnalyzer:
    """Análise técnica profissional com indicadores quantitativos"""

    def __init__(self, symbol: str, years: int = 5):
        self.symbol = symbol
        self.years = years
        self.data = []
        self.prices = []
        self.dates = []

    def fetch_historical_data(self) -> bool:
        """Busca dados históricos de 5+ anos"""

        print(f"\n📥 Buscando {self.years} anos de dados para {self.symbol}...")

        try:
            # BRAPI suporta: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, max
            range_map = {
                1: "1y",
                2: "2y",
                3: "2y",
                4: "5y",
                5: "5y",
                10: "10y"
            }
            range_param = range_map.get(self.years, "5y")

            response = requests.get(
                f"{BASE_URL}/quote/{self.symbol}",
                params={
                    "range": range_param,
                    "interval": "1mo"  # Mensal para ter mais pontos
                },
                headers=HEADERS,
                timeout=15
            )

            if response.status_code == 200:
                result = response.json()
                if 'results' in result and result['results']:
                    self.data = sorted(
                        result['results'],
                        key=lambda x: x.get('timestamp', 0)
                    )
                    self.prices = [x.get('close', x.get('regularMarketPrice', 0)) for x in self.data]
                    self.dates = [datetime.fromtimestamp(x.get('timestamp', 0)) if x.get('timestamp') else datetime.now() for x in self.data]

                    print(f"✅ {len(self.data)} candles obtidos")
                    print(f"   Período: {self.dates[0].date()} a {self.dates[-1].date()}")
                    return True
            else:
                print(f"❌ Erro {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Erro: {e}")
            return False

    def calculate_sma(self, period: int) -> List[float]:
        """Média Móvel Simples (Simple Moving Average)"""
        if len(self.prices) < period:
            return []
        return [np.mean(self.prices[i-period:i]) for i in range(period, len(self.prices)+1)]

    def calculate_rsi(self, period: int = 14) -> float:
        """Índice de Força Relativa (RSI) — últimos 14 dias"""
        if len(self.prices) < period + 1:
            return 0

        prices = self.prices[-period-1:]
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)

        avg_gain = np.mean(gains)
        avg_loss = np.mean(losses)

        if avg_loss == 0:
            return 100 if avg_gain > 0 else 0

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def calculate_macd(self) -> Dict[str, float]:
        """MACD (Moving Average Convergence Divergence)"""
        if len(self.prices) < 26:
            return {'macd': 0, 'signal': 0, 'histogram': 0}

        ema_12 = self._calculate_ema(self.prices, 12)
        ema_26 = self._calculate_ema(self.prices, 26)

        macd_line = ema_12[-1] - ema_26[-1]
        signal_line = np.mean([ema_12[-9:]] if len(ema_12) >= 9 else [macd_line])

        return {
            'macd': macd_line,
            'signal': signal_line,
            'histogram': macd_line - signal_line
        }

    def _calculate_ema(self, data: List[float], period: int) -> List[float]:
        """Exponential Moving Average"""
        if len(data) < period:
            return data
        ema = [np.mean(data[:period])]
        multiplier = 2 / (period + 1)
        for price in data[period:]:
            ema.append((price - ema[-1]) * multiplier + ema[-1])
        return ema

    def find_support_resistance(self) -> Dict[str, Any]:
        """Identifica suporte e resistência dos últimos 2 anos"""
        if len(self.prices) < 24:  # 24 meses
            return {}

        recent = self.prices[-24:]  # Últimos 2 anos
        highs = []
        lows = []

        # Encontrar picos e vales locais
        for i in range(1, len(recent) - 1):
            if recent[i-1] < recent[i] > recent[i+1]:
                highs.append(recent[i])
            elif recent[i-1] > recent[i] < recent[i+1]:
                lows.append(recent[i])

        return {
            'resistances': sorted(set(highs), reverse=True)[:3] if highs else [],
            'supports': sorted(set(lows))[:3] if lows else [],
            'recent_high': max(recent),
            'recent_low': min(recent),
            'range': max(recent) - min(recent)
        }

    def identify_trend(self) -> str:
        """Identifica tendência: alta, baixa ou lateral"""
        if len(self.prices) < 3:
            return "indeterminado"

        sma_short = np.mean(self.prices[-5:])  # Últimos 5
        sma_long = np.mean(self.prices[-20:])  # Últimos 20

        if sma_short > sma_long * 1.05:
            return "ALTA"
        elif sma_short < sma_long * 0.95:
            return "BAIXA"
        else:
            return "LATERAL"

    def calculate_volatility(self) -> float:
        """Volatilidade nos últimos 3 meses"""
        if len(self.prices) < 3:
            return 0
        recent = self.prices[-3:]
        returns = np.diff(recent) / recent[:-1]
        volatility = np.std(returns) * 100
        return volatility

    def generate_report(self) -> Dict[str, Any]:
        """Gera relatório completo de análise técnica"""

        if not self.data:
            return {}

        current_price = self.prices[-1]
        previous_price = self.prices[-2] if len(self.prices) > 1 else current_price

        report = {
            'symbol': self.symbol,
            'timestamp': datetime.now().isoformat(),
            'data_period': f"{self.dates[0].date()} a {self.dates[-1].date()}",

            # Preço atual
            'price': {
                'current': current_price,
                'previous': previous_price,
                'change': current_price - previous_price,
                'change_pct': ((current_price - previous_price) / previous_price * 100) if previous_price > 0 else 0,
            },

            # Histórico
            'history': {
                'all_time_high': max(self.prices),
                'all_time_low': min(self.prices),
                'year_high': max(self.prices[-12:]) if len(self.prices) >= 12 else max(self.prices),
                'year_low': min(self.prices[-12:]) if len(self.prices) >= 12 else min(self.prices),
            },

            # Indicadores técnicos
            'indicators': {
                'rsi_14': round(self.calculate_rsi(14), 2),
                'sma_50': round(np.mean(self.prices[-50:]) if len(self.prices) >= 50 else np.mean(self.prices), 2),
                'sma_200': round(np.mean(self.prices[-200:]) if len(self.prices) >= 200 else np.mean(self.prices), 2),
                'macd': self.calculate_macd(),
                'volatility_3m': round(self.calculate_volatility(), 2),
            },

            # Suporte e resistência
            'support_resistance': self.find_support_resistance(),

            # Tendência
            'trend': self.identify_trend(),

            # Interpretação
            'interpretation': self._interpret_signals(current_price)
        }

        return report

    def _interpret_signals(self, current_price: float) -> Dict[str, str]:
        """Interpreta os sinais técnicos em português"""

        rsi = self.calculate_rsi(14)
        trend = self.identify_trend()
        sr = self.find_support_resistance()

        interpretation = {
            'rsi_signal': self._rsi_interpretation(rsi),
            'trend_signal': f"Tendência {trend}",
            'support': f"Suporte próximo em {sr['supports'][0]:.2f}" if sr.get('supports') else "Sem suporte identificado",
            'resistance': f"Resistência próxima em {sr['resistances'][0]:.2f}" if sr.get('resistances') else "Sem resistência identificada",
        }

        return interpretation

    def _rsi_interpretation(self, rsi: float) -> str:
        """Interpreta RSI"""
        if rsi > 70:
            return "RSI > 70: Sobrecomprado (possível reversão para baixo)"
        elif rsi < 30:
            return "RSI < 30: Sobrevendido (possível reversão para cima)"
        elif 40 <= rsi <= 60:
            return "RSI 40-60: Zona neutra (sem sinal claro)"
        else:
            return f"RSI {rsi:.1f}: Zona intermediária"

    def print_report(self):
        """Imprime o relatório formatado"""

        report = self.generate_report()

        if not report:
            print(f"❌ Não foi possível gerar relatório")
            return

        print("\n" + "=" * 80)
        print(f"📊 ANÁLISE TÉCNICA: {self.symbol}")
        print("=" * 80)

        print(f"\n💰 PREÇO")
        print(f"   Atual: R$ {report['price']['current']:.2f}")
        print(f"   Variação: {report['price']['change_pct']:+.2f}%")

        print(f"\n📈 HISTÓRICO ({report['data_period']})")
        print(f"   Máxima: R$ {report['history']['all_time_high']:.2f}")
        print(f"   Mínima: R$ {report['history']['all_time_low']:.2f}")
        print(f"   Amplitude: R$ {report['history']['all_time_high'] - report['history']['all_time_low']:.2f}")

        print(f"\n📊 INDICADORES TÉCNICOS")
        ind = report['indicators']
        print(f"   RSI (14 dias): {ind['rsi_14']} → {report['interpretation']['rsi_signal']}")
        print(f"   SMA 50: R$ {ind['sma_50']:.2f}")
        print(f"   SMA 200: R$ {ind['sma_200']:.2f}")
        print(f"   MACD: {ind['macd']['macd']:.4f} | Signal: {ind['macd']['signal']:.4f} | Histogram: {ind['macd']['histogram']:.4f}")
        print(f"   Volatilidade (3m): {ind['volatility_3m']:.2f}%")

        print(f"\n🎯 SUPORTE E RESISTÊNCIA")
        sr = report['support_resistance']
        if sr.get('resistances'):
            for i, r in enumerate(sr['resistances'][:2], 1):
                print(f"   Resistência {i}: R$ {r:.2f}")
        if sr.get('supports'):
            for i, s in enumerate(sr['supports'][:2], 1):
                print(f"   Suporte {i}: R$ {s:.2f}")

        print(f"\n🔄 TENDÊNCIA: {report['trend']}")

        print(f"\n💡 INSIGHTS TÉCNICOS")
        for key, value in report['interpretation'].items():
            print(f"   • {value}")

        print("\n" + "=" * 80)

        return report

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("📊 TECHNICAL ANALYZER — Análise com 5+ anos de dados")
    print("=" * 80)

    # Analisar principais ativos
    symbols = ['PETR4', 'VALE3', 'ITUB4']

    for symbol in symbols:
        analyzer = TechnicalAnalyzer(symbol, years=5)
        if analyzer.fetch_historical_data():
            analyzer.print_report()
        else:
            print(f"❌ Não consegui analisar {symbol}")

    print("\n✅ ANÁLISE CONCLUÍDA")
    print("\nPróximos passos:")
    print("1. Use estes dados técnicos no Morning Call")
    print("2. Cite suporte, resistência, RSI, tendência")
    print("3. Sem opinião — apenas dados quantitativos")
    print("4. Exemplo: 'PETR4 acima da SMA 200, RSI em zona neutra, próxima resistência em R$ 42,50'")
