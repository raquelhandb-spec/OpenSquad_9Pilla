# 🚀 COMECE AGORA (30 minutos)

**Seu Voice ID está configurado:** `0r2zCQO0vO1jOfWbm7N7` ✅

---

## ⚡ PASSO 1: Setup Local (5 min)

Abra o terminal e copie/cole:

```bash
cd /home/user/OpenSquad_9Pilla/squads/shorts-maestro

# Criar ambiente Python
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

Se tiver erro, avisa!

---

## ⚡ PASSO 2: Configurar Credenciais (3 min)

```bash
# Copiar template
cp .env.example .env

# Abrir no editor
nano .env
```

Procure essas linhas e deixe assim:

```env
# Já configuradas (não mude):
BRAPI_API_KEY=tky3Vocipoj9ZocxEumbCe
ELEVENLABS_API_KEY=sk_2e12b95dc92a231055f4e9d4f275ae9fab83940d59b26a3e
ELEVENLABS_VOICE_ID=0r2zCQO0vO1jOfWbm7N7
HEYGEN_API_KEY=sk_V2_hgu_kkX2jmyuQzW_9R8ocwO4rBLzHX0mrIyQwKAJWLAGrJjW
ZAPI_INSTANCE_ID=3F11BDD3D23071C40CFC9EED2DF277BD
ZAPI_API_TOKEN=D06BC58B1E9B2833DB10EBF3
MANYCHAT_API_KEY=11058963:93a19ff0c8e75129c2d9303960e974dd

# CRÍTICO - Configure isso (Telegram):
TELEGRAM_BOT_TOKEN=SEU_BOT_TOKEN_AQUI
TELEGRAM_CHAT_ID=SEU_CHAT_ID_AQUI
```

**Como obter Telegram (2 min):**
1. Abra Telegram
2. Procure por `@BotFather`
3. Envie `/newbot`
4. Siga as instruções
5. Copie o token que receber
6. Crie um grupo ou use seu chat pessoal
7. Coloque token + chat ID no .env

**Salvar .env:** Ctrl+X → Y → Enter

---

## ⚡ PASSO 3: Instalar Ollama (10 min)

Abra NOVO terminal:

```bash
# Download e instale: https://ollama.ai/download

# Depois de instalar, execute:
ollama serve
```

**Deixe esse terminal ABERTO!** (roda em background)

---

## ⚡ PASSO 4: Validar Setup (2 min)

Volte ao terminal original (onde está em venv):

```bash
python orchestrator.py --validate
```

**Deve aparecer:**
```
✅ Prospector Agent
✅ Writer Agent (Ollama)
✅ Reviewer Agent (Telegram)
✅ ElevenLabs Agent
✅ HeyGen Agent
✅ Publisher Agent
✅ Z-API Broadcaster Agent
✅ ManyChat Agent
✅ Investing Analysis Agent

ready_to_run: true
```

Se algo estiver vermelho, avisa aqui!

---

## ⚡ PASSO 5: Seu Primeiro Short (5 min)

```bash
python orchestrator.py --cycle
```

**O que acontece:**
1. Prospector busca tema do mercado
2. Writer gera script com SUA voz
3. Telegram envia script para você
4. **VOCÊ reage com 👍 para aprovar**
5. HeyGen cria vídeo
6. YouTube publica
7. WhatsApp notifica turma

---

## ⚡ PASSO 6: Aprovar no Telegram (1 min)

Você vai receber uma mensagem assim:

```
📝 NOVO SCRIPT PARA APROVAÇÃO

🎯 Ticker: PETR4
⏰ Data: 10/06/2026 14:30

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Bom dia! Aqui é Raquel!

📊 TERMÔMETRO DO DIA
💵 Dólar: R$ 5,03
📈 Ibovespa: 174.197
🛢️ Petróleo Brent: US$ 95,45
🏦 PETR4: 📉 queda 1.76%

...

✅ RESPONDA:
👍 APROVA
👎 REJEITA
```

**Clique no emoji 👍 no Telegram!**

---

## 🎉 PRONTO!

Seu vídeo está sendo criado:
- ⏳ 2-5 minutos: HeyGen gerando avatar
- 📺 YouTube Shorts ao vivo
- 💬 WhatsApp notifica turma
- 📊 Analytics começam

---

## 📊 Fluxo Visual

```
VOCÊ AGORA:                          DEPOIS (Automático):
└─ Clona voz ✅                      └─ Prospector (dados)
└─ Setup .env                        └─ Writer (script)
└─ Roda orchestrator                 └─ ElevenLabs (áudio)
└─ Aprova no Telegram (👍)           └─ HeyGen (vídeo)
                                     └─ YouTube (publicar)
                                     └─ Z-API (notificar)
```

---

## 🚨 Se Algo Der Erro

### "Ollama não conecta"
```bash
# Verificar se Ollama está rodando
ps aux | grep ollama

# Se não, volte e execute em novo terminal:
ollama serve
```

### "Telegram não funciona"
```bash
# Testar token
curl https://api.telegram.org/bot{SEU_TOKEN}/getMe

# Se retornar erro, token está errado
# Refaça: @BotFather → /newbot
```

### "Voice ID errado"
Seu Voice ID correto é: `0r2zCQO0vO1jOfWbm7N7`

Se quiser testar, vai em:
https://elevenlabs.io/voice-lab
Procura por sua voz clonada

---

## ✅ Checklist Final

Antes de rodar `python orchestrator.py --cycle`:

- [ ] Python venv ativado
- [ ] pip install -r requirements.txt ✅
- [ ] .env preenchido com credentials
- [ ] Ollama rodando (`ollama serve` em outro terminal)
- [ ] Telegram bot token + chat ID no .env
- [ ] `python orchestrator.py --validate` retorna tudo verde

**Tudo ok?** 

```bash
python orchestrator.py --cycle
```

---

## 📈 Próximos Passos (Hoje)

1. **Publicar 1º short** (30 min total)
2. **Aprovar no Telegram** (1 min)
3. **Deixar rodar** (5 min)
4. **Ver vídeo ao vivo** 🎉

---

## 🔄 Amanhã

Rodar de novo:
```bash
python orchestrator.py --cycle
```

Seu segundo short!

---

## 📞 Precisa de Ajuda?

- ❌ Setup: Envie screenshot do erro
- ❌ Telegram: Avisa que não conseguiu token
- ❌ Ollama: Envia a mensagem de erro
- ❓ Dúvida: Pergunta em português

---

## 🎯 Objetivo Final

- ✅ Shorts publicados: Hoje (1º)
- ✅ Próximos 7 meses: 50-75 shorts
- ✅ Janeiro 2027: Monetização

**Vamos lá!** 🚀

---

**Voice ID Raquel:** `0r2zCQO0vO1jOfWbm7N7` ✅  
**Status:** 🟢 PRONTO PARA COMEÇAR
