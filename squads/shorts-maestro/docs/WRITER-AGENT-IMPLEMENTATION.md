# 📝 WriterAgent — Implementação com Claude API

**Versão:** 2.0 (Claude)
**Data:** 11 de Junho de 2026
**Arquivo:** `agents/writer.py`

---

## Visão Geral

O WriterAgent gera scripts de YouTube Shorts com a **voz autêntica da Raquel**,
usando a Claude API (Anthropic) com um system prompt construído a partir da
análise de **16 Morning Calls reais** (ver `docs/RAQUEL-VOICE-TEMPLATE.md` na raiz do repo).

---

## Como Funciona

```
market_data (Prospector) ──┐
analyst_insights (opcional) ┼──→ Claude API ──→ script estruturado
RAQUEL_VOICE_PROMPT ───────┘     (system prompt)   [ABERTURA][TERMÔMETRO]
                                                    [ANÁLISE][BOLSO]
                                                    [PÍLLULA][FECHAMENTO]
```

### Interface (igual à versão Ollama — compatível com orchestrator)

```python
agent = WriterAgent(claude_api_key="sk-ant-...", model="claude-sonnet-4-6")

result = agent.generate_script(
    market_data={
        'ticker': 'PETR4',
        'change_percent': -1.76,
        'trend_topic': 'Queda do petróleo pressiona PETR4',
        'full_market': {...}  # termômetro completo do Prospector
    },
    analyst_insights=None,      # opcional (InvestingAnalysisAgent)
    video_format="shorts"       # shorts | morning_call | tiktok
)

# result['status']          → 'generated' ou 'error'
# result['script_full']     → script completo com marcadores
# result['script_sections'] → dict: hook, thermometer, analysis,
#                                   wallet_impact, insight, closing
```

### Métodos auxiliares

| Método | Função |
|--------|--------|
| `validate_connection()` | Testa API key + créditos (ping de 10 tokens) |
| `run_setup_test()` | Usado pelo `orchestrator.py --validate` |
| `get_narration_text(script_data)` | Remove marcadores `[SEÇÃO]` para enviar texto limpo ao ElevenLabs |

---

## Escolha de Modelo

| Modelo | Custo/script | Qualidade | Quando usar |
|--------|-------------|-----------|-------------|
| `claude-sonnet-4-6` ⭐ | ~US$ 0,01-0,02 | Excelente | **Padrão — recomendado** |
| `claude-opus-4-8` | ~US$ 0,05-0,10 | Máxima | Scripts especiais/campanhas |
| `claude-haiku-4-5` | ~US$ 0,003 | Boa | Testes em volume |

Trocar via `.env`:
```
CLAUDE_MODEL=claude-sonnet-4-6
```

---

## Prompt Engineering — Voz Raquel

O system prompt embute os padrões dos 16 Morning Calls:

1. **Aberturas reais** — "Bom dia, bom dia! Aqui é Raquel! ☕" + ritual do café
2. **Frases-assinatura** — "seu bolso" (2-3x), "turma", "Traduzindo...", "Fica o alerta"
3. **Princípio nº 1: conexão causal** — nunca notícia solta, sempre cadeia:
   `petróleo → inflação → Selic → bolsa → seu bolso`
4. **Píllula de Sabedoria** — 1 por script (Buffett, Graham, Barsi, Marks)
5. **Fechamento fixo** — "dinheiro não é destino. É a jornada para a liberdade. 💛"
6. **Disclaimer CVM** — obrigatório em 100% dos scripts

O user prompt injeta **dados reais do dia** (termômetro do Prospector via
`full_market`), garantindo que Claude use números verdadeiros, não inventados.

---

## Ajustando Tom/Estilo

Para refinar a voz, edite `self.raquel_voice_prompt` em `agents/writer.py`:

- **Mais formal?** Remova "turma", reduza emojis
- **Mais opinião?** Adicione exemplos de takes da Raquel
- **Novo bordão?** Adicione na seção "LINGUAGEM OBRIGATÓRIA"

Feedbacks de rejeição no Telegram (👎 + comentário) devem ser incorporados
aqui — é o "fine-tuning manual" do sistema.

---

## Tratamento de Erros

| Erro | Causa | Solução |
|------|-------|---------|
| `credit balance is too low` | Conta sem créditos | https://console.anthropic.com/settings/billing |
| `authentication_error` | Chave inválida | Gerar nova em console.anthropic.com/keys |
| `ANTHROPIC_API_KEY não configurada` | .env incompleto | Adicionar chave ao .env |
| Pacote não instalado | `anthropic` ausente | `pip install anthropic` |

**Importante:** Diferente da versão Ollama, o Writer agora **NÃO gera mock script**
em caso de erro — ele falha explicitamente. Isso protege os leads da Turma 9Pilla
de receberem conteúdo genérico.

---

## Teste Standalone

```bash
cd squads/shorts-maestro
python agents/writer.py
```

Saída esperada: setup test + script PETR4 completo no estilo Morning Call.
