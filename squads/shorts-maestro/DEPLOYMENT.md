# 🚀 9Pilla Shorts-Maestro — Deployment Guide

**Status:** ✅ Pipeline completa e pronta para deployment  
**Last Updated:** Junho 2026  
**Branch:** `claude/moneprinter-9pilla-integration-9gm87x`

---

## 📋 VISÃO GERAL

Este guia walk-through completo para colocar a pipeline 9Pilla em produção.

**Fluxo:**
```
Prospector → Writer → Reviewer → Executor → Publisher → Z-API
   (dados)   (script)  (aprova)  (vídeo)   (YouTube)  (WhatsApp)
```

**Tempo estimado:** 2-3 horas para setup completo

---

## ✅ PRÉ-REQUISITOS

### Hardware
- [ ] Computador com 8GB+ RAM
- [ ] 50GB+ espaço em disco (para videos)
- [ ] Conexão internet estável
- [ ] Microfone (para clonar voz ElevenLabs)

### Contas externas (GRÁTIS)
- [ ] GitHub (para clonar repo)
- [ ] Google Cloud Console (para YouTube OAuth)
- [ ] Telegram (para aprovação)

### Contas pagas (já têm credenciais)
- [ ] Brapi API ✅ (credencial: `tky3Vocipoj9ZocxEumbCe`)
- [ ] ElevenLabs ✅ (credencial: `sk_2e12b95dc92a231055f4e9d4f275ae9fab83940d59b26a3e`)
- [ ] HeyGen ✅ (credencial: `sk_V2_hgu_kkX2jmyuQzW_9R8ocwO4rBLzHX0mrIyQwKAJWLAGrJjW`)
- [ ] Z-API ✅ (credenciais: instance + token)
- [ ] ManyChat ✅ (credencial: `11058963:93a19ff0c8e75129c2d9303960e974dd`)

---

## 🔧 PASSO 1: SETUP LOCAL (30 min)

### 1.1 Clonar repositório

```bash
git clone https://github.com/raquelhandb-spec/OpenSquad_9Pilla.git
cd OpenSquad_9Pilla
git checkout claude/moneprinter-9pilla-integration-9gm87x
cd squads/shorts-maestro
```

### 1.2 Setup Python

```bash
# Criar virtual environment
python3 -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate (Windows)

# Instalar dependências
pip install -r requirements.txt
```

### 1.3 Configurar .env

```bash
# Copiar template
cp .env.example .env

# Editar .env com suas credenciais
nano .env  # ou seu editor favorito
```

**Mínimo necessário para testar:**
```env
BRAPI_API_KEY=tky3Vocipoj9ZocxEumbCe
ELEVENLABS_API_KEY=sk_2e12b95dc92a231055f4e9d4f275ae9fab83940d59b26a3e
HEYGEN_API_KEY=sk_V2_hgu_kkX2jmyuQzW_9R8ocwO4rBLzHX0mrIyQwKAJWLAGrJjW
ZAPI_INSTANCE_ID=3F11BDD3D23071C40CFC9EED2DF277BD
ZAPI_API_TOKEN=D06BC58B1E9B2833DB10EBF3
MANYCHAT_API_KEY=11058963:93a19ff0c8e75129c2d9303960e974dd
```

---

## 🎙️ PASSO 2: CLONAR SUA VOZ (10-15 min)

**CRÍTICO:** Script gerado precisa da sua voz para soar autêntico!

### 2.1 Acessar ElevenLabs Voice Lab

```
URL: https://elevenlabs.io/voice-lab
```

### 2.2 Clonar voz

1. Faça login
2. Clique em "[Clone Voice]"
3. Grave 10-30 segundos falando naturalmente
   - **Exemplo**: "Olá, meu nome é Raquel. Aqui na 9Pilla a gente fala de dinheiro sem tabu."
4. Nomeie: "Raquel 9Pilla"
5. Copie o **Voice ID** (código longo tipo: `21m00Tcm4TlvDq8ikWAM`)

### 2.3 Configurar Voice ID

```bash
# Editar .env
ELEVENLABS_VOICE_ID=SEU_VOICE_ID_AQUI
```

---

## 🤖 PASSO 3: SETUP OLLAMA (15 min)

Ollama roda localmente no seu computador para gerar scripts.

### 3.1 Instalar Ollama

```
Download: https://ollama.ai/download
```

Após instalar, abra um terminal e execute:

```bash
ollama serve
```

Deixar rodando em terminal separado.

### 3.2 Verificar Ollama

Em outro terminal:

```bash
curl http://localhost:11434/api/tags
# Deve retornar um JSON com modelos disponíveis
```

Se não tiver `llama2`, execute:

```bash
ollama pull llama2
```

---

## 💬 PASSO 4: SETUP TELEGRAM (15 min)

Telegram é onde você aprova scripts (👍/👎).

### 4.1 Criar bot Telegram

