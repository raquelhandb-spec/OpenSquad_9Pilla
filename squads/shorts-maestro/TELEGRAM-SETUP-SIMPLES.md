# 📱 TELEGRAM - Passo a Passo SUPER Simples

**Você vai criar um bot que vai enviar scripts pra você aprovar!**

**Tempo:** 5 minutos  
**Dificuldade:** Muito fácil!

---

## PASSO 1: Abrir Telegram

Abra Telegram no seu celular ou web: https://web.telegram.org

---

## PASSO 2: Procurar BotFather

Na caixa de busca (lupa no topo), escreva:

```
@BotFather
```

Vai aparecer um usuário chamado **BotFather** (com símbolo de verificado ✓)

**Clique nele**

---

## PASSO 3: Enviar /newbot

Na conversa, escreva:

```
/newbot
```

**Aperte Enter/Enviar**

---

## PASSO 4: Escolher Nome do Bot

BotFather vai perguntar:

```
What's the name of your bot? 
Example: MyAwesomeBot
```

Você responde:

```
9Pilla Shorts Bot
```

**Aperte Enter/Enviar**

---

## PASSO 5: Escolher Username (IMPORTANTE!)

BotFather vai perguntar:

```
Alright, a new bot. How are we going to call it? 
Please choose a username for your bot. It must end in 'bot'. 
For example, TetrisBot or tetris_bot.
```

Você responde:

```
9pilla_shorts_bot_raquel
```

**⚠️ TEM QUE TERMINAR EM "_bot" e ser único!**

**Aperte Enter/Enviar**

---

## PASSO 6: COPIAR O TOKEN (SUPER IMPORTANTE!)

BotFather vai enviar uma mensagem com seu TOKEN!

Vai ser algo assim:

```
Done! Congratulations on your new bot. 
You will find it at t.me/9pilla_shorts_bot_raquel 
Use this token to access the HTTP API:
123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefg
```

**VOCÊ TEM QUE COPIAR ESSE TOKEN LONGO!**

(O número gigante depois de "Use this token to access the HTTP API:")

**Coloque em um Bloco de Notas para não perder**

---

## PASSO 7: OBTER SEU CHAT ID

Abra uma conversa com seu bot novo:

Clique no link que BotFather deu:
```
t.me/9pilla_shorts_bot_raquel
```

Ou procure na busca pelo username que você criou.

**Quando abrir o chat, envie qualquer mensagem:**

```
oi
```

ou

```
teste
```

**Aperte Enter/Enviar**

---

## PASSO 8: EXECUTAR COMANDO (Copia e Cola!)

Abra o Terminal/Prompt do seu computador e **copie exatamente isso:**

```bash
TELEGRAM_TOKEN="123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefg"
CHAT_ID=$(curl -s "https://api.telegram.org/bot${TELEGRAM_TOKEN}/getUpdates" | grep -o '"id":[0-9]*' | head -1 | grep -o '[0-9]*')
echo "Seu Chat ID é: $CHAT_ID"
```

**MAS ANTES, substitua o token!**

Onde escreve:
```
123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefg
```

Você coloca o TOKEN que BotFather deu (do Passo 6)

**Depois aperte Enter/Executar**

---

## PASSO 9: COPIAR SEU CHAT ID

A resposta vai ser assim:

```
Seu Chat ID é: 987654321
```

**Copie esse número!**

---

## ✅ Agora Você Tem 2 Números

```
TELEGRAM_BOT_TOKEN=123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefg
TELEGRAM_CHAT_ID=987654321
```

**Me manda esses 2 números que eu configuro tudo!**

---

## 📋 Resumo Visual

```
1. Abrir Telegram
   ↓
2. Procurar @BotFather
   ↓
3. Enviar /newbot
   ↓
4. Nome: 9Pilla Shorts Bot
   ↓
5. Username: 9pilla_shorts_bot_raquel
   ↓
6. COPIAR TOKEN (aquele número gigante)
   ↓
7. Enviar mensagem ao bot novo
   ↓
8. Executar comando no terminal
   ↓
9. COPIAR CHAT ID (número resultado)
   ↓
✅ PRONTO! Me manda os 2 números
```

---

## 🆘 Se Ficar Confuso

**Mandar print aqui que eu guio!**

Mesmo que esteja achando difícil, é fácil!

---

## 📞 Próximas Etapas

Depois que você me mandar os 2 IDs:

```
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID=...
```

Eu:
1. Configuro no sistema
2. Rodo o primeiro ciclo
3. Você recebe **SCRIPT + ÁUDIO + VÍDEO** no Telegram
4. Você aprova ou rejeita
5. Se aprovar → publica!

---

**Consegue fazer isso?** 

Manda os 2 IDs quando tiver! 🚀
