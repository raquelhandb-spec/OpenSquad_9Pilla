#!/usr/bin/env python3
"""
MarketAnalystAgent — Analista especialista em mercado financeiro
Macro, geopolítica e fluxo, com dados históricos da Brapi.

Criado em 11/06/2026 a pedido da Raquel:
"seria interessante ter um agente analista de dados financeiros,
especialista em leitura de mercado financeiro macro, geopolitica e fluxo"

COMPLIANCE CVM: este agente NUNCA afirma que um ativo vai subir ou cair.
Toda leitura é probabilística: "existe a possibilidade de", "o cenário sugere",
"fica alerta". A decisão é sempre do espectador.
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, Any, List, Optional

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


class MarketAnalystAgent:
    def __init__(self, brapi_key: str = None, claude_api_key: str = None, model: str = None):
        """
        Args:
            brapi_key: Token Brapi (dados históricos)
            claude_api_key: Chave Anthropic (síntese da análise)
            model: Modelo Claude (default: claude-sonnet-4-6)
        """
        self.brapi_key = brapi_key or os.getenv('BRAPI_API_KEY', '')
        self.base_url = "https://brapi.dev/api"
        self.headers = {"Authorization": f"Bearer {self.brapi_key}"}

        self.claude_api_key = claude_api_key or os.getenv('ANTHROPIC_API_KEY', '')
        self.model = model or os.getenv('CLAUDE_MODEL', 'claude-sonnet-4-6')
        self.client = None
        if ANTHROPIC_AVAILABLE and self.claude_api_key:
            self.client = Anthropic(api_key=self.claude_api_key)

        self.analyst_prompt = """Você é um analista sênior de mercado financeiro brasileiro,
especialista em três frentes:
1. MACRO: inflação (IPCA), juros (Selic/Copom, Fed), câmbio, atividade econômica
2. GEOPOLÍTICA: Oriente Médio, Estreito de Ormuz, guerras comerciais, eleições, OPEP
3. FLUXO: capital estrangeiro na B3, rotação setorial, apetite a risco global

⚖️ COMPLIANCE CVM (REGRA ABSOLUTA, INEGOCIÁVEL):
Você NUNCA afirma que um ativo vai subir ou cair. NUNCA recomenda compra ou venda.
Toda leitura usa linguagem probabilística e branda:
- PROIBIDO: "PETR4 vai subir" / "compre" / "venda" / "vai disparar"
- CERTO: "existe a possibilidade de alta no curto prazo, fica alerta"
- CERTO: "o cenário atual sugere pressão vendedora, mas nada é garantido"
- CERTO: "historicamente esse padrão antecedeu correções. Fique de olho"
Sempre apresente os DOIS lados (cenário de alta E de baixa) quando relevante.

🚫 NUNCA use o travessão "—". Escreva frases fluidas com vírgula ou ponto.

FORMATO DA SUA ANÁLISE (seja direto, sem enrolação):
1. LEITURA MACRO: o que os indicadores dizem hoje (2-3 frases)
2. LEITURA GEOPOLÍTICA: riscos e tensões no radar (2-3 frases)
3. LEITURA DE FLUXO E TÉCNICA: o que os dados históricos mostram (tendência,
   volatilidade, posição vs máximas/mínimas) (2-3 frases)
