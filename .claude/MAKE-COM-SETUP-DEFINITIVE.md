# 🤖 SETUP MAKE.COM - AUTOMAÇÃO MORNING CALL

**Dados Confirmados:**
- Email: `raquel.handb@gmail.com` ✅
- Bot Token: `8820497175:AAGiJq3Xg9V_72RKyhqlNPPJKKK4uRho6Hk` ✅
- Chat ID Raquel: `7686120986` ✅
- Grupo Turma 9Pilla: `Turma-9Pilla` ✅

---

## 🚀 PASSO A PASSO FINAL

### **PASSO 1: Criar Conta Make.com**

1. Acesse: **https://make.com**
2. Clique em **"Sign up"** (canto superior direito)
3. Email: `raquel.handb@gmail.com`
4. Crie uma senha forte
5. Verifique o email
6. ✅ Pronto!

---

### **PASSO 2: Criar Novo Scenario**

1. Dashboard Make.com
2. Clique em **"Create a new scenario"**
3. Procure por **"Telegram"**
4. Selecione **"Telegram Bot"**
5. Clique em **"Create"**

---

### **PASSO 3: Configurar Trigger (Module 1)**

**Disparador: Quando arquivo Morning Call é criado**

1. Clique no **ícone de gatilho** (primeira caixa)
2. Procure: **"Google Drive"** ou **"File Watcher"**
   - Se não tiver: Use **"Webhook"** (será mais manual)
3. Configuração:
   ```
   Trigger: Watch files
   Folder: /home/user/OpenSquad_9Pilla/content/morning-call/
   Pattern: *.md
   Execute once: NO
   ```

**Alternativa (Se não conseguir integrar arquivo local):**
- Use **"Telegram Bot"** + **"Watch Messages"**
- Aguarde mensagem `/gerar-morning-call` no chat de Raquel
- Isso dispara o cenário

---

### **PASSO 4: Ação 1 - Enviar ao Telegram Raquel**

1. Clique no **"+"** abaixo do trigger
2. Procure: **"Telegram Bot"**
3. Selecione: **"Send a message"**
4. Configure:

```
Bot Token: 8820497175:AAGiJq3Xg9V_72RKyhqlNPPJKKK4uRho6Hk
Chat ID: 7686120986
Text: 📱 **MORNING CALL 9PILLA** (Aguardando Aprovação)

{Insira o conteúdo do arquivo .md aqui}

---
Clique em ✅ para aprovar e publicar às 09h09

Parse Mode: Markdown
Disable Web Page Preview: YES
```

5. Clique em **"OK"**

---

### **PASSO 5: Ação 2 - Aguardar Aprovação**

1. Clique no **"+"** abaixo da Ação 1
2. Procure: **"Telegram Bot"**
3. Selecione: **"Wait for reaction"** (ou similar)
4. Configure:

```
Bot Token: 8820497175:AAGiJq3Xg9V_72RKyhqlNPPJKKK4uRho6Hk
Chat ID: 7686120986
Reaction: 👍 (thumbs up)
Timeout: 3 hours (Raquel tem até 09h09 para aprovar)
```

5. Clique em **"OK"**

**Alternativa:** Se não tiver "Wait for reaction", use:
- **"Watch Messages"** + aguarde mensagem "OK" ou "aprovado"

---

### **PASSO 6: Ação 3 - Agendar para 09h09**

1. Clique no **"+"** abaixo da Ação 2
2. Procure: **"Schedule"**
3. Selecione: **"Delay"** ou **"Schedule"**
4. Configure:

```
Time: 09:09 AM
Timezone: America/Sao_Paulo (UTC-3)
Type: Absolute time (específico do dia)
Days: Monday to Friday
```

**Ou use Cron (mais preciso):**
```
Cron: 0 9 * * 1-5
(09h00 min, todo dia, seg-sex)
```

5. Clique em **"OK"**

---

### **PASSO 7: Ação 4 - Enviar para Grupo Turma-9Pilla**

