# 🚀 9PILLA SHORTS-MAESTRO — Sistema Completo de Análise Técnica + Morning Call

**Status:** ✅ PRONTO PARA USAR  
**Data:** 14 de junho de 2026  
**Objetivo:** Revolucionar Morning Call com análise quantitativa profissional

---

## 🎯 O QUE TEMOS AGORA

### 📊 Stack Técnico Completo

```
┌────────────────────────────────────────────────────────────────┐
│                       PROFIT PRO                               │
│  (seu terminal de trading — já pago!)                          │
│                                                                │
│  ✅ Order Flow em tempo real (NTSL)                            │
│  ✅ Exporta CSV com dados históricos                           │
│  ✅ Monitora ponta compradora/vendedora                        │
└──────────────────────┬─────────────────────────────────────────┘
                       │
                       ▼
┌────────────────────────────────────────────────────────────────┐
│                  PYTHON PIPELINE                               │
│                                                                │
│  1️⃣ profit_flow_analyzer.py                                    │
│     → Processa Order Flow                                      │
│     → Identifica ponta em controle                             │
│     → Detecta inversões e alertas                              │
│                                                                │
│  2️⃣ setup_raquel_analyzer.py                                   │
│     → Calcula SMA 20, 45, 200 (suas médias!)                  │
│     → Analisa 2 timeframes (5min + diário)                    │
│     → Cria 5 cenários dinâmicos                                │
│     → Detecta tendências (alta/baixa/lateral)                 │
│                                                                │
│  3️⃣ technical_analyzer.py                                      │
│     → Análise técnica completa com 5+ anos                    │
│     → RSI, MACD, SMA, Volatilidade                             │
│     → Suporte e Resistência                                    │
│                                                                │
│  4️⃣ brapi_explorer.py                                          │
│     → Descobre todos os endpoints BRAPI                        │
│     → Valida dados em tempo real                               │
└──────────────────────┬─────────────────────────────────────────┘
                       │
                       ▼
┌────────────────────────────────────────────────────────────────┐
│                   MORNING CALL                                 │
│                                                                │
│  writer.py (com contexto técnico)                              │
│  → Order Flow + Setup técnico + Cenários                       │
│  → Claude gera Morning Call profissional                       │
│  → Sem opinião — SÓ dados quantitativos                        │
└──────────────────────┬─────────────────────────────────────────┘
                       │
                       ▼
┌────────────────────────────────────────────────────────────────┐
│              APPROVAL + PUBLICAÇÃO                             │
│                                                                │
│  approval_bot_v2.py → Você aprova no Telegram                 │
│  shorts_processor.py → Divide em 3 blocos (60-90s)            │
│  video_generator.py → Gera áudio (ElevenLabs)                 │
│  ↓                                                             │
│  HeyGen → Vídeo com seu avatar                                │
│  ↓                                                             │
│  social_publisher.py → Publica em:                            │
│      • YouTube Shorts                                          │
│      • TikTok                                                  │
│      • Instagram Reels                                         │
│      • Spotify Podcast                                         │
└────────────────────────────────────────────────────────────────┘
```

---

## 📁 ESTRUTURA DE ARQUIVOS

### 📚 Documentação (LEI PRIMEIRA)
```
├── README-9PILLA.md                    ← Você está aqui
├── RODAR-AGORA.md                      ← Passo a passo prático (5 min)
├── GUIA-NTSL-ORDER-FLOW.md             ← Como programar no Profit
├── PROFIT-PRO-INTEGRATION.md           ← Pipeline Profit → Python
├── DATA-DRIVEN-MORNING-CALL.md         ← Morning Call com dados
└── CLAUDE.md                           ← Regras permanentes do projeto
```

