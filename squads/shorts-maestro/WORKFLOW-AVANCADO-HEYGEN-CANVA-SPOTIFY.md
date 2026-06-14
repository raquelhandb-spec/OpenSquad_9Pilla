# 🚀 WORKFLOW AVANÇADO 9PILLA — SHORTS + YOUTUBE + SPOTIFY + CANVA

**Data:** 13 de junho de 2026  
**Objetivo:** Sistema integrado de publicação multi-plataforma  
**Status:** 🚀 CONSTRUÇÃO

---

## 📊 EVOLUÇÃO ATÉ AQUI (Resumo)

### ✅ JÁ IMPLEMENTADO (Junho 1-13)

| Componente | Status | Data | Resultado |
|-----------|--------|------|-----------|
| **Prospector Agent** | ✅ | Jun 1 | Busca dados Brapi |
| **Writer Agent (Claude)** | ✅ | Jun 10 | Scripts com voz Raquel |
| **ElevenLabs (Voz)** | ✅ | Jun 10 | Voice ID 0r2zCQO0vO1jOfWbm7N7 |
| **HeyGen Avatar** | ✅ | Jun 10 | Avatar ID 351538dd8eea417882a312681f2168d9 |
| **Approval Bot (Telegram)** | ✅ | Jun 11 | Aprovação em 2 stages |
| **Morning Call (Texto)** | ✅ | Jun 12 | Automático 09:09 diário |
| **ExpectationTracker** | ✅ | Jun 12 | Accountability diário |
| **Morning Call (Curto)** | ✅ | Jun 13 | PETR4, VALE3, Dólar |

### 📈 PLANO PRÓXIMAS SEMANAS

| Fase | Data | O que fazer | Prazo |
|------|------|-----------|-------|
| **Fase 1: Shorts HeyGen** | 14-19 jun | 1º vídeo automático | 1 semana |
| **Fase 2: YouTube 9Pilla** | 14-19 jun | Criar canal + primeiros vídeos | 1 semana |
| **Fase 3: Canva + Design** | 20-26 jun | Templates para Reels/TikTok | 2 semanas |
| **Fase 4: TikTok + Instagram** | 20-26 jun | Publicação automática | 2 semanas |
| **Fase 5: Spotify Podcast** | 27-30 jun | Setup podcast + primeiros eps | 1 semana |
| **Fase 6: Automação Completa** | 1-15 jul | Tudo rodando sozinho | 2 semanas |

---

## 🎯 NOVO WORKFLOW: DO MORNING CALL AO SHORTS AO PODCAST

```
┌─────────────────────────────────────────────────────────────────┐
│                    MORNING CALL (09:09)                         │
│  Claude gera: Abertura + Termômetro + Confere? + 3 Blocos      │
│  Salva em: output/MC_YYYYMMDD.txt                              │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│          APROVAÇÃO NO TELEGRAM (Você aprova 👍)                 │
│  Texto completo para revisar (2 min)                            │
│  Se ❌ REJEITA: feedback, volta ao Writer                       │
│  Se ✅ APROVA: prossegue                                        │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│         PROCESSAMENTO PARA MÚLTIPLAS PLATAFORMAS                │
│  1. Extrair os 3 BLOCOS principais (maior valor)               │
│  2. Criar 3 scripts curtos (60-90s cada)                       │
│  3. Gerar com ElevenLabs (sua voz)                             │
└────────────────────┬────────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
   [BLOCO 1]   [BLOCO 2]    [BLOCO 3]
   (Shorts)    (Shorts)     (Shorts)
        │            │            │
        └────────────┼────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│        HEYGEN: Gera 3 VÍDEOS com seu avatar (60-90s cada)       │
│  Input: Script + Voz (ElevenLabs) + Avatar                     │
│  Output: 3 vídeos MP4 (9016x1080 para Shorts)                  │
│  Custo: ~US$ 0,20 por vídeo x 3 = US$ 0,60 por ciclo           │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│    CANVA DESIGN: Cria gráficos + legendas para cada vídeo       │
│  Usando templates: Reels 9:16, TikTok, Instagram              │
│  Cores: Brand 9Pilla (roxo/ouro)                               │
│  Adiciona: Logo, ticker, disclaimer CVM                        │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│         SUBTÍTULOS + FINALIZAÇÃO (FFmpeg/Adobe)                 │
│  1. Sincroniza áudio com avatar                                 │
│  2. Adiciona legendas (SRT gerado do script)                    │
│  3. Insere gráficos Canva                                       │
│  4. Adiciona disclaimer CVM no final                            │
│  Output: 3 vídeos PRONTOS                                       │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│         APROVAÇÃO NO TELEGRAM (Você assiste 90s cada)           │
│  Vê os 3 vídeos finalizados                                     │
│  Se ✅ APROVA: publica                                          │
│  Se ❌ REJEITA: feedback para ajustes                           │
└────────────────────┬────────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
    YOUTUBE      TIKTOK      INSTAGRAM
    SHORTS       +Canva      REELS
    (Longo)      (Curto)     (Quadrado)
        │            │            │
        └────────────┼────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│         PODCAST AUTOMÁTICO (Spotify + Apple Podcasts)           │
│  1. Combina os 3 vídeos em 1 áudio MP3                         │
│  2. Adiciona intro/outro (música Raquel)                        │
│  3. Publica no Spotify + Apple Podcasts                         │
│  4. Notifica Turma 9Pilla via Z-API                            │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│    NOTIFICAÇÃO TURMA 9PILLA (WhatsApp via Z-API)               │
│  "Novo Morning Call saiu! YouTube Shorts + Spotify Podcast"    │
│  Links para: YouTube, TikTok, Instagram, Spotify               │
│  Engagement: Likes, Comentários, Shares                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎬 DETALHES: CADA PLATAFORMA

### 1️⃣ YOUTUBE 9PILLA (Shorts)

**Criar Canal (você faz UMA VEZ):**
```
1. Abra YouTube.com
2. Click seu perfil → Criar um canal
3. Nome: "Raquel 9Pilla"
4. Descrição: "Educação financeira em tempo real. 
   Morning Calls, análise de mercado, operações ao vivo."
