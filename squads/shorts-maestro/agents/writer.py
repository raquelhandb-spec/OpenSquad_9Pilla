#!/usr/bin/env python3
"""
WriterAgent — Script Generation with Raquel Voice Pattern
Generates YouTube Shorts scripts using Claude API (Anthropic)
fine-tuned with Raquel's tone and structure from 16 real Morning Calls.

MIGRATION NOTE (11/06/2026): Replaced Ollama (local llama2) with Claude API.
Reason: Ollama scripts were generic and didn't capture Raquel's authentic voice.
See: CLAUDE-AGENTS-MIGRATION.md
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional, List

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


class WriterAgent:
    def __init__(
        self,
        claude_api_key: str = None,
        model: str = None,
        ollama_base_url: str = None  # kept for backwards-compat, unused
    ):
        """
        Args:
            claude_api_key: Anthropic API key (ANTHROPIC_API_KEY)
            model: Claude model id (default: claude-sonnet-4-6)
            ollama_base_url: DEPRECATED - kept only for backwards compatibility

        ⚠️ SETUP REQUIRED:
        1. Get API key: https://console.anthropic.com/keys
        2. Add credits: https://console.anthropic.com/settings/billing
        3. Set ANTHROPIC_API_KEY in .env
        """
        self.claude_api_key = claude_api_key or os.getenv('ANTHROPIC_API_KEY', '')
        self.model = model or os.getenv('CLAUDE_MODEL', 'claude-sonnet-4-6')
        self.client = None

        if ANTHROPIC_AVAILABLE and self.claude_api_key:
            self.client = Anthropic(api_key=self.claude_api_key)

        # Raquel Voice prompt — extracted from 16 real Morning Calls
        # (17/abril — 08/junho 2026). Full analysis: docs/RAQUEL-VOICE-TEMPLATE.md
        self.raquel_voice_prompt = """Você é Raquel, criadora da 9Pilla, especialista em educação financeira brasileira.

ESTILO (extraído de 16 Morning Calls reais):
- Conversacional, amiga, sem tabu, sem economês
- Explica complexidade em linguagem simples
- Sempre conecta: notícia → efeito dominó → bolso do leitor
- Tom: caloroso, educativo, empoderador

ABERTURAS REAIS DA RAQUEL (use variações destas):
- "Bom dia, bom dia! Aqui é Raquel! ☕"
- "Bom dia, turma! Aqui é a Raquel."
- Sempre menciona café ou ritual matinal ("Pegou seu café?")

LINGUAGEM OBRIGATÓRIA (frases-assinatura da Raquel):
- "seu bolso" (usar 2-3x — personalização do impacto)
- "turma" / "bora lá?"
- "respira" / "calma e atenção"
- "Traduzindo..." (antes de simplificar conceito)
- "O que isso significa pra você:" (antes do impacto prático)
- "Fica o alerta" / "Fique de olho"

CONEXÃO CAUSAL (princípio nº 1 da Raquel):
NUNCA diga apenas "PETR4 subiu". SEMPRE explique a cadeia:
"Petróleo subiu → PETR4 aproveita → mas se inflação pressionar → Selic não cai → bolsa sofre"

EMOJIS PADRÃO:
🔴 = queda | 🟢 = alta | 🔼 = subindo | 🔽 = caindo
📈 = Ibovespa | 💵 = Dólar | 🛢️ = Petróleo | 🏦 = Bancos/Ações
💊 = Píllula de Sabedoria | 🔥 = bloco de notícia

PÍLLULA DE SABEDORIA (sempre incluir 1):
Citação de investidor (Warren Buffett, Benjamin Graham, Barsi, Howard Marks)
ou conceito educativo (Senhor Mercado, margem de segurança, paciência vs pânico).

FECHAMENTO OBRIGATÓRIO:
"Raquel | 9Pilla - dinheiro não é destino. É a jornada para a liberdade. 💛"
+ Disclaimer: "⚠️ Conteúdo educacional. Não constitui recomendação de investimento. CVM Res. 20/2021."

