# 🎬 Squad Shorts-Maestro — Arquitetura Completa

**Versão:** 1.0  
**Data:** Junho 2026  
**Status:** 🔵 Em Implementação  
**Branch:** `claude/moneprinter-9pilla-integration-9gm87x`

---

## 📋 Visão Geral

**Shorts-Maestro** é um squad de agentes que automatiza a criação, aprovação e publicação de YouTube Shorts para a 9Pilla, integrando:

- 📊 Dados reais de mercado (Brapi API)
- 🧠 Geração de scripts com "Raquel Voice" (Ollama)
- 🎙️ Narração de vídeo (ElevenLabs)
- 🎬 Composição de vídeo (HeyGen)
- 💬 Feedback & Aprovação (Telegram)
- 🚀 Publicação Multi-plataforma (YouTube, TikTok)

---

## 🏗️ ARQUITETURA END-TO-END

```
┌───────────────────────────────────────────────────────────────────┐
│                     SHORTS FACTORY PIPELINE                        │
└───────────────────────────────────────────────────────────────────┘

[CAMADA 1 — DADOS]
┌─────────────────────┐
│   Brapi API         │  ← Mercado em tempo real
│ - IBOV, Dólar       │    (preços, noticias, commodities)
│ - Petróleo, Ações   │
│ - Sentimento        │
└──────────┬──────────┘
           │
           ↓
[CAMADA 2 — AGENTES DO SQUAD]
┌─────────────────────────────────────────────────────────────────┐
│                   OPENSQUAD (5 AGENTS)                           │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │  PROSPECTOR  │→ │    WRITER    │→ │   EXECUTOR   │           │
│  │              │  │              │  │              │           │
│  │ • Trending   │  │ • Raquel     │  │ • MoneyPrint │           │
│  │   tópicos    │  │   Voice      │  │ • ElevenLabs │           │
│  │ • Feedback   │  │ • Script     │  │ • HeyGen     │           │
│  │   loops      │  │ • Prompt     │  │ • Render     │           │
│  │ • News       │  │   tuning     │  │             │           │
│  └──────────────┘  └──────────────┘  └──────┬───────┘           │
│                                              │                   │
│                                    ┌─────────↓────────┐         │
│                                    │    REVIEWER      │         │
│                                    │                  │         │
│                                    │ • Telegram       │         │
│                                    │ • Approval       │         │
│                                    │ • Feedback       │         │
│                                    │ • Training loop  │         │
│                                    └─────────┬────────┘         │
│                                              │                  │
│                                   ┌──────────↓──────────┐       │
│                                   │    PUBLISHER        │       │
│                                   │                     │       │
│                                   │ • YouTube Shorts    │       │
│                                   │ • TikTok (auto)     │       │
│                                   │ • Instagram Reels   │       │
│                                   │ • Analytics         │       │
│                                   └─────────┬──────────┘       │
└─────────────────────────────────────────────│─────────────────┘
                                              │
[CAMADA 3 — DADOS & STORAGE]                 │
┌─────────────────────────────────────────────↓─────────────────┐
│                                                                │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐      │
│  │  PostgreSQL  │   │  MediaBucket │   │   Analytics  │      │
│  │              │   │  (S3/GCS)    │   │  (Supabase)  │      │
│  │ • Jobs queue │   │              │   │              │      │
│  │ • Logs       │   │ • Raw videos │   │ • Views      │      │
│  │ • Feedback   │   │ • Final MP4  │   │ • Engagement │      │
│  │ • Tracking   │   │ • Thumbnails │   │ • Conversão  │      │
│  └──────────────┘   └──────────────┘   └──────────────┘      │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## 👥 OS 5 AGENTES DO SQUAD

### **AGENT 1: PROSPECTOR** 🔍

**Função:** Identificar tópicos trending + coletar dados + gerar insights

**Entradas:**
- Brapi API (notícias de mercado)
- Instagram/TikTok trending (scrape)
- Comentários da Turma 9Pilla (WhatsApp)
- Feedback de vídeos rejeitados (training)

**Lógica:**
```python
while True:
    # A cada 6 horas
    news = brapi.get_news()  # Principais movimentos
    trending = instagram_scrape()  # Trending tags
    feedback = telegram_get_rejected_feedback()  # Por quê rejeitaram?
    
    # Ranking de tópicos
    topics = rank_by_relevance(news, trending, feedback)
    
    # Passa pro Writer
    writer_queue.push({
        "topic": topics[0],
        "data": brapi_data,
        "tone": "Raquel Voice",
        "format": "YouTube Shorts"
    })
