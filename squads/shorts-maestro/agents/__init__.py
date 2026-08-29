"""
Agents para o Squad Shorts-Maestro

Cada agente é responsável por uma etapa do pipeline:
- Prospector: Buscar dados (Brapi)
- Writer: Gerar scripts (Ollama)
- Executor: Renderizar vídeos (MoneyPrinter + ElevenLabs)
- Reviewer: Aprovar via Telegram
- Publisher: Publicar em YouTube/TikTok
"""

from .prospector import ProspectorAgent

__all__ = [
    "ProspectorAgent",
]