1. Abra Telegram e vá para `@BotFather`
2. Envie `/newbot`
3. Escolha um nome: "9PillaBot"
4. Escolha username: "9pilla_bot" (único)
5. Copie o **TOKEN** (tipo: `123456:ABC-DEF...`)

### 4.2 Obter seu Chat ID

```bash
# Substitua {TOKEN} pelo token acima
curl https://api.telegram.org/bot{TOKEN}/getMe

# Resposta (copie o id)
{"ok":true,"result":{"id":123456789,...}}
```

Seu Chat ID é o número grande (ex: `123456789`)

### 4.3 Configurar .env

```bash
# Editar .env
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
TELEGRAM_CHAT_ID=123456789
```

### 4.4 Testar bot

```bash
# Enviar mensagem teste
curl -X POST https://api.telegram.org/bot{TOKEN}/sendMessage \
  -d "chat_id={CHAT_ID}&text=Oi Raquel!"
```

Se receber mensagem no Telegram ✅ Configurado!

---

## 🎥 PASSO 5: YOUTUBE SETUP (20 min)

YouTube é onde os Shorts são publicados.

### 5.1 Criar conta YouTube 9Pilla

```
https://www.youtube.com/@9pilla (crie como rascunho)
```

### 5.2 Configurar Google OAuth

1. Vá para Google Cloud Console: https://console.cloud.google.com
2. Create new project: "9Pilla"
3. Enable APIs:
   - YouTube Data API v3
   - Google Drive API
4. Create OAuth2 credentials (Desktop app)
5. Download `credentials.json`
6. Salve em `./credentials/youtube_credentials.json`

Primeira vez que usar vai abrir browser para você autorizar. Depois usa refresh token automaticamente.

---

## ✅ PASSO 6: VALIDAR SETUP (5 min)

Verificar se tudo está configurado:

```bash
cd squads/shorts-maestro
python orchestrator.py --validate
```

**Output esperado:**
```
✅ Prospector Agent (BRAPI_API_KEY)
✅ Writer Agent (Ollama) 
✅ Reviewer Agent (Telegram)
✅ ElevenLabs Agent
✅ HeyGen Agent
✅ Publisher Agent
✅ Z-API Broadcaster Agent
✅ ManyChat Agent
✅ Investing Analysis Agent

✅ CREDENCIAIS CRÍTICAS:
✅ BRAPI_API_KEY
✅ OLLAMA_RUNNING
✅ TELEGRAM_BOT
✅ ELEVENLABS_VOICE_ID

ready_to_run: true
```

Se alguma falhar:
- [ ] Volte ao passo correspondente
- [ ] Verifique credenciais no .env
- [ ] Confirme Ollama está rodando

---

## 🚀 PASSO 7: EXECUTAR PRIMEIRO CICLO

### 7.1 Rodar pipeline completa

```bash
python orchestrator.py --cycle
```

**O que acontece:**

1. **Prospector** → Identifica tema trending (ex: PETR4 caiu)
2. **Writer** → Gera script de 60-90s em português, soando como Raquel
3. **Reviewer** → Envia para você aprovar no Telegram
4. **Aguarda sua reação:**
   - 👍 = Cria vídeo HeyGen (US$ 0.30) → Publica YouTube
   - 👎 = Zero gasto, tenta novamente

### 7.2 Aprovar no Telegram

Você vai receber mensagem com:
- Script completo
- Link do vídeo
- Instruções (👍 aprova, 👎 rejeita)

Reaja com 👍 para aprovar.

### 7.3 Monitorar criação

Após aprovar:
- HeyGen cria avatar vídeo (2-5 min)
- Publisher publica no YouTube
- Z-API notifica Turma 9Pilla no WhatsApp

**Seu primeiro vídeo está ao vivo!** 🎉

---

## 📊 PASSO 8: CONFIGURAÇÃO AVANÇADA (Opcional)

### 8.1 Database (PostgreSQL)

Para tracking de ciclos, historico de aprovações:

```bash
# Instalar PostgreSQL
# Criar database
createdb 9pilla

# Configure em .env
DATABASE_URL=postgresql://user:password@localhost:5432/9pilla
```

### 8.2 TikTok & Instagram (Futuros)

Infraestrutura pronta em `publisher.py`, aguardando credenciais.

### 8.3 Spotify Podcast (Futuro)

Escalabilidade para podcast automático:
- Script gerado por Writer
- Narrado por ElevenLabs
- Publicado em Spotify/Anchor

---

## 🔄 OPERAÇÃO DIÁRIA

### Rotina automática

```bash
# Rodar a cada 1-2 horas
python orchestrator.py --cycle

# Cron job (Linux/Mac)
0 */2 * * * cd /path/to/9pilla && python orchestrator.py --cycle
```

### Monitorar

```bash
# Ver estatísticas
python orchestrator.py --stats

# Ver logs
tail -f logs/9pilla.log
```

### Raquel's daily checklist