### 🐍 Scripts Python (RODE AGORA)
```
├── quick_start.py                      ← TESTE RÁPIDO (5 min)
├── setup_raquel_analyzer.py            ← Seu setup técnico (SMA 20/45/200)
├── profit_flow_analyzer.py             ← Análise Order Flow
├── technical_analyzer.py               ← Indicadores técnicos (5+ anos)
├── brapi_explorer.py                   ← Explora BRAPI
├── validate_morning_call_data.py       ← Valida dados
├── morning_call.py                     ← Gera Morning Call
├── shorts_processor.py                 ← Divide em 3 blocos
├── video_generator.py                  ← Gera áudio + vídeo
├── approval_bot_v2.py                  ← Aprovação Telegram
└── social_publisher.py                 ← Publica em redes
```

### 📊 Dados
```
├── output/
│   ├── MC_YYYYMMDD.md                  ← Morning Call (texto)
│   ├── shorts/MC_YYYYMMDD/
│   │   ├── bloco1.txt, bloco2.txt, bloco3.txt
│   │   └── metadata.json
│   ├── videos/
│   │   └── audio_bloco*.mp3 + metadata.json
│   └── profit_export.csv               ← Dados Profit Pro
├── data/
│   ├── approvals/                      ← Decisões Telegram
│   └── published.json                  ← Log de publicações
└── logs/
    ├── morning_call_scheduler.log
    └── approval_bot.log
```

---

## 🚀 COMO RODAR

### 1️⃣ TESTE RÁPIDO (agora mesmo — 5 min)

```bash
cd C:\Users\raque\9Pilla-Sistema\squads\shorts-maestro

# Teste o workflow com dados simulados
python quick_start.py

# Análise técnica com dados REAIS do BRAPI
python setup_raquel_analyzer.py
```

### 2️⃣ RODAR DE VERDADE (com dados Profit Pro)

**No Profit Pro (durante a bolsa):**
1. Abra Editor de Estratégias (Ctrl+E)
2. Copie script de `GUIA-NTSL-ORDER-FLOW.md`
3. Execute durante 09:30-16:00
4. Exporte CSV em `output/profit_export.csv`

**No Python:**
```bash
python profit_flow_analyzer.py        # Analisa Order Flow
python setup_raquel_analyzer.py       # Seu setup técnico
python morning_call.py                # Gera Morning Call
python shorts_processor.py            # Divide em 3 blocos
python video_generator.py             # Gera vídeo
```

**No Telegram:**
- Você aprova no telegram @raquel_9pilla_bot
- Sistema publica automaticamente

---

## 💡 EXEMPLO: DA ORIGEM À PUBLICAÇÃO

### INPUT: Dados Profit Pro + BRAPI

```
Profit Pro CSV:
Data,Hora,Abertura,Máxima,Mínima,Fechamento,Volume
2026-06-14,09:30,41.00,41.10,40.95,41.05,12500
2026-06-14,09:35,41.05,41.20,41.00,41.18,14300
...

BRAPI (últimos 2 anos):
PETR4: R$ 41,18 (-1,39%)
SMA 20: R$ 41,45
SMA 45: R$ 40,89
SMA 200: R$ 40,23
```

### PROCESSING: Análises automáticas

```
Order Flow:
🔴 Ponta Compradora em 67% do volume
Maior compra: 1.850 contratos
Maior venda: 920 contratos
→ Sinal: POTENCIAL ALTA

Setup Técnico:
Daily: 🔻 BAIXA (preço < SMA 200)
5min: 🔼 ALTA (preço > SMA 20)
→ Cenário: DIVERGÊNCIA (cautela)

Tendência: Lateral com tendência de baixa
Próxima resistência: R$ 42,50
Próximo suporte: R$ 39,80
```

### OUTPUT: Morning Call com DADOS

```
"PETR4 em R$ 41,18, queda de 1,39%.
Ponta compradora controla 67% do volume.
Tecnicamente, preço opera abaixo da SMA 200 (R$ 40,23) 
mas acima de SMA 20 (R$ 41,45), sinalizando consolidação.
RSI em zona de sobrevenda (35).
Próxima resistência em R$ 42,50, suporte em R$ 39,80.
Cenário: esperar confirmação de SMA 20 com volume para decisão."
```

