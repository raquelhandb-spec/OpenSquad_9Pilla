# 🚀 PLANO DE INFRAESTRUTURA — PRÓXIMO MÊS (JUNHO 2026)

**Data:** 13 de junho de 2026 (sábado)  
**Objetivo:** Operacionalizar Morning Call automático com qualidade profissional  
**Status:** 🟢 EM EXECUÇÃO

---

## 📋 CHECKLIST SEMANAL

### SEMANA 1 (13-19 de junho)
- [x] Morning Call histórico de 12/06 ✅
- [x] Abertura épica com história real ✅
- [x] Formatação WhatsApp profissional ✅
- [ ] Setup automação Windows Task Scheduler (você faz)
- [ ] ExpectationTracker diário (revisar ontem vs hoje)
- [ ] Approval Bot escutando Telegram

### SEMANA 2-4 (20-30 de junho)
- [ ] Rodar Morning Call automático 5x por semana (seg-sex)
- [ ] Monitorar qualidade dos textos
- [ ] Ajustar análises baseado em feedback
- [ ] Acumular histórico de decisões (data/approvals/)
- [ ] Preparar primeiro Shorts (HeyGen) com Morning Call aprovado

---

## 🎯 STACK ATUAL

| Componente | Status | Local | Custo |
|-----------|--------|-------|-------|
| **Morning Call (texto)** | ✅ Pronto | Windows local | ~US$ 0,02/dia |
| **Approval Bot** | ✅ Pronto | Windows local | Free |
| **ExpectationTracker** | ⚠️ Manual | Linux remoto | Free |
| **Claude API** | ✅ Pronto | API Anthropic | ~US$ 0,02/dia |
| **Brapi** | ⚠️ Bloqueado | servidor remoto | Pago |
| **Telegram Bot** | ✅ Pronto | Windows local | Free |

---

## ⚙️ SETUP: WINDOWS TASK SCHEDULER (VOCÊ FAZ AGORA!)

### Passo 1: Abra Task Scheduler
```
Windows + R → taskschd.msc → Enter
```

### Passo 2: Criar Tarefa Básica
No painel esquerdo, clique "Criar Tarefa Básica"

### Passo 3: Informações Gerais
```
Nome: Morning Call 9Pilla
Descrição: Gera Morning Call automáticamente todos os dias
Executar com privilégios mais elevados: ☑ SIM
```

### Passo 4: Gatilho (Trigger)
Clique "Novo..." > Diariamente
```
Hora: 09:09
Recorrência: Todos os dias
```

### Passo 5: Ação
Clique "Novo..."
```
Programa: C:\Users\raque\AppData\Local\Python\pythoncore-3.14-64\python.exe
  (ou simplesmente: python.exe)

Argumentos: C:\Users\raque\9Pilla-Sistema\squads\shorts-maestro\morning_call_scheduler.py --run

Iniciar em: C:\Users\raque\9Pilla-Sistema\squads\shorts-maestro\
```

### Passo 6: Condições
```
☑ Executar apenas quando o usuário estiver conectado
☑ Se a tarefa não terminar em 24 horas, forçar parada
```

### Passo 7: Configurações
```
☑ Permitir na demanda
☑ Mostrar mensagem quando a tarefa é iniciada
```

### Passo 8: OK!

**Pronto!** Task vai rodar todo dia às 09:09. Logs em:
```
C:\Users\raque\9Pilla-Sistema\squads\shorts-maestro\logs\morning_call_scheduler.log
```

---

## 📊 EXPECTATION TRACKER — REVISAR DIÁRIO

Você precisa executar MANUALMENTE (por enquanto):

```bash
python morning_call.py
```

Isso vai:
1. Ler expectativa de ONTEM (data/expectations/2026-06-12.json)
2. Comparar com dados REAIS de hoje
3. Gerar bloco [CONFERE?]
4. Salvar nova expectativa para amanhã

Arquivo de revisão fica em: `data/expectations/2026-06-13.json`

---

## 💰 ORÇAMENTO ESTIMADO (JUNHO 2026)

