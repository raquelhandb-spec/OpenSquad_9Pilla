# 🎬 Shorts-Maestro Squad

**Automação completa de YouTube Shorts para 9Pilla**

Integração com:
- 📊 Brapi API (dados de mercado em tempo real)
- 🧠 Ollama (geração de scripts com Raquel Voice)
- 🎙️ ElevenLabs (narração IA)
- 🎬 HeyGen (vídeo com avatar)
- 💬 Telegram (aprovação via bot)
- 🚀 YouTube/TikTok (publicação automática)

---

## 📁 Estrutura

```
squads/shorts-maestro/
├── agents/
│   ├── __init__.py
│   ├── prospector.py       # Busca dados de mercado (Brapi)
│   ├── writer.py           # Gera scripts com Raquel Voice (Ollama)
│   ├── executor.py         # Renderiza vídeos (MoneyPrinter+ElevenLabs)
│   ├── reviewer.py         # Envia para aprovação (Telegram)
│   └── publisher.py        # Publica em YouTube/TikTok
├── config/
│   ├── squad.yaml          # Definição do Squad
│   └── .env.example        # Template de variáveis
├── scripts/
│   ├── test_prospector.py
│   └── run_full_pipeline.py
└── README.md
```

---

## 🚀 Quick Start

### 1. Setup

```bash
# Clonar o repo
cd /home/user/OpenSquad_9Pilla/squads/shorts-maestro

# Criar .env
cp config/.env.example .env

# Editar .env com suas credenciais
nano .env
```

### 2. Testar Prospector Agent

```bash
python agents/prospector.py
```

Output esperado:
```json
{
  "status": "success",
  "top_topic": {
    "title": "PETR4 em movimento: -1.76% - Análise do dia",
    "relevance_score": 9
  },
  "market_data": {...}
}
```

### 3. Próximos Passos

- [ ] Implementar Writer Agent (Ollama)
- [ ] Implementar Executor Agent (MoneyPrinter + ElevenLabs)
- [ ] Implementar Reviewer Agent (Telegram)
- [ ] Implementar Publisher Agent (YouTube)
- [ ] Integrar no OpenSquad

---

## 🔧 Agents

### **Prospector** ✅ (COMPLETO)
```python
agent = ProspectorAgent(brapi_key="seu_token")
result = agent.run()
# → top_topic, market_data, timestamp
```

**Responsabilidades:**
- Buscar dados de mercado via Brapi
- Identificar tópicos trending
- Rankear por relevância
- Coletar feedback de vídeos rejeitados

---

### **Writer** 🔲 (PRÓXIMO)
Gera scripts de YouTube Shorts usando Ollama com Raquel Voice.

```python
agent = WriterAgent(ollama_host="http://localhost:11434")
result = agent.run(
    topic="PETR4 em movimento",
    market_data={...}
)
# → script (formatado), metadata, title, description
```

---

### **Executor** 🔲
Renderiza vídeo usando MoneyPrinter + ElevenLabs.

```python
agent = ExecutorAgent(
    moneprinter_path="/path/to/MoneyPrinter",
    elevenlabs_key="xxx",
    voice_id="xxx"
)
result = agent.run(script, market_data)
# → video_path, thumbnail, metadata
```

---

### **Reviewer** 🔲
Envia para aprovação via Telegram bot.

```python
agent = ReviewerAgent(
    telegram_token="xxx",
    chat_id="xxx"
)
result = agent.run(video_path, metadata)
# → status (approved/rejected), feedback
```

---

### **Publisher** 🔲
Publica em YouTube/TikTok.

```python
agent = PublisherAgent(youtube_credentials)
result = agent.run(video_path, metadata)
# → youtube_id, youtube_url, tiktok_status
```

---

## 🔑 Credenciais Necessárias

```env
# Brapi (Dados de Mercado)
BRAPI_API_KEY=tky3Vocipoj9ZocxEumbCe

# Ollama (Geração de Scripts)
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama2  # ou raquel-7b (fine-tuned)

# ElevenLabs (Narração)
ELEVENLABS_API_KEY=xxx
ELEVENLABS_VOICE_ID=xxx

# HeyGen (Avatar Video)
HEYGAN_API_KEY=xxx

# Telegram (Aprovação)
TELEGRAM_BOT_TOKEN=xxx
TELEGRAM_CHAT_ID=xxx

# YouTube (Publicação)
YOUTUBE_CREDENTIALS_JSON='{ ... }'

# MoneyPrinter
MONEPRINTER_PATH=/path/to/MoneyPrinter
```

---

## 📊 Fluxo Completo

```
1. PROSPECTOR
   ├─ Brapi → Buscar dados de mercado
   ├─ Identificar tópicos trending
   └─ Output: top_topic + market_data

2. WRITER
   ├─ Ollama → Gerar script com Raquel Voice
   ├─ Estrutura: Hook → Delivery → Punchline
   └─ Output: script + metadata

3. EXECUTOR
   ├─ MoneyPrinter → Renderizar vídeo base
   ├─ ElevenLabs → Narração sincronizada
   ├─ HeyGen → Avatar (opcional)
   └─ Output: video_path (MP4 60s, 9:16)

4. REVIEWER
   ├─ Telegram → Enviar preview
   ├─ Raquel → Aprovar/Rejeitar
   ├─ Se rejeitado → Coletar feedback
   └─ Output: status + feedback

5. PUBLISHER
   ├─ YouTube → Publicar Shorts
   ├─ TikTok → Queue para upload
   └─ Output: youtube_id, urls
```

---

## 🧪 Testes

### Testar Prospector
```bash
python agents/prospector.py
```

### Rodas todos os agents (depois de implementados)
```bash
python scripts/run_full_pipeline.py
```

---

## 📝 Documentação

Ver `/docs/` no repo root:
- `RAQUEL-VOICE-TEMPLATE.md` — Padrões da voz
- `SHORTS-MAESTRO-ARCHITECTURE.md` — Arquitetura completa
- `SQUAD-INTEGRATION-CHECKLIST.md` — Roadmap detalhado

---

## 🔄 Fluxo de Feedback

```
Vídeo Rejeitado
    ↓
Feedback do Telegram
    ↓
Armazenar em BD
    ↓
Atualizar Ollama Prompt
    ↓
Próximo vídeo sai melhor
```

---

## 📈 Métricas

**KPIs Rastreados:**
- Videos gerados/dia
- Taxa de aprovação (1ª tentativa)
- Views + Engagement por vídeo
- CTR para WhatsApp
- Custo por vídeo publicado

---

## 🚀 Próximos Passos

1. ✅ Prospector Agent (PRONTO)
2. 🔲 Writer Agent (Ollama)
3. 🔲 Executor Agent (MoneyPrinter)
4. 🔲 Reviewer Agent (Telegram)
5. 🔲 Publisher Agent (YouTube)
6. 🔲 Integração OpenSquad
7. 🔲 Deploy em produção

---

**Status:** 🟡 Em desenvolvimento  
**Última atualização:** Junho 2026