4. POSSIBILIDADES: 2-3 cenários possíveis, SEMPRE com linguagem probabilística
5. ALERTA DO DIA: o que o investidor pessoa física deve observar"""

    # ─────────────────────────────────────────────────────────────
    # DADOS HISTÓRICOS (Brapi)
    # ─────────────────────────────────────────────────────────────

    def get_historical_data(self, ticker: str, range_period: str = "3mo") -> Optional[List[Dict]]:
        """
        Busca histórico de preços via Brapi.
        Ranges válidos: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
        """
        try:
            response = requests.get(
                f"{self.base_url}/quote/{ticker}",
                params={"range": range_period, "interval": "1d"},
                headers=self.headers,
                timeout=10
            )
            if response.status_code == 200:
                results = response.json().get('results', [])
                if results:
                    return results[0].get('historicalDataPrice', [])
            else:
                print(f"⚠️ Brapi histórico {ticker}: status {response.status_code}")
        except Exception as e:
            print(f"⚠️ Erro Brapi histórico: {e}")
        return None

    def compute_technical_stats(self, historical: List[Dict]) -> Dict[str, Any]:
        """Calcula estatísticas técnicas localmente (grátis, sem gastar Claude)"""
        if not historical or len(historical) < 5:
            return {}

        closes = [h.get('close') for h in historical if h.get('close')]
        volumes = [h.get('volume', 0) for h in historical if h.get('volume')]

        if len(closes) < 5:
            return {}

        current = closes[-1]
        period_max = max(closes)
        period_min = min(closes)

        # Médias móveis simples
        ma21 = sum(closes[-21:]) / min(len(closes), 21)
        ma5 = sum(closes[-5:]) / min(len(closes), 5)

        # Volatilidade simples (desvio % médio dia a dia)
        daily_changes = [
            abs(closes[i] - closes[i-1]) / closes[i-1] * 100
            for i in range(1, len(closes))
        ]
        volatility = sum(daily_changes) / len(daily_changes)

        # Tendência de volume (últimos 5 dias vs média do período)
        vol_trend = None
        if volumes and len(volumes) >= 5:
            avg_vol = sum(volumes) / len(volumes)
            recent_vol = sum(volumes[-5:]) / 5
            vol_trend = (recent_vol / avg_vol - 1) * 100 if avg_vol else None

        return {
            'current_price': round(current, 2),
            'period_max': round(period_max, 2),
            'period_min': round(period_min, 2),
            'distance_from_max_pct': round((current / period_max - 1) * 100, 2),
            'distance_from_min_pct': round((current / period_min - 1) * 100, 2),
            'ma5': round(ma5, 2),
            'ma21': round(ma21, 2),
            'above_ma21': current > ma21,
            'avg_daily_volatility_pct': round(volatility, 2),
            'volume_trend_pct': round(vol_trend, 1) if vol_trend is not None else None,
            'period_change_pct': round((closes[-1] / closes[0] - 1) * 100, 2),
            'data_points': len(closes)
        }

    # ─────────────────────────────────────────────────────────────
    # ANÁLISE (Claude)
    # ─────────────────────────────────────────────────────────────

    def analyze(
        self,
        ticker: str,
        market_data: Dict[str, Any],
        news_context: str = "",
        range_period: str = "3mo"
    ) -> Dict[str, Any]:
        """
        Gera leitura completa de mercado: macro + geopolítica + fluxo.

        Args:
            ticker: Ativo em foco (ex: PETR4)
            market_data: Termômetro atual do Prospector (ibov, dolar, petr4, brent...)
            news_context: Contexto de notícias do dia (opcional)
            range_period: Janela de histórico Brapi (default 3 meses)

        Returns:
            Dict com analysis_text (leitura completa) + technical_stats
        """

        print(f"\n🧠 MarketAnalyst — Analisando {ticker} (macro + geopolítica + fluxo)...")

        # 1. Dados históricos (grátis, local)
        historical = self.get_historical_data(ticker, range_period)
        stats = self.compute_technical_stats(historical) if historical else {}

        if stats:
            print(f"   ✅ Histórico Brapi: {stats['data_points']} pregões analisados")
        else:
            print(f"   ⚠️ Histórico Brapi indisponível (análise seguirá com dados atuais)")

        # 2. Montar contexto para Claude
        thermometer = json.dumps(market_data, ensure_ascii=False, indent=2) if market_data else "indisponível"
        stats_block = json.dumps(stats, ensure_ascii=False, indent=2) if stats else "indisponível (rede ou plano Brapi)"

        user_prompt = f"""Analise o cenário de hoje ({datetime.now().strftime('%d/%m/%Y')}) para o investidor pessoa física brasileiro.

ATIVO EM FOCO: {ticker}

TERMÔMETRO ATUAL DO MERCADO:
{thermometer}

ESTATÍSTICAS TÉCNICAS ({range_period} de histórico Brapi):
{stats_block}

CONTEXTO DE NOTÍCIAS DO DIA:
{news_context or 'Sem contexto adicional. Use o cenário macro Brasil 2026: IPCA acima do teto, Selic em ciclo de corte lento, tensão Oriente Médio recorrente.'}

Produza sua análise no formato definido (Macro, Geopolítica, Fluxo/Técnica, Possibilidades, Alerta do Dia).
Lembre: linguagem probabilística SEMPRE. Nada de "vai subir". Máximo 350 palavras."""

        if not self.client:
            return {
                'status': 'error',
                'message': 'Claude API não configurada para o Analyst',
                'technical_stats': stats
            }

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=800,
                temperature=0.4,  # análise pede consistência, menos criatividade
                system=self.analyst_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )

            analysis_text = response.content[0].text.strip()
            # Trava anti-travessão (regra Raquel)
            analysis_text = analysis_text.replace(' — ', ', ').replace('— ', ', ').replace(' —', ',').replace('—', ', ')

            print(f"   ✅ Análise gerada ({len(analysis_text.split())} palavras)")

            return {
                'status': 'completed',
                'ticker': ticker,
                'analysis_text': analysis_text,
                'technical_stats': stats,
                'range_analyzed': range_period,
                'created_at': datetime.now().isoformat(),
                'agent': 'MarketAnalyst',
                'compliance': 'Linguagem probabilística CVM aplicada'
            }

        except Exception as e:
            print(f"❌ Erro na análise: {e}")
            return {
                'status': 'error',
                'message': str(e),
                'technical_stats': stats
            }


# Test
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

    agent = MarketAnalystAgent()
    result = agent.analyze(
        ticker='PETR4',
        market_data={
            'ibov': {'value': 168668, 'change_pct': -0.21},
            'dolar': {'value': 5.18, 'change_pct': 0.50},
            'petr4': {'value': 41.08, 'change_pct': 0.43},
            'brent': {'value': 93.50, 'change_pct': 0.43},
        },
        news_context='Tensão Israel-Irã eleva dólar ao maior nível em 2 meses. Estreito de Ormuz no radar.'
    )
    print("\n" + "="*60)
    if result['status'] == 'completed':
        print(result['analysis_text'])
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))