| Item | Frequência | Custo Unit. | Subtotal |
|------|-----------|------------|----------|
| Morning Call (Claude) | 20 dias | US$ 0,02 | US$ 0,40 |
| Approval Bot | 20 dias | Free | US$ 0,00 |
| ExpectationTracker | 20 dias | US$ 0,01 | US$ 0,20 |
| Brapi API | 20 dias | Pago* | ~US$ 2,00 |
| **TOTAL JUNHO** | — | — | **~US$ 2,60** |

*Brapi precisa de plan pago para uso heavy (histórico, múltiplos tickers)

---

## 🎬 PRÓXIMO MARCO: PRIMEIRO SHORTS (HeyGen)

Quando: Próxima semana (17-19 de junho)

**Plano:**
1. Escolher 1 Morning Call aprovado (que ficou ÉPICO)
2. Mandar para HeyGen (Avatar, ElevenLabs, subtítulos)
3. Raquel aprova vídeo
4. Publicar no YouTube Shorts + Instagram Reels + TikTok
5. Notificar Turma 9Pilla no WhatsApp

**Custo:** ~US$ 0,60 (HeyGen + ElevenLabs)
**ROI:** 1 vídeo pode gerar 100+ leads para 9Pilla

---

## 📈 MÉTRICAS PARA ACOMPANHAR

- **Diários:**
  - Morning Call gerado? ✅/❌
  - Aprovação no Telegram? ✅/❌
  - Tempo de redação (< 15 min?)
  - Reações no WhatsApp (👍/💬)

- **Semanais:**
  - Qualidade de análises (vs histórico)
  - Taxa de aprovação (% aprovados vs rejeitados)
  - Lucros operacionais (como 12/06 com R$ 466)
  - Aprendizados capturados

- **Mensais:**
  - Total gasto em APIs
  - Total gerado em leads
  - Vídeos Shorts publicados
  - Crescimento de followers

---

## 🔐 SEGURANÇA & BACKUPS

**Credenciais (Protegidas):**
- `.env` com BRAPI_API_KEY, ANTHROPIC_API_KEY, TELEGRAM_BOT_TOKEN
- Salvo em Windows, NÃO no Git

**Dados (Versionados):**
- `data/morning_calls/*.txt` — histórico completo
- `data/expectations/*.json` — diário de análises
- `data/approvals/*.json` — decisões de aprovação

**GitHub:**
- Todo dia após sucesso, fazer `git pull` + `git push`
- Manter histórico versionado (auditoria)

---

## 📞 TROUBLESHOOTING COMUM

**Problem:** Task Scheduler não roda
- Solução: Verifique "Histórico" da tarefa em Task Scheduler
- Logs: `logs/morning_call_scheduler.log`

**Problem:** Brapi retorna 403
- Solução: Remota (servidor bloqueado). Rodar na Windows onde há acesso
- Contorno: approval_bot.py roda normal

**Problem:** Morning Call genérico (sem voz Raquel)
- Solução: Verificar RAQUEL-VOICE-TEMPLATE em writer.py
- Ajuste: Chamar MarketAnalystAgent com mais contexto

**Problem:** Approval Bot não recebe cliques
- Solução: Verificar que approval_bot.py está RODANDO (outra janela CMD)
- Teste: `python approval_bot.py --send-test`

---

## 🚀 PRÓXIMAS 48H

- [ ] Setup Windows Task Scheduler (09:09)
- [ ] Teste da automação: `python morning_call_scheduler.py --run`
- [ ] Verificar logs: `logs/morning_call_scheduler.log`
- [ ] ExpectationTracker de 13/06: `python morning_call.py`
- [ ] Git push com tudo pronto

**Goal:** Na segunda 14/06, Morning Call sai 100% automático às 09:09! 🎯

---

## 📚 REFERÊNCIA RÁPIDA

```bash
# Morning Call automático
python morning_call_scheduler.py --run

# Rodar agora (não esperar 09:09)
python morning_call_scheduler.py --run

# Revisar expectativas + gerar MC
python morning_call.py

# Approval Bot escutando
python approval_bot.py

# Coletar dados epicos
python data_collector_epic.py

# Ver logs
type logs/morning_call_scheduler.log  # Windows
tail -f logs/morning_call_scheduler.log  # Mac/Linux
```

---

**Status:** 🚀 PRONTO PARA PRÓXIMO MÊS ÉPICO!
**Próxima Review:** 20 de junho (pós-primeira semana)
