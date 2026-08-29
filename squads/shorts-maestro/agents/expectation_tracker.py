#!/usr/bin/env python3
"""
ExpectationTrackerAgent — O loop de accountability do Morning Call

Conceito da Raquel (11/06/2026):
"uma inteligencia que fala todo dia de mercado financeiro utilizando dados
passados e no dia seguinte lendo o que aconteceu ontem pra ver se o que foi
dito fez sentido ou nao... aconteceu o que se esperava? A expectativa foi atendida?"

Fundamento financeiro: o mercado precifica a expectativa consensual.
O que move preço é a SURPRESA (realizado vs esperado). Este agente mede
exatamente isso, dia após dia, criando um histórico auditável de leituras.

Diferencial de credibilidade: o Morning Call abre dizendo "ontem a gente
falou X, e aconteceu Y". Mostra acertos E erros. Nenhum influencer faz isso.
"""

import os
import json
import glob
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


class ExpectationTrackerAgent:
    def __init__(
        self,
        ledger_dir: str = None,
        claude_api_key: str = None,
        model: str = None
    ):
        """
        Args:
            ledger_dir: Pasta onde o diário de expectativas é salvo (versionado no git!)
            claude_api_key: Chave Anthropic (revisão do dia seguinte)
            model: Modelo Claude
        """
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.ledger_dir = ledger_dir or os.path.join(base_dir, 'data', 'expectations')
        os.makedirs(self.ledger_dir, exist_ok=True)

        self.claude_api_key = claude_api_key or os.getenv('ANTHROPIC_API_KEY', '')
        self.model = model or os.getenv('CLAUDE_MODEL', 'claude-sonnet-4-6')
        self.client = None
        if ANTHROPIC_AVAILABLE and self.claude_api_key:
            self.client = Anthropic(api_key=self.claude_api_key)

        self.reviewer_prompt = """Você é um auditor honesto de previsões de mercado.

Sua função: comparar o que foi dito ONTEM (cenários probabilísticos) com o que
ACONTECEU hoje (dados reais), e produzir uma revisão curta e franca.

REGRAS:
1. Seja 100% honesto. Se a leitura de ontem errou, diga que errou e explique por quê
   (surpresa de dados? evento inesperado? leitura ruim mesmo?)
2. Se acertou, diga qual cenário se materializou, sem arrogância
3. Lembre o conceito: o mercado precifica expectativa, o que move preço é a SURPRESA
4. Linguagem da Raquel: conversacional, "turma", "seu bolso", sem economês
5. ⚖️ CVM: nunca afirme movimento futuro. Linguagem probabilística sempre.
6. 🚫 NUNCA use travessão "—". Frases fluidas com vírgula ou ponto.

FORMATO (máximo 120 palavras):
[CONFERE?]
Ontem a gente falou que [resumo da expectativa]. E o que aconteceu? [realizado].
[Avaliação honesta: bateu, não bateu, ou parcial. Por quê.]
[Lição rápida sobre expectativa vs surpresa, se couber.]"""

    # ─────────────────────────────────────────────────────────────
    # DIÁRIO (salvar expectativas do dia)
    # ─────────────────────────────────────────────────────────────

    def save_expectations(
        self,
        analysis: Dict[str, Any],
        market_snapshot: Dict[str, Any],
        date: str = None
    ) -> str:
        """
        Salva a leitura do dia no diário (data/expectations/YYYY-MM-DD.json).
        Este arquivo É VERSIONADO no git, criando histórico auditável.
        """
        date = date or datetime.now().strftime('%Y-%m-%d')
        path = os.path.join(self.ledger_dir, f'{date}.json')

        entry = {
            'date': date,
            'ticker': analysis.get('ticker'),
            'analysis_text': analysis.get('analysis_text', ''),
            'technical_stats': analysis.get('technical_stats', {}),
            'market_snapshot': market_snapshot,
            'saved_at': datetime.now().isoformat(),
            'reviewed': False
        }

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(entry, f, ensure_ascii=False, indent=2)

        print(f"📔 Expectativas salvas no diário: {path}")
        return path

    def get_latest_entry(self, before_date: str = None) -> Optional[Dict[str, Any]]:
        """Busca a entrada mais recente do diário anterior à data dada (default: hoje)"""
        before_date = before_date or datetime.now().strftime('%Y-%m-%d')

        entries = sorted(glob.glob(os.path.join(self.ledger_dir, '*.json')))
        previous = [e for e in entries if os.path.basename(e).replace('.json', '') < before_date]

        if not previous:
            return None

        with open(previous[-1], 'r', encoding='utf-8') as f:
            return json.load(f)

    # ─────────────────────────────────────────────────────────────
    # REVISÃO (o dia seguinte confere o dia anterior)
    # ─────────────────────────────────────────────────────────────

    def review_yesterday(
        self,
        today_market: Dict[str, Any],
        today_date: str = None
    ) -> Dict[str, Any]:
        """
        Lê a expectativa de ontem, compara com os dados de hoje e produz
        o bloco [CONFERE?] para abrir o Morning Call.

        Returns:
            Dict com review_text (ou status 'no_history' no primeiro dia)
        """
        today_date = today_date or datetime.now().strftime('%Y-%m-%d')

        yesterday = self.get_latest_entry(before_date=today_date)
        if not yesterday:
            print("📔 Primeiro dia: ainda não há expectativa anterior para revisar")
            return {'status': 'no_history'}

        print(f"\n🔍 ExpectationTracker — Revisando leitura de {yesterday['date']}...")

        if not self.client:
            return {'status': 'error', 'message': 'Claude API não configurada'}

        user_prompt = f"""EXPECTATIVA REGISTRADA EM {yesterday['date']}:

Ativo em foco: {yesterday.get('ticker')}
Termômetro daquele dia: {json.dumps(yesterday.get('market_snapshot', {}), ensure_ascii=False)}

Leitura completa do analista naquele dia:
{yesterday.get('analysis_text', '')}

═══════════════════════════════════════

DADOS REAIS DE HOJE ({today_date}):
{json.dumps(today_market, ensure_ascii=False, indent=2)}

═══════════════════════════════════════

Compare e produza o bloco [CONFERE?]. A expectativa foi atendida?
Qual cenário se materializou? Seja honesto sobre acertos e erros."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=400,
                temperature=0.3,
                system=self.reviewer_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )

            review_text = response.content[0].text.strip()
            review_text = review_text.replace(' — ', ', ').replace('— ', ', ').replace(' —', ',').replace('—', ', ')

            # Marcar entrada como revisada
            path = os.path.join(self.ledger_dir, f"{yesterday['date']}.json")
            yesterday['reviewed'] = True
            yesterday['review'] = {
                'reviewed_on': today_date,
                'review_text': review_text,
                'today_market': today_market
            }
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(yesterday, f, ensure_ascii=False, indent=2)

            print(f"   ✅ Revisão concluída (diário atualizado)")

            return {
                'status': 'completed',
                'reviewed_date': yesterday['date'],
                'review_text': review_text,
                'agent': 'ExpectationTracker'
            }

        except Exception as e:
            print(f"❌ Erro na revisão: {e}")
            return {'status': 'error', 'message': str(e)}


# Test
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

    tracker = ExpectationTrackerAgent()
    print(json.dumps(tracker.get_latest_entry() or {'ledger': 'vazio'}, ensure_ascii=False, indent=2)[:500])
