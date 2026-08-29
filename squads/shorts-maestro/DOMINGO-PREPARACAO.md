# 🔵 DOMINGO-PREPARACAO — O dia mais importante da semana

**Status:** 🟢 ESSENCIAL PARA MORNING CALLS SEG-SEX  
**Frequência:** Todo domingo (depois que bolsas fecham)  
**Duração:** ~2 horas (10h-16h)  
**Propósito:** Gerar INSIGHTS que guiam toda a semana

---

## 🎯 **Por que Domingo é Crítico**

Enquanto você dorme, o mundo está PREPARANDO o palco para a semana:

```
DOMINGO = Todas as bolsas FECHARAM a semana
        = Você tem padrão COMPLETO
        = Pode ver o quadro MACRO
        = Tira INSIGHTS que GUIAM seg-sex

SEGUNDA-SEXTA = Você executa baseado em INSIGHTS de domingo
              = Profit Pro coleta DADOS do dia
              = Morning Call combina: Insights + Dados
```

**Exemplo prático:**
```
DOMINGO você vê:
  • Petróleo caiu TODA a semana (4 dias)
  • Wall Street teve rally (entrada de capital)
  • Cripto em alta (risk on)
  
Você GUARDA isso:
  "Próxima semana deve ter entrada de estrangeiro"
  
SEGUNDA você roda morning_call.py:
  • Profit Pro traz dados de SEGUNDA
  • Você já SABE o contexto (insights DOMINGO)
  • Morning Call fica MUITO mais rico:
    "Turma, lembram que domingo vimos petróleo caindo?
     Pois bem, isso continua. Aí SEGUNDA teve...
     Combinando tudo: esperamos..."
```

---

## 📊 **O que analisar no DOMINGO**

### **Bloco 1: Dados Fechados (10:00-11:00)**

Pega dados de TODA a semana que terminou:

```
✅ WALL STREET (NY, NASDAQ)
   • S&P 500: subiu ou caiu na semana?
   • Dow Jones: tendência?
   • NASDAQ: tech forte ou fraca?
   • Fed decisions ou sinalizações?
   
✅ ÁSIA (Tokyo, Hong Kong, Shanghai)
   • Nikkei: como começou a semana?
   • Hang Seng: China tá forte?
   • Shanghai Composite: tech asiática?
   
✅ EUROPA (Frankfurt, London)
   • DAX: economia alemã?
   • FTSE: commodities?
   • ECB: notícias sobre euro?
   
✅ BRASIL (B3)
   • IBOVESPA: como terminou a semana?
   • PETR4: seguiu petróleo ou deviated?
   • VALE3: ouro e commodities?
   • ITUB4: bancos e selic?
```

### **Bloco 2: Commodities (11:00-12:00)**

```
✅ PETRÓLEO BRENT
   • Subiu ou caiu na semana?
   • Qual o driver (geopolítica, oferta, demanda)?
   • Próxima semana: vai continuar?
   
✅ DÓLAR
   • Fortaleceu ou enfraqueceu?
   • Fed rate decisions?
   • Fluxo estrangeiro?
   
✅ OURO
   • Oferta de segurança (medo)?
   • Ou inflação (proteção)?
   
✅ CRIPTO
   • Bitcoin/Ethereum: semana forte?
   • Sentimento risk on ou off?
```

### **Bloco 3: Padrões (12:00-14:00)**

```
✅ CONVERGÊNCIAS
   • Todas as bolsas subiram? (risk on global)
   • Todas caíram? (risk off global)
   • Algumas subiram, outras caíram? (divergência)
   
✅ MOVIMENTOS GRANDES
   • Houve gap importante em alguma bolsa?
   • Alguma commodity fez movimento extremo?
   
✅ FLUXO ESTRANGEIRO
   • Entrada ou saída do Brasil?
   • Ibovespa acompanhando NY?
   
✅ INDICADORES ECONÔMICOS
   • Teve data importante? (FOMC, BCE, Banco Central BR)
   • Dados econômicos (desemprego, inflação, PIB)?
```

### **Bloco 4: Insights e Cenários (14:00-16:00)**

```
Baseado em tudo que você viu, tira 3-5 INSIGHTS:

INSIGHT 1: "Petróleo caiu 3% na semana"
Implicação: "PETR4 deve reagir para baixo segunda"
Ação: "Alertar turma pra cautela com PETR4"

INSIGHT 2: "Wall Street em rallye"
Implicação: "Entrada de estrangeiro esperada"
Ação: "Alertar turma: pode ser semana de alta"

INSIGHT 3: "Selic em corte ciclo"
Implicação: "Bonds atraindo, bancos sofrem"
Ação: "Alertar turma: ITUB4 pode cair"

INSIGHT 4: "Cripto forte (risk on)"
Implicação: "Mercado com apetite"
Ação: "Alertar turma: oportunidades aparecem"

INSIGHT 5: "Dólar enfraqueceu"
Implicação: "Importadores se beneficiam"
Ação: "Alertar turma: setores exportadores apreciam"
```

---

## 📝 **Documento: INSIGHTS-SEMANA.txt**

Domingo você CRIA um arquivo com os insights:

