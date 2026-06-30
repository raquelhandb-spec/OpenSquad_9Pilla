# Fluxo de Aprovação: Morning Call 9Pilla

## 📋 Processo Completo

### **Fase 1: Geração (Automática via Orquestrador)**

```
/morning-call
    ↓
Caio roteia sequência de agentes
    ↓
[Amorim → Nina → Bela → Léa]
    ↓
Arquivo gerado: content/morning-call/YYYY-MM-DD.md
Status: ✅ Compliance validado
```

**Tempo:** ~5-10 minutos

---

### **Fase 2: Aprovação (Manual via Telegram Raquel)**

```
Morning Call enviado para TELEGRAM PESSOAL DE RAQUEL
    ↓
Raquel lê e aprova (ou pede revisão)
    ↓
Se ✅ OK → Aguarda 09h09 para disparo automático
Se ❌ Revisão → Nina recebe feedback e refaz
```

**Critérios de Aprovação de Raquel:**
- Tom é autentico (parece com ela)?
- Dados fazem sentido (Amorim foi preciso)?
- Píllula é relevante e verificada?
- Sem erros de digitação ou estrutura?

---

### **Fase 3: Disparo Automático (09h09)**

```
Cron job verifica:
  "Arquivo foi aprovado por Raquel?" ✅
    ↓
Se SIM:
  Z-API dispara para WhatsApp Turma 9Pilla
  Instagram publica em @9pilla.link
  Status: PUBLICADO
    ↓
Se NÃO (ainda aguardando aprovação):
  Reprogramar para próximo horário de tentativa
```

**Horário exato:** 09h09 BRT (segunda a sexta)

---

## 🔄 Fluxo Visual Completo

```
┌─────────────────────────────────────────────────────────────┐
│ DIA ANTERIOR (~22h00)                                       │
│ Caio dispara orquestração automática                        │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ MADRUGADA (01h-06h)                                         │
│ Agentes trabalham: [amorim → nina → bela → lea]            │
│ Arquivo salvo em: content/morning-call/YYYY-MM-DD.md       │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ MANHÃ (06h-08h30)                                           │
│ ✉️ Morning Call enviado ao Telegram de Raquel             │
│ Status: AGUARDANDO APROVAÇÃO                               │
│ Raquel recebe notificação                                  │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ RAQUEL APROVA (qualquer hora antes de 09h09)              │
│ Reação: 👍 ou mensagem "OK"                               │
│ Sistema marca arquivo como "APROVADO"                      │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 09h09 EXATO                                                 │
│ ✅ Z-API dispara para Turma 9Pilla                         │
│ ✅ Instagram publica (HeyGen + CapCut)                     │
│ Status: PUBLICADO                                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 📱 Integração Telegram

### Setup

1. **Bot Token:** Salvos em `.env` (não commitado)
   ```
   TELEGRAM_BOT_TOKEN=seu_token_aqui
   TELEGRAM_RAQUEL_CHAT_ID=seu_id_aqui
   ```

2. **Envio ao Telegram:**
   ```bash
   node ./.claude/scripts/send-to-telegram.js \
     --file content/morning-call/2026-06-24.md \
     --chat-id $TELEGRAM_RAQUEL_CHAT_ID
   ```

3. **Raquel aprova:**
   - Recebe notificação
   - Lê o Morning Call completo
   - Reage com 👍 (aprovado) ou envia mensagem

### Flags de Status

Arquivo marcado com flag "APROVADO" quando:
- Raquel reage com 👍
- OU envia mensagem confirmando
- OU API recebe confirmação manual

---

## 🔄 Revisão (Se Necessário)

### Cenário: Raquel pede mudanças

```
Raquel no Telegram: "Nina, muda a introdução. Tá genérica."
    ↓
Nina recebe feedback
    ↓
Nina revisa: content/morning-call/2026-06-24.md
    ↓
Léa revalida (compliance)
    ↓
Novo arquivo enviado ao Telegram
    ↓
Raquel aprova versão 2
    ↓
