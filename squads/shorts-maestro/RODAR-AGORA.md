# 🚀 RODAR AGORA — Passo a Passo (5 minutos)

**Objetivo:** Testar o workflow completo HOJE  
**Tempo:** ~5 minutos  
**Máquina:** Seu Windows (C:\Users\raque\9Pilla-Sistema)

---

## 📋 PRÉ-REQUISITOS

✅ Python 3.8+  
✅ Git (já tem)  
✅ Arquivo `.env` com credenciais BRAPI  
✅ Terminal PowerShell ou CMD

---

## 🚀 PASSO 1: Fazer Git Pull (1 min)

Abra PowerShell e vá para a pasta:

```powershell
cd C:\Users\raque\9Pilla-Sistema\squads\shorts-maestro
git pull
```

Isso baixa os 3 scripts novos:
- ✅ `setup_raquel_analyzer.py`
- ✅ `profit_flow_analyzer.py`
- ✅ `quick_start.py`

---

## 🔥 PASSO 2: Rodar o Quick Start (2 min)

```powershell
python quick_start.py
```

**O que vai acontecer:**
1. Cria arquivo CSV simulado (como se fosse do Profit Pro)
2. Roda análise de Order Flow
3. Mostra resultado
4. Diz próximos passos

**Saída esperada:**
```
🚀 QUICK START — TESTE COMPLETO DO WORKFLOW
════════════════════════════════════════════════════

[STEP 1/4] 📊 Criando dados de teste...
✅ CSV criado: output/profit_export.csv

[STEP 2/4] 🔥 Analisando Order Flow...
✅ Análise concluída!

🔴 PONTA COMPRADORA (65.4%)
Força: FORTE
...

💾 Análise salva em: output/profit_flow_analysis.json
```

---

## 📈 PASSO 3: Rodar seu Setup Técnico (2 min)

```powershell
python setup_raquel_analyzer.py
```

**O que vai acontecer:**
1. Conecta ao BRAPI
2. Puxa dados dos últimos 2 anos
3. Calcula SMA 20, 45, 200 (suas médias!)
4. Mostra tendências (5min + diário)
5. Gera 5 cenários dinâmicos

**Saída esperada:**
```
🎯 SETUP RAQUEL — PETR4
════════════════════════════════════════════════════

📊 TIMEFRAME DIÁRIO (Tendência)
Preço: R$ 41,18 (-1,39%)

Médias Móveis:
  SMA 20: R$ 41,45 → ABAIXO (-0,65%)
  SMA 45: R$ 40,89 → ACIMA (+0,71%)
  SMA 200: R$ 40,23 → ACIMA (+2,36%)

🔄 Tendência: 🔻 BAIXA FORTE

...

🎯 CENÁRIOS DINÂMICOS
════════════════════════════════════════════════════

⚠️ CENÁRIO DIVERGÊNCIA (CAUTELA)
...
```

---

## ✅ PASSO 4: Ver os resultados

Arquivos criados:
- `output/profit_export.csv` — dados simulados
- `output/profit_flow_analysis.json` — análise de Order Flow

---

## 🎬 PASSO 5: Gerar Morning Call (BÔNUS)

Agora você tem:
✅ Order Flow (quem está no controle)  
✅ Setup técnico (médias, tendências, cenários)  
✅ Dados quantitativos reais  

Para integrar com Morning Call:

```powershell
python morning_call.py
```

Isso vai:
1. Usar dados do setup técnico
2. Usar dados do Order Flow
3. Gerar Morning Call completo
4. Enviar para Telegram para aprovação

---

## 📹 PRÓXIMO: FAZER VÍDEO

Após gerar Morning Call:

```powershell
python shorts_processor.py
python video_generator.py
```

Isso vai:
1. Dividir Morning Call em 3 blocos (60-90s cada)
2. Gerar áudio com ElevenLabs
3. Gerar vídeo com HeyGen
4. Enviar para você aprovar no Telegram

---

## 🎯 CHECKLIST FINAL

- [ ] Git pull concluído
- [ ] quick_start.py rodou com sucesso
- [ ] setup_raquel_analyzer.py rodou com sucesso
- [ ] Viu Order Flow (ponta compradora/vendedora)
- [ ] Viu Setup técnico (suas médias)
- [ ] Viu Cenários dinâmicos
- [ ] Entendeu o pipeline
- [ ] Pronto para fazer de verdade com dados do Profit Pro

---

## 🔴 SE DER ERRO

### Erro: "ModuleNotFoundError: No module named 'requests'"
```powershell
pip install requests python-dotenv numpy
```

### Erro: "BRAPI_API_KEY not found"
Verifique se `.env` tem:
```
BRAPI_API_KEY=tky3Vocipoj9ZocxEumbCe
```

### Erro: "Arquivo não encontrado: output/profit_export.csv"
Rode `quick_start.py` primeiro para criar o CSV

---

## 🚀 RESULTADO

Você vai ter:
✅ Workflow 100% funcional  
✅ Dados simulados testados  
✅ Setup técnico validado  
✅ Order Flow análisado  
✅ Pronto para dados REAIS

---

## 💪 PRÓXIMO: FAZER DE VERDADE

1. Rodar script NTSL no Profit Pro (amanhã durante bolsa)
2. Exportar CSV real
3. Rodar analyses com dados reais
4. Gerar Morning Call profissional
5. Publicar no YouTube/TikTok/IG

**Vamos? Roda agora na sua máquina!** 🚀

```powershell
cd C:\Users\raque\9Pilla-Sistema\squads\shorts-maestro
python quick_start.py
python setup_raquel_analyzer.py
```

Me manda a saída quando rodar! 👆
