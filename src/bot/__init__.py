"""
Módulo principal do bot SocialBot AI

Contém as classes e funcionalidades principais para automação de redes sociais.
"""

from .social_bot import SocialBot
from .twitter_bot import TwitterBot
from .scheduler import PostScheduler
from .rate_limiter import RateLimiter

__all__ = [
    "SocialBot",
    "TwitterBot",
    "PostScheduler",
    "RateLimiter"
]
