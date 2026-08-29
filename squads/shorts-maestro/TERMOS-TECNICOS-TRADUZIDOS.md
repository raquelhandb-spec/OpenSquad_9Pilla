# 📚 TERMOS TÉCNICOS TRADUZIDOS — Guia para o Morning Call

**Objetivo:** Explicar cada termo técnico em português claro, transformando em aprendizado

**Regra:** Não diga o termo sem explicar. Exemplo ERRADO vs CERTO:

```
❌ ERRADO: "A SMA20 cruzou acima da SMA45"
✅ CERTO:  "A média de 20 dias SUBIU acima da média de 45 dias. 
            Isso é como comparar: 'como foi meu desempenho na última 3 semanas' 
            vs 'como foi no último mês e meio?'. Quando a curta prazo supera 
            a longa prazo, historicamente sinaliza força de alta."
```

---

## 🎓 **DICIONÁRIO: Termos → Explicação Clara**

### **SMA (Simple Moving Average) = Média Móvel**

**Termo técnico:** "SMA20"  
**Tradução:** "Média de preço dos últimos 20 dias"

**Explicação para Turma 9Pilla:**
```
Imagina que você quer saber se tá ganhando peso. 
Você pesa TODA hora? Não, né? Você vê a tendência.

A "média de 20 dias" é a mesma coisa. 
Pega os preços dos últimos 20 dias e faz uma MÉDIA.
Se essa média está subindo = peso aumentando = ALTA
Se essa média está caindo = peso diminuindo = QUEDA
```

**3 SMAs que você usa:**
- **SMA 20** = "últimos 3 semanas" (curto prazo, reações rápidas)
- **SMA 45** = "último mês e meio" (médio prazo, tendência real)
- **SMA 200** = "últimos 9 meses" (longo prazo, trend estrutural)

**Cruzamento SMA20 > SMA45 > SMA200 = ALTA FORTE**
Explicação: "Curto prazo, médio prazo E longo prazo tudo subindo. Tá tudo alinhado para cima!"

---

### **PONTA COMPRADORA vs VENDEDORA = Quem está no controle?**

**Termo técnico:** "Ponta compradora em controle (78%)"  
**Tradução:** "Mais gente querendo COMPRAR do que VENDER"

**Explicação para Turma 9Pilla:**
```
Imagina um jogo de tira-corda.

PONTA COMPRADORA = Um time puxando (COMPRADORES)
PONTA VENDEDORA = Outro time puxando (VENDEDORES)

Se 78% das forças estão puxando para CIMA (compradores),
o preço tende a SUBIR, né?

Porque tem mais gente querendo comprar do que vender.
É oferta vs demanda. Básico!
```

**No código:** `profit_flow_analyzer.py` calcula isso automaticamente

---

### **ORDER FLOW = Fluxo de Ordens (quem está comprando/vendendo)**

**Termo técnico:** "Order Flow analysis mostra ponta compradora dominante"  
**Tradução:** "Analisando quem está comprando e quem está vendendo"

**Explicação para Turma 9Pilla:**
```
Toda vez que alguém COMPRA uma ação, a ordem vai pro sistema.
Toda vez que alguém VENDE, a ordem também vai.

A gente CONTA essas ordens:
- Quantas foram COMPRA?
- Quantas foram VENDA?
- Quem ganhou?

Se mais ordens de COMPRA = preço sobe (naturalmente)
Se mais ordens de VENDA = preço cai (naturalmente)

É matemática pura, sem opinião.
```

---

### **CONVERGÊNCIA vs DIVERGÊNCIA = Tudo alinhado ou não?**

**Convergência:** Tudo apontando para a mesma direção  
**Divergência:** Sinais conflitantes

**Explicação para Turma 9Pilla:**

**CONVERGÊNCIA (SINAL FORTE):**
```
Daily em ALTA
5min em ALTA
Order Flow em ALTA
Tudo junto = 🔥 SINAL FORTE!

É como todos os especialistas concordando.
Quando isso acontece, o movimento é ROBUSTO.
```

**DIVERGÊNCIA (CUIDADO):**
```
Daily em ALTA
Mas 5min em QUEDA
= ⚠️ Tem algo estranho

É como médicos discordando do diagnóstico.
Precisa investigar mais.
```

---

### **VOLATILIDADE = Ação do preço subindo e descendo**

**Termo técnico:** "Volatilidade aumentou 15%"  
**Tradução:** "O preço tá mexendo mais do que antes"

**Explicação para Turma 9Pilla:**
```
Baixa volatilidade = preço mudando pouco
                   = "está em calmaria"
                   = menos oportunidade mas menos risco

Alta volatilidade = preço mudando muito
                  = "está em pânico"
                  = mais oportunidade mas mais risco
```

---

### **SUPORTE vs RESISTÊNCIA = Pisos e tetos de preço**

