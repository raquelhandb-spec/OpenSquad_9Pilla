# 📊 DATA-DRIVEN MORNING CALL — Análise Técnica + Claude

**Data:** 14 de junho de 2026  
**Objetivo:** Morning Call baseado APENAS em dados técnicos quantitativos  
**Slogan:** "Sem opinião. Só fatos."

---

## 🎯 A REVOLUÇÃO 9PILLA

Antes:
> "Acho que PETR4 vai subir..." ❌ OPINIÃO SEM FUNDAMENTO

Depois:
> "PETR4 acima da SMA 200, RSI em 45, próxima resistência em R$ 42,50, volatilidade em queda" ✅ FATOS QUANTITATIVOS

---

## 🔄 NOVO PIPELINE

```
┌─────────────────────────────────────────────┐
│  1. PROSPECTOR AGENT                        │
│  Busca dados reais do BRAPI (quote + fx)    │
└────────────────────┬────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│  2. TECHNICAL ANALYZER                      │
│  Calcula indicadores com 5+ anos de dados:  │
│  - RSI, MACD, SMA 50/200                    │
│  - Suporte/Resistência                      │
│  - Tendência (Alta/Baixa/Lateral)           │
│  - Volatilidade                             │
└────────────────────┬────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│  3. CLAUDE WRITER AGENT                     │
│  Com contexto técnico, gera Morning Call:   │
│  "PETR4 acima de SMA 200..."                │
│  SEM especulação, SÓ fatos                  │
└────────────────────┬────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│  4. APPROVAL BOT (Telegram)                 │
│  Raquel aprova o texto baseado em dados     │
└────────────────────┬────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│  5. VIDEO GENERATOR                         │
│  HeyGen + ElevenLabs + YouTube/TikTok/IG    │
└─────────────────────────────────────────────┘
```

---

## 📋 PASSO A PASSO PRÁTICO

### 1️⃣ Rodar Technical Analyzer

```bash
python technical_analyzer.py
```

Saída esperada:
```
📊 ANÁLISE TÉCNICA: PETR4
═════════════════════════════════════════
💰 PREÇO
   Atual: R$ 41,18
   Variação: -1,39%

📈 HISTÓRICO (2021-06-14 a 2026-06-14)
   Máxima: R$ 47,50
   Mínima: R$ 35,20
   Amplitude: R$ 12,30

📊 INDICADORES TÉCNICOS
   RSI (14 dias): 35.42 → RSI < 30: Sobrevendido (possível reversão para cima)
   SMA 50: R$ 41,45
   SMA 200: R$ 40,89
   MACD: 0.4521 | Signal: 0.3891 | Histogram: 0.0630
   Volatilidade (3m): 2.85%

🎯 SUPORTE E RESISTÊNCIA
   Resistência 1: R$ 42,50
   Resistência 2: R$ 44,00
   Suporte 1: R$ 39,80
   Suporte 2: R$ 37,50

🔄 TENDÊNCIA: BAIXA

💡 INSIGHTS TÉCNICOS
   • RSI < 30: Sobrevendido
   • Tendência BAIXA
   • Suporte próximo em R$ 39,80
   • Resistência próxima em R$ 42,50
```

### 2️⃣ Passar dados para o Writer Agent

Dentro do Writer, adicionar contexto técnico:

```python
technical_context = {
    "symbol": "PETR4",
    "price": 41.18,
    "rsi": 35.42,
    "trend": "BAIXA",
    "sma_50": 41.45,
    "sma_200": 40.89,
    "resistance_1": 42.50,
    "support_1": 39.80,
    "volatility": 2.85,
    "signal": "Sobrevendido, próxima resistência em R$ 42,50"
}

# Passar ao Claude com prompt técnico
prompt = f"""
Você é especialista em análise técnica de mercado de ações.
Com base APENAS nos dados técnicos abaixo, gere um parágrafo de análise.
Não especule, não opine. Apenas relate os fatos técnicos.

Dados:
{technical_context}

Exemplo de saída esperada:
"PETR4 opera em R$ 41,18, abaixo da SMA 50 (R$ 41,45) mas acima da SMA 200 (R$ 40,89), 
indicando resistência de médio prazo. RSI em 35,42 sinaliza zona de sobrevenda, 
com próxima resistência em R$ 42,50 e suporte em R$ 39,80."
"""
```

---

## 📝 EXEMPLO: NOVO MORNING CALL COM DADOS TÉCNICOS

### BLOCO 1 — TERMÔMETRO

**ANTES (OPINIÃO):**
> "Mercado em queda hoje... acho que pode voltar a subir nos próximos dias..."

**DEPOIS (DADOS):**
> "IBOVESPA em 171.133 pts, queda de -0,21%, operando abaixo da SMA 200 (172.450). 
> RSI em zona neutra (48,5). Próxima resistência em 172.000, suporte em 170.500.
> Dólar em R$ 5,08, queda de -1,26%, volatilidade em 1,2% (em queda)."

---

### BLOCO 2 — ANÁLISE SETORIAL

**ANTES (OPINIÃO):**
> "Petrobras em destaque porque o petróleo está caindo... pode ser uma oportunidade..."

**DEPOIS (DADOS):**
> "PETR4 em R$ 41,18, queda de -1,39%, operando abaixo de ambas as médias móveis 
> (SMA 50: R$ 41,45, SMA 200: R$ 40,89). RSI em 35,42 indica zona de sobrevenda.
> Tecnicamente, próxima resistência em R$ 42,50, suporte em R$ 39,80.
> Correlação com Brent: preço do barril em queda de 2,5%."