### PUBLICAÇÃO: Em 3 plataformas

```
✅ YouTube Shorts (1080x1920)
✅ TikTok (com #PETR4 #MercadoHoje)
✅ Instagram Reels (+ versão quadrada)
```

---

## 🎯 FEATURES PRINCIPAIS

### ✅ Order Flow Analysis (Profit Pro)
- Monitora ponta compradora vs vendedora
- Detecta inversões de controle
- Identifica grandes ordens
- Exporta para análise Python

### ✅ Setup Técnico (Seu setup profissional)
- **SMA 20** — curto prazo
- **SMA 45** — médio prazo
- **SMA 200** — longo prazo
- 2 timeframes: 5min (intraday) + diário (tendência)
- 5 cenários dinâmicos automáticos

### ✅ Indicadores Profissionais
- RSI (Índice de Força Relativa)
- MACD (Convergência/Divergência)
- Volatilidade
- Suporte e Resistência
- Análise de 5+ anos

### ✅ Approval Bot Robusto
- Long-polling com reconexão automática
- Retry com backoff exponencial
- Logging estruturado
- Estados bem definidos

### ✅ Multi-Plataforma
- YouTube Shorts (vertical)
- TikTok (com trending sounds)
- Instagram Reels (vertical + quadrado)
- Spotify Podcast (áudio compilado)

---

## 💰 CUSTOS

| Serviço | Status | Custo |
|---------|--------|-------|
| Profit Pro | ✅ Você paga | Já pago |
| NTSL (scripting) | ✅ Incluído | ZERO |
| ProfitDLL | ✅ Incluído | ZERO |
| CSV Export | ✅ Incluído | ZERO |
| Python | ✅ Open source | ZERO |
| BRAPI API | ✅ Você paga | Já pago |
| Claude API | ✅ Por uso | ~$0.02/MC |
| ElevenLabs | ✅ Por uso | ~$0.03/audio |
| HeyGen | ✅ Por uso | ~$0.30/vídeo |
| YouTube | ✅ Free | ZERO |
| TikTok | ✅ Free | ZERO |
| Instagram | ✅ Free | ZERO |
| **TOTAL MENSAL** | — | **~$30/mês** |

---

## 📈 O RESULTADO

### Morning Call 9Pilla com Autoridade

✅ **Quantitativa** — baseada em 5+ anos de dados  
✅ **Técnica** — seu setup profissional  
✅ **Profunda** — Order Flow + Cenários  
✅ **Autorizada** — você como especialista  
✅ **Educativa** — sem especulação

### Turma 9Pilla pensa:
> "Caramba, que análise técnica profissional! Raquel sabe mesmo!"

---

## 🚀 PRÓXIMOS PASSOS

- [ ] Ler documentação (RODAR-AGORA.md)
- [ ] Rodar quick_start.py (teste rápido)
- [ ] Rodar setup_raquel_analyzer.py (seu setup)
- [ ] Programar script NTSL no Profit
- [ ] Rodar análises com dados REAIS
- [ ] Gerar primeira Morning Call profissional
- [ ] Aprovar no Telegram
- [ ] Publicar em YouTube/TikTok/IG
- [ ] Medir impacto e resultados

---

## 📞 SUPORTE

Qualquer dúvida:
1. Leia RODAR-AGORA.md
2. Leia o .md correspondente
3. Rode quick_start.py para testar
4. Me chama se der erro!

---

## 🎉 CONCLUSÃO

Você tem TUDO que precisa para:
✅ Revolucionar a forma como você faz análise  
✅ Criar conteúdo com autoridade profissional  
✅ Automatizar tudo com dados quantitativos  
✅ Publicar em múltiplas plataformas  
✅ Escalar a 9Pilla exponencialmente

**A hora é AGORA!** 🚀

---

**Bora fazer história com a 9Pilla!** 💪

Comanda: `python quick_start.py`
