# CLAUDE.md — Memória do Projeto 9Pilla

Regras permanentes definidas pela Raquel. Valem para TODA sessão neste repositório.

## Comunicação
- Falar SEMPRE em português do Brasil (Raquel não fala inglês fluente)
- Documentar tudo em arquivos .md e salvar no GitHub

## Regras de Conteúdo (scripts, Morning Calls, Shorts)
- **NUNCA usar travessão "—"** em nenhum texto gerado. É linguagem de IA.
  Escrever frases fluidas como conversa real, usando vírgula ou ponto.
  (Regra da Raquel, 11/06/2026. Implementada em `squads/shorts-maestro/agents/writer.py`
  com dupla proteção: prompt + pós-processamento)
- **COMPLIANCE CVM: NUNCA afirmar movimento futuro de ativo.** Proibido "PETR4 vai subir".
  Usar sempre linguagem probabilística e branda: "existe a possibilidade de PETR4 subir
  no curto prazo, fica alerta". Nunca dar recomendação direta de compra ou venda.
  (Regra da Raquel, 11/06/2026. Motivo: regulação CVM Res. 20/2021 e proteção jurídica)
- Setas "→" para cadeia causal são permitidas (visuais, não faladas)
- Voz da Raquel: ver `docs/RAQUEL-VOICE-TEMPLATE.md` (análise de 16 Morning Calls)
- Fechamento obrigatório: "dinheiro não é destino. É a jornada para a liberdade. 💛"
- Disclaimer CVM obrigatório em todo conteúdo

## Proteção de Orçamento e Qualidade
- Leads da Turma 9Pilla são clientes quentes: ZERO margem para erro de conteúdo
- Aprovação em 2 estágios: Raquel aprova SCRIPT e depois VÍDEO antes de publicar
- HeyGen (US$ 0,30/vídeo) SÓ roda após aprovação do script
- Economizar créditos Claude: validar qualidade ANTES de gerar em volume
- Nada de criar conteúdo "sem sentido" para aprovação: qualidade primeiro

## Stack
- Scripts: Claude API (claude-sonnet-4-6), NÃO Ollama (migrado 11/06/2026)
- Dados de mercado: Brapi (`https://brapi.dev/api`, dólar via `/v2/currency?currency=USD-BRL`)
- Narração: ElevenLabs (Voice ID 0r2zCQO0vO1jOfWbm7N7)
- Avatar: HeyGen (Avatar ID 351538dd8eea417882a312681f2168d9)
- Aprovação: Telegram @raquel_9pilla_bot (Chat ID 7686120986)
- WhatsApp: Z-API | Funis: ManyChat (sem vendas até janeiro 2027)

## Limitações do Ambiente
- Servidor remoto BLOQUEIA: Telegram, Brapi, ElevenLabs, HeyGen, Z-API (403 allowlist)
- Servidor remoto PERMITE: api.anthropic.com (Claude funciona daqui!)
- APIs bloqueadas precisam rodar da máquina Windows local da Raquel
