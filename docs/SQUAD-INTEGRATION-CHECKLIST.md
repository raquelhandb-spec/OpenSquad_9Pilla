# ✅ Squad Integration Checklist — Roadmap Detalhado

**Versão:** 1.0  
**Data:** Junho 2026  
**Status:** 🔵 Implementação começando  
**Branch:** `claude/moneprinter-9pilla-integration-9gm87x`

---

## 📋 FASES DE IMPLEMENTAÇÃO

---

## 🔴 PHASE 1: SETUP & TRAINING (2-3 horas)

### 1.1 — Análise & Documentação (✓ COMPLETO)

- [x] Analisar 16 Morning Calls publicados
- [x] Extrair padrões de VOZ (Raquel)
- [x] Criar `RAQUEL-VOICE-TEMPLATE.md`
- [x] Criar `SHORTS-MAESTRO-ARCHITECTURE.md`
- [x] Criar `MORNING-CALL-SEO-STRATEGY.md`
- [x] Criar `SQUAD-INTEGRATION-CHECKLIST.md` (este arquivo)

**Tempo:** 3h  
**Resultado:** 4 docs completos no GitHub

---

### 1.2 — Setup Local (PostgreSQL + MoneyPrinter + Ollama)

#### Pré-requisitos
```bash
# Verificar versões
docker --version        # >= 20.10
docker-compose --version # >= 1.29
git --version           # >= 2.30
```

#### Instalação PostgreSQL
```bash
# Via Docker
docker run --name postgres-shorts \
  -e POSTGRES_USER=raquel \
  -e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} \
  -e POSTGRES_DB=shorts_factory \
  -v postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  -d postgres:15-alpine

# Aguardar init (~10s)
sleep 10

# Testar conexão
psql -h localhost -U raquel -d shorts_factory -c "SELECT 1;"
```

**Checklist:**
- [ ] PostgreSQL rodando (`docker ps`)
- [ ] Database `shorts_factory` criada
- [ ] User `raquel` com permissões
- [ ] Conexão testada com `psql`

#### Instalação Ollama
```bash
# Download + Install
# MacOS/Windows: https://ollama.ai/download
# Linux:
curl https://ollama.ai/install.sh | sh

# Iniciar daemon
ollama serve &

# Aguardar inicialização (~30s)
sleep 30

# Testar
curl http://localhost:11434/api/tags
```

**Modelos a baixar:**
```bash
# Modelo padrão (para teste)
ollama pull llama2:7b

# (Opcional) Modelo maior (mais preciso)
ollama pull llama2:13b

# (Opcional) Mistral (mais rápido)
ollama pull mistral:7b
```

**Checklist:**
- [ ] Ollama daemon rodando
- [ ] Modelos baixados (`ollama list`)
- [ ] Resposta do `/api/tags` endpoint
- [ ] Teste de prompt (ex: `ollama run llama2 "Olá"`)

#### Instalação MoneyPrinter
```bash
# Clone repository
git clone https://github.com/FujiwaraChoki/MoneyPrinter.git
cd MoneyPrinter

# Criar .env
cat > .env << EOF
POSTGRES_URL=postgresql://raquel:${POSTGRES_PASSWORD}@localhost:5432/shorts_factory
REDIS_URL=redis://localhost:6379
IMAGEMAGICK_PATH=/usr/bin/convert
EOF

# Instalar dependências
pip install -r requirements.txt

# Testar
python -m moneprinter.cli --help
```

**Checklist:**
- [ ] MoneyPrinter clonado
- [ ] `.env` criado com credenciais
- [ ] `requirements.txt` instalado
- [ ] CLI funcional (`python -m moneprinter --help`)

#### Instalação Redis (opcional, mas recomendado)
```bash
docker run --name redis-shorts \
  -p 6379:6379 \
  -d redis:7-alpine

# Testar
redis-cli ping  # PONG
```

**Checklist:**
- [ ] Redis rodando (opcional)
- [ ] Ping funcional
- [ ] Connection pooling testado

---

### 1.3 — Setup Telegram Bot