**Termo técnico:** "Preço encontrou suporte em 45.50"  
**Tradução:** "Preço desceu até R$ 45.50 e não caiu mais"

**Explicação para Turma 9Pilla:**
```
SUPORTE = Piso histórico (preço não consegue cair abaixo)
          = "Sempre que cai pra aqui, compram muito"
          = Compradores formam uma "parede" de proteção

RESISTÊNCIA = Teto histórico (preço não consegue subir acima)
            = "Sempre que sobe pra aqui, vendem muito"
            = Vendedores formam uma "parede" de proteção

Se quebra o suporte = Tendência MUDA para BAIXA
Se quebra a resistência = Tendência MUDA para ALTA
```

---

### **LUCRO x RISCO = Relação R:R (Risk Reward)**

**Termo técnico:** "Trade com R:R 1:3"  
**Tradução:** "Risco de R$ 1 para ganhar R$ 3"

**Explicação para Turma 9Pilla:**
```
Sempre que você entra numa operação, tem 2 pontos:

STOP LOSS (onde você sai se errar) = RISCO
ALVO (onde você pega o lucro) = RECOMPENSA

Razão R:R = Recompensa / Risco

Se risco é R$ 100 e recompensa é R$ 300:
R:R = 3:1 (bom negócio!)

Se risco é R$ 100 e recompensa é R$ 50:
R:R = 0.5:1 (péssimo negócio!)

Você SÓ faz trade com R:R POSITIVO.
```

---

### **BREAKOUT = Quando quebra o padrão**

**Termo técnico:** "Preço fez breakout acima de 50"  
**Tradução:** "Preço conseguiu ultrapassar uma barreira importante"

**Explicação para Turma 9Pilla:**
```
Breakout = "QUEBRA DO PADRÃO"

Tipo: preço tava oscilando entre 45-50 há 2 meses.
De repente, consegue SAIR dessa faixa e vai para 55.

Isso é um BREAKOUT. 
Geralmente sinaliza nova tendência.
```

---

## 🎬 **EXEMPLO: Morning Call com Tradução**

### ❌ VERSÃO ERRADA (muito técnica):
```
"SMA20 cruzou acima de SMA45. Daily em ALTA FORTE.
Order Flow mostra ponta compradora dominante (78%).
Convergência entre timeframes. Breakout acima de resistência em 50."
```

Ninguém entende isso! 😱

### ✅ VERSÃO CORRETA (explicada):
```
"Turma, vem comigo! A PETR4 está mandando um sinal forte hoje.

Olha só: a média de 20 dias (curto prazo) subiu ACIMA da média de 45 dias 
(médio prazo). Isso é como dizer 'tá acelerado agora'. Tá bom, mas aí a 
gente vê: E a média de 200 dias? Tá subindo também! Tudo junto, entende?
Curto, médio e longo prazo TODOS subindo. Isso é força de verdade!

Aí a gente olha pra quem tá comprando e quem tá vendendo 
(a gente faz essa conta todo dia aqui). E adivinha? 
78% das ordens foram de COMPRA. Significa o seguinte: 
tem mais gente querendo levar a ação pra cima do que pra baixo. 
Quando a demanda vence a oferta, o preço sobe. Matemática pura!

E ainda tem mais: a ação conseguiu SAIR de uma faixa de preço 
que ficava oscilando. Agora tá em terreno novo, pra cima.

Resultado: tudo apontando para CIMA. Tudo alinhado.
Fica o alerta pra aproveitar."
```

Isso SIM faz sentido! 🔥

---

## 📝 **Template para você usar**

Sempre que for mencionar um termo técnico, siga esse padrão:

```
[TERMO TÉCNICO]: [O que é em português simples]

[ANALOGIA ou EXPLICAÇÃO VISUAL]

[IMPACTO PRÁTICO para o bolso do leitor]
```

**Exemplo pronto:**
```
SMA20 cruzou acima de SMA45: Basicamente a ação tá acelerando agora. 
É como quando você tá andando devagar, aí de repente começa a andar mais 
rápido. Isso geralmente antecede movimentos maiores. Fique atento!
```

---

## 🎯 **Checklist para escrever cada Morning Call**

```
☑️ Usei um termo técnico? Expliquei em português?
☑️ Usei uma analogia? (comparação com algo do dia a dia)
☑️ Deixei claro O QUE significa?
☑️ Expliquei POR QUE importa?
☑️ Conectei ao bolso do leitor? ("isso significa pro você...")
☑️ Sem travessão (—)?
☑️ Sem recomendação direta (apenas probabilidade)?
☑️ Sem opinião, só dados?
```

---

**STATUS: 🟢 USE ESSE GUIA PARA TREINAR O WRITER AGENT**

Vamos atualizar o prompt do WriterAgent para SEMPRE traduzir termos técnicos!
