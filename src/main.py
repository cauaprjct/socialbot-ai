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
        """Inicia o SocialBot AI"""
        try:
            self.logger.info("🎆 Iniciando SocialBot AI...")
            
            # Inicia o bot
            if self.bot:
                await self.bot.start()
            
            # Inicia o dashboard em background
            if self.dashboard:
                asyncio.create_task(self.dashboard.run())
            
            self.running = True
            self.logger.info("✅ SocialBot AI iniciado com sucesso!")
            
            # Mantém o programa rodando
            await self._keep_alive()
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao iniciar SocialBot AI: {e}")
            raise
    
    async def stop(self):
        """Para o SocialBot AI graciosamente"""
        try:
            self.logger.info("🛑 Parando SocialBot AI...")
            
            self.running = False
            
            # Para o bot
            if self.bot:
                await self.bot.stop()
            
            # Para o dashboard
            if self.dashboard:
                await self.dashboard.stop()
            
            self.logger.info("✅ SocialBot AI parado com sucesso!")
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao parar SocialBot AI: {e}")
    
    async def _keep_alive(self):
        """Mantém o programa rodando"""
        try:
            while self.running:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("👋 Interrupção do usuário detectada")
            await self.stop()
    
    def _setup_signal_handlers(self):
        """Configura handlers para sinais do sistema"""
        def signal_handler(signum, frame):
            self.logger.info(f"🚨 Sinal {signum} recebido, parando...")
            asyncio.create_task(self.stop())
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)


async def main():
    """Função principal"""
    app = SocialBotAI()
    
    try:
        # Configura handlers de sinal
        app._setup_signal_handlers()
        
        # Inicializa e inicia
        await app.initialize()
        await app.start()
        
    except KeyboardInterrupt:
        print("
👋 Encerrando SocialBot AI...")
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
        sys.exit(1)
    finally:
        await app.stop()


if __name__ == "__main__":
    # Configurações do asyncio para Windows
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    # Executa a aplicação
    asyncio.run(main())