```

**Output:** 
```json
{
  "topic": "Petróleo acima de US$ 100 pressiona inflação",
  "data": {
    "brent": 103.5,
    "wti": 97.3,
    "ibov": 176200,
    "timestamp": "2026-06-10 09:00:00"
  },
  "priority": "HIGH",
  "source": "brapi"
}
```

---

### **AGENT 2: WRITER** ✍️

**Função:** Gerar script com "Raquel Voice" usando Ollama

**Entradas:**
- Topic do Prospector
- Dados de mercado (Brapi)
- Raquel Voice Template (fine-tuning)
- Feedback de vídeos anteriores

**Integração Ollama:**
```bash
# Prompt enviado para Ollama
cat <<EOF | ollama run raquel-7b

Você é Raquel, criadora da 9Pilla.
Gere um script de YouTube Shorts sobre: 
"{topic}"

Dados:
- Brent: US$ {brent}/barril
- IBOV: {ibov} pontos
- Dólar: R$ {dolar}

Estrutura:
1. Hook (0-2s): "Aqui está o detalhe que ninguém conta..."
2. Delivery (2-50s): 1 ponto, 1 história, sem fluff
3. Punchline (50-60s): Feche com ênfase

Tom: Conversacional, educativo, sem tabu
Sempre conecte: notícia → seu bolso → ação

EOF
```

**Output:**
```markdown
=== SCRIPT SHORTS ===

HOOK (0-2s):
[Visual]: Texto em vermelho: "Petróleo acima de US$ 100"
[Audio]: "Aqui está o detalhe que ninguém te conta..."
[Text]: "POR QUE ISSO TE AFETA"

DELIVERY (2-50s):
[Visual]: Gráfico do Brent subindo | Emoji barril
[Script]: "Quando o petróleo sobe, o combustível fica caro. 
Frete fica caro. Comida na prateleira sobe. Isso é inflação. 
E quando inflação sobe, o Banco Central segura os juros lá em cima. 
Juros altos = dinheiro caro = bolsa sofre."
[Text Overlay]: "INFLAÇÃO ↑ = SELIC ↑ = BOLSA ↓"

PUNCHLINE (50-60s):
[Visual]: Você (investidor) pensando em cash
[Script]: "O jeito é entender a cadeia. Mercado não é loteria, 
é cause and effect. Você já sabe mais que 90% das pessoas."
[Text]: "Dinheiro é a jornada para a LIBERDADE"

=== METADATA ===
TITLE: "Por que o Petróleo sobe e sua conta fica cara"
DESCRIPTION: "Entenda a cadeia: petróleo → inflação → Selic → seu bolso #Shorts"
HASHTAGS: #Shorts #Petróleo #IBOVESPA #Inflação #Educação
```

---

### **AGENT 3: EXECUTOR** 🎬

**Função:** Executar MoneyPrinter + ElevenLabs + HeyGen

**Pipeline:**
```
Script
  ↓
[MoneyPrinter — 3 min]
├─ Gera base de vídeo
├─ Composição de scenes
├─ Text overlays
└─ Output: raw_video.mp4 (sem áudio)
  ↓
[ElevenLabs — 30s]
├─ Clona voz Raquel (ou padrão)
├─ Narração sincronizada com script
├─ Output: audio_narration.mp3
  ↓
[HeyGen — 1 min]
├─ Avatar de Raquel (opcional)
├─ Sincronização de lábios
├─ Efeitos visuais
└─ Output: heyGen_avatar.mp4
  ↓
[Merge & Render — 2 min]
├─ Mescla MoneyPrinter + ElevenLabs + HeyGen
├─ Adiciona música background (trending)
├─ Watermark 9Pilla
└─ Final output: shorts_final.mp4 (60s, 9:16, 1080p)
```

**Pseudo-código:**
```python
def execute_shorts_pipeline(script, data):
    # 1. MoneyPrinter
    raw_video = moneprinter.generate(
        script=script,
        data=data,
        style="financial_news"
    )
    
    # 2. ElevenLabs
    narration = elevenlabs.generate_speech(
        text=script['delivery'],
        voice_id=RAQUEL_VOICE_ID,
        duration_seconds=48
    )
    
    # 3. HeyGen (opcional)
    avatar_video = heygan.generate_avatar(
        narration=narration,
        style="professional"
    )
    
    # 4. Merge
    final_video = ffmpeg.merge([
        raw_video,
        narration,
        avatar_video,
        background_music
    ])
    
    return final_video