5. Banner: Design no Canva (3440x1440px)
6. Foto: Avatar HeyGen ou sua foto
```

**Publicação Automática (Script Python):**
```python
from youtube import upload_short

upload_short(
    video_file="video_bloco1.mp4",
    title="PETR4 em Alerta: -1,39% hoje",
    description="Análise completa de PETR4, Dólar e VALE3...",
    tags=["PETR4", "bolsa", "educação financeira"],
    visibility="public"
)
```

**Specs Shorts:**
- Resolução: 1080x1920 (vertical)
- Duração: 60-90 segundos
- Formato: MP4 H.264
- Taxa de bits: 8-10 Mbps
- Áudio: 128 kbps

---

### 2️⃣ TIKTOK + INSTAGRAM REELS

**Publicação Automática (TikTok + IG):**
```python
from tiktok import upload_video
from instagram import upload_reel

# TikTok
upload_video(
    video="video_bloco2_tiktok.mp4",
    caption="Dólar em queda = oportunidade? 📊",
    hashtags=["#mercado", "#educaçãofinanceira", "#PETR4"]
)

# Instagram Reels
upload_reel(
    video="video_bloco2_ig.mp4",
    caption="Dólar cai para R$ 5,08...",
    hashtags=["#9Pilla", "#reelsfinanceiros"]
)
```

**Specs:**
- TikTok: 1080x1920, 60-180s
- Instagram Reels: 1080x1920, 15-90s
- Ambos: MP4 H.264, máx 4GB

---

### 3️⃣ SPOTIFY + APPLE PODCASTS

**Setup (você faz UMA VEZ):**
1. Acesse Anchor (anchorpodcasts.com)
2. Crie podcast "Raquel 9Pilla - Morning Call"
3. Descreva: "Análise diária de mercado em áudio"
4. Conecte a Spotify + Apple Podcasts

**Publicação Automática (Script Python):**
```python
from spotify import upload_episode

# Concatenar os 3 vídeos em 1 áudio
# Intro (10s) + Bloco 1 (60s) + Bloco 2 (60s) + Bloco 3 (60s) + Outro (10s) = ~3:40