#### Criar Bot
```bash
# No Telegram:
# 1. Abrir @BotFather
# 2. Comando: /newbot
# 3. Nome: "Shorts-Maestro-9Pilla"
# 4. Username: "shorts_maestro_9pilla_bot" (único)
# 5. Copiar token

# Salvar token em .env
TELEGRAM_BOT_TOKEN=xxx:yyy
```

#### Testar Bot
```bash
# Teste básico
curl -X POST https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getMe

# Resultado esperado:
# { "ok": true, "result": { "id": 123, "username": "shorts_maestro..." } }
```

#### Setup Chat ID
```bash
# No Telegram:
# 1. Falar com bot: /start
# 2. Bot responde com chat_id
# 3. Salvar em .env

TELEGRAM_CHAT_ID=123456
```

**Checklist:**
- [ ] Bot criado no @BotFather
- [ ] Token salvo em `.env`
- [ ] Chat ID obtido
- [ ] Teste de envio: `/getMe` funciona

---

### 1.4 — Setup Brapi (Dados de Mercado)

```bash
# Em https://brapi.dev:
# 1. Criar conta
# 2. Gerar API Key
# 3. Testar endpoint

BRAPI_API_KEY=xxx

# Testar
curl -s https://api.brapi.dev/api/v2/quote/PETR4 \
  -H "Authorization: Bearer ${BRAPI_API_KEY}" | jq
```

**Checklist:**
- [ ] Conta Brapi criada
- [ ] API Key gerada
- [ ] Teste de quote (`PETR4`, `VALE3`, `IBOV`)
- [ ] Teste de news (últimas notícias)

---

## 🟡 PHASE 2: MVP SQUAD (3-5 horas)

### 2.1 — Criar Agents no OpenSquad

#### Agent 1: PROSPECTOR
```python
# /squads/shorts-maestro/agents/prospector.py

import requests
from datetime import datetime

class ProspectorAgent:
    def __init__(self, brapi_key):
        self.brapi_key = brapi_key
    
    def fetch_news(self):
        """Fetch market news from Brapi"""
        headers = {"Authorization": f"Bearer {self.brapi_key}"}
        response = requests.get(
            "https://api.brapi.dev/api/v2/news",
            headers=headers,
            params={"limit": 10}
        )
        return response.json()
    
    def rank_topics(self, news):
        """Rank topics by relevance"""
        # Priorizar: Geopolítica > Inflação > Bolsa > Educação
        priorities = {
            "oriente médio": 10,
            "petróleo": 8,
            "inflação": 7,
            "ibovespa": 6,
            "fed": 7,
            "dólar": 6,
        }
        
        for item in news:
            for keyword, score in priorities.items():
                if keyword.lower() in item['title'].lower():
                    item['relevance_score'] = score
                    break
        
        return sorted(news, key=lambda x: x.get('relevance_score', 0), reverse=True)
    
    def run(self):
        news = self.fetch_news()
        ranked = self.rank_topics(news)
        top_topic = ranked[0] if ranked else None
        
        return {
            "topic": top_topic['title'],
            "data": top_topic,
            "timestamp": datetime.now().isoformat()
        }
```

**Checklist:**
- [ ] Arquivo criado: `agents/prospector.py`
- [ ] Classe `ProspectorAgent` implementada
- [ ] Método `run()` testado com Brapi
- [ ] Output retorna tópico + dados

---

