#!/usr/bin/env python3
"""
WriterAgent — Script Generation with Raquel Voice Pattern
Generates YouTube Shorts scripts using Ollama (local LLM) fine-tuned with Raquel's tone and structure
"""

import requests
import json
from datetime import datetime
from typing import Dict, Any, Optional, List

class WriterAgent:
    def __init__(self, ollama_base_url: str = "http://localhost:11434"):
        """
        Args:
            ollama_base_url: URL para Ollama local (default: localhost:11434)

        ⚠️ SETUP REQUIRED:
        1. Install Ollama: https://ollama.ai
        2. Run: ollama pull llama2
        3. Start Ollama: ollama serve
        4. Verify: curl http://localhost:11434/api/tags
        """
        self.ollama_base_url = ollama_base_url
        self.model = "llama2"
        self.headers = {"Content-Type": "application/json"}

        # Raquel Voice prompt template (extracted from 16 Morning Calls analysis)
        self.raquel_voice_prompt = """Você é Raquel, especialista em educação financeira da 9Pilla.

CARACTERÍSTICAS DA SUA VOZ:
- Tom: Amigável, casual, sem distância formal
- Sempre quebra o formalismo com expressões como "Bom dia!" ou referências ao café
- Conecta dados de mercado com o "bolso do brasileiro"
- Estrutura clara: Hook → Desenvolvimento → Insight → Call-to-Action

ESTRUTURA PADRÃO PARA SHORTS (60-90 segundos):
1. [ABERTURA CALOROSA - 5s] Saudação casual (ex: "Bom dia! Aqui é Raquel!")
2. [TERMÔMETRO DO DIA - 15s] Indicadores principais: Dólar, Ibov, Petróleo (com emojis)
3. [BLOCO 1 PRINCIPAL - 20s] Notícia macro com contexto global
4. [BLOCO 2 EFEITO DOMINÓ - 15s] Como isso afeta o Brasil/Bolso
5. [PÍLLULA DE SABEDORIA - 10s] Insight ou lição financeira
6. [FECHAMENTO - 5s] CTA + Disclaimer

TÓPICOS RECORRENTES (presentes em 90% dos calls):
- Oriente Médio & petróleo (aparece em ~80% das edições)
- Inflação e política monetária (juros)
- Dólar e reservas cambiais
- Ações de bancos (ITUB4, BBDC4)
- Commodities (Brent, WTI)

ESTILO DE LINGUAGEM:
- Use emojis estrategicamente 📊 💵 🛢️ 🏦
- Números sempre contextualizados ("Para você ver...")
- Perguntas retóricas ("Sabe o que isso significa?")
- Expressões de confiança ("Não é coincidência...")
- Fórmula de fechamento: "Continue nos acompanhando!" + disclaimer de risco

DADOS A INCORPORAR (você receberá):
- Ticker/Índice com % de variação
- Preço alvo do analista (opcional)
- Sentimento dos analistas (COMPRA/VENDA/NEUTRA)
- Notícia relevante ou contexto macro
"""

    def validate_connection(self) -> bool:
        """Valida se Ollama está rodando localmente"""
        try:
            response = requests.get(
                f"{self.ollama_base_url}/api/tags",
                headers=self.headers,
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            print(f"⚠️ Erro ao conectar Ollama: {e}")
            print(f"   Certifique-se que Ollama está rodando: ollama serve")
            return False

    def generate_script(
        self,
        market_data: Dict[str, Any],
        analyst_insights: Optional[Dict[str, Any]] = None,
        video_format: str = "shorts"  # shorts, morning_call, or tiktok
    ) -> Dict[str, Any]:
        """
        Gera script com voz Raquel usando Ollama local

        Args:
            market_data: Dados do Prospector Agent
                {
                    'ticker': 'PETR4',
                    'price': 27.50,
                    'change_percent': -1.76,
                    'trend_topic': 'Queda do petróleo pressiona PETR4'
                }
            analyst_insights: Dados do InvestingAnalysisAgent (opcional)
                {
                    'sentiment': 'VENDA',
                    'analysts': [{...}],
                    'technical_analysis': {...}
                }
            video_format: Formato do vídeo (shorts=60-90s, morning_call=2-3min, tiktok=45-60s)

        Returns:
            Dict com script estruturado pronto para ElevenLabs + HeyGen
        """

        if not self.validate_connection():
            print("\n⚠️ Ollama não está disponível!")
            print("   Usando fallback: mock script gerado")
            return self._get_mock_script(market_data)

        # Montar prompt com contexto específico
        ticker = market_data.get('ticker', 'IBOV')
        change = market_data.get('change_percent', 0)
        trend = market_data.get('trend_topic', 'Notícia de mercado')

        # Indicadores gerais (sempre inclusos)
        prompt = f"""{self.raquel_voice_prompt}

TAREFA: Gere um script de YouTube Short (60-90 segundos) sobre o seguinte:

📊 MERCADO HOJE:
- Ticker/Índice: {ticker}
- Variação: {change:+.2f}%
- Tema: {trend}

"""

        if analyst_insights:
            sentiment = analyst_insights.get('sentiment', 'NEUTRA')
            analysts = analyst_insights.get('analysts', [])

            prompt += f"""📈 ANÁLISE DE PROFISSIONAIS:
- Sentimento geral: {sentiment}
- {len(analysts)} analistas consultados
"""

            if analysts:
                analyst_names = [a.get('analyst', 'Desconhecido') for a in analysts[:3]]
                prompt += f"- Principais: {', '.join(analyst_names)}\n"

        prompt += f"""
DURAÇÃO ALVO: {60 if video_format == 'shorts' else 120} segundos (ler em voz alta)
FORMATO: {video_format.upper()}
DATA: {datetime.now().strftime('%d/%m/%Y')}

Gere o script seguindo a estrutura padrão. Inclua:
1. Abertura calorosa (natural, como Raquel fala)
2. Termômetro do dia com emojis
3. Análise do tema com contexto Brasil
4. Píllula de sabedoria ou insight
5. Fechamento + CTA

Dê como resposta APENAS o script (sem explicações adicionais).
Formato esperado:
[ABERTURA]
...

[TERMÔMETRO]
...

[ANÁLISE]
...

[PÍLLULA]
...

[FECHAMENTO]
...
"""

        print(f"\n🎬 WriterAgent — Gerando script via Ollama")
        print(f"   Ticker: {ticker}")
        print(f"   Tema: {trend}")
        print(f"   Aguardando resposta do Ollama...\n")

        try:
            response = requests.post(
                f"{self.ollama_base_url}/api/generate",
                headers=self.headers,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.7,  # Creative mas consistente
                    "num_predict": 500   # ~120s of speech ≈ 500 tokens
                },
                timeout=120  # Ollama pode levar um tempo
            )

            if response.status_code == 200:
                data = response.json()
                script_text = data.get('response', '').strip()

                if script_text:
                    # Parse script em seções
                    script_sections = self._parse_script_sections(script_text)

                    return {
                        'status': 'generated',
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

            return {
                'status': 'error',
                'message': f"Ollama retornou status {response.status_code}",
                'fallback': 'Usando mock script'
            }

        except requests.exceptions.Timeout:
            print("⏱️ Timeout ao conectar Ollama (modelo pode estar carregando)")
            return self._get_mock_script(market_data)
        except Exception as e:
            print(f"❌ Erro ao gerar script: {e}")
            return self._get_mock_script(market_data)

    def _parse_script_sections(self, full_script: str) -> Dict[str, str]:
        """Parse script em seções (abertura, termômetro, análise, píllula, fechamento)"""
        sections = {
            'hook': '',
            'thermometer': '',
            'analysis': '',
            'insight': '',
            'closing': ''
        }

        # Lógica simples: tenta identificar seções pelo conteúdo
        lines = full_script.split('\n')
        current_section = None

        for line in lines:
            if '[ABERTURA]' in line or 'Bom dia' in line:
                current_section = 'hook'
            elif '[TERMÔMETRO]' in line or 'TERMÔMETRO' in line:
                current_section = 'thermometer'
            elif '[ANÁLISE]' in line or 'ANÁLISE' in line:
                current_section = 'analysis'
            elif '[PÍLLULA]' in line or 'PÍLLULA' in line or 'SABEDORIA' in line:
                current_section = 'insight'
            elif '[FECHAMENTO]' in line or 'Continue' in line:
                current_section = 'closing'

            if current_section and line.strip() and not any(x in line for x in ['[', ']']):
                sections[current_section] += line.strip() + ' '

        # Cleanup
        for key in sections:
            sections[key] = sections[key].strip()

        return sections

    def _get_mock_script(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock script quando Ollama não está disponível"""

        ticker = market_data.get('ticker', 'IBOV')
        change = market_data.get('change_percent', 0)
        trend_topic = market_data.get('trend_topic', 'Notícia de mercado')

        direction = "📈 alta" if change > 0 else "📉 queda"

        mock_script = f"""Bom dia, bom dia! Aqui é Raquel. Já pegou seu café? ☕

📊 TERMÔMETRO DO DIA
💵 Dólar: R$ 5,03
📈 Ibovespa: 174.197
🛢️ Petróleo Brent: US$ 95,45
🏦 {ticker}: {direction} {abs(change):.2f}%

{ticker} está em {direction} hoje. Por quê? Porque {trend_topic}.

Isso pode parecer um número só, mas afeta seu bolso de três formas diferentes. Vou explicar.

A primeira conexão é direta: preço da ação muda, seu patrimônio muda. Simples. A segunda é no bolso pela inflação. A terceira é nas oportunidades que você deixa passar.

Lição do dia: Não é coincidência. Quando {ticker} cai, sempre tem um contexto. Pode ser geopolítica, pode ser balanço, pode ser sentimento do mercado. O importante é você entender a conexão.

Continue nos acompanhando para as próximas análises! Disclaimer: Conteúdo educacional apenas."""

        sections = {
            'hook': f"Bom dia, bom dia! Aqui é Raquel. Já pegou seu café? ☕",
            'thermometer': "💵 Dólar: R$ 5,03\n📈 Ibovespa: 174.197\n🛢️ Petróleo Brent: US$ 95,45",
            'analysis': f"{ticker} está em {direction} hoje. Por quê? Porque {trend_topic}.",
            'insight': "Lição do dia: Não é coincidência. Quando {ticker} cai, sempre tem um contexto.",
            'closing': "Continue nos acompanhando! Disclaimer: Conteúdo educacional apenas."
        }

        return {
            'status': 'generated_mock',
            'ticker': ticker,
            'script_full': mock_script,
            'script_sections': sections,
            'market_data': market_data,
            'format': 'shorts',
            'created_at': datetime.now().isoformat(),
            'ready_for_review': True,
            'warning': '⚠️ Script de teste (Ollama não disponível) — Substitua por script real quando Ollama estiver rodando',
            'next_step': 'Enviar para Reviewer (Telegram) para aprovação Raquel'
        }

    def run_setup_test(self) -> Dict[str, Any]:
        """Testa se Ollama está corretamente configurado"""

        print("\n🧪 WriterAgent — Teste de Setup")
        print("=" * 60)

        is_valid = self.validate_connection()

        if is_valid:
            print("✅ Ollama conectado com sucesso!")
            print(f"   URL: {self.ollama_base_url}")
            print(f"   Modelo: {self.model}")
        else:
            print("⚠️ Ollama não está rodando")
            print("\n📋 SETUP RÁPIDO:")
            print("1. Instale Ollama: https://ollama.ai")
            print("2. Execute no terminal: ollama serve")
            print("3. Em outra aba: ollama pull llama2")
            print("4. Volte aqui e rode novamente\n")

        print("=" * 60)

        return {
            'status': 'ready' if is_valid else 'needs_setup',
            'ollama_connected': is_valid,
            'ollama_url': self.ollama_base_url,
            'model': self.model,
            'raquel_voice_prompt_loaded': True,
            'setup_guide': 'https://ollama.ai/download'
        }


# INTEGRAÇÃO: Prospector → Writer → Executor
class ProspectorToWriterPipeline:
    """
    Conecta Prospector → Writer → Executor
    Fluxo: Dados mercado → Script → Vídeo
    """

    def __init__(self, writer_agent: WriterAgent):
        self.writer = writer_agent

    def generate_script_from_prospector_data(
        self,
        prospector_output: Dict[str, Any],
        analyst_insights: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Converte saída do Prospector em script via Writer

        Fluxo: Prospector.identify_trending_topic()
               ↓
          ProspectorToWriterPipeline.generate_script_from_prospector_data()
               ↓
          Reviewer Agent (Telegram) aprova
               ↓
          Executor Agent (HeyGen/ElevenLabs) cria vídeo
        """

        print("\n📊 → 📝 Pipeline: Prospector → Writer")

        # Usar dados do Prospector como entrada do Writer
        script_result = self.writer.generate_script(
            market_data={
                'ticker': prospector_output.get('trending_ticker'),
                'price': prospector_output.get('current_price'),
                'change_percent': prospector_output.get('price_change'),
                'trend_topic': prospector_output.get('topic')
            },
            analyst_insights=analyst_insights,
            video_format='shorts'
        )

        return {
            'prospector_input': prospector_output,
            'writer_output': script_result,
            'pipeline_status': 'script_ready',
            'next_step': 'Enviar para Reviewer'
        }


# Test
if __name__ == "__main__":
    print("\n" + "="*60)
    print("WRITER AGENT TEST")
    print("="*60 + "\n")

    writer = WriterAgent(ollama_base_url="http://localhost:11434")

    # Teste 1: Validar setup
    print("📋 Teste 1: Setup Ollama")
    setup = writer.run_setup_test()
    print(json.dumps(setup, indent=2, ensure_ascii=False))

    # Teste 2: Gerar script com dados mock
    print("\n📝 Teste 2: Gerar script")

    mock_prospector = {
        'ticker': 'PETR4',
        'price': 27.50,
        'change_percent': -1.76,
        'trend_topic': 'Queda do petróleo pressiona Petrobras'
    }

    mock_analyst = {
        'sentiment': 'VENDA',
        'analysts': [
            {'analyst': 'Itaú BBA', 'recommendation': 'VENDA', 'target_price': 'R$ 25.00'},
            {'analyst': 'Bradesco BBI', 'recommendation': 'MANUTENÇÃO', 'target_price': 'R$ 28.00'}
        ]
    }

    script = writer.generate_script(
        market_data=mock_prospector,
        analyst_insights=mock_analyst,
        video_format='shorts'
    )

    print(json.dumps(script, indent=2, ensure_ascii=False))

    print("\n" + "="*60)
    print("PIPELINE USAGE:")
    print("="*60)
    print("""
# 1. Prospector identifica tema
prospector = ProspectorAgent(brapi_key='...')
topic = prospector.identify_trending_topic()

# 2. Writer gera script
writer = WriterAgent()
script = writer.generate_script(
    market_data={
        'ticker': topic['ticker'],
        'price': topic['price'],
        'change_percent': topic['change'],
        'trend_topic': topic['topic']
    }
)

# 3. Enviar para Reviewer aprovar
reviewer.send_to_telegram(script)

# 4. Se aprovado, Executor cria vídeo
if reviewer.status == 'APROVADO':
    executor.create_video_from_script(script)
    """)