```
⏰ 08:55 — Script enviado para Telegram
👤 09:00 — VOCÊ aprova/rejeita (1 min)
🎬 09:01-09:05 — HeyGen cria vídeo
📺 09:10 — YouTube Shorts ao vivo
💬 09:11 — WhatsApp notifica Turma
```

---

## 🆘 TROUBLESHOOTING

### "Ollama não está conectando"

```bash
# Verificar se Ollama está rodando
ps aux | grep ollama

# Se não, abra novo terminal e execute
ollama serve

# Se falhar, reinstale: https://ollama.ai/download
```

### "Telegram não recebe mensagem"

```bash
# Verificar token
curl https://api.telegram.org/bot{TOKEN}/getMe
# Deve retornar info do bot

# Verificar chat_id
curl https://api.telegram.org/bot{TOKEN}/sendMessage \
  -d "chat_id={CHAT_ID}&text=teste"
# Você deve receber "teste" no Telegram
```

### "HeyGen: Insufficient credits"

```
⚠️ Significa que os US$ 15 acabaram

Opções:
1. Comprar mais créditos
2. Usar vídeos só com áudio (ElevenLabs) sem avatar (HeyGen)
3. Pausar geração até novo crédito
```

### "Script não está soando como Raquel"

```
Problema: Voice ID não foi clonado corretamente

Solução:
1. Vá para https://elevenlabs.io/voice-lab
2. Clique em "Clone Voice" novamente
3. Grave sua voz com melhor qualidade (sem ruído)
4. Copie novo Voice ID
5. Atualize em .env: ELEVENLABS_VOICE_ID=novo_id
6. Teste novamente
```

---

## 📈 SCALING & PERFORMANCE

### Para 50+ shorts/mês

**Atual (Manual):**
- 1 ciclo = 15-20 min (incluindo sua aprovação)
- 2-3 ciclos/dia = 6-9 shorts/dia
- 50 shorts/mês ✅ (25-30 dias úteis)

**Para aumentar:**

```python
# Rodar múltiplas vezes
for i in range(5):
    orchestrator.run_full_cycle()
    time.sleep(60)  # 1 min entre ciclos
```

**Mas cuidado com limites:**
- Brapi: 1000 req/dia (suficiente)
- ElevenLabs: 10K chars/mês (BÁSICO plano)
- HeyGen: US$ 15 = ~50 avatares (custo!)
- YouTube: unlimited Shorts
- Z-API: unlimited mensagens (plano pago)

**Recomendação:** Aumentar budget ElevenLabs + HeyGen conforme crescer.

---

## 🎯 PRÓXIMOS PASSOS

### Fase 1 (Agora - Junho)
- ✅ Setup completo
- ✅ Teste com 3-5 shorts
- ✅ Validar qualidade scripts
- ✅ Ajustar Raquel Voice prompt se necessário

### Fase 2 (Julho-Agosto)  
- [ ] Aumentar para 20+ shorts/mês
- [ ] TikTok integration (se tiver Business Account)
- [ ] Instagram Reels (Meta Business API)
- [ ] Database + Analytics dashboard

### Fase 3 (Setembro-Dezembro)
- [ ] Podcast automático (Spotify/Anchor)
- [ ] Blog SEO (9pilla.com)
- [ ] Lead magnet funnels (ManyChat)
- [ ] Monetização (E-courses, memberships)

### Fase 4 (Janeiro 2027)
- [ ] Activate paid products
- [ ] Scale to 100+ shorts/mês
- [ ] Multi-language support
- [ ] Agent marketplace integrations

---

## 📞 SUPORTE

### Erros/Dúvidas

1. **Código/Setup:** Check `troubleshooting` section acima
2. **API errors:** Verifique credenciais em `.env`
3. **Voz clonagem:** ElevenLabs docs: https://elevenlabs.io/docs
4. **HeyGen:** Docs: https://heygen.com/docs
5. **YouTube:** Google Cloud docs: https://developers.google.com/youtube

---

## 📝 CHECKLIST FINAL

Antes de considerar "LIVE":

- [ ] .env preenchido com todas credenciais
- [ ] Ollama rodando (`ollama serve`)
- [ ] Voz clonada no ElevenLabs (Voice ID configurado)
- [ ] Telegram bot testado (mensagem chega)
- [ ] YouTube OAuth configurado
- [ ] `python orchestrator.py --validate` retorna "ready_to_run: true"
- [ ] Primeiro ciclo executado com sucesso
- [ ] Vídeo publicado no YouTube
- [ ] Turma 9Pilla notificada via WhatsApp

**Tudo verde?** 🟢

```bash
# Você está pronto para produção!
python orchestrator.py --cycle
```

🚀 **Bem-vindo ao futuro da criação de conteúdo!**

---

**Última atualização:** Junho 10, 2026  
**Branch:** `claude/moneprinter-9pilla-integration-9gm87x`  
**Status:** ✅ READY FOR PRODUCTION