#### Agent 2: WRITER
```python
# /squads/shorts-maestro/agents/writer.py

import requests
import json
from datetime import datetime

class WriterAgent:
    def __init__(self, ollama_host="http://localhost:11434"):
        self.ollama_host = ollama_host
        self.model = "llama2"  # ou raquel-7b (fine-tuned)
    
    def generate_script(self, topic, market_data):
        """Generate YouTube Shorts script using Ollama"""
        
        prompt = f"""
Você é Raquel, criadora da 9Pilla.

Gere um script de YouTube Shorts sobre: "{topic}"

DADOS:
- Ibovespa: {market_data.get('ibov')} pts
- Dólar: R$ {market_data.get('dolar')}
- Petróleo Brent: US$ {market_data.get('brent')}/barril

ESTRUTURA:
1. Hook (0-2s): Capte atenção imediatamente
2. Delivery (2-50s): 1 ponto, 1 história, sem fluff
3. Punchline (50-60s): Feche com ênfase e call-to-action

TON: Conversacional, educativo, sem tabu
SEMPRE: Conecte notícia → seu bolso → ação
MISSÃO: "Dinheiro não é destino. É a jornada para a liberdade."

FORMATO SAÍDA:
=== SCRIPT SHORTS ===
HOOK (0-2s):
[Visual]: ...
[Audio]: ...

DELIVERY (2-50s):
[Visual]: ...
[Script]: ...

PUNCHLINE (50-60s):
[Visual]: ...
[Script]: ...

=== METADATA ===
TITLE: [título curiosity-driven]
DESCRIPTION: [descrição com hashtags]
HASHTAGS: #Shorts #Finança ...
"""
        
        response = requests.post(
            f"{self.ollama_host}/api/generate",
            json={"model": self.model, "prompt": prompt},
            stream=False
        )
        
        script = response.json()['response']
        return script
    
    def run(self, topic, market_data):
        script = self.generate_script(topic, market_data)
        
        return {
            "script": script,
            "topic": topic,
            "generated_at": datetime.now().isoformat()
        }
```

**Checklist:**
- [ ] Arquivo criado: `agents/writer.py`
- [ ] Classe `WriterAgent` implementada
- [ ] Ollama endpoint configurado
- [ ] Teste com prompt simples
- [ ] Output retorna script formatado

---

#### Agent 3: EXECUTOR
```python
# /squads/shorts-maestro/agents/executor.py

import subprocess
import requests
import json
from pathlib import Path

class ExecutorAgent:
    def __init__(self, moneprinter_path="/path/to/MoneyPrinter"):
        self.moneprinter = moneprinter_path
    
    def generate_video_moneprinter(self, script, data):
        """Execute MoneyPrinter CLI"""
        
        script_file = Path("/tmp/script.json")
        script_file.write_text(json.dumps({
            "topic": script['topic'],
            "script": script['script'],
            "data": data
        }))
        
        result = subprocess.run([
            "python", "-m", "moneprinter",
            "--script", str(script_file),
            "--output", "/tmp/video_raw.mp4"
        ], capture_output=True, text=True)
        
        return "/tmp/video_raw.mp4" if result.returncode == 0 else None
    
    def generate_narration_elevenlabs(self, script_text, voice_id):
        """Generate narration via ElevenLabs"""
        
        response = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            headers={
                "xi-api-key": self.elevenlabs_key,
                "Content-Type": "application/json"
            },
            json={"text": script_text, "model_id": "eleven_monolingual_v1"}
        )
        
        audio_path = "/tmp/narration.mp3"
        with open(audio_path, 'wb') as f:
            f.write(response.content)
        
        return audio_path
    
    def merge_video_audio_ffmpeg(self, video_path, audio_path):
        """Merge video + audio with FFmpeg"""
        
        output = "/tmp/shorts_final.mp4"
        
        subprocess.run([
            "ffmpeg", "-i", video_path, "-i", audio_path,
            "-c:v", "copy", "-c:a", "aac",
            "-shortest", output
        ], capture_output=True)
        
        return output
    
    def run(self, script, market_data, elevenlabs_key, voice_id):
        # 1. MoneyPrinter
        video = self.generate_video_moneprinter(script, market_data)
        
        # 2. ElevenLabs
        audio = self.generate_narration_elevenlabs(
            script['script'], 
            voice_id
        )
        
        # 3. Merge
        final_video = self.merge_video_audio_ffmpeg(video, audio)
        
        return {
            "video_path": final_video,
            "status": "ready",
            "created_at": datetime.now().isoformat()
        }
```

**Checklist:**
- [ ] Arquivo criado: `agents/executor.py`
- [ ] MoneyPrinter integration testada
- [ ] ElevenLabs integration testada
- [ ] FFmpeg merge funcionando
- [ ] Output retorna vídeo final

---