```
# INSIGHTS SEMANA 15/06 - 19/06/2026

## CONTEXTO GLOBAL
• Wall Street: Fechou em alta (risk on)
• Petróleo: Caiu 3% (pressão baixista)
• Dólar: Enfraqueceu 1% (estrangeiro entra)
• Cripto: Bitcoin em alta (sentimento positivo)

## BRASIL
• IBOVESPA: Fechou semana anterior em 176.450 (+0,71%)
• PETR4: Sofreu com queda de petróleo
• VALE3: Seguiu commodities
• ITUB4: Sofreu com expectativa de corte Selic

## CENÁRIOS PARA PRÓXIMA SEMANA

### CENÁRIO 1 (Probabilidade: 60%)
"Risco On continua"
- Entrada de estrangeiro
- Petróleo estabiliza
- IBOVESPA pode tentar novo máximo
- PETR4 recupera

### CENÁRIO 2 (Probabilidade: 25%)
"Petróleo cai mais"
- PETR4 continua pressionado
- VALE3 também sofre
- IBOVESPA diverge para baixo

### CENÁRIO 3 (Probabilidade: 15%)
"Selic cai rápido"
- Bancos sofrem (ITUB4, BBDC4)
- Bonds ganham
- Ibovespa pode ter reação positiva (renda variável)

## ALERTS PARA SEGUNDA-SEXTA
✅ Monitorar PETR4 (petróleo guia)
✅ Monitorar fluxo estrangeiro (NY lidera)
✅ Atentar para ITUB4 (bancos)
✅ Oportunidades em exportadores (dólar fraco)
```

---

## 🔄 **Como usar INSIGHTS-SEMANA na Morning Call**

**SEGUNDA-FEIRA (18:30) python morning_call.py:**

```python
# Inside WriterAgent, lê INSIGHTS-SEMANA.txt
insights = open('INSIGHTS-SEMANA.txt').read()

# Combina com dados de SEGUNDA
market_data = {
    'insights_global': insights,  # De DOMINGO
    'data_segunda': [...],        # De SEGUNDA (Profit Pro)
}

# Morning Call fica rico:
"Turma, lembram do que eu falei ontem? 
 [resumo insights de DOMINGO]
 
 Pois bem, hoje SEGUNDA tivemos [dados de SEGUNDA].
 
 Combinando: [análise + ação]"
```

---

## 📋 **Checklist DOMINGO (2 horas)**

```
⏰ 10:00-10:30
☑️ Dados Wall Street (semana)
☑️ Dados Ásia (semana)
☑️ Dados Europa (semana)

⏰ 10:30-11:00
☑️ Dados B3 (semana)
☑️ Petróleo, Dólar, Ouro, Cripto (semana)

⏰ 11:00-13:00
☑️ Identificar padrões globais
☑️ Risk on ou risk off?
☑️ Convergências ou divergências?

⏰ 13:00-14:00
☑️ Tirar 3-5 insights principais
☑️ Documentar em INSIGHTS-SEMANA.txt

⏰ 14:00-16:00
☑️ Revisar e validar insights
☑️ Preparar cenários para seg-sex
☑️ Documentar alerts
```

---

## 💡 **Template: INSIGHTS-SEMANA.txt**

```
# INSIGHTS SEMANA [DATA]

## CONTEXTO GLOBAL
• Wall Street: [subiu/caiu] %
• Petróleo Brent: [subiu/caiu] % = [impacto PETR4]
• Dólar: [subiu/caiu] % = [impacto importações/exportadores]
• Cripto: [forte/fraca] = [sentimento risco]
• Ásia: [tendência]
• Europa: [tendência]

## BRASIL
• IBOVESPA: [subiu/caiu] % (motivo)
• PETR4: [comportamento vs petróleo]
• VALE3: [comportamento vs commodities]
• ITUB4: [comportamento vs Selic]

## CENÁRIOS PARA PRÓXIMA SEMANA

### CENÁRIO 1 (Prob: XX%)
[Descrição]
→ Impacto: [quem sobe/cai]

### CENÁRIO 2 (Prob: XX%)
[Descrição]
→ Impacto: [quem sobe/cai]

### CENÁRIO 3 (Prob: XX%)
[Descrição]
→ Impacto: [quem sobe/cai]

## ALERTS PARA SEGUNDA-SEXTA
✅ [Indicador 1: monitorar X]
✅ [Indicador 2: monitorar Y]
✅ [Indicador 3: monitorar Z]

## OPORTUNIDADES
🎯 [Setor/ação com alta prob positiva]
🎯 [Setor/ação com cautela]
🎯 [Setor/ação com entrada esperada]
```

---

## 🚀 **Fluxo Semanal Completo**

```
DOMINGO (16:00):
  └─ INSIGHTS-SEMANA.txt criado e salvo

SEGUNDA-FEIRA (18:30):
  └─ python morning_call.py roda
  └─ Lê INSIGHTS-SEMANA.txt
  └─ Combina com dados de SEGUNDA
  └─ Morning Call é CONTEXTUALIZADO

TERÇA-SEXTA (18:30):
  └─ Mesmo fluxo
  └─ INSIGHTS-SEMANA.txt continua guiando
  └─ Dados novos (seg, ter, qua, qui, sex) complementam

PRÓXIMO DOMINGO (16:00):
  └─ Nova análise macro
  └─ Novo INSIGHTS-SEMANA.txt
```

---

## ✨ **Por que isso funciona**

```
SEM INSIGHTS-SEMANA:
Morning Call de SEGUNDA = análise isolada
"PETR4 caiu por isso hoje"
(sem contexto maior)

COM INSIGHTS-SEMANA:
Morning Call de SEGUNDA = análise contextualizada
"Petróleo vinha caindo desde... (DOMINGO insights)
 Hoje SEGUNDA tivemos [movimento novo]
 Expectativa para próximos dias: ..."
(tudo conectado, narrativa clara)
```

---

## 🎯 **Status: 🟢 DOMINGO É O ALICERCE**

Você estava 100% certo! Domingo não é folga, é o dia mais importante da semana.

DOMINGO = Você entende o padrão global
SEGUNDA-SEXTA = Você executa com inteligência

**Próxima semana: implementar INSIGHTS-SEMANA.txt a partir do domingo! 💛**