CONTEXTO BRASIL 2026:
- Geopolítica: Oriente Médio, Estreito de Ormuz (20% do petróleo mundial)
- Macro: IPCA ~5% (acima do teto 4,50%), Selic 14,50% em ciclo de corte, Dólar ~R$ 5
- Mercado: Ibovespa volátil, fluxo estrangeiro oscilando, Brent US$ 95-110"""

    def validate_connection(self) -> bool:
        """Valida se Claude API está acessível e com créditos"""
        if not ANTHROPIC_AVAILABLE:
            print("⚠️ Pacote 'anthropic' não instalado: pip install anthropic")
            return False
        if not self.client:
            print("⚠️ ANTHROPIC_API_KEY não configurada no .env")
            return False
        try:
            self.client.messages.create(
                model=self.model,
                max_tokens=10,
                messages=[{"role": "user", "content": "ping"}]
            )
            return True
        except Exception as e:
            print(f"⚠️ Erro ao conectar Claude API: {e}")
            if 'credit balance' in str(e).lower():
                print("   💳 Adicione créditos: https://console.anthropic.com/settings/billing")
            return False

    def run_setup_test(self) -> Dict[str, Any]:
        """Teste de setup usado pelo orchestrator --validate"""
        print("\n🧪 WriterAgent — Teste de Setup (Claude API)")
        print("=" * 60)

        connected = self.validate_connection()

        if connected:
            print("✅ Claude API conectado com sucesso!")
            print(f"   Modelo: {self.model}")
        else:
            print("⚠️ Claude API não disponível")
            print("\n📋 SETUP RÁPIDO:")
            print("   1. pip install anthropic")
            print("   2. Obter chave: https://console.anthropic.com/keys")
            print("   3. Adicionar créditos: https://console.anthropic.com/settings/billing")
            print("   4. Configurar ANTHROPIC_API_KEY no .env")

        return {
            'status': 'ready' if connected else 'error',
            'engine': 'Claude API',
            'model': self.model,
            'api_key_configured': bool(self.claude_api_key),
            'timestamp': datetime.now().isoformat()
        }

    def generate_script(
        self,
        market_data: Dict[str, Any],
        analyst_insights: Optional[Dict[str, Any]] = None,
        video_format: str = "shorts"  # shorts, morning_call, or tiktok
    ) -> Dict[str, Any]:
        """
        Gera script com voz Raquel usando Claude API

        Args:
            market_data: Dados do Prospector Agent
                {
                    'ticker': 'PETR4',
                    'price': 27.50,
                    'change_percent': -1.76,
                    'trend_topic': 'Queda do petróleo pressiona PETR4',
                    'full_market': {...}  # opcional: termômetro completo
                }
            analyst_insights: Dados do InvestingAnalysisAgent (opcional)
            video_format: shorts (60-90s), morning_call (2-3min), tiktok (45-60s)

        Returns:
            Dict com script estruturado pronto para Reviewer → ElevenLabs → HeyGen
        """

        ticker = market_data.get('ticker', 'IBOV')
        change = market_data.get('change_percent', 0)
        trend = market_data.get('trend_topic', 'Notícia de mercado')
        full_market = market_data.get('full_market', {})

        # Montar termômetro com dados reais (se disponível)
        thermometer = ""
        if full_market:
            thermometer = "\n📊 DADOS REAIS DO TERMÔMETRO (use exatamente estes números):\n"
            if 'ibov' in full_market:
                thermometer += f"- Ibovespa: {full_market['ibov'].get('value', 0):,.0f} ({full_market['ibov'].get('change_pct', 0):+.2f}%)\n"
            if 'dolar' in full_market:
                thermometer += f"- Dólar: R$ {full_market['dolar'].get('value', 0):.2f} ({full_market['dolar'].get('change_pct', 0):+.2f}%)\n"
            if 'petr4' in full_market:
                thermometer += f"- PETR4: R$ {full_market['petr4'].get('value', 0):.2f} ({full_market['petr4'].get('change_pct', 0):+.2f}%)\n"
            if 'vale3' in full_market:
                thermometer += f"- VALE3: R$ {full_market['vale3'].get('value', 0):.2f} ({full_market['vale3'].get('change_pct', 0):+.2f}%)\n"
            if 'brent' in full_market:
                thermometer += f"- Petróleo Brent: US$ {full_market['brent'].get('value', 0):.2f} ({full_market['brent'].get('change_pct', 0):+.2f}%)\n"

        analyst_block = ""
        if analyst_insights:
            sentiment = analyst_insights.get('sentiment', 'NEUTRA')
            analysts = analyst_insights.get('analysts', [])
            analyst_block = f"""
📈 ANÁLISE DE PROFISSIONAIS (Investing.com):
- Sentimento geral dos analistas: {sentiment}
- {len(analysts)} analistas consultados
"""

        duration = {'shorts': 75, 'tiktok': 50, 'morning_call': 150}.get(video_format, 75)

        user_prompt = f"""TAREFA: Escreva um script de YouTube Short de ~{duration} segundos (lido em voz alta) sobre:

🎯 TEMA PRINCIPAL: {trend}
- Ativo em destaque: {ticker}
- Variação: {change:+.2f}%
{thermometer}{analyst_block}
DATA: {datetime.now().strftime('%d/%m/%Y')}

