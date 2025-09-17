#!/usr/bin/env python3
"""
SocialBot AI - Script de execução principal

Este script é o ponto de entrada para executar o SocialBot AI.
Pode ser usado tanto para desenvolvimento quanto para produção.
"""

import sys
import asyncio
from pathlib import Path

# Adiciona o diretório src ao path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.main import main

if __name__ == "__main__":
    # Configurações do asyncio para Windows
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    # Executa a aplicação
    asyncio.run(main())