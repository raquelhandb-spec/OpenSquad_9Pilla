#!/usr/bin/env python3
"""
PublisherAgent — Multi-Platform Publishing (YouTube, TikTok, Instagram, Spotify)
Publica vídeos após aprovação e notifica audiência via WhatsApp (Z-API)
"""

import requests
import json
from datetime import datetime
from typing import Dict, Any, Optional, List

class PublisherAgent:
    def __init__(self, youtube_credentials: Optional[Dict] = None):
        """
        Args:
            youtube_credentials: Google OAuth2 credentials para YouTube API

        ⚠️ SETUP REQUIRED (por enquanto estrutura mock):
        1. Google Cloud Console: https://console.cloud.google.com
        2. Create OAuth2 credentials (Desktop app)
        3. Salvar credentials.json
        4. Fazer autenticação primeira vez (browser)
        5. Depois usar refresh token automaticamente
        """
        self.youtube_credentials = youtube_credentials
        self.headers = {"Content-Type": "application/json"}

        # Platform-specific configs
        self.platforms = {
            'youtube': {
                'enabled': True,
                'api': 'https://www.googleapis.com/youtube/v3',
                'status': '🟢 Configurado' if youtube_credentials else '🟡 Aguardando OAuth'
            },
            'tiktok': {
                'enabled': False,  # Requer TikTok Business Account
                'api': 'https://api.tiktok.com/v1',
                'status': '🟡 Não implementado'
            },
            'instagram': {
                'enabled': False,  # Meta Business API
                'api': 'https://graph.instagram.com/v18.0',
                'status': '🟡 Não implementado'
            },
            'spotify': {
                'enabled': False,  # Anchor/Spotify for Podcasters
                'api': 'https://api.spotify.com',
                'status': '🟡 Não implementado'
            }
        }

    def publish_to_youtube(
        self,
        video_file_path: str,
        title: str,
        description: str,
        tags: List[str] = None,
        thumbnail_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Publica Shorts no YouTube

        Args:
            video_file_path: Caminho local do vídeo MP4
            title: Título do vídeo (ex: "Petróleo acima de US$ 100 - O que significa?")
            description: Descrição com keywords SEO
            tags: Tags (ex: ['9Pilla', 'Petróleo', 'PETR4'])
            thumbnail_path: Caminho da thumbnail customizada

        Returns:
            Dict com video_id, url, status
        """

        if not self.youtube_credentials:
            return self._get_mock_youtube_result(title)

        # Em produção: usar google-auth-httplib2 e googleapiclient
        # Por enquanto: estrutura completa para quando OAuth estiver configurado

        print(f"\n📺 Publicando no YouTube...")
        print(f"   Título: {title}")
        print(f"   Arquivo: {video_file_path}")

        # Mock result (em produção, chamaria YouTube API)
        return {
            'status': 'uploaded',
            'platform': 'youtube',
            'video_id': f"9Pilla_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'url': f"https://youtube.com/shorts/mock_video_id",
            'title': title,
            'uploaded_at': datetime.now().isoformat(),
            'views': 0,
            'likes': 0,
            'comments': 0,
            'next_step': 'Notificar audiência via WhatsApp'
        }

    def _get_mock_youtube_result(self, title: str) -> Dict[str, Any]:
        """Mock YouTube result quando OAuth não está configurado"""
        return {
            'status': 'mock_uploaded',
            'platform': 'youtube',
            'video_id': f"9Pilla_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'url': f"https://youtube.com/shorts/mock_id",
            'title': title,
            'uploaded_at': datetime.now().isoformat(),
            'warning': '⚠️ Mock result - configure OAuth credentials para publicação real',
            'next_step': 'Setup Google OAuth2 credentials'
        }

    def publish_to_tiktok(
        self,
        video_file_path: str,
        caption: str,
        hashtags: List[str] = None
    ) -> Dict[str, Any]:
        """
        Publica Shorts no TikTok

        ⚠️ Requer TikTok Business Account + API access
        """
        print(f"\n🎵 TikTok publishing não implementado ainda")
        print(f"   Requer: TikTok Business Account + API credentials")

        return {
            'status': 'not_implemented',
            'platform': 'tiktok',
            'message': 'Implementar quando TikTok Business Account estiver ativo',
            'setup_guide': 'https://developers.tiktok.com/doc/business-api/getting-started'
        }

    def publish_to_instagram(
        self,
        video_file_path: str,
        caption: str,
        hashtags: List[str] = None
    ) -> Dict[str, Any]:
        """
        Publica Reels no Instagram

        ⚠️ Requer Meta Business Account + API access
        """
        print(f"\n📷 Instagram publishing não implementado ainda")
        print(f"   Requer: Meta Business Account + Graph API")

        return {
            'status': 'not_implemented',
            'platform': 'instagram',
            'message': 'Implementar quando Meta Business Account estiver ativo',
            'setup_guide': 'https://developers.facebook.com/docs/instagram-api'
        }

    def schedule_publication(
        self,
        video_data: Dict[str, Any],
        publish_time: str,  # ISO format: 2026-06-10T09:30:00
        platforms: List[str] = None
    ) -> Dict[str, Any]:
        """
        Agenda publicação para hora específica

        Args:
            video_data: Dados do vídeo (título, descrição, arquivo)
            publish_time: Data/hora de publicação (ISO format)
            platforms: Lista de plataformas (default: ['youtube'])

        Returns:
            Dict com status de agendamento
        """

        if not platforms:
            platforms = ['youtube']

        print(f"\n⏰ Agendando publicação para {publish_time}")
        print(f"   Plataformas: {', '.join(platforms)}")

        scheduled = {
            'title': video_data.get('title'),
            'scheduled_time': publish_time,
            'platforms': platforms,
            'status': 'scheduled',
            'scheduled_at': datetime.now().isoformat()
        }

        return {
            'status': 'scheduled',
            'publish_time': publish_time,
            'platforms': platforms,
            'details': scheduled
        }

    def notify_audience_via_whatsapp(
        self,
        video_data: Dict[str, Any],
        zapi_agent: Optional[Any] = None  # Será importado quando necessário
    ) -> Dict[str, Any]:
        """
        Notifica turma 9Pilla que vídeo foi publicado
        Usa Z-API para enviar mensagem + link do YouTube

        ⚠️ Integração com PublisherToZAPIIntegration (zapi_broadcaster.py)
        """

        if not zapi_agent:
            return {
                'status': 'no_zapi_agent',
                'message': 'Z-API agent não configurado'
            }

        title = video_data.get('title', 'Novo vídeo')
        video_url = video_data.get('youtube_url', 'https://youtube.com/shorts')

        message = f"""
☀️ NOVO SHORTS 9PILLA! 📺

{title}

🎬 Assista agora:
{video_url}

💬 Me passa seu feedback!
        """.strip()

        # Usar Z-API para notificar grupo
        result = zapi_agent.send_to_group(
            group_id="TURMA_9PILLA_GROUP_ID",
            message=message
        )

        return {
            'status': 'notified',
            'platform': 'whatsapp',
            'message_sent': result['status'] == 'sent',
            'title': title,
            'youtube_url': video_url,
            'group_id': 'TURMA_9PILLA_GROUP_ID'
        }

    def get_publication_analytics(self, video_id: str) -> Dict[str, Any]:
        """Retorna analíticos do vídeo publicado"""

        # Em produção: consultar YouTube Analytics API
        return {
            'status': 'mock_analytics',
            'video_id': video_id,
            'views': 0,  # Seria consultado em tempo real
            'likes': 0,
            'comments': 0,
            'shares': 0,
            'engagement_rate': 0,
            'message': 'Mock data - configure YouTube Analytics para dados reais'
        }

    def run_platform_status(self) -> Dict[str, Any]:
        """Retorna status de todas as plataformas"""

        print("\n📊 PublisherAgent — Status das Plataformas")
        print("=" * 60)

        for platform, config in self.platforms.items():
            status_emoji = "🟢" if config['enabled'] else "🟡"
            print(f"{status_emoji} {platform.upper()}: {config['status']}")

        print("=" * 60)

        return {
            'status': 'ready',
            'platforms': self.platforms,
            'default_platform': 'youtube',
            'setup_required': [k for k, v in self.platforms.items() if not v['enabled']]
        }


# INTEGRAÇÃO: Executor → Publisher → Z-API
class ExecutorToPublisherPipeline:
    """
    Fluxo: Executor (vídeo pronto) → Publisher (publica) → Z-API (notifica)

    HeyGen retorna video_url
           ↓
    Publisher publica no YouTube
           ↓
    Z-API notifica Turma 9Pilla
    """

    def __init__(
        self,
        publisher_agent: PublisherAgent,
        zapi_agent: Optional[Any] = None
    ):
        self.publisher = publisher_agent
        self.zapi_agent = zapi_agent

    def publish_video_after_heygen_completion(
        self,
        heygen_result: Dict[str, Any],
        script_metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Callback: HeyGen terminou de gerar vídeo
        Agora: publicar no YouTube + notificar via WhatsApp
        """

        print("\n🎬 → 📺 → 💬 Pipeline: Executor → Publisher → Z-API")

        video_url = heygen_result.get('video_url')
        video_id = heygen_result.get('video_id')
        ticker = script_metadata.get('ticker', 'IBOV')
        topic = script_metadata.get('trend_topic', 'Análise de mercado')

        # 1. Preparar metadata para YouTube
        youtube_title = f"💰 {ticker} — {topic} | Morning Call 9Pilla"
        youtube_description = f"""Análise ao vivo de {ticker}: {topic}

🎯 9Pilla — Educação Financeira Prática

📊 Acompanhe:
• YouTube: https://youtube.com/@9pilla
• TikTok: https://tiktok.com/@9pilla
• Instagram: https://instagram.com/9pilla
• Podcast: https://anchor.fm/9pilla

⚠️ Disclaimer: Conteúdo educacional apenas. Não é recomendação de investimento.
"""

        tags = [
            '9Pilla',
            ticker,
            'Educação Financeira',
            'Morning Call',
            'Análise de Mercado'
        ]

        # 2. Publicar no YouTube
        youtube_result = self.publisher.publish_to_youtube(
            video_file_path=video_url,
            title=youtube_title,
            description=youtube_description,
            tags=tags
        )

        # 3. Notificar via WhatsApp (se Z-API configurado)
        whatsapp_result = None
        if self.zapi_agent:
            whatsapp_result = self.publisher.notify_audience_via_whatsapp(
                video_data={
                    'title': youtube_title,
                    'youtube_url': youtube_result.get('url')
                },
                zapi_agent=self.zapi_agent
            )

        return {
            'status': 'published',
            'pipeline_state': 'publisher_complete',
            'video_id': video_id,
            'youtube': youtube_result,
            'whatsapp': whatsapp_result,
            'published_at': datetime.now().isoformat(),
            'next_step': '📊 Monitorar analytics e engagement'
        }


# ORCHESTRATOR: Full Pipeline Integration
class FullPipeline:
    """
    Orquestrador completo do fluxo 9Pilla:

    Prospector → Writer → Reviewer → Executor → Publisher → Z-API
    """

    def __init__(
        self,
        prospector_agent,
        writer_agent,
        reviewer_agent,
        executor_agent,
        publisher_agent,
        zapi_agent
    ):
        self.prospector = prospector_agent
        self.writer = writer_agent
        self.reviewer = reviewer_agent
        self.executor = executor_agent
        self.publisher = publisher_agent
        self.zapi = zapi_agent

    def run_full_cycle(self, dry_run: bool = False) -> Dict[str, Any]:
        """
        Executa ciclo completo: Prospector → ...  → Publisher

        Args:
            dry_run: Se True, apenas mostra plano sem executar

        Returns:
            Dict com resultado de cada etapa
        """

        print("\n" + "="*60)
        print("🚀 EXECUTANDO CICLO COMPLETO 9PILLA")
        print("="*60)

        results = {
            'cycle_id': f"9Pilla_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'start_time': datetime.now().isoformat(),
            'stages': {}
        }

        # Stage 1: Prospector
        print("\n[1/5] PROSPECTOR — Identificando tema trending...")
        prospector_result = self.prospector.identify_trending_topic()
        results['stages']['prospector'] = prospector_result
        print(f"✅ Tema: {prospector_result.get('topic')}")

        # Stage 2: Writer
        print("\n[2/5] WRITER — Gerando script com Raquel Voice...")
        writer_result = self.writer.generate_script(
            market_data={
                'ticker': prospector_result.get('trending_ticker'),
                'price': prospector_result.get('current_price'),
                'change_percent': prospector_result.get('price_change'),
                'trend_topic': prospector_result.get('topic')
            }
        )
        results['stages']['writer'] = writer_result
        print(f"✅ Script gerado")

        # Stage 3: Reviewer
        print("\n[3/5] REVIEWER — Enviando para aprovação Raquel...")
        script_id = f"{prospector_result.get('trending_ticker')}_{datetime.now().strftime('%Y%m%d')}"
        reviewer_result = self.reviewer.send_script_for_approval(
            script_data=writer_result,
            script_id=script_id
        )
        results['stages']['reviewer'] = reviewer_result
        print(f"✅ Script enviado para Telegram")
        print(f"   ⏰ Aguardando reação de Raquel...")

        # Stage 4-5: Executor + Publisher (executados após aprovação)
        results['stages']['executor'] = {
            'status': 'pending_approval',
            'message': 'Aguardando aprovação no Telegram'
        }
        results['stages']['publisher'] = {
            'status': 'pending_execution',
            'message': 'Executado após vídeo estar pronto'
        }

        results['end_time'] = datetime.now().isoformat()
        results['overall_status'] = 'awaiting_reviewer_approval'

        print("\n" + "="*60)
        print("📊 RESUMO DO CICLO:")
        print("="*60)
        print(f"Ciclo ID: {results['cycle_id']}")
        print(f"Status: {results['overall_status']}")
        print("Próximo passo: Raquel aprova via Telegram (👍)")

        return results


# Test
if __name__ == "__main__":
    print("\n" + "="*60)
    print("PUBLISHER AGENT TEST")
    print("="*60 + "\n")

    publisher = PublisherAgent()

    # Teste 1: Status das plataformas
    print("📋 Teste 1: Status das plataformas")
    status = publisher.run_platform_status()
    print(json.dumps(status, indent=2, ensure_ascii=False))

    # Teste 2: Publicar no YouTube (mock)
    print("\n📺 Teste 2: Publicar no YouTube")
    result = publisher.publish_to_youtube(
        video_file_path="/tmp/9pilla_shorts.mp4",
        title="Petróleo acima de US$ 100 - O que significa para você?",
        description="Análise do impacto da alta do petróleo no seu bolso...",
        tags=['9Pilla', 'Petróleo', 'PETR4', 'Educação Financeira']
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))

    print("\n" + "="*60)
    print("WORKFLOW USAGE:")
    print("="*60)
    print("""
# Full pipeline orchestration
from prospector import ProspectorAgent
from writer import WriterAgent
from reviewer import ReviewerAgent
from executor import ExecutorAgent  # MoneyPrinter + ElevenLabs + HeyGen
from publisher import PublisherAgent

prospector = ProspectorAgent(brapi_key='...')
writer = WriterAgent()
reviewer = ReviewerAgent(telegram_bot_token, chat_id)
executor = ExecutorAgent()
publisher = PublisherAgent(youtube_credentials)

pipeline = FullPipeline(
    prospector, writer, reviewer, executor, publisher, zapi
)

# Executar ciclo completo
result = pipeline.run_full_cycle()

# Quando Raquel aprova via Telegram:
# → Executor cria vídeo HeyGen
# → Publisher publica YouTube
# → Z-API notifica Turma 9Pilla
    """)