#### Agent 4: REVIEWER
```python
# /squads/shorts-maestro/agents/reviewer.py

import requests
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime

class ReviewerAgent:
    def __init__(self, telegram_token, chat_id, db):
        self.bot = Bot(token=telegram_token)
        self.chat_id = chat_id
        self.db = db
    
    async def send_for_approval(self, video_path, metadata):
        """Send video preview to Telegram"""
        
        keyboard = [
            [
                InlineKeyboardButton("✅ Aprovado", callback_data="approve"),
                InlineKeyboardButton("❌ Rejeitado", callback_data="reject"),
            ],
            [InlineKeyboardButton("💬 Feedback", callback_data="feedback")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        with open(video_path, 'rb') as f:
            message = await self.bot.send_video(
                chat_id=self.chat_id,
                video=f,
                caption=f"📹 {metadata['title']}\n\n{metadata['description']}",
                reply_markup=reply_markup
            )
        
        # Store message_id para tracking
        self.db.store_review_request(
            message_id=message.message_id,
            video_path=video_path,
            metadata=metadata
        )
        
        return message.message_id
    
    async def wait_for_response(self, message_id, timeout=1800):  # 30 min timeout
        """Aguarda resposta de Raquel"""
        
        # Polling (simplificado)
        # Em produção, usar webhook
        start_time = datetime.now()
        
        while (datetime.now() - start_time).seconds < timeout:
            response = self.db.get_review_response(message_id)
            
            if response:
                return response
            
            await asyncio.sleep(5)  # Check a cada 5 segundos
        
        return {"status": "timeout", "action": "auto_reject"}
    
    def run(self, video_path, metadata):
        import asyncio
        
        # Send para Telegram
        message_id = asyncio.run(self.send_for_approval(video_path, metadata))
        
        # Aguardar resposta
        response = asyncio.run(self.wait_for_response(message_id))
        
        return {
            "video_path": video_path,
            "status": response['status'],
            "action": response['action'],  # 'approve', 'reject', 'feedback'
            "feedback": response.get('feedback', None),
            "reviewed_at": datetime.now().isoformat()
        }
```

**Checklist:**
- [ ] Arquivo criado: `agents/reviewer.py`
- [ ] Telegram bot funcionando
- [ ] Callbacks funcionando (approve/reject)
- [ ] Feedback storage em BD
- [ ] Timeout handling implementado

---

#### Agent 5: PUBLISHER
```python
# /squads/shorts-maestro/agents/publisher.py

import requests
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import json

class PublisherAgent:
    def __init__(self, youtube_credentials, db):
        self.youtube = self._init_youtube(youtube_credentials)
        self.db = db
    
    def _init_youtube(self, creds_json):
        creds = Credentials.from_service_account_info(json.loads(creds_json))
        return build('youtube', 'v3', credentials=creds)
    
    def publish_youtube_shorts(self, video_path, metadata):
        """Publish to YouTube Shorts"""
        
        request = self.youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": metadata['title'],
                    "description": metadata['description'],
                    "tags": metadata['hashtags'],
                    "categoryId": "22"
                },
                "status": {
                    "privacyStatus": "public"
                }
            },
            media_body=MediaFileUpload(video_path, mimetype='video/mp4')
        )
        
        response = request.execute()
        
        self.db.store_published_video({
            "platform": "youtube",
            "video_id": response['id'],
            "url": f"https://youtube.com/shorts/{response['id']}",
            "published_at": datetime.now().isoformat()
        })
        
        return response['id']
    
    def publish_tiktok(self, video_path, metadata):
        """Publish to TikTok (via API ou manual)"""
        
        # TikTok API exige user auth complexa
        # Por enquanto: salvar em fila para upload manual
        
        self.db.queue_tiktok_upload({
            "video_path": video_path,
            "metadata": metadata,
            "status": "pending"
        })
        
        return {"status": "queued", "note": "Manual upload needed"}
    
    def run(self, video_path, metadata):
        # YouTube (automático)
        youtube_id = self.publish_youtube_shorts(video_path, metadata)
        
        # TikTok (fila para upload)
        tiktok_status = self.publish_tiktok(video_path, metadata)
        
        return {
            "video_path": video_path,
            "youtube_id": youtube_id,
            "youtube_url": f"https://youtube.com/shorts/{youtube_id}",
            "tiktok_status": tiktok_status,
            "published_at": datetime.now().isoformat()
        }
```

