# 🔍 ExpectationTracker — O Loop de Accountability do Morning Call

**Criado:** 11 de Junho de 2026, conceito da Raquel
**Arquivo:** `agents/expectation_tracker.py`

> "imagina uma inteligencia que fala todo dia de mercado financeiro utilizando
> dados passados e no dia seguinte lendo o que aconteceu ontem pra ver se o que
> foi dito fez sentido ou nao... A expectativa foi atendida?" — Raquel

---

## O Conceito (e o fundamento financeiro)

O mercado precifica a **expectativa consensual**. O que move preço é a
**SURPRESA**: a diferença entre o realizado e o esperado. Se todo mundo espera
IPCA de 0,5% e vem 0,5%, nada acontece. Se vem 0,8%, o preço se mexe.

Este agente mede exatamente isso, dia após dia:

```
DIA 1 (manhã):
  MarketAnalyst gera leitura com cenários probabilísticos
  → Tracker SALVA no diário (data/expectations/2026-06-11.json)

DIA 2 (manhã):
  Tracker LÊ a expectativa de ontem + dados reais de hoje
  → Claude compara: qual cenário se materializou? Bateu? Por quê?
  → Gera o bloco [CONFERE?] que abre o Morning Call
  → Salva a nova expectativa de hoje (loop continua)
```

---

## Por Que Isso É Um Diferencial Brutal

1. **Credibilidade:** o Morning Call abre dizendo "ontem a gente falou X,
   aconteceu Y". Mostra acertos E erros com honestidade. Nenhum influencer
   de finanças faz isso publicamente.
2. **Histórico auditável:** o diário fica versionado no git. Qualquer pessoa
   pode conferir o que foi dito em qualquer data. Transparência total.
3. **Educa o público:** ensina na prática o conceito de expectativa vs surpresa,
   que é como o mercado realmente funciona.
4. **Compliance:** como tudo é probabilístico ("existe a possibilidade"),
   revisar não é admitir erro de recomendação. É refinar leitura de cenários.

---

## O Diário (data/expectations/)

Um JSON por dia, **VERSIONADO NO GIT** (histórico permanente):

```json
{
  "date": "2026-06-11",
  "ticker": "PETR4",
  "analysis_text": "...cenários do MarketAnalyst...",
  "market_snapshot": { "ibov": ..., "dolar": ..., "brent": ... },
  "reviewed": false
}
```

Quando revisado no dia seguinte, ganha o campo `review` com o texto do
[CONFERE?] e os dados reais do dia da revisão.

---

## Posição no Pipeline

```
PROSPECTOR (termômetro)
    ↓
ANALYST (leitura macro/geo/fluxo)
    ↓
TRACKER ──→ revisa ONTEM vs HOJE  →  bloco [CONFERE?]
        └─→ salva expectativa de HOJE no diário
    ↓
WRITER (Morning Call com [CONFERE?] logo após o termômetro)
    ↓
REVIEWER (aprovação Raquel) → ...
```

---

## Demo Validada (11/06/2026)

Testamos com um "dia seguinte" simulado (Brent rompendo US$ 97,80):

> **[CONFERE?]** Ontem a gente falou que uma escalada geopolítica poderia
> empurrar o Brent acima de US$ 95-100 e dar suporte à PETR4. E o que aconteceu?
> Brent disparou 4,6%, chegando a US$ 97,80, e PETR4 subiu 3,09%...
> A lição do dia: a surpresa foi a magnitude do movimento. O mercado ainda não
> tinha precificado tudo, e foi exatamente aí que o preço se moveu.

✅ Zero travessões | ✅ Zero afirmações proibidas CVM | ✅ Honestidade na avaliação

**Nota:** a revisão demo foi removida do diário. A primeira revisão REAL
acontece no próximo ciclo (12/06), comparando a expectativa salva de 11/06
com os dados reais do dia.

---

## Custo

| Operação | Custo |
|----------|-------|
| Salvar expectativa | R$ 0 (arquivo local) |
| Revisão diária (1 chamada Claude, temp 0.3) | ~US$ 0,01 |

---

## Formato Morning Call Completo

O WriterAgent agora suporta `video_format='morning_call'` com a estrutura
completa dos 16 MCs analisados:

```
[ABERTURA] → [TERMÔMETRO] → [CONFERE?] → [BLOCO1] 🔥 → [BLOCO2] 🔥
→ [BLOCO3] 🔥 → [PÍLLULA] 💊 → [CTA] → [FECHAMENTO]
```

Uso direto:
```python
writer.generate_script(
    market_data={...},
    analyst_insights=analysis,
    video_format='morning_call',
    yesterday_review=review_text  # bloco [CONFERE?] do Tracker
)
```