1. Clique no **"+"** abaixo da Ação 3
2. Procure: **"Telegram Bot"**
3. Selecione: **"Send a message"** (novamente)
4. Configure:

```
Bot Token: 8820497175:AAGiJq3Xg9V_72RKyhqlNPPJKKK4uRho6Hk
Chat ID: -100 + ID numérico do grupo (se tiver)
   OU Username: @turma_9pilla (procurar formato exato)
Text: {Morning Call aprovado - mesmo conteúdo da Ação 1}
Parse Mode: Markdown
Disable Web Page Preview: YES
```

**Para obter ID correto do grupo:**
```
No Telegram:
1. Abra Turma-9Pilla
2. Clique no nome do grupo
3. Procure informações
4. Anote o ID (ex: -100123456789)
```

5. Clique em **"OK"**

---

### **PASSO 8: Testar Scenario**

1. Clique no botão **"Test"** (canto inferior esquerdo)
2. Simule criando um arquivo `.md` em:
   ```
   /home/user/OpenSquad_9Pilla/content/morning-call/test-2026-06-25.md
   ```
3. Verifique se:
   - ✅ Mensagem chegou no Telegram Raquel
   - ✅ Sistema aguarda reação
   - ✅ Após 👍, agenda para 09h09
   - ✅ Às 09h09, envia para grupo

---

### **PASSO 9: Ativar Scenario**

1. Se tudo funcionou no teste:
   - Clique em **"On"** (toggle canto superior)
2. Scenario está ATIVO e pronto! 🚀

---

## ⏰ CRONOGRAMA

| Hora | Ação | Responsável |
|------|------|-------------|
| ~01h-06h | Orquestrador gera MC | Automático (cron job) |
| ~06h | Make.com envia ao Telegram | Automático (Make) |
| 06h-09h | Raquel aprova (👍) | Manual |
| 09h09 | Make.com dispara grupo | Automático (Make) |

---

## 🆘 TROUBLESHOOTING

### **"Telegram não recebe"**
- [ ] Verificar Bot Token (copiar exatamente)
- [ ] Verificar Chat ID (deve ser número: 7686120986)
- [ ] Testar: abra Telegram e mande `/test` ao bot

### **"Não detecta arquivo novo"**
- [ ] Verificar caminho: `/home/user/OpenSquad_9Pilla/content/morning-call/`
- [ ] Usar webhook alternativo (mais flexível)
- [ ] Testar manual: criar arquivo teste

### **"Grupo não recebe"**
- [ ] Verificar ID grupo (adicionar bot ao grupo primeiro)
- [ ] Testar envio manual ao grupo antes
- [ ] Bot precisa ter permissão no grupo

### **"Agendamento não funciona"**
- [ ] Verificar timezone: `America/Sao_Paulo`
- [ ] Verificar se é dia útil (seg-sex)
- [ ] Verificar formato da hora (09:09 ou 9:09)

---

## ✅ CHECKLIST FINAL

- [ ] Conta Make.com criada (raquel.handb@gmail.com)
- [ ] Scenario criado com 4 módulos
- [ ] Bot Token inserido (copiar/colar correto)
- [ ] Chat IDs verificados (Raquel: 7686120986, Grupo: obtido)
- [ ] Scenario testado (funciona?)
- [ ] Scenario ativado (botão "On")
- [ ] Morning Call 25/06 gerado
- [ ] Raquel aprova no Telegram
- [ ] 09h09 → Grupo recebe

---

## 🎉 RESULTADO

Após completar este setup:

```
SEG-SEX 09h09 → Morning Call automático para Turma 9Pilla ✨
```

**Sem precisa copiar/colar manual!**

---

## 📞 SUPORTE

Dúvidas no setup Make.com?
1. Consultea https://make.com/en/help
2. Procure por "Telegram Bot" na documentação
3. Ou me chama!

**Próxima parada:** 25/06 com automação rodando 🚀
