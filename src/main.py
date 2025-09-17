#!/usr/bin/env python3
"""
SocialBot AI - Ponto de entrada principal

Este arquivo inicializa e executa o SocialBot AI com todas suas funcionalidades.
"""

import asyncio
import sys
import signal
from pathlib import Path
from typing import Optional

# Adiciona o diretório src ao path
sys.path.insert(0, str(Path(__file__).parent))

from utils.config import Config
from utils.logger import Logger
from bot.social_bot import SocialBot
from dashboard.app import DashboardApp


class SocialBotAI:
    """Classe principal do SocialBot AI"""
    
    def __init__(self):
        self.config = Config()
        self.logger = Logger().get_logger(__name__)
        self.bot: Optional[SocialBot] = None
        self.dashboard: Optional[DashboardApp] = None
        self.running = False
        
    async def initialize(self):
        """Inicializa todos os componentes do bot"""
        try:
            self.logger.info("🚀 Inicializando SocialBot AI...")
            
            # Inicializa o bot principal
            self.bot = SocialBot(self.config)
            await self.bot.initialize()
            
            # Inicializa o dashboard
            self.dashboard = DashboardApp(self.config, self.bot)
            
            self.logger.info("✅ SocialBot AI inicializado com sucesso!")
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao inicializar SocialBot AI: {e}")
            raise
    
    async def start(self):
        """Inicia o bot e todos os serviços"""
        try:
            await self.initialize()
            
            self.running = True
            self.logger.info("🎯 SocialBot AI iniciado!")
            
            # Configura handlers para shutdown graceful
            signal.signal(signal.SIGINT, self._signal_handler)
            signal.signal(signal.SIGTERM, self._signal_handler)
            
            # Inicia o bot em background
            bot_task = asyncio.create_task(self.bot.start())
            
            # Inicia o dashboard
            dashboard_task = asyncio.create_task(self.dashboard.start())
            
            # Aguarda ambos os serviços
            await asyncio.gather(bot_task, dashboard_task)
            
        except KeyboardInterrupt:
            self.logger.info("🛑 Interrupção pelo usuário")
        except Exception as e:
            self.logger.error(f"❌ Erro durante execução: {e}")
        finally:
            await self.stop()
    
    async def stop(self):
        """Para o bot e limpa recursos"""
        if not self.running:
            return
            
        self.logger.info("🛑 Parando SocialBot AI...")
        self.running = False
        
        try:
            if self.bot:
                await self.bot.stop()
                
            if self.dashboard:
                await self.dashboard.stop()
                
            self.logger.info("✅ SocialBot AI parado com sucesso!")
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao parar SocialBot AI: {e}")
    
    def _signal_handler(self, signum, frame):
        """Handler para sinais de sistema"""
        self.logger.info(f"📡 Sinal recebido: {signum}")
        self.running = False


async def main():
    """Função principal"""
    try:
        # Banner de inicialização
        print("""
╔══════════════════════════════════════════════════════════════╗
║                        🤖 SocialBot AI                       ║
║                                                              ║
║           Automação Inteligente para Redes Sociais          ║
║                                                              ║
║  🐦 Twitter  📸 Instagram  💼 LinkedIn  🎵 TikTok           ║
║  🧠 IA       📊 Analytics  📅 Agendamento  🔄 Auto-resposta ║
╚══════════════════════════════════════════════════════════════╝
        """)
        
        # Cria e inicia o bot
        socialbot_ai = SocialBotAI()
        await socialbot_ai.start()
        
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Verifica versão do Python
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ é necessário!")
        sys.exit(1)
    
    # Executa o bot
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 SocialBot AI finalizado!")
    except Exception as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)
