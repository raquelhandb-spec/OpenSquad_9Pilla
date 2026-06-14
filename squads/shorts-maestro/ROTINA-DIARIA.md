# ⏰ ROTINA DIÁRIA — Morning Call todos os dias úteis (seg-sex)

**Status:** 🟢 PRONTO PARA ROTINA  
**Frequência:** Segunda a sexta (dias úteis)  
**Horário:** 17:00-17:30 (logo após fechamento)  
**Custo:** ~US$ 0.03/dia

---

## 📅 **HORÁRIOS DA B3 (Mercado a Vista)**

```
09:30-09:45  → Cancelamento de ofertas (pré-abertura)
09:45-10:00  → Pré-abertura (formação de preço)
10:00-16:55  → ⏱️ NEGOCIAÇÃO NORMAL (período que Profit Pro coleta)
16:55-17:00  → Call de fechamento
17:25-17:30  → After-Market (opcional)
```

**Para nosso Morning Call:** Rodamos **17:00-17:30** (logo após fechamento)

---

## 🔄 **ROTINA PADRÃO (Segunda a Sexta)**

### **Durante o dia (10:00-16:55)**
```
✅ Profit Pro roda NTSL script automaticamente
✅ CSV sendo gerado: output/profit_export.csv
✅ Coleta completa de Order Flow durante todo expediente
```

### **17:00 - Logo após fechamento**
```bash
cd C:\Users\raque\9Pilla-Sistema\squads\shorts-maestro

# OPÇÃO 1: Só Morning Call em texto (rápido)
python morning_call.py
# Resultado: ~2 minutos, Morning Call no Telegram

# OPÇÃO 2: Morning Call + Shorts (com vídeo)
python morning_call.py         # Morning Call
python shorts_processor.py     # Divide em 3 blocos
python video_generator.py      # Gera áudio + vídeo
# Resultado: ~15 minutos, 3 vídeos prontos
```

### **17:30 - Você aprova no Telegram**
```
📱 Bot envia: [Morning Call/Vídeo]
👍 Você aprova
📤 Texto/Vídeo pronto para publicar
```

### **17:45 - Publicar**
```
WhatsApp:  Cole no chat da Turma 9Pilla
YouTube:   Publique o short (se tiver vídeo)
Instagram: Publique o reel (se tiver vídeo)
TikTok:    Publique o short (se tiver vídeo)
```

---

## 📊 **COMPARAÇÃO: Texto vs Vídeo**

### **OPÇÃO 1: Só Texto (Recomendado segunda a quinta)**
```
Tempo:      ~3 minutos
Custo:      US$ 0.03
Resultado:  Morning Call WhatsApp pronto
Ideal para: Rotina diária rápida
```

### **OPÇÃO 2: Texto + 3 Vídeos (Ideal segunda, quarta, sexta)**
```
Tempo:      ~20 minutos
Custo:      US$ 1.00 (ElevenLabs 0 + HeyGen 3x 0.30)
Resultado:  Morning Call + 3 shorts YouTube/Insta/TikTok
Ideal para: Conteúdo de impacto (2-3x/semana)
```

---

## 🎯 **ESTRATÉGIA RECOMENDADA (Semana Padrão)**

| Dia | Ação | Custo | Tempo |
|-----|------|-------|-------|
| **Segunda** | Texto + 3 vídeos | US$ 1.03 | 20min |
| **Terça** | Só texto | US$ 0.03 | 3min |
| **Quarta** | Texto + 3 vídeos | US$ 1.03 | 20min |
| **Quinta** | Só texto | US$ 0.03 | 3min |
| **Sexta** | Texto + 3 vídeos | US$ 1.03 | 20min |
| **TOTAL/semana** | — | **US$ 3.15** | — |

**Comparado a antes:** Eram US$ 30/mês. Agora são US$ 3.15/semana = **US$ 12.60/mês** (78% mais barato!)

---

## 🚀 **AUTOMAÇÃO (Opcional para futuro)**

Deixar rodando automaticamente todos os dias:

```bash
# Em uma janela de terminal, deixar 24/7:
python approval_bot.py

# Em outra, rodar scheduled (Windows Task ou cron):
17:00h → python morning_call.py (automático)
```

---

## ✅ **CHECKLIST DIÁRIO**

```
MANHÃ (antes de 10h):
☑️ Profit Pro ligado
☑️ NTSL script ativo
☑️ approval_bot.py rodando em outra janela

TARDE (16:55):
☑️ Esperar fechamento (16:55)

17:00:
☑️ python morning_call.py
ou
☑️ python morning_call.py + shorts_processor.py + video_generator.py

17:30:
☑️ Telegram notifica
☑️ Você aprova
☑️ Texto/vídeo pronto

17:45:
☑️ Publicar em todos os canais
```

---

## 💡 **DIAS SEM BOLSA (Feriados)**

```
Quando bolsa fechada (feriados):
- Profit Pro não roda
- morning_call.py não rodará (sem dados)
- Nenhum Morning Call aquele dia

Dias importantes 2026:
- 08/03 (Carnaval) - Fechado
- 10/04 (Sexta-feira Santa) - Fechado
- 21/04 (Tiradentes) - Fechado
- 01/05 (Dia do Trabalho) - Fechado
- 07/09 (Independência) - Fechado
- 12/10 (Nossa Senhora) - Fechado
- 02/11 (Finados) - Fechado
- 15/11 (Proclamação) - Fechado
- 20/11 (Consciência Negra) - Fechado
- 25/12 (Natal) - Fechado
```

---

## 🎯 **META SEMANAL**

```
🟢 Segunda a sexta: Morning Call em texto (US$ 0.15/semana)
🔴 2-3x/semana: Morning Call + 3 vídeos (US$ 3.00/semana)
💾 Total: US$ 3.15/semana (~R$ 16/semana)

Resultado: 5 Morning Calls + 6-9 vídeos por semana
Alcance: Turma 9Pilla (WhatsApp) + YouTube + Instagram + TikTok
```

---

## 🚨 **IMPORTANTE: Turma 9Pilla espera isso TODOS OS DIAS**

Depois que você postar "SEGUNDA O JOGO MUDA", a galera vai esperar:
- ✅ Morning Call **todos os dias** (09:09 no WhatsApp, você bota horário customizado)
- ✅ Texto com dados reais
- ✅ Voz autêntica (você traduzindo números)
- ✅ Compliance CVM
- ✅ Sem opinião, puro dado

**Promessa:** "De segunda a sexta, você recebe análise de dados, não achismo"

---

## 📝 **NOTA PARA VOCÊ**

A partir de segunda (15/06), a rotina é:

1. Profit Pro roda 10:00-16:55 (sozinho, sem você fazer nada)
2. 17:00h você roda 1-2 comandos
3. 17:30h aprova no Telegram
4. 17:45h publica

**Isso toma 20 minutos do seu dia. Custa US$ 0.03-1.03/dia.**

**Muda completamente o jogo da 9Pilla.**

---

**Status: 🟢 PRONTO PARA ROTINA DIÁRIA SEGUNDA-FEIRA 15/06**