ESTRUTURA DO SHORT (adaptação do Morning Call para vídeo curto):
1. [ABERTURA] Saudação calorosa Raquel (5s)
2. [TERMÔMETRO] 3-4 indicadores principais com emojis (15s)
3. [ANÁLISE] O tema principal com CADEIA CAUSAL explícita (25s)
4. [BOLSO] "O que isso significa pro seu bolso:" com 2-3 setas → (15s)
5. [PÍLLULA] Uma lição rápida de sabedoria (10s)
6. [FECHAMENTO] CTA leve + assinatura + disclaimer (5s)

IMPORTANTE:
- Texto será NARRADO em voz alta pela voz clonada da Raquel (ElevenLabs)
- Escreva como FALA, não como texto escrito
- Use os números REAIS fornecidos acima
- Responda APENAS com o script, marcando as seções com [ABERTURA], [TERMÔMETRO], [ANÁLISE], [BOLSO], [PÍLLULA], [FECHAMENTO]"""

        print(f"\n🎬 WriterAgent — Gerando script via Claude ({self.model})")
        print(f"   Ticker: {ticker}")
        print(f"   Tema: {trend}")

        if not self.client:
            return {
                'status': 'error',
                'message': 'Claude API não configurada (ANTHROPIC_API_KEY ausente ou pacote anthropic não instalado)',
                'fix': 'pip install anthropic && configure ANTHROPIC_API_KEY no .env'
            }

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                temperature=0.7,
                system=self.raquel_voice_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )

            script_text = response.content[0].text.strip()

            if not script_text:
                return {
                    'status': 'error',
                    'message': 'Claude retornou resposta vazia'
                }

            script_sections = self._parse_script_sections(script_text)

            return {
                'status': 'generated',
                'engine': 'claude',
                'model': self.model,
                'ticker': ticker,
                'script_full': script_text,
                'script_sections': script_sections,
                'market_data': market_data,
                'analyst_insights': analyst_insights,
                'format': video_format,
                'created_at': datetime.now().isoformat(),
                'ready_for_review': True,
                'next_step': 'Enviar para Reviewer (Telegram) para aprovação Raquel'
            }

        except Exception as e:
            error_msg = str(e)
            print(f"❌ Erro ao gerar script via Claude: {error_msg}")
            if 'credit balance' in error_msg.lower():
                print("   💳 SOLUÇÃO: Adicione créditos em https://console.anthropic.com/settings/billing")
            return {
                'status': 'error',
                'message': error_msg,
                'engine': 'claude'
            }

    def _parse_script_sections(self, full_script: str) -> Dict[str, str]:
        """Parse script em seções marcadas com [ABERTURA], [TERMÔMETRO], etc"""
        section_map = {
            'ABERTURA': 'hook',
            'TERMÔMETRO': 'thermometer',
            'TERMOMETRO': 'thermometer',
            'ANÁLISE': 'analysis',
            'ANALISE': 'analysis',
            'BOLSO': 'wallet_impact',
            'PÍLLULA': 'insight',
            'PILLULA': 'insight',
            'PÍLULA': 'insight',
            'FECHAMENTO': 'closing'
        }

        sections = {'hook': '', 'thermometer': '', 'analysis': '',
                    'wallet_impact': '', 'insight': '', 'closing': ''}
        current_section = None

        for line in full_script.split('\n'):
            stripped = line.strip()

            # Detectar marcador de seção: [ABERTURA], [TERMÔMETRO], etc
            if stripped.startswith('['):
                marker = stripped.strip('[]').strip().upper()
                if marker in section_map:
                    current_section = section_map[marker]
                    continue

            if current_section and stripped:
                sections[current_section] += stripped + ' '

        for key in sections:
            sections[key] = sections[key].strip()

        return sections

    def get_narration_text(self, script_data: Dict[str, Any]) -> str:
        """Extrai texto limpo (sem marcadores de seção) para narração ElevenLabs"""
        full = script_data.get('script_full', '')
        lines = []
        for line in full.split('\n'):
            stripped = line.strip()
            if stripped.startswith('[') and stripped.endswith(']'):
                continue
            lines.append(line)
        return '\n'.join(lines).strip()


# Test
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    agent = WriterAgent()
    print(json.dumps(agent.run_setup_test(), indent=2, ensure_ascii=False))

    result = agent.generate_script(
        market_data={
            'ticker': 'PETR4',
            'price': 47.50,
            'change_percent': -1.76,
            'trend_topic': 'Queda do petróleo pressiona PETR4',
            'full_market': {
                'ibov': {'value': 176200, 'change_pct': 0.71},
                'dolar': {'value': 4.96, 'change_pct': 0.40},
                'petr4': {'value': 47.50, 'change_pct': -1.76},
                'brent': {'value': 103.45, 'change_pct': 3.92},
            }
        }
    )
    print("\n" + "="*60)
    if result['status'] == 'generated':
        print(result['script_full'])
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))