**Checklist:**
- [ ] Arquivo criado: `agents/publisher.py`
- [ ] YouTube OAuth setup
- [ ] Teste de upload (vídeo teste)
- [ ] TikTok queue funcionando
- [ ] Analytics tracking implementado

---

### 2.2 — Integrar Agents no OpenSquad

```yaml
# /squads/shorts-maestro/squad.yaml

name: "Shorts-Maestro"
description: "Automação de YouTube Shorts para 9Pilla"
version: "1.0.0"

agents:
  - name: "Prospector"
    type: "data_gatherer"
    file: "agents/prospector.py"
    class: "ProspectorAgent"
    inputs:
      - brapi_key: "${BRAPI_API_KEY}"
    outputs:
      - topic: string
      - data: json
  
  - name: "Writer"
    type: "content_generator"
    file: "agents/writer.py"
    class: "WriterAgent"
    inputs:
      - topic: "Prospector.topic"
      - market_data: "Prospector.data"
      - ollama_host: "http://localhost:11434"
    outputs:
      - script: string
  
  - name: "Executor"
    type: "video_generator"
    file: "agents/executor.py"
    class: "ExecutorAgent"
    inputs:
      - script: "Writer.script"
      - market_data: "Prospector.data"
      - elevenlabs_key: "${ELEVENLABS_API_KEY}"
      - voice_id: "${RAQUEL_VOICE_ID}"
    outputs:
      - video_path: string
  
  - name: "Reviewer"
    type: "approval_manager"
    file: "agents/reviewer.py"
    class: "ReviewerAgent"
    inputs:
      - video_path: "Executor.video_path"
      - metadata: "Writer.metadata"
      - telegram_token: "${TELEGRAM_BOT_TOKEN}"
      - chat_id: "${TELEGRAM_CHAT_ID}"
    outputs:
      - status: enum[approved, rejected, timeout]
      - feedback: string
  
  - name: "Publisher"
    type: "distribution_manager"
    file: "agents/publisher.py"
    class: "PublisherAgent"
    inputs:
      - video_path: "Executor.video_path"
      - metadata: "Writer.metadata"
      - condition: "Reviewer.status == 'approved'"
      - youtube_credentials: "${YOUTUBE_CREDENTIALS_JSON}"
    outputs:
      - youtube_id: string
      - youtube_url: string
      - tiktok_status: string

workflow:
  - step: 1
    agents: ["Prospector"]
    
  - step: 2
    agents: ["Writer"]
    depends_on: ["Prospector"]
    
  - step: 3
    agents: ["Executor"]
    depends_on: ["Writer"]
    
  - step: 4
    agents: ["Reviewer"]
    depends_on: ["Executor"]
    conditional: true
    
  - step: 5
    agents: ["Publisher"]
    depends_on: ["Reviewer"]
    condition: "status == 'approved'"

schedule:
  frequency: "daily"
  time: "09:00"
  timezone: "America/Sao_Paulo"
  days: ["MON", "TUE", "WED", "THU", "FRI"]
```

**Checklist:**
- [ ] Squad YAML criado
- [ ] Todos 5 agents registrados
- [ ] Workflow dependencies corretos
- [ ] Schedule configurado (Seg-Sex 09h)

---

### 2.3 — Testes com 3 Shorts Reais

#### Teste 1: Shorts sobre Petróleo
```bash
# Tema: "Petróleo acima de US$ 100 — por que afeta você"

cd /squads/shorts-maestro

python -c "
from squad import ShortsMaestroSquad
squad = ShortsMaestroSquad()
result = squad.run(
    topic='Petróleo acima de US$ 100',
    dry_run=False  # Gerar vídeo real
)
print(json.dumps(result, indent=2))
"
```

**Validar:**
- [ ] Script gerado (sem erros)
- [ ] Vídeo renderizado (60s, 9:16, 1080p)
- [ ] Narração sincronizada
- [ ] Preview enviado para Telegram

