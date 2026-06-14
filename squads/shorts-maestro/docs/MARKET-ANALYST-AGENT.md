# 🧠 MarketAnalystAgent — Analista de Mercado (Macro, Geopolítica e Fluxo)

**Criado:** 11 de Junho de 2026, a pedido da Raquel
**Arquivo:** `agents/market_analyst.py`

> "seria interessante ter um agente analista de dados financeiros, especialista
> em leitura de mercado financeiro macro, geopolitica e fluxo" — Raquel

---

## O Que Ele Faz

Um analista sênior virtual que roda ANTES do Writer e entrega uma leitura
profissional do dia em 5 partes:

1. **LEITURA MACRO** — inflação, juros (Selic/Fed), câmbio
2. **LEITURA GEOPOLÍTICA** — Oriente Médio, Ormuz, OPEP, eleições
3. **LEITURA DE FLUXO E TÉCNICA** — capital estrangeiro, tendência, volatilidade
4. **POSSIBILIDADES** — cenários de alta E de baixa (nunca certezas)
5. **ALERTA DO DIA** — o que o investidor pessoa física deve observar

O Writer recebe essa análise e transforma em script com a voz da Raquel.

---

## ⚖️ Compliance CVM (Regra Absoluta)

**O agente NUNCA afirma movimento futuro de ativo.** Regra da Raquel (11/06/2026):

| ❌ PROIBIDO | ✅ CERTO |
|------------|---------|
| "PETR4 vai subir" | "existe a possibilidade de PETR4 subir no curto prazo, fica alerta" |
| "compre agora" | "o cenário sugere espaço para alta, mas nada é garantido" |
| "hora de vender" | "fique de olho, a decisão é sempre sua" |

Implementado em 3 camadas:
1. System prompt do MarketAnalyst (regra explícita)
2. System prompt do Writer (regra explícita)
3. Checagem automática no teste (busca por frases proibidas)

Motivo: CVM Res. 20/2021. Afirmar movimento futuro é dar recomendação de
investimento, o que exige certificação de analista (CNPI). Linguagem
probabilística + disclaimer protege a 9Pilla juridicamente.

---

## Dados Históricos da Brapi

O agente usa o histórico de preços da Brapi (`/api/quote/{ticker}?range=3mo&interval=1d`)
e calcula **localmente, sem gastar Claude**:

- Preço atual vs máxima/mínima do período
- Médias móveis (5 e 21 pregões)
- Volatilidade média diária
- Tendência de volume (últimos 5 dias vs média)
- Variação acumulada do período

Ranges disponíveis: `1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max`

**Nota:** do servidor remoto a Brapi é bloqueada (rede), então as estatísticas
técnicas só funcionam rodando da máquina local da Raquel. A análise
macro/geopolítica via Claude funciona de qualquer lugar.

---

## Posição no Pipeline

```
PROSPECTOR (termômetro do dia)
    ↓
🧠 ANALYST (macro + geopolítica + fluxo + histórico Brapi)   ← NOVO
    ↓
WRITER (script com voz Raquel, baseado na análise)
    ↓
REVIEWER (aprovação Raquel via Telegram)
    ↓
ElevenLabs → HeyGen → YouTube → Z-API
```

---

## Custo

| Operação | Custo |
|----------|-------|
| Histórico Brapi + estatísticas | R$ 0 (plano Brapi já pago + cálculo local) |
| Análise Claude (1 chamada, temperature 0.4) | ~US$ 0,01-0,02 |
| **Total por ciclo (Analyst + Writer)** | **~US$ 0,03-0,05** |

---

## Teste Standalone

```bash
cd squads/shorts-maestro
python agents/market_analyst.py
```

## Teste Validado (11/06/2026)

✅ Análise PETR4 com tensão Israel-Irã gerada com sucesso
✅ Zero travessões "—"
✅ Zero afirmações proibidas ("vai subir", "compre" etc)
✅ Cenários de alta E baixa apresentados
✅ Script final do Writer incorporou a análise com a voz da Raquel
