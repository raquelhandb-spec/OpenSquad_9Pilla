# 📱 Setup Telegram (5 minutos)

**Único bloqueador que falta é o Telegram Bot!**

Depois disso você rodar tudo.

---

## ✅ Passo 1: Criar Bot no BotFather

1. Abra Telegram no seu celular ou web
2. Procure por: `@BotFather` (usuário oficial do Telegram)
3. Clique em "Iniciar"
4. Envie a mensagem: `/newbot`

---

## ✅ Passo 2: Nomear o Bot

BotFather vai pedir:

**"Qual será o nome do seu bot?"**

Responda:
```
9Pilla Shorts Bot
```

(Pode ser outro nome, não importa)

---

## ✅ Passo 3: Escolher Username

**"Escolha um username para o bot."**

Responda algo único:
```
9pilla_shorts_bot_raquel
```

(Tem que terminar em `_bot`)

---

## ✅ Passo 4: Receber o Token

BotFather vai enviar uma mensagem assim:

```
✅ Done! Congratulations on your new bot.
You will find it at t.me/9pilla_shorts_bot_raquel
Use this token to access the HTTP API:
123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefg

For a description of the Bot API, see this page:
https://core.telegram.org/bots/api
```

**COPIE o token longo** (tipo `123456789:ABC...`)

---

## ✅ Passo 5: Obter seu Chat ID

Abra um novo chat com seu bot novo:
```
@9pilla_shorts_bot_raquel
```

(ou o username que você escolheu)

Envie qualquer mensagem, tipo:
```
oi
```

Agora execute no terminal:

```bash
TELEGRAM_TOKEN="123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefg"

curl https://api.telegram.org/bot${TELEGRAM_TOKEN}/getUpdates
```

Você vai receber algo assim:

```json
{
  "ok": true,
  "result": [
    {
      "update_id": 123456789,
      "message": {
        "message_id": 1,
        "from": {
          "id": 987654321,  ← COPIE ESSE NÚMERO
          "first_name": "Raquel"
        },
        "text": "oi",
        ...
      }
    }
  ]
}
```

**Seu Chat ID é o número `id`** (ex: `987654321`)

---

## ✅ Passo 6: Configurar .env

Abra o arquivo `.env`:

```bash
nano .env
```

Encontre essas linhas:

```env
TELEGRAM_BOT_TOKEN=SEU_BOT_TOKEN_AQUI
TELEGRAM_CHAT_ID=SEU_CHAT_ID_AQUI
```

Substitua:

```env
TELEGRAM_BOT_TOKEN=123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefg
TELEGRAM_CHAT_ID=987654321
```

**Salvar:** Ctrl+X → Y → Enter

---

## ✅ Pronto!

Agora você tem:
- ✅ Bot Token
- ✅ Chat ID
- ✅ .env configurado

**Próximo:**

```bash
python orchestrator.py --validate
```

Deve aparecer verde ✅ no Reviewer Agent!

---

## 🧪 Testar Telegram (Opcional)

Para ter certeza que funcionou:

```bash
TELEGRAM_TOKEN="seu_token_aqui"
TELEGRAM_CHAT_ID="seu_chat_id_aqui"

curl -X POST https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage \
  -d "chat_id=${TELEGRAM_CHAT_ID}&text=Teste%20de%20conexao%20-%20Funciona!"
```

Se receber uma mensagem no Telegram → Funciona! ✅

---

## ⏱️ Tempo Total

- BotFather: 1 min
- Nomear bot: 1 min
- Obter token: 1 min
- Obter chat ID: 2 min

**Total: 5 minutos**

---

## 🎯 Resumo

```
BotFather → /newbot → Nome do bot → Username → Token
                                                   ↓
                                              Mensagem ao bot
                                                   ↓
                                              curl getUpdates
                                                   ↓
                                              Chat ID
                                                   ↓
                                              .env preenchido
```

---

**Pronto?** Execute:

```bash
python orchestrator.py --cycle
```

🎉 Seu primeiro short sai hoje!