#### Teste 2: Shorts sobre IBOVESPA
```bash
# Tema: "Por que IBOVESPA caiu 3% em um dia"

# Mesmo processo...
```

#### Teste 3: Shorts sobre Inflação
```bash
# Tema: "IPCA subiu — o que fazer com seu dinheiro"

# Mesmo processo...
```

**Checklist:**
- [ ] Teste 1 completo (Petróleo)
- [ ] Teste 2 completo (IBOVESPA)
- [ ] Teste 3 completo (Inflação)
- [ ] 1 vídeo publicado no YouTube (teste)
- [ ] 1 vídeo publicado no TikTok (teste)
- [ ] Feedback de Raquel coletado

---

## 🟢 PHASE 3: PRODUCTION (1-2 horas)

### 3.1 — Deploy em Produção

```bash
# 1. Build Docker images
docker-compose build

# 2. Start services
docker-compose up -d

# 3. Run migrations
docker-compose exec api python manage.py migrate

# 4. Verify all services
docker-compose ps
curl http://localhost:3000/health

# 5. Setup cron job (1x/dia)
# Adicionar ao crontab:
# 0 9 * * 1-5 /path/to/run_squad.sh
```

**Checklist:**
- [ ] Docker Compose rodando
- [ ] Todos services healthy
- [ ] Migrations executadas
- [ ] Cron job configurado

---

### 3.2 — Setup de Monitoramento

```bash
# Supabase dashboard para analytics
# Criar tabelas em PostgreSQL:

CREATE TABLE IF NOT EXISTS squad_runs (
    id SERIAL PRIMARY KEY,
    run_id UUID DEFAULT gen_random_uuid(),
    status VARCHAR(50),  -- 'success', 'failed', 'timeout'
    topic VARCHAR(500),
    prospector_time INT,
    writer_time INT,
    executor_time INT,
    reviewer_time INT,
    publisher_time INT,
    total_time INT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS published_videos (
    id SERIAL PRIMARY KEY,
    youtube_id VARCHAR(255) UNIQUE,
    youtube_url VARCHAR(500),
    tiktok_status VARCHAR(50),
    views INT DEFAULT 0,
    likes INT DEFAULT 0,
    comments INT DEFAULT 0,
    published_at TIMESTAMP,
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS reviewer_feedback (
    id SERIAL PRIMARY KEY,
    video_id VARCHAR(255),
    feedback TEXT,
    category VARCHAR(100),
    severity VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW()
);
```

**Checklist:**
- [ ] Tabelas criadas em PostgreSQL
- [ ] Conexão Supabase testada
- [ ] Dashboard Metabase configurado
- [ ] Alertas configurados (erro, timeout)

---

### 3.3 — Publicação do Primeiro Shorts em Produção

```bash
# Trigger squad manualmente
curl -X POST http://localhost:3000/api/squad/run \
  -H "Content-Type: application/json" \
  -d '{"manual": true}'

# Monitorar
curl http://localhost:3000/api/squad/status

# Resultado esperado:
# {
#   "run_id": "uuid-...",
#   "status": "running",
#   "step": "prospector",
#   "progress": "20%"
# }
```

**Checklist:**
- [ ] Squad rodou sem erros
- [ ] Vídeo gerado e aprovado
- [ ] YouTube publicado com sucesso
- [ ] TikTok fila criada
- [ ] Analytics registrado

---

## 📋 CREDENCIAIS NECESSÁRIAS

Para **COMEÇAR AGORA**, você precisa entregar:

```env
# OBRIGATÓRIO (para Phase 2 + 3)
BRAPI_API_KEY=xxxxx
ELEVENLABS_API_KEY=xxxxx
ELEVENLABS_VOICE_ID=xxxxx  # Voz Raquel (clonada ou padrão)
HEYGAN_API_KEY=xxxxx  # Se usar HeyGen
TELEGRAM_BOT_TOKEN=xxxxx
TELEGRAM_CHAT_ID=xxxxx
YOUTUBE_CREDENTIALS_JSON='{ ... }'

# BANCO DE DADOS
POSTGRES_PASSWORD=xxxxx
POSTGRES_URL=postgresql://raquel:xxxxx@localhost:5432/shorts_factory

# OPCIONAL (nice-to-have)
REDDIT_API_KEY=xxxxx  # Para trending topics
TWITTER_API_KEY=xxxxx  # Para trending topics
TIKTOK_API_KEY=xxxxx  # Para auto-upload TikTok
```

