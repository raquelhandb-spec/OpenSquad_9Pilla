# 🌅 Morning Call Automático via Z-API

## ✅ Status: Configurado e Pronto

Seu Morning Call automático foi configurado com sucesso para executar **seg-sex às 09h09** via Z-API.

---

## 📦 O Que Foi Criado

### 1. **Script Principal** 📄
```
.claude/scripts/send-morning-call.js
```
- Valida se é dia útil (seg-sex)
- Lê conteúdo do arquivo `content/morning-call/YYYY-MM-DD.md`
- Envia via POST para a Z-API
- Trata erros com retry automático (3 tentativas)

### 2. **Arquivo de Configuração** ⚙️
```
.claude/config-morning-call.json
```
Contém:
- Schedule: `9 9 * * 1-5` (seg-sex 09h09)
- Timezone: `America/Sao_Paulo`
- Retry policy: 3 tentativas com backoff de 5s
- Notificações de sucesso/erro

### 3. **Script de Teste** 🧪
```
.claude/scripts/test-morning-call.js
```
Valida:
- ✅ Scripts existem
- ✅ Configurações são válidas
- ✅ Conteúdo disponível
- ✅ Permissões corretas

### 4. **Documentação Setup** 📚
```
.claude/commands/morning-call-setup.md
```
Guia completo com troubleshooting e exemplos

### 5. **Arquivo do Dia** 📋
```
content/morning-call/2026-04-15.md
```
Template criado para hoje (atualizar conforme necessário)

---

## 🚀 Como Ativar

### Opção 1: Paperclip CLI (Recomendado)
```bash
npx paperclipai routine add --config .claude/config-morning-call.json
npx paperclipai routine enable morning-call
```

### Opção 2: Claude Code (via /schedule)
```bash
/schedule create "Morning Call" "0 9 * * 1-5" "node .claude/scripts/send-morning-call.js"
```

### Opção 3: Teste Manual Primeiro
```bash
# Executar manualmente para testar
node .claude/scripts/send-morning-call.js
```

---

## 📅 Estrutura de Conteúdo

Crie um arquivo por dia em:
```
content/morning-call/
├── 2026-04-15.md  ← terça-feira
├── 2026-04-16.md  ← quarta-feira
├── 2026-04-17.md  ← quinta-feira
└── ... (seg-sex)
```

### Formato Recomendado
```markdown
# 🌅 Morning Call - [DATA]

## 📊 Resumo do Dia
[Breve resumo do dia]

## 🎯 Objetivos
- Objetivo 1
- Objetivo 2

## 💪 Motivação
> Citação inspiradora

---

## 🚀 Vamos Começar!
```

---

## 🔐 Credenciais Z-API

Armazenadas em: `.claude/config-morning-call.json`

```json
{
  "z-api": {
    "instanceId": "3F11BDD3D23071C40CFC9EED2DF277BD",
    "token": "D06BC58B1E9B2833DB10EBF3",
    "clientToken": "F5d5ff0989cdd4d139fa2e026cf0be0c4",
    "groupJid": "120363407926604570-group",
    "apiUrl": "https://api.z-api.io/instances/..."
  }
}
```

> ⚠️ **Aviso:** Esses arquivos contêm tokens sensíveis. Adicione a `.gitignore` se necessário:
```bash
echo ".claude/config-morning-call.json" >> .gitignore
```

---

## 🧪 Validação

Todos os testes passaram ✅:

```
✅ Script principal encontrado
✅ Arquivo de configuração válido
✅ Pasta de conteúdo existe
✅ Arquivo do dia existe
✅ Horário válido (seg-sex)
✅ Permissões corretas
```

Execute novamente para revalidar:
```bash
node .claude/scripts/test-morning-call.js
```

---

## 📊 Logs

Após ativar, os logs serão armazenados em:
```
.claude/logs/morning-call.log
```

Monitorar em tempo real:
```bash
tail -f .claude/logs/morning-call.log
```

---

## 🔄 Próximos Passos

1. **Ativar a Rotina**
   ```bash
   npx paperclipai routine enable morning-call
   ```

2. **Customizar Conteúdo**
   - Editar `content/morning-call/YYYY-MM-DD.md` diariamente
   - Ou criar um template automático

3. **Monitorar Execução**
   - Verificar logs em `.claude/logs/morning-call.log`
   - Confirmar envios no WhatsApp do grupo

4. **Ajustar Horário (se necessário)**
   - Editar `schedule` em `.claude/config-morning-call.json`
   - Formato: `minuto hora dia-mês dia-semana`
   - Exemplo: `30 8 * * 1-5` = 08h30, seg-sex

---

## 🆘 Troubleshooting

### "Arquivo não encontrado"
```bash
# Certifique-se que existe:
ls content/morning-call/2026-04-15.md
```

### "Erro de conexão"
```bash
# Teste credenciais Z-API:
curl -X GET "https://api.z-api.io/instances/3F11BDD3D23071C40CFC9EED2DF277BD/token/D06BC58B1E9B2833DB10EBF3/instance"
```

### "EPERM ao criar symlinks"
```bash
# Habilitar modo Developer do Windows:
reg add HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock /t REG_DWORD /f /v AllowDevelopmentWithoutDevLicense /d 1
```

---

## 📞 Contato & Suporte

- **Z-API Docs:** https://z-api.io/docs
- **Z-API Status:** https://status.z-api.io
- **Issues:** Verificar `.claude/logs/morning-call.log`

---

**Criado em:** 2026-04-15  
**Status:** ✅ Pronto para Ativar