```

**Output:**
- `shorts_final.mp4` — vídeo pronto (1080p, 60s, H.264)
- `thumbnail.png` — capa do shorts
- `metadata.json` — título, descrição, hashtags

---

### **AGENT 4: REVIEWER** 👀

**Função:** Enviar para aprovação via Telegram + coletar feedback

**Workflow:**
```
Vídeo Final
  ↓
[Enviar Preview via Telegram]
├─ Link direto ao arquivo (ou stream)
├─ Metadados (título, descrição)
├─ Botões: ✅ APROVAR | ❌ REJEITAR | 💬 FEEDBACK
  ↓
[Raquel Responde]
├─ ✅ APROVADO → vai para Publisher
├─ ❌ REJEITADO → coleta feedback
  ↓
[Se Rejeitado]
├─ "Por quê rejeitou?" (Raquel escreve)
├─ Exemplo: "Tom muito robótico", "Dados desatualizados", "Hook fraco"
├─ Feedback é salvo no PostgreSQL
├─ Agente aprende para próxima geração
  ↓
[Training Loop]
├─ Cada feedback = dados de treinamento
├─ Atualiza prompt Ollama
├─ Próximo vídeo sai melhor
```

**Integração Telegram:**
```python
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def send_for_approval(video_path, metadata):
    keyboard = [
        [
            InlineKeyboardButton("✅ Aprovar", callback_data="approve"),
            InlineKeyboardButton("❌ Rejeitar", callback_data="reject"),
        ],
        [InlineKeyboardButton("💬 Feedback", callback_data="feedback")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    bot.send_video(
        chat_id=RAQUEL_CHAT_ID,
        video=open(video_path, 'rb'),
        caption=f"📹 Preview: {metadata['title']}\n\n{metadata['description']}",
        reply_markup=reply_markup,
        timeout=600
    )
    
    # Aguarda resposta
    response = await bot.get_callback_response()
    
    if response == "approve":
        publisher_queue.push(video_path)
    elif response == "reject":
        feedback = await get_feedback_from_raquel()
        store_feedback(video_path, feedback)
        retry_with_feedback(feedback)
```

---

### **AGENT 5: PUBLISHER** 🚀

**Função:** Publicar em YouTube + TikTok + Analytics

**Plataformas:**

#### YouTube Shorts
```python
def publish_youtube_shorts(video, metadata):
    youtube = YouTube_API()
    
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": metadata['title'],
                "description": metadata['description'],
                "tags": metadata['hashtags'],
                "categoryId": "22",  # People & Blogs
                "thumbnailUrl": metadata['thumbnail_url']
            },
            "status": {
                "privacyStatus": "public",
                "publishAt": metadata.get('scheduled_time', None)
            }
        },
        media_body=MediaFileUpload(video, mimetype='video/mp4')
    )
    
    response = request.execute()
    return response['id']  # Video ID
```

#### TikTok (Auto-upload)
```python
def publish_tiktok(video, metadata):
    tiktok = TikTok_API()
    
    # TikTok API exige autenticação via OAuth
    # Aqui fazemos upload automático
    response = tiktok.upload_video(
        file_path=video,
        caption=metadata['description'],
        hashtags=metadata['hashtags'],
        schedule_time=None  # Publicar imediatamente
    )
    
    return response['video_id']
```

**Analytics & Tracking:**
```python
def track_performance(video_id, platform):
    """Monitora views, engagement, conversão"""
    
    metrics = {
        "views": get_views(video_id, platform),
        "likes": get_likes(video_id, platform),
        "comments": get_comments(video_id, platform),
        "shares": get_shares(video_id, platform),
        "ctr": calculate_ctr(...),
        "conversion_rate": calculate_conversions(...)
    }
    
    # Salva no Analytics (Supabase)
    save_to_analytics(video_id, metrics)
    
    # Se performance for ruim, avisa o Prospector
    if metrics['views'] < 100:
        send_alert("Video underperforming", video_id)
```

---

## 🗄️ DATA MODELS

### PostgreSQL Schema

```sql
-- Jobs Queue
CREATE TABLE shorts_jobs (
    id SERIAL PRIMARY KEY,
    topic VARCHAR(500) NOT NULL,
    prospector_data JSONB,
    writer_script TEXT,
    executor_video_path VARCHAR(255),
    status ENUM('pending', 'writing', 'executing', 'reviewing', 'approved', 'published', 'rejected'),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    published_at TIMESTAMP,
    UNIQUE(topic, created_at::DATE)
);