---

## 🎯 TIMELINE

| Fase | Descrição | Duração | Status |
|------|-----------|---------|--------|
| **1** | Setup + Training | 2-3h | ✓ Completo (documentação) |
| **2** | MVP Squad + Testes | 3-5h | 🟡 Aguardando credenciais |
| **3** | Production + Deploy | 1-2h | 🔴 Depois Phase 2 |
| **4** | Blog SEO (paralelo) | 3-4h | 🔴 Depois Phase 1 |

**Total:** ~9-14 horas para MVP completo

**Timeline Realista:**
- Hoje: Phase 1 ✓
- Amanhã (assim que credenciais): Phase 2 + 3
- Próxima semana: Blog SEO
- **Resultado em 48 horas:** Sistema rodando 100%

---

## ✅ VALIDATION GATES

Antes de avançar para próxima fase:

### Gate 1 (Phase 1 → 2)
- [ ] 4 documentos finalizados no GitHub
- [ ] PostgreSQL + Ollama + MoneyPrinter rodando locally
- [ ] Telegram bot funcionando
- [ ] Brapi API testada

### Gate 2 (Phase 2 → 3)
- [ ] 5 Agents criados e testados individually
- [ ] Squad orchestration funcionando
- [ ] 3 shorts gerados e aprovados
- [ ] Pelo menos 1 shorts publicado no YouTube

### Gate 3 (Phase 3 → Escalação)
- [ ] Sistema rodando 1x/dia automático
- [ ] Analytics dashboard operacional
- [ ] Blog SEO configurado
- [ ] 10+ vídeos publicados com sucesso

---

## 📞 SUPORTE & DEBUGGING

### Comum Issues & Soluções

#### Ollama não responde
```bash
# Verificar daemon
ollama serve --debug

# Ou reiniciar
pkill -f ollama
ollama serve &
```

#### PostgreSQL connection refused
```bash
# Verificar container
docker ps | grep postgres

# Check logs
docker logs postgres-shorts

# Reiniciar
docker restart postgres-shorts
```

#### Telegram timeout no review
```bash
# Aumentar timeout em reviewer.py
timeout = 3600  # 1 hora ao invés de 30 min

# Ou implementar webhook ao invés de polling
# Docs: https://core.telegram.org/bots/webhooks
```

#### ElevenLabs quota exceeded
```bash
# Usar voz padrão ao invés de clonada
# Ou esperar próximo ciclo de billing
# Logs: check `/logs/elevenlabs_errors.log`
```

---

## 🔗 Referências

**Documentos relacionados:**
- `RAQUEL-VOICE-TEMPLATE.md` — conteúdo dos scripts
- `SHORTS-MAESTRO-ARCHITECTURE.md` — detalhes técnicos
- `MORNING-CALL-SEO-STRATEGY.md` — estratégia blog

**Repos & APIs:**
- MoneyPrinter: https://github.com/FujiwaraChoki/MoneyPrinter
- Ollama: https://ollama.ai
- Brapi: https://brapi.dev
- ElevenLabs: https://elevenlabs.io
- YouTube Data API: https://developers.google.com/youtube/v3
- Telegram Bot API: https://core.telegram.org/bots/api

---

**Documento criado:** Junho 2026  
**Autor:** Claude Code  
**Status:** 🟢 Pronto para implementação

---

## 🚀 PRÓXIMO PASSO

**Raquel**, quando você tiver as credenciais, me avisa que eu:
1. ✅ Configuro Phase 2 completo
2. ✅ Testo Squad com 3 shorts reais
3. ✅ Deploy em produção
4. ✅ Setup Blog SEO em paralelo

**Tá tudo documentado. Bora fazer isso acontecer!** 🔥
