# 🌍 COLETA DE DADOS ÉPICA — Morning Call 12/06/2026

**Hora:** 03:35 da madrugada (sexta-feira)  
**Objetivo:** Coletar TODOS os dados globais + contexto Trump para gerar o Morning Call mais épico de 2026  
**Tempo estimado:** 5-10 minutos

---

## 📋 O QUE VAI COLETAR

✅ **Brasil (Brapi)**
- PETR4, VALE3, IBOV (índice), USD-BRL, Brent (petróleo)

✅ **Bolsas Globais**
- S&P 500 (SPY)
- VIX (Índice do Medo)
- FTSE 100 (Londres)
- Nikkei 225 (Tóquio)
- Hang Seng (Hong Kong)

✅ **Commodities**
- Ouro (GOLD)
- Prata (SILVER)
- Cobre (COPPER)

✅ **Crypto**
- Bitcoin
- Ethereum

✅ **Contexto Geopolítico**
- Trump + Negociações de Paz
- Impacto esperado no mercado

---

## 🚀 COMO RODAR (Na sua Windows)

### Passo 1: Abra CMD ou PowerShell
```
Windows + R → cmd → Enter
```

### Passo 2: Vá para a pasta do projeto
```cmd
cd C:\caminho\para\OpenSquad_9Pilla\squads\shorts-maestro
```
(Substitua `C:\caminho` pelo seu caminho real)

### Passo 3: Rode o script
```cmd
python data_collector_epic.py
```

**Esperado ver:**
```
======================================================================
🌍 DATA COLLECTOR ÉPICO — 12/06/2026 — 03:35 MADRUGADA
======================================================================

🇧🇷 COLETANDO DADOS BRASIL (Brapi)...
  ✅ PETR4: R$ 47,50 (-1,76%)
  ✅ VALE3: R$ 84,30 (+1,32%)
  ✅ ^BVSP: 176.200 (+0,71%)
  ✅ USD-BRL: R$ 4,96 (+0,40%)
  ✅ Brent: US$ 103,45 (+3,92%)

🌎 COLETANDO BOLSAS GLOBAIS...
  ✅ S&P 500 (SPY): ...
  ✅ VIX (Índice do Medo): ...
  [etc]

💾 SALVANDO DADOS...
✅ ARQUIVO SALVO: C:\...\data\epic_collection\data_epic_20260612_033500.json
```

### Passo 4: Git Push (IMPORTANTE!)
```cmd
git add squads/shorts-maestro/data/epic_collection/
git commit -m "Coleta épica de dados globais para Morning Call 12/06/2026"
git push
```

---

## ⚠️ SE ALGO DER ERRO

**Erro 1: "ModuleNotFoundError: No module named 'requests'"**
```cmd
python -m pip install requests
```

**Erro 2: "Brapi: 403 ou erro de autenticação"**
- Verifique que `BRAPI_API_KEY` está correto em `.env`
- Se não tiver, o script continua mesmo assim (coleta parcial)

**Erro 3: "ConnectionError" ou timeout**
- Sua internet pode estar lenta
- Espere 30s e rode novamente
- Se persistir, pode rodar parcialmente

---

## 📊 O QUE ACONTECE DEPOIS

1. Script coleta dados → salva em `data/epic_collection/data_epic_YYYYMMDD_HHMMSS.json`
2. Você dá Git Push
3. Claudenho lê os dados na máquina remota
4. Claude faz análise PROFUNDA (macro + geo + fluxo)
5. Montamos o Morning Call ÉPICO com tudo integrado
6. Você aprova e publica às 09:09 no WhatsApp

---

## 🎯 TIMELINE

- **03:35** ← Você agora
- **04:00** ← Script finalizou, dados no Git
- **06:00** ← Morning Call ÉPICO pronto para revisão
- **09:09** ← Publica no Turma 9Pilla

---

## 💡 DICAS

- Deixa o script rodar completo (mesmo que vire "⚠️" em algumas fontes)
- Se der erro em uma fonte, outras continuam (resiliente)
- O arquivo JSON vai ficar salvo mesmo que falhe no final
- Qualquer dúvida, você pode verificar a saída e passar para mim

---

**VAMOS LÁ! BORA FAZER O MAIOR MORNING CALL DA NOSSA HISTÓRIA RECENTE! 🚀**