---

### BLOCO 3 — SETUP TÉCNICO

**ANTES (OPINIÃO):**
> "PETR4 pode ser uma boa entrada para operações curtas..."

**DEPOIS (DADOS):**
> "PETR4 forma padrão de queda com mínima em R$ 39,50 (suporte-chave).
> MACD em zona negativa (histogram: -0,0854), sinal de baixa.
> Volatilidade em queda (2,85%), indicando possível movimento brusco próximo.
> Níveis técnicos para operadores: entrada em suporte (R$ 39,80), stop acima da resistência (R$ 42,50)."

---

## 🔧 INTEGRAÇÃO NO CODE

### Modificar: `agents/writer.py`

```python
from technical_analyzer import TechnicalAnalyzer

class WriterAgent:
    def generate_script(self, market_data, technical_analysis=None, video_format="shorts"):
        """Gera script com contexto técnico"""
        
        # Se temos análise técnica, usar no contexto
        technical_context = ""
        if technical_analysis:
            tech = technical_analysis
            technical_context = f"""
            Dados Técnicos do Ativo:
            - Preço: R$ {tech['price']['current']:.2f}
            - RSI: {tech['indicators']['rsi_14']}
            - Tendência: {tech['trend']}
            - SMA 50: R$ {tech['indicators']['sma_50']:.2f}
            - SMA 200: R$ {tech['indicators']['sma_200']:.2f}
            - Resistência próxima: R$ {tech['support_resistance']['resistances'][0]:.2f}
            - Suporte próximo: R$ {tech['support_resistance']['supports'][0]:.2f}
            """
        
        prompt = f"""
        Você é Raquel, especialista em educação financeira.
        
        IMPORTANTE: Seu texto deve ser baseado APENAS em dados técnicos e análise quantitativa.
        Nada de opinião especulativa. Apenas fatos numéricos que tragam LUZ ao leitor.
        
        Dados técnicos disponíveis:
        {technical_context}
        
        Gere um parágrafo de 60-90 segundos que:
        1. Cite preço e variação percentual
        2. Mencione RSI e o que significa (sobrecomprado/sobrev endido)
        3. Compare com médias móveis (SMA 50 e 200)
        4. Identifique suporte e resistência próximos
        5. Descreva a tendência observada
        6. NUNCA especule sobre futuro
        
        Exemplo:
        "PETR4 opera em R$ 41,18, queda de 1,39%, abaixo da SMA 50 e 200.
        RSI em 35 indica sobrevenda técnica. Suporte próximo em R$ 39,80,
        resistência em R$ 42,50. Volatilidade em queda, indicando consolidação."
        """
        
        return self.client.messages.create(
            model=self.model,
            max_tokens=500,
            system=prompt,
            messages=[...]
        )
```

---

## 📊 INDICADORES EXPLICADOS

### RSI (Índice de Força Relativa)
- **< 30**: Sobrevenda (preço caiu muito, pode haver reversão para CIMA)
- **30-70**: Zona neutra (sem sinal claro)
- **> 70**: Sobrecompra (preço subiu muito, pode haver reversão para BAIXO)

### SMA (Médias Móveis)
- **SMA 50**: Tendência de médio prazo (50 dias)
- **SMA 200**: Tendência de longo prazo (200 dias)
- Se preço **acima de SMA 200**: Tendência de ALTA
- Se preço **abaixo de SMA 200**: Tendência de BAIXA

### MACD (Convergência/Divergência de Médias Móveis)
- **Histogram positivo**: Sinal de ALTA
- **Histogram negativo**: Sinal de BAIXA
- **Cruzamento**: Mudança de tendência iminente

### Suporte e Resistência
- **Suporte**: Nível onde preço tende a pular para cima (compra se chegar lá)
- **Resistência**: Nível onde preço tende a cair (venda se chegar lá)

---

## ✅ CHECKLIST: IMPLEMENTAÇÃO

- [ ] Testar `technical_analyzer.py` com seus 3 ativos (PETR4, VALE3, IBOV)
- [ ] Validar que dados históricos estão corretos (5+ anos)
- [ ] Modificar Writer Agent para aceitar contexto técnico
- [ ] Teste: Gerar Morning Call com análise técnica completa
- [ ] Validar que NÃO há opinião especulativa
- [ ] Enviar para Raquel aprovar no Telegram
- [ ] Medir impacto: leads se interessam mais por conteúdo com DATA?

---

## 🚀 RESULTADO ESPERADO

**Morning Call com Autoridade:**
- ✅ Baseado em 5+ anos de dados históricos
- ✅ Indicadores técnicos profissionais
- ✅ Sem especulação — só fatos
- ✅ Raquel como especialista, não opinador
- ✅ Conteúdo que educa E impressiona

**Turma 9Pilla pensa:**
> "Caramba, que análise técnica profissional! Raquel sabe o que fala!"

---

## 💬 PRÓXIMOS PASSOS

1. Rodar `technical_analyzer.py` na sua máquina
2. Ver quais indicadores fazem mais sentido para seu público
3. Integrar com Writer Agent
4. Gerar 1º Morning Call baseado em dados
5. Enviar para aprovação no Telegram
6. Medir engajamento

**Você pronto?** 🚀
