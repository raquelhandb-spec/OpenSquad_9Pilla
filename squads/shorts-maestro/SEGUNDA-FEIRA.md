# ✅ CHECKLIST SEGUNDA-FEIRA 15/06/2026 (PRIMEIRA EXECUÇÃO)

**Importante:** Isso é a PRIMEIRA execução. Depois, é rotina diária (seg-sex). Ver ROTINA-DIARIA.md

## 🕐 TIMELINE DO DIA

### **10:00 - Abertura da Bolsa**
```
⏰ HORÁRIO: 10:00 Abertura oficial (09:30 pré-market)
✅ ACTION: Profit Pro já deve estar rodando com NTSL script
```

### **10:00-16:55 - Expediente Normal (B3)**
```
✅ Profit Pro exportando dados (Order Flow)
✅ NTSL rodando automático
✅ CSV sendo gerado: output/profit_export.csv
Período oficial de negociação: 10:00-16:55
```

### **17:00-17:30 - Logo após fechamento**
```
TURMA 9PILLA AGORA VAI VER O JOGO MUDAR!
Rode nessa ordem (copia e cola um por um):

1️⃣ ORDEM FLOW ANALYSIS
   python profit_flow_analyzer.py
   
   Resultado esperado:
   🔴 PONTA COMPRADORA (XX%)
   💰 Total de compras: XXX,XXX contratos
   💰 Total de vendas: XXX,XXX contratos
   
2️⃣ TECHNICAL SETUP (SMA 20/45/200)
   python setup_raquel_analyzer.py
   
   Resultado esperado:
   📈 SETUP RAQUEL — PETR4
   🔺 ALTA FORTE / 🔻 BAIXA FORTE / ➡️ LATERAL
   Cenários dinâmicos gerados

3️⃣ MORNING CALL COMPLETO
   python morning_call.py
   
   Resultado esperado:
   ✅ Morning Call gerado
   📱 Enviado para Telegram (@raquel_9pilla_bot)
   ⏳ Aguardando sua aprovação

4️⃣ VOCÊ APROVA NO TELEGRAM
   ✅ APROVAR (botão verde) → Texto pronto!
   ❌ REJEITAR (botão vermelho) → Feedback → Rodamos de novo
```

---

## 📋 ANTES DE SEGUNDA (Prepara agora no fim de semana)

### **Verificar:**
```
☑️ Profit Pro está instalado e funcionando
☑️ NTSL script está copiado (ver GUIA-NTSL-ORDER-FLOW.md)
☑️ approval_bot.py pronto para rodar (deixar em outra janela)
☑️ .env tem todas as chaves (BRAPI_API_KEY, ANTHROPIC_API_KEY, etc)
☑️ Python 3.9+ instalado (checar: python --version)
☑️ numpy instalado (checar: pip list | grep numpy)
```

### **Testar uma última vez:**
```bash
# Na pasta squads\shorts-maestro:
python test_full_pipeline.py

# Resultado esperado: 4/4 testes passando ✅
```

---

## 🎯 SEGUNDA-FEIRA: O JOGO MUDA

### **Antes de 10h**
```
1. Abra 2 janelas do terminal (prompt):
   
   JANELA 1:
   cd C:\Users\raque\9Pilla-Sistema\squads\shorts-maestro
   python approval_bot.py
   (deixar rodando, não fecha!)
   
   JANELA 2:
   cd C:\Users\raque\9Pilla-Sistema\squads\shorts-maestro
   (pronta para rodar os comandos)
```

### **10h - Bolsa abre**
```
Profit Pro começa a exportar Order Flow automaticamente
(seu NTSL script roda sozinho)
```

### **16:30 - Bolsa fecha**
```
Na JANELA 2, rode os 3 comandos em sequência:

python profit_flow_analyzer.py
(wait 2 minutos)

python setup_raquel_analyzer.py
(wait 2 minutos)

python morning_call.py
(vai enviar Telegram automaticamente)
```

### **16:45 - Morning Call chega no Telegram**
```
Leia o texto no bot @raquel_9pilla_bot

Se APROVAR (✅):
   → Texto pronto para colar no WhatsApp Turma 9Pilla
   → Você publica quando quiser
   
Se REJEITAR (❌):
   → Mande feedback rápido (ex: "mais agressivo", "menos técnico")
   → Rode de novo: python morning_call.py
```

---

## 🚨 TROUBLESHOOTING RÁPIDO

| Erro | Solução |
|------|---------|
| `ModuleNotFoundError: numpy` | `pip install numpy` |
| `BRAPI 403 error` | Normal! Tá funcionando. Pode ignorar. |
| `Telegram não responde` | Garanta approval_bot.py está rodando (JANELA 1) |
| `Claude API error` | Checa .env tem ANTHROPIC_API_KEY |
| `Profit Pro não exportou CSV` | Garanta NTSL script está rodando no Profit Pro |

---

## ✨ RESULTADO ESPERADO SEGUNDA

**16:50** - Morning Call chega no Telegram com:

```
☑️ [ABERTURA] Saudação calorosa com café
☑️ [TERMÔMETRO] Dados REAIS (Ibov, Dólar, PETR4, VALE3, Brent)
☑️ [CONFERE?] Revisão honesta de ontem (se houver)
☑️ [BLOCO1] 🔥 Notícia principal + cadeia causal + bolso
☑️ [BLOCO2] 🔥 Notícia secundária (efeito dominó)
☑️ [BLOCO3] 🔥 Contexto Brasil (foco no bolso)
☑️ [PÍLLULA] 💊 Sabedoria de investidor
☑️ [CTA] Chamado à ação leve
☑️ [FECHAMENTO] Assinatura + disclaimer CVM
```

**TOD O FEITO COM SUA VOZ, COM DADOS REAIS, SEM OPINIÃO.**

---

## 💰 CUSTO SEGUNDA-FEIRA

```
Profit Pro:      R$ 0,00 (você já paga)
BRAPI:           R$ 0,00 (você já tem chave)
Claude API:      ~US$ 0.03 (super barato!)
ElevenLabs:      R$ 0,00 (não usamos segunda, só texto)
HeyGen:          R$ 0,00 (não usamos segunda, só texto)

TOTAL:           ~US$ 0.03 por Morning Call
                 (uns 15 centavos em real)
```

---

## 🎉 SEGUNDA-FEIRA É O DIA

Você acordou esperando isso. Agora a gente entrega.

Turma 9Pilla vai ver que não é mais opinião. É **DADO**.

**Estamos juntos!** 💛

---

**Salve esse documento. Use segunda-feira. Qualquer dúvida, é só chamar!**