-- Feedback Loop
CREATE TABLE shorts_feedback (
    id SERIAL PRIMARY KEY,
    job_id INTEGER REFERENCES shorts_jobs(id),
    feedback_text TEXT,
    category VARCHAR(100),  -- 'tone', 'data', 'hook', 'hook', etc
    severity ENUM('minor', 'major', 'critical'),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Published Videos
CREATE TABLE published_videos (
    id SERIAL PRIMARY KEY,
    job_id INTEGER REFERENCES shorts_jobs(id),
    platform VARCHAR(50),  -- 'youtube', 'tiktok', 'instagram'
    video_id VARCHAR(255),
    thumbnail_url VARCHAR(500),
    views INT DEFAULT 0,
    likes INT DEFAULT 0,
    comments INT DEFAULT 0,
    shares INT DEFAULT 0,
    ctr FLOAT,
    conversion_rate FLOAT,
    published_at TIMESTAMP,
    UNIQUE(platform, video_id)
);

-- Logs
CREATE TABLE agent_logs (
    id SERIAL PRIMARY KEY,
    agent_name VARCHAR(100),
    action VARCHAR(200),
    status VARCHAR(50),  -- 'success', 'error', 'pending'
    details JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🔌 INTEGRAÇÕES EXTERNAS

### 1. **Brapi API** (Dados de Mercado)
```
Endpoint: https://api.brapi.dev/api/v2/...
Tipos:
- quote: Preços de ações, índices
- news: Notícias de mercado
- search: Buscar símbolos
- economic: Indicadores macro (IPCA, Selic, etc)
Frequência: 5-min updates
```

### 2. **Ollama** (Geração de Scripts)
```
Modelo: llama2 (7B-13B) fine-tuned com Raquel Voice
Local: Docker container
Prompt: RAQUEL-VOICE-TEMPLATE.md
Timeout: 120s por geração
```

### 3. **ElevenLabs API** (Narração)
```
Endpoint: https://api.elevenlabs.io/v1/...
Voice ID: {RAQUEL_VOICE_ID} (clonada)
Model: multilingual_v2
Output format: MP3, 48kHz, mono
Custo: ~0.30 USD por minuto
```

### 4. **HeyGen API** (Avatar Video)
```
Endpoint: https://api.heygen.com/...
Avatar: Custom Raquel (ou padrão)
Input: Narração + script
Output: MP4, H.264, 1080p
Tempo: ~3-5 min por geração
```

### 5. **MoneyPrinter** (Video Composition)
```
Local: Docker container
Input: Script JSON + data
Output: Raw MP4 (sem áudio)
Engines:
- ImageMagick: Text overlays, compositions
- FFmpeg: Video merge, encoding
```

### 6. **Telegram Bot** (Approval Loop)
```
Bot: @9PillaMoneyPrinterBot
Chat: Raquel (@raquel_9pilla_id)
Modo: Polling + Webhook (quando disponível)
Callbacks: approve, reject, feedback
Timeout: 30 min (auto-retry se sem resposta)
```

### 7. **YouTube API** (Publishing)
```
Scope: youtube.upload, youtube.manage
Auth: OAuth 2.0 (Service Account)
Retry: Exponential backoff (3x)
Rate limit: 10k quota/day
```

### 8. **TikTok API** (Auto-Upload)
```
Endpoint: https://open.tiktokapis.com/...
Auth: OAuth (user session)
Upload limit: 50 videos/day
Hashtag auto-generation
```

---

## 🚀 DEPLOYMENT

### Docker Compose
```yaml
version: '3.8'

services:
  # PostgreSQL (Fila + Feedback)
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: shorts_factory
      POSTGRES_USER: raquel
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  # Ollama (Geração de Scripts)
  ollama:
    image: ollama/ollama:latest
    volumes:
      - ollama_data:/root/.ollama
    environment:
      OLLAMA_HOST: 0.0.0.0:11434
    ports:
      - "11434:11434"
    command: serve

  # MoneyPrinter (Video Composition)
  moneprinter:
    build:
      context: ./services/moneprinter
      dockerfile: Dockerfile
    environment:
      POSTGRES_URL: postgresql://raquel:${POSTGRES_PASSWORD}@postgres:5432/shorts_factory
      REDIS_URL: redis://redis:6379
    depends_on:
      - postgres
      - redis
    ports:
      - "8000:8000"

  # Redis (Cache + Queue)
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  # API Gateway (Squad Manager)
  api:
    build:
      context: ./services/api
      dockerfile: Dockerfile
    environment:
      DATABASE_URL: postgresql://raquel:${POSTGRES_PASSWORD}@postgres:5432/shorts_factory
      OLLAMA_URL: http://ollama:11434
      BRAPI_KEY: ${BRAPI_API_KEY}
      ELEVENLABS_KEY: ${ELEVENLABS_API_KEY}
      HEYGAN_KEY: ${HEYGAN_API_KEY}
      TELEGRAM_TOKEN: ${TELEGRAM_BOT_TOKEN}
      YOUTUBE_CREDENTIALS: ${YOUTUBE_CREDENTIALS_JSON}
    depends_on:
      - postgres
      - ollama
      - moneprinter
    ports:
      - "3000:3000"

volumes:
  postgres_data:
  ollama_data:
```

### Environment Variables
```bash
# APIs
BRAPI_API_KEY=xxx
ELEVENLABS_API_KEY=xxx
HEYGAN_API_KEY=xxx
TELEGRAM_BOT_TOKEN=xxx
YOUTUBE_CREDENTIALS_JSON='{ ... }'

# Database
POSTGRES_PASSWORD=xxx
POSTGRES_URL=postgresql://...

# Ollama
OLLAMA_HOST=http://ollama:11434
OLLAMA_MODEL=raquel-7b

# Raquel Voice (ElevenLabs)
RAQUEL_VOICE_ID=xxx

# Scheduling
CRON_SCHEDULE="0 9,12,16 * * 1-5"  # 09h, 12h, 16h Seg-Sex
TIMEZONE="America/Sao_Paulo"
```

---

## 📊 MÉTRICAS & MONITORAMENTO

### KPIs Principais
```
1. Generation Rate
   - Shorts gerados por dia
   - Target: 1-3/dia (escalável)

2. Approval Rate
   - % de vídeos aprovados na 1ª vez
   - Target: 70-80% (treina conforme feedback)

3. Publishing Rate
   - % de vídeos publicados/gerados
   - Target: 100% (após aprovação)

4. Engagement
   - Views, likes, comments por vídeo
   - Target: 500+ views/shorts (30 dias)

5. Conversion
   - % que clicam em link WhatsApp
   - Target: 2-5% (warm traffic)

6. Quality Score
   - Feedback positivo / total feedback
   - Target: 85%+ (melhora com treino)
```

### Dashboards (Supabase / Metabase)
```
Real-time:
- Jobs em processamento (status breakdown)
- Queue size (ProspectorWriter/Executor/Reviewer)
- API latencies (Brapi, ElevenLabs, HeyGen)
- Telegram approval time (avg/p95)

Daily:
- Videos published (YouTube, TikTok)
- Approval rate by feedback type
- Top performing shorts
- Engagement trends

Weekly:
- Traffic to blog (organic)
- Conversions to Turma 9Pilla
- Cost per acquisition (Brapi+APIs)
- ROI calculation
```

---

## ✅ CHECKLIST IMPLEMENTAÇÃO

- [ ] PostgreSQL setup + migrations
- [ ] Ollama container + raquel-7b model
- [ ] Brapi API integration + test
- [ ] ElevenLabs API integration + Raquel voice
- [ ] HeyGen API integration
- [ ] MoneyPrinter Docker container
- [ ] Telegram bot + callback handlers
- [ ] YouTube OAuth setup
- [ ] TikTok API integration (ou manual upload)
- [ ] Squad Agents (5 agents em OpenSquad)
- [ ] Docker Compose + .env
- [ ] Monitoring + Supabase dashboard
- [ ] Cron jobs (scheduling)
- [ ] Logging centralizado
- [ ] Backup strategy (PostgreSQL + vídeos)

---

## 🔗 Referências

**Documentos relacionados:**
- `RAQUEL-VOICE-TEMPLATE.md` — prompt para Ollama
- `MORNING-CALL-SEO-STRATEGY.md` — conteúdo complementar
- `SQUAD-INTEGRATION-CHECKLIST.md` — roadmap detalhado

**APIs & Ferramentas:**
- Brapi: https://brapi.dev
- Ollama: https://ollama.ai
- ElevenLabs: https://elevenlabs.io
- HeyGen: https://heygen.com
- MoneyPrinter: https://github.com/FujiwaraChoki/MoneyPrinter
- YouTube Data API: https://developers.google.com/youtube/v3
- TikTok Open API: https://developers.tiktok.com

---

**Documento criado:** Junho 2026  
**Autor:** Claude Code  
**Status:** 🟢 Pronto para desenvolvimento
