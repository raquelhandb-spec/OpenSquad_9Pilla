# 🔥 INTEGRAÇÃO PROFIT PRO — Order Flow + Setup Raquel + Morning Call

**Data:** 14 de junho de 2026  
**Status:** ✅ COMPLETO E DOCUMENTADO  
**Objetivo:** Pipeline completo de análise de Order Flow usando Profit Pro

---

## 📋 ÍNDICE

1. [Visão Geral](#visão-geral)
2. [Arquivos do Projeto](#arquivos-do-projeto)
3. [Passo a Passo Completo](#passo-a-passo-completo)
4. [Integração com Morning Call](#integração-com-morning-call)
5. [Exemplos de Saída](#exemplos-de-saída)

---

## 👁️ VISÃO GERAL

### O Problema
Você quer análise **profissional e quantitativa** baseada em:
- ✅ Order Flow (quem está comprando/vendendo)
- ✅ Poder de ponta (quem está puxando para cima/baixo)
- ✅ Setup técnico específico (SMA 20, 45, 200)
- ✅ Cenários dinâmicos em 2 timeframes (5min + diário)

### A Solução
Pipeline completo usando **Profit Pro** (que você JÁ paga):

```
┌─────────────────────────────────────────────────┐
│  1. PROFIT PRO (seu terminal de trading)        │
│  • Monitora Order Flow em tempo real (NTSL)     │
│  • Exporta CSV com dados de cada barra          │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│  2. PYTHON — profit_flow_analyzer.py            │
│  • Lê CSV do Profit Pro                         │
│  • Calcula fluxo de ordens                      │
│  • Identifica ponta compradora/vendedora        │
│  • Detecta mudanças e alertas                   │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│  3. PYTHON — setup_raquel_analyzer.py           │
│  • Calcula SMA 20, 45, 200                      │
│  • Analisa 2 timeframes (5min + diário)         │
│  • Cria 5 cenários dinâmicos                    │
│  • Integra dados de fluxo                       │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│  4. MORNING CALL                                │
│  • Texto baseado em dados reais                 │
│  • Order Flow + Setup técnico + Cenários        │
│  • Zero opinião, só fatos quantitativos         │
└─────────────────────────────────────────────────┘
```

---

## 📁 ARQUIVOS DO PROJETO

### 📖 Documentação
- **`GUIA-NTSL-ORDER-FLOW.md`** ← Como programar no Profit
- **`PROFIT-PRO-INTEGRATION.md`** ← Este arquivo
- **`DATA-DRIVEN-MORNING-CALL.md`** ← Morning Call com dados
- **`setup_raquel_analyzer.py`** ← Seu setup técnico

### 🐍 Scripts Python
- **`profit_flow_analyzer.py`** ← Processa Order Flow
- **`setup_raquel_analyzer.py`** ← Análise técnica 2 timeframes
- **`technical_analyzer.py`** ← Indicadores profissionais
- **`brapi_explorer.py`** ← Descobre endpoints BRAPI

### 📊 Dados
- `output/profit_export.csv` ← Dados exportados do Profit Pro
- `output/profit_flow_analysis.json` ← Resultado da análise

---

## 🚀 PASSO A PASSO COMPLETO

### FASE 1: CONFIGURAR PROFIT PRO (5 min)

#### 1.1 Abrir Editor de Estratégias
- Clique em **Ferramentas → Editor de Estratégias** (ou Ctrl+E)
- Crie novo arquivo: **File → New → Strategy**

#### 1.2 Copiar o Script NTSL
Copie o código do `GUIA-NTSL-ORDER-FLOW.md` e cole no editor

#### 1.3 Rodar durante a bolsa
- Clique em **Executar** (Play)
- Script vai monitorar Order Flow em tempo real
- Gera alertas quando há mudanças significativas

#### 1.4 Exportar dados
- **Ferramentas → Exportar Dados**
- Selecione período (ex: últimas 24h)
- Campos: Data, Hora, Abertura, Máxima, Mínima, Fechamento, Volume
- Salve em: `C:\Users\raque\9Pilla-Sistema\squads\shorts-maestro\output\profit_export.csv`

---

### FASE 2: ANALISAR ORDER FLOW (2 min)

```bash
cd C:\Users\raque\9Pilla-Sistema\squads\shorts-maestro
python profit_flow_analyzer.py
```

**Saída esperada:**
```
🔥 PROFIT PRO — ORDER FLOW ANALYSIS
════════════════════════════════════════════

🎯 CENÁRIO BASEADO EM ORDER FLOW
════════════════════════════════════════════

🔴 PONTA COMPRADORA (67.3%)
Força: FORTE
Poder de compra: 67%

Análise:
• Total de compras: 15.420 contratos
• Total de vendas: 7.540 contratos
• Saldo: 7.880 contratos
• Proporção: 67.3% compras vs 32.7% vendas

Maior ordem:
• Compra máxima: 850 contratos
• Venda máxima: 620 contratos

════════════════════════════════════════════

🚨 MUDANÇAS DETECTADAS:
...
```

---

### FASE 3: ANÁLISE TÉCNICA + CENÁRIOS (3 min)

```bash
python setup_raquel_analyzer.py
```

**Saída esperada:**
```
🎯 SETUP RAQUEL — PETR4
═══════════════════════════════════════════

📊 TIMEFRAME DIÁRIO (Tendência)
Preço: R$ 41,18 (-1,39%)

Médias Móveis:
  SMA 20: R$ 41,45 → ABAIXO (-0,65%)
  SMA 45: R$ 40,89 → ACIMA (+0,71%)
  SMA 200: R$ 40,23 → ACIMA (+2,36%)

🔄 Tendência: 🔻 BAIXA FORTE

...

🎯 CENÁRIOS DINÂMICOS
════════════════════════════════════════════

⚠️ CENÁRIO DIVERGÊNCIA (CAUTELA)
• Daily em ALTA (tendência de médio prazo)
• Mas 5min em BAIXA (pullback intraday)
• Sinal: ESPERAR VOLTA DA SMA20
...
```

---

### FASE 4: GERAR MORNING CALL (5 min)

Agora você tem:
- ✅ Order Flow data (quem está no controle)
- ✅ Setup técnico (médias, tendências)
- ✅ Cenários dinâmicos (o que fazer)

Integrar tudo no **Writer Agent** para gerar Morning Call:

```python
# Exemplo de texto gerado COM dados:

"PETR4 em R$ 41,18, queda de 1,39%.
Ponta compradora controla com 67% do volume.
Tecnicamente, preço opera abaixo da SMA 20 (R$ 41,45) 
mas acima de SMA 200 (R$ 40,23), sinalizando 
resistência de longo prazo. 
RSI em 35 indica sobrevenda.
Próxima resistência em R$ 42,50, suporte em R$ 39,80.
Cenário: se SMA 20 voltar a subir com volume, 
possível reversão para cima."
```

---

## 🔄 INTEGRAÇÃO COM MORNING CALL

### Modificar: `agents/writer.py`

```python
from profit_flow_analyzer import ProfitFlowAnalyzer
from setup_raquel_analyzer import SetupRaquelAnalyzer

class WriterAgent:
    def generate_script(self, symbol="PETR4", video_format="shorts"):
        """Gera script com Order Flow + Setup Técnico"""
        
        # 1. Analisar Order Flow
        flow_analyzer = ProfitFlowAnalyzer(
            csv_file="output/profit_export.csv"
        )
        flow_analysis = flow_analyzer.analyze_order_flow()
        flow_ponta = flow_analyzer.identify_ponta(flow_analysis)
        
        # 2. Analisar Setup Técnico
        tech_analyzer = SetupRaquelAnalyzer(symbol)
        tech_analyzer.fetch_intraday_data()
        tech_analyzer.fetch_daily_data()
        analysis_5min = tech_analyzer.analyze_timeframe(
            tech_analyzer.prices_5min, "5MIN"
        )
        analysis_daily = tech_analyzer.analyze_timeframe(
            tech_analyzer.prices_daily, "DAILY"
        )
        
        # 3. Construir contexto
        context = f"""
        Order Flow: {flow_ponta['ponta_controle']}
        Setup 5min: {analysis_5min['trend']}
        Setup Daily: {analysis_daily['trend']}
        Cenários: {...}
        """
        
        # 4. Gerar texto com Claude
        prompt = f"""
        Baseado APENAS em dados quantitativos:
        {context}
        
        Gere um parágrafo de 60-90 segundos para Morning Call.
        Cite preço, Order Flow, médias móveis, tendência.
        ZERO opinião — apenas fatos.
        """
        
        return self.claude_api.messages.create(
            model=self.model,
            system=prompt,
            messages=[...]
        )
```

---

## 📊 EXEMPLOS DE SAÍDA

### Exemplo 1: Ponta Compradora Dominante

```
🔴 PONTA COMPRADORA (72% do volume)
Força: FORTE
Setup: ALTA em 5min e Daily
Cenário: OTIMISTA (COMPRA)

Morning Call: "PETR4 com forte presença de compradores 
(72% do volume). Ponta compradora controla fluxo. 
Tecnicamente em alta nos dois timeframes com SMA 20 > SMA 45 > SMA 200. 
Próxima resistência em R$ 42,50. Entrada de compra com 
stop abaixo da SMA 45."
```

### Exemplo 2: Divergência (Daily Alta, Intraday Baixa)

```
⚠️ DIVERGÊNCIA
Daily: ALTA (SMA 20 > SMA 45 > SMA 200)
5min: BAIXA (pullback)
Fluxo: Vendedora tentando reverter

Morning Call: "PETR4 em consolidação. Daily em alta mas 
5min pullback. Fluxo mostra tentativa de reversão vendedora. 
Vigilância: se 5min quebrar SMA 45 para baixo com volume, 
confirma reversão."
```

---

## 🔐 PRÓXIMAS ETAPAS

1. ✅ Copiar script NTSL e rodar no Profit
2. ✅ Exportar CSV após a bolsa
3. ✅ Rodar `profit_flow_analyzer.py`
4. ✅ Rodar `setup_raquel_analyzer.py`
5. ✅ Integrar com Writer Agent
6. ✅ Gerar Morning Call com dados reais
7. ✅ Enviar para Telegram para aprovação

---

## 📝 CHECKLIST

- [ ] Script NTSL criado no Profit Pro
- [ ] CSV exportado de profit_export.csv
- [ ] profit_flow_analyzer.py rodou com sucesso
- [ ] setup_raquel_analyzer.py rodou com sucesso
- [ ] Writer Agent integrado
- [ ] Morning Call gerado com dados
- [ ] Morning Call aprovado no Telegram
- [ ] Vídeo publicado em YouTube/TikTok/IG

---

## 🚀 RESULTADO FINAL

Uma Morning Call que é:
✅ **Quantitativa** — baseada em dados reais de 5+ anos
✅ **Técnica** — seu setup profissional (SMA 20/45/200)
✅ **Profunda** — Order Flow + Cenários dinâmicos
✅ **Autorizada** — você como especialista
✅ **Educativa** — sem especulação, só fatos

---

## 📚 REFERÊNCIAS

- `GUIA-NTSL-ORDER-FLOW.md` — Script NTSL para Profit
- `profit_flow_analyzer.py` — Processamento de dados
- `setup_raquel_analyzer.py` — Análise técnica
- `DATA-DRIVEN-MORNING-CALL.md` — Integração com Morning Call

---

**Status:** ✅ Pronto para usar!  
**Próximo:** Você implementa e a gente revoluciona a 9Pilla! 🚀
