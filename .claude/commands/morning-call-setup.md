# Morning Call Automático - Setup

## 📋 Resumo

Configuração de envio automático do **Morning Call** via Z-API, seg-sex às **09h09**.

## 🔧 Configuração Realizada

### 1. Script de Envio
**Arquivo:** `.claude/scripts/send-morning-call.js`

- ✅ Valida se é dia útil (seg-sex)
- ✅ Lê conteúdo de `content/morning-call/[YYYY-MM-DD].md`
- ✅ Envia via POST para Z-API
- ✅ Trata erros com retry automático

### 2. Configuração da Rotina
**Arquivo:** `.claude/config-morning-call.json`

```json
{
  "schedule": "9 9 * * 1-5",  // seg-sex 09h09
  "timezone": "America/Sao_Paulo",
  "retry": {
    "maxAttempts": 3,
    "backoffMs": 5000
  }
}
```

### 3. Credenciais Z-API
- **Instance ID:** 3F11BDD3D23071C40CFC9EED2DF277BD
- **Token:** D06BC58B1E9B2833DB10EBF3
- **Client-Token:** F5d5ff0989cdd4d139fa2e026cf0be0c4
- **Group JID:** 120363407926604570-group
- **API URL:** https://api.z-api.io/instances/3F11BDD3D23071C40CFC9EED2DF277BD/token/D06BC58B1E9B2833DB10EBF3/send-text

## 🚀 Como Ativar

### Opção 1: Via Paperclip CLI
```bash
npx paperclipai routine add --config .claude/config-morning-call.json
npx paperclipai routine enable morning-call
```

### Opção 2: Via Claude Code (Cron)
```bash
/schedule create daily morning-call "9 9 * * 1-5"
```

### Opção 3: Via Systemd (Linux/macOS)
```bash
# Criar cron job
(crontab -l 2>/dev/null; echo "9 9 * * 1-5 cd /path/to/project && node .claude/scripts/send-morning-call.js") | crontab -
```

## 🧪 Testes

### Teste Manual
```bash
# Executar script manualmente
node .claude/scripts/send-morning-call.js
```

### Teste com Data Específica
```bash
# Simular envio para uma data específica
node -e "
  process.env.TEST_DATE = '2026-04-16';
  require('./.claude/scripts/send-morning-call.js');
"
```

## 📝 Estrutura de Arquivos Esperada

```
content/morning-call/
├── README.md
├── 2026-04-15.md
├── 2026-04-16.md  ← arquivo do dia
└── ...
```

## ⚙️ Variáveis de Ambiente (Opcional)

Para maior segurança, você pode usar variáveis de ambiente:

```bash
export Z_API_INSTANCE_ID="3F11BDD3D23071C40CFC9EED2DF277BD"
export Z_API_TOKEN="D06BC58B1E9B2833DB10EBF3"
export Z_API_CLIENT_TOKEN="F5d5ff0989cdd4d139fa2e026cf0be0c4"
export Z_API_GROUP_JID="120363407926604570-group"
```

## 🔍 Logs

Os logs são armazenados em:
- **Local:** `.claude/logs/morning-call.log`
- **Formato:** JSON com timestamp

## 🚨 Troubleshooting

### "Arquivo não encontrado"
- Certifique-se que `content/morning-call/YYYY-MM-DD.md` existe
- Formato de data deve ser exato: `2026-04-15.md`

### "EPERM" ao criar symlinks
- Modo Developer do Windows deve estar ativado
- Execute: `reg add HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock /t REG_DWORD /f /v AllowDevelopmentWithoutDevLicense /d 1`

### Erro de conexão Z-API
- Verifique se as credenciais estão corretas
- Confirme que o grupo existe
- Teste a conexão: `curl -X GET "https://api.z-api.io/instances/3F11BDD3D23071C40CFC9EED2DF277BD/token/D06BC58B1E9B2833DB10EBF3/instance"`

## 📞 Suporte

Para mais informações sobre Z-API:
- Docs: https://z-api.io/docs
- Status: https://status.z-api.io
