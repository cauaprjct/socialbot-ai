"""
SocialBot AI - Automação Inteligente para Redes Sociais

Um bot avançado que automatiza suas redes sociais usando IA para gerar conteúdo,
agendar posts e analisar engajamento em tempo real.

Autor: Seu Nome
Versão: 1.0.0
Licença: MIT
"""

__version__ = "1.0.0"
__author__ = "Seu Nome"
__email__ = "seu.email@exemplo.com"
__description__ = "Bot de automação inteligente para redes sociais com IA"

# Importações principais
from .bot import SocialBot
from .ai import ContentGenerator, SentimentAnalyzer
from .analytics import EngagementTracker, ReportGenerator
from .utils import Config, Logger

__all__ = [
    "SocialBot",
    "ContentGenerator", 
    "SentimentAnalyzer",
    "EngagementTracker",
    "ReportGenerator",
    "Config",
    "Logger"
]