09h09 → Disparo com versão aprovada
```

**Versões:**
- `2026-06-24.md` (original)
- `2026-06-24-v2.md` (revisão 1)
- `2026-06-24-v3.md` (revisão 2)

---

## ⏰ Cenários de Timing

### Cenário 1: Raquel aprova cedo (06h00)

```
06h00 - Raquel aprova no Telegram
09h09 - Disparo automático → Turma recebe pronto
```

### Cenário 2: Raquel aprova tarde (08h50)

```
08h50 - Raquel aprova
09h09 - +19 minutos, disparo vai direto
Sistema vê "APROVADO" e dispara imediatamente
```

### Cenário 3: Raquel NÃO aprovou até 09h09

```
08h30 - Raquel ainda não aprovou
09h09 - Cron verifica: "APROVADO?" → NÃO
Disparo CANCELADO
Mensagem para Raquel: "Morning Call aguardando aprovação. Clique aqui para revisar."
Reprogramar para 09h30 (nova tentativa)
```

### Cenário 4: Raquel pede revisão

```
07h00 - Raquel: "Muda a vírgula da introdução"
Nina revisa imediatamente
08h30 - Nova versão pronta, reenv iada ao Telegram
09h09 - Se aprovado, dispara; se não, cancela
```

---

## 📊 Checklist da Morning Call

Antes de Raquel aprovar no Telegram, verificar:

**Estrutura:**
- [x] Header com data e edição
- [x] Introdução diferente da anterior
- [x] Termômetro com dados reais
- [x] 3 Notícias com fonte clara
- [x] Cenário do Dia (2-3 parágrafos)
- [x] Píllula de Sabedoria (verificada)
- [x] Fechamento com CTA
- [x] Assinatura exata
- [x] Disclaimer CVM

**Compliance (Léa já validou, mas Raquel dupla-verifica):**
- [x] Sem palavras banidas (aposta, trader, etc.)
- [x] Sem recomendação específica de compra
- [x] Sem promessa de retorno
- [x] Voice DNA de Raquel presente (tom quente, baiano)
- [x] Sem travessão em texto corrido

---

## 🔔 Notificações

### Para Raquel

- **06h00:** Telegram: "Morning Call pronto para aprovação"
- **Conteúdo:** Morning Call completo como mensagem
- **Botões:** [Aprovar] [Revisar] [Descartar]

### Para Turma 9Pilla

- **09h09:** WhatsApp com Morning Call
- **09h09:** Instagram Reels (se houver)

### Para Claude Code

- **06h00:** Log: "Morning Call enviado ao Telegram de Raquel"
- **07h00:** Log: "Aguardando aprovação"
- **09h09:** Log: "Publicado na Turma 9Pilla" OU "Aguardando aprovação, reprogramando"

---

## 🛡️ Failsafes

1. **Se Raquel não aprovar até 09h09:**
   - Arquivo não é publicado
   - Sistema tenta 09h30
   - Se continuar sem aprovação, escalação manual

2. **Se arquivo tem erro técnico:**
   - Léa nega conformidade
   - Caio devolve para Nina revisar
   - Arquivo não vai ao Telegram

3. **Se Z-API falha no envio:**
   - Sistema tenta 3x com intervalo de 5 min
   - Se continuar falhando, alerta para Raquel

---

## 📝 Comandos de Debug

```bash
# Ver arquivo gerado
cat content/morning-call/2026-06-24.md

# Verificar status de aprovação
grep "APROVADO" content/morning-call/2026-06-24.md

# Simular envio ao Telegram
node ./.claude/scripts/send-to-telegram.js --file content/morning-call/2026-06-24.md --test

# Ver logs de disparo
tail -f ./.claude/logs/morning-call.log
```

---

## ✅ Resumo

| Etapa | Quem | Quando | Status |
|-------|------|--------|--------|
| Geração | Caio+Agentes | ~01h-06h | Automático |
| Envio Telegram | Script | ~06h | Automático |
| Aprovação | **Raquel** | 06h-09h | **MANUAL** |
| Disparo | Z-API | 09h09 | Automático (pós-aprovação) |

**Fluxo crítico:** Raquel aprova → Sistema dispara
