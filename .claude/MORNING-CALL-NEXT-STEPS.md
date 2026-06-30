# 🚀 PRÓXIMOS PASSOS - Morning Call 9Pilla

**Status:** Sistema de orquestração implementado e testado ✅  
**Data:** 24 de junho de 2026  
**Hora:** 09h09 passada (Morning Call gerado, aguardando aprovação)

---

## 📋 O Que Foi Feito

✅ **Arquitetura completa**
- Config centralizado (9pilla-orchestrator.yml)
- 5 Agentes + 5 Skills implementados
- Morning Call 24/06/2026 gerado com sucesso

✅ **Validações**
- Compliance CVM (Léa aprovada)
- Voice DNA de Raquel validado
- Sem palavras banidas
- Disclaimer presente

✅ **Documentação**
- MORNING-CALL-APPROVAL-WORKFLOW.md (fluxo completo)
- Script send-telegram-morning-call.js (pronto para usar)
- Squad.yaml com orquestração

---

## 🎯 AÇÃO 1: Hoje (24/06) - Manual

Como não conseguimos automação de Telegram ainda, faça **manualmente**:

```
1. Pegue o Morning Call:
   /home/user/OpenSquad_9Pilla/content/morning-call/2026-06-24.md

2. Copie o conteúdo completo

3. No seu Telegram:
   - Abra o bot @morning_call_9pilla_bot
   - Cole o Morning Call
   - Revise (dados, tom, erros)
   
4. Se OK → Aprove com 👍 ou "OK"

5. Copie novamente o Morning Call

6. Grupo Turma 9Pilla:
   - Cole a mensagem
   - Publique

7. Instagram (opcional):
   - Use Canva + HeyGen + CapCut
```

**Timing:** Agora mesmo, antes de 10h (melhor janela é 09h-11h)

---

## 🎯 AÇÃO 2: Amanhã (25/06) - Configurar Make.com

Para **automático de verdade** a partir de amanhã:

### **Pré-requisitos:**

1. **Email:** ✅ raquel.handb@gmail.com
2. **Bot Token:** ✅ 8820497175:AAGiJq3Xg9V_72RKyhqlNPPJKKK4uRho6Hk
3. **Chat ID Raquel:** ✅ 7686120986
4. **ID/Username Grupo Turma 9Pilla:** ❓ FALTA

### **Como obter o ID do grupo:**

**Forma 1 (Simples):**
```
1. Abra Telegram
2. Clique no grupo "Turma 9Pilla"
3. Topo: clique no nome
4. Procure por @turma9pilla (ou similar)
```

**Forma 2 (Segura):**
```
1. @userinfobot no Telegram
2. /start
3. Adicione ao grupo Turma 9Pilla
4. Ele mostra o ID
```

---

## 🔧 AÇÃO 3: Setup no Make.com (25/06)

Após obter o ID do grupo, siga este **passo a passo**:

### **1. Criar conta Make.com**
```
https://make.com
Email: raquel.handb@gmail.com
Sign up → verificar email
```

### **2. Criar novo Scenario**
```
New Scenario → Telegram (módulo)
```

### **3. Configurar Trigger**

**Module 1: Watch File**
```
- Tipo: File Watcher
- Caminho: /home/user/OpenSquad_9Pilla/content/morning-call/
- Padrão: *.md
- Trigger: Quando novo arquivo .md é criado
```

### **4. Configurar Ação 1: Enviar ao Telegram Raquel**

**Module 2: Telegram Bot**
```
- Action: Send Message
- Bot Token: 8820497175:AAGiJq3Xg9V_72RKyhqlNPPJKKK4uRho6Hk
- Chat ID: 7686120986
- Message: {conteúdo do arquivo .md}
- Parse Mode: Markdown
```

### **5. Configurar Ação 2: Aguardar Aprovação**

**Module 3: Telegram Bot**
```
- Action: Watch Messages
- Bot Token: mesmo
- Chat ID: 7686120986
- Aguardar: Reação 👍 ou mensagem "OK"
```

### **6. Configurar Ação 3: Disparar às 09h09**

**Module 4: Schedule**
```
- Tipo: Cron
- Horário: 9:09 AM
- Timezone: America/Sao_Paulo (UTC-3)
- Frequência: Seg-Sex
```

### **7. Configurar Ação 5: Enviar para Grupo Turma 9Pilla**

**Module 5: Z-API (WhatsApp)**
```
- API Key: (você terá que gerar em z-api.io)
- Instance ID: (seu ID Z-API)
- Send to: ID do Grupo Turma 9Pilla
- Message: Morning Call aprovado
```

**OU (Mais simples)**

**Module 5 (Alternativo): Telegram para Grupo**
```
- Action: Send Message to Group
- Bot Token: mesmo
- Chat ID: ID do Grupo Turma 9Pilla
- Message: {Morning Call}
```

---

## 📊 Fluxo Automático (Após Setup)

```
MADRUGADA (01h-06h):
  Orquestrador gera Morning Call
  → Arquivo salvo: content/morning-call/YYYY-MM-DD.md

MANHÃ (~06h):
  Make.com detecta novo arquivo
  → Envia ao Telegram Raquel
  → Aguarda reação 👍

RAQUEL APROVA:
  Clica 👍 no Telegram
  → Make.com detecta
  → Agenda envio para 09h09

09h09 EXATO:
  Make.com dispara
  → WhatsApp Turma 9Pilla recebe Morning Call
  → Instagram publica (se HeyGen integrado)
```

---

## ✅ Checklist Final

**HOJE (24/06):**
- [ ] Copiar Morning Call
- [ ] Publicar manualmente no Telegram Raquel
- [ ] Publicar no grupo Turma 9Pilla
- [ ] Verificar se chegou certo

**AMANHÃ (25/06):**
- [ ] Obter ID do grupo Turma 9Pilla
- [ ] Criar conta Make.com (raquel.handb@gmail.com)
- [ ] Configurar Scenario de automação
- [ ] Testar com Morning Call 25/06

**DIA 26/06 EM DIANTE:**
- [ ] Rodar automático (Telegram → Aprovação → 09h09 → Grupo)
- [ ] Verificar logs diariamente
- [ ] Ajustar se necessário

---

## 🆘 Se Algo Não Funcionar

**Make.com não detecta arquivo?**
- Verifique se o caminho está correto
- Reinicie o Scenario

**Telegram não recebe mensagem?**
- Verifique Bot Token (copiar exato)
- Verifique Chat ID (deve ser número)

**Grupo não recebe?**
- Verifique ID do grupo (com @)
- Testeviar enviar mensagem manual antes

**Z-API não funciona?**
- Criar conta em z-api.io
- Gerar API Key
- Testar envio manual primeiro

---

## 📞 Suporte

Qualquer dúvida:
1. Verificar `.claude/MORNING-CALL-APPROVAL-WORKFLOW.md`
2. Testar manualmente (copy/paste)
3. Comparar com este documento

---

**Objetivo:** Sistema totalmente automático seg-sex 09h09 ✨

**Status:** Pronto para MVP (manual) + Configuração Make.com (automático)

**Próxima milestone:** 25/06 com Make.com rodando
