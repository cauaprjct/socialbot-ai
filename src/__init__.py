"""
SocialBot AI - Bot de Automação para Redes Sociais com IA

Um sistema completo de automação para redes sociais que combina
inteligência artificial avançada com arquitetura robusta de produção.
"""

__version__ = "1.0.0"
__author__ = "SocialBot AI Team"
__email__ = "socialbot.ai@gmail.com"
__description__ = "Bot de Automação para Redes Sociais com IA"

# Imports principais
from .main import SocialBotAI
from .bot.social_bot import SocialBot
from .utils.config import Config
from .utils.logger import Logger

__all__ = [
    "SocialBotAI",
    "SocialBot", 
    "Config",
    "Logger"
]