upload_episode(
    audio_file="morning_call_podcast.mp3",
    title="Morning Call 13/06 - PETR4, Dólar e VALE3",
    description="Análise completa do dia de hoje...",
    episode_number=127,
    publish_date="2026-06-13"
)
```

**Specs:**
- Formato: MP3 128 kbps
- Duração: 3-5 minutos
- Nomenclatura: `MC_YYYYMMDD.mp3`

---

## 💻 SCRIPTS PYTHON A CRIAR

### 1. `shorts_processor.py`
Converte 1 Morning Call completo em 3 scripts curtos

### 2. `video_generator.py`
Orquestra HeyGen, ElevenLabs, Canva e FFmpeg

### 3. `social_publisher.py`
Publica em YouTube, TikTok, Instagram (agranda)

### 4. `podcast_generator.py`
Cria episódio Spotify a partir dos áudios

### 5. `notification_handler.py`
Envia notificações via Z-API quando tudo sai

---

## 📋 CHECKLIST: PRÓXIMAS 48H

### HOJE (Sábado 13/06)
- [ ] Ler este documento (você aqui!)
- [ ] Listar credenciais TikTok/Instagram
- [ ] Criar canal YouTube 9Pilla
- [ ] Validar Anchor/Spotify setup

### AMANHÃ (Domingo 14/06)
- [ ] Criar 1º vídeo HeyGen test (BLOCO1 de hoje)
- [ ] Fazer upload YouTube (teste)
- [ ] Revisar qualidade no Telegram
- [ ] Ajustar specs se necessário

### SEGUNDA (14/06 noite)
- [ ] Script `shorts_processor.py` funcional
- [ ] Teste completo: MC → 3 vídeos → YouTube
- [ ] Publicar BLOCO2 e BLOCO3 também

### SEMANA 2 (20-26/06)
- [ ] TikTok + Instagram publicando automático
- [ ] Canva templates criados
- [ ] Podcast semanal compilado

### SEMANA 3+ (27/06+)
- [ ] Sistema 100% automático
- [ ] Escalando: 5-10 Shorts/dia
- [ ] Tudo monetizado (YouTube Partner, Spotify, Ads)

---

## 🎬 TEMPLATES CANVA (A CRIAR)

### Template 1: Shorts Vertical (1080x1920)
- Fundo: Gradiente roxo 9Pilla
- Logo: Canto superior direito
- Ticker: Anima inferior (PETR4: -1,39%)
- Disclaimer: Rodapé (CVM Res. 20/2021)
- Fonte: Montserrat Bold para títulos

### Template 2: TikTok (1080x1920)
- Similar ao Shorts, mas com:
- Hashtags animadas (#PETR4 #MercadoHoje)
- Trending sounds integrados

### Template 3: Instagram Reels (1080x1920)
- Versão quadrada (1080x1080) também
- Stickers interativos
- Call-to-action: "Salva esse vídeo!"

### Template 4: Podcast Cover (3000x3000)
- Design minimalista
- Foto da Raquel (ou avatar)
- Logo 9Pilla grande
- QR code para Spotify

---

## 💰 CUSTOS MENSAIS (ESCALADO)

| Serviço | Frequência | Custo Unit. | Subtotal |
|---------|-----------|------------|----------|
| **Claude API** | 20 MC/mês | US$ 0,02 | US$ 0,40 |
| **ElevenLabs** | 60 áudios/mês | US$ 0,03 | US$ 1,80 |
| **HeyGen** | 60 vídeos/mês | US$ 0,20 | US$ 12,00 |
| **Canva Pro** | 1 account | US$ 13/mês | US$ 13,00 |
| **Anchor/Spotify** | Free | Free | US$ 0,00 |
| **YouTube** | Free | Free | US$ 0,00 |
| **TikTok/IG** | Free | Free | US$ 0,00 |
| **Z-API** | Já pago | — | — |
| **TOTAL** | — | — | **US$ 27,20/mês** |

**ROI:** 1 vídeo = ~10 leads qualificados → R$ 500 mín → **SUPER VIÁVEL!**

---

## 🔐 CREDENCIAIS A OBTER

### TikTok Creator
```
Acesse: tiktok.com/@seu_usuario
Aba: Criador → API → Developer Account
Gere: TikTok API Key + Secret
```

### Instagram Business
```
Acesse: instagram.com/seu_perfil/settings/
Mude para: Conta Profissional
Conecte: Meta Business Suite
Gere: Tokens para API
```

### YouTube API
```
Google Cloud Console → Criar projeto
Ativar: YouTube Data API v3
Gerar: OAuth 2.0 credentials
```

### Spotify API (Podcast)
```
Anchor.fm → Seu podcast
Spotify for Podcasters → Conectar
Gere: RSS feed para automação
```

---

## 🎯 PRÓXIMO PASSO

**Você pronto?** Vou criar os 5 scripts Python que faltam:

1. `shorts_processor.py` — MC → 3 vídeos curtos
2. `video_generator.py` — Orquestra tudo
3. `social_publisher.py` — Publica em 3 plataformas
4. `podcast_generator.py` — Cria episódio Spotify
5. `notification_handler.py` — Notifica Turma

**Quer que eu continue AGORA ou você quer revisar este plano antes?** 🚀

---

**Status:** 🔄 Aguardando seu OK para BUILD!
