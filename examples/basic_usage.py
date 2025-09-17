#!/usr/bin/env python3
"""
Exemplo Básico de Uso do SocialBot AI

Este exemplo demonstra como usar o SocialBot AI para:
- Configurar o bot
- Publicar posts
- Gerar conteúdo com IA
- Agendar posts
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Adiciona o diretório src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.main import SocialBotAI
from src.ai.content_generator import ContentRequest, ContentTone, ContentType
from src.utils.config import Config
from src.utils.logger import Logger


async def exemplo_basico():
    """Exemplo básico de uso do SocialBot AI"""
    
    print("🤖 Iniciando SocialBot AI - Exemplo Básico")
    print("=" * 50)
    
    try:
        # 1. Inicializa o bot
        print("📋 Inicializando bot...")
        bot = SocialBotAI()
        await bot.initialize()
        
        if not bot.bot.is_initialized:
            print("❌ Erro: Bot não foi inicializado corretamente")
            print("Verifique suas configurações no arquivo .env")
            return
        
        print("✅ Bot inicializado com sucesso!")
        
        # 2. Publica um post simples
        print("\n📝 Publicando post simples...")
        
        result = await bot.bot.post_to_platforms(
            content="Olá mundo! Este é meu primeiro post automatizado com SocialBot AI! 🤖✨",
            platforms=["twitter"]  # Ajuste conforme suas plataformas configuradas
        )
        
        if result.get("success"):
            print(f"✅ Post publicado com sucesso!")
            for platform, data in result.get("results", {}).items():
                print(f"   {platform}: {data.get('url', 'Publicado')}")
        else:
            print(f"❌ Erro ao publicar: {result.get('error')}")
        
        # 3. Gera conteúdo com IA
        print("\n🧠 Gerando conteúdo com IA...")
        
        content_request = ContentRequest(
            topic="inteligência artificial e automação",
            platform="twitter",
            tone=ContentTone.PROFESSIONAL,
            content_type=ContentType.POST,
            max_length=280,
            include_hashtags=True,
            include_emojis=True
        )
        
        generated_content = await bot.bot.ai_content_generator.generate_content(content_request)
        
        if generated_content:
            print(f"✅ Conteúdo gerado:")
            print(f"   Texto: {generated_content.text}")
            print(f"   Hashtags: {', '.join(generated_content.hashtags)}")
            print(f"   Confiança: {generated_content.confidence_score:.2f}")
            
            # Publica o conteúdo gerado
            print("\n🚀 Publicando conteúdo gerado...")
            result = await bot.bot.post_to_platforms(
                content=generated_content.text,
                platforms=["twitter"]
            )
            
            if result.get("success"):
                print("✅ Conteúdo gerado publicado com sucesso!")
            else:
                print(f"❌ Erro ao publicar conteúdo gerado: {result.get('error')}")
        else:
            print("❌ Erro ao gerar conteúdo")
        
        # 4. Agenda um post para o futuro
        print("\n📅 Agendando post para o futuro...")
        
        schedule_time = datetime.now() + timedelta(hours=1)
        
        scheduled_result = await bot.bot.schedule_post(
            content="Este post foi agendado automaticamente! 🕰️🤖",
            platforms=["twitter"],
            schedule_time=schedule_time
        )
        
        if scheduled_result.get("success"):
            print(f"✅ Post agendado para: {schedule_time.strftime('%d/%m/%Y %H:%M')}")
            print(f"   ID do agendamento: {scheduled_result.get('schedule_id')}")
        else:
            print(f"❌ Erro ao agendar post: {scheduled_result.get('error')}")
        
        # 5. Obtém estatísticas
        print("\n📊 Obtendo estatísticas...")
        
        stats = await bot.bot.get_statistics()
        
        if stats:
            print("✅ Estatísticas:")
            print(f"   Posts publicados hoje: {stats.get('posts_today', 0)}")
            print(f"   Posts agendados: {stats.get('scheduled_posts', 0)}")
            print(f"   Plataformas ativas: {', '.join(stats.get('active_platforms', []))}")
            print(f"   Última atividade: {stats.get('last_activity', 'N/A')}")
        else:
            print("❌ Erro ao obter estatísticas")
        
        print("\n🎉 Exemplo concluído com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro durante execução: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Para o bot
        if 'bot' in locals():
            await bot.stop()


async def exemplo_avancado():
    """Exemplo avançado com múltiplas funcionalidades"""
    
    print("🚀 Iniciando SocialBot AI - Exemplo Avançado")
    print("=" * 50)
    
    try:
        bot = SocialBotAI()
        await bot.initialize()
        
        # 1. Gera uma série de posts sobre um tópico
        print("📚 Gerando série de posts...")
        
        topics = [
            "benefícios da inteligência artificial",
            "futuro da automação",
            "IA no dia a dia",
            "tendências tecnológicas 2024"
        ]
        
        for i, topic in enumerate(topics, 1):
            print(f"\n📝 Gerando post {i}/{len(topics)}: {topic}")
            
            content_request = ContentRequest(
                topic=topic,
                platform="twitter",
                tone=ContentTone.EDUCATIONAL,
                content_type=ContentType.POST,
                include_hashtags=True,
                include_emojis=True
            )
            
            content = await bot.bot.ai_content_generator.generate_content(content_request)
            
            if content:
                # Agenda posts com intervalo de 2 horas
                schedule_time = datetime.now() + timedelta(hours=i * 2)
                
                result = await bot.bot.schedule_post(
                    content=content.text,
                    platforms=["twitter"],
                    schedule_time=schedule_time
                )
                
                if result.get("success"):
                    print(f"✅ Post agendado para {schedule_time.strftime('%H:%M')}")
                else:
                    print(f"❌ Erro ao agendar: {result.get('error')}")
            
            # Pausa entre gerações
            await asyncio.sleep(1)
        
        # 2. Monitora menções e responde automaticamente
        print("\n👁️ Monitorando menções...")
        
        mentions = await bot.bot.get_mentions(limit=5)
        
        if mentions:
            print(f"✅ Encontradas {len(mentions)} menções")
            
            for mention in mentions:
                print(f"\n💬 Menção de @{mention.get('username')}:")
                print(f"   {mention.get('text')}")
                
                # Gera resposta automática
                response_request = ContentRequest(
                    topic=f"resposta para: {mention.get('text')}",
                    platform="twitter",
                    tone=ContentTone.CASUAL,
                    content_type=ContentType.REPLY,
                    max_length=280
                )
                
                response = await bot.bot.ai_content_generator.generate_content(response_request)
                
                if response:
                    print(f"   🤖 Resposta gerada: {response.text}")
                    
                    # Aqui você pode escolher responder automaticamente ou não
                    # await bot.bot.reply_to_mention(mention['id'], response.text)
        else:
            print("💭 Nenhuma menção encontrada")
        
        # 3. Análise de performance
        print("\n📈 Analisando performance...")
        
        analytics = await bot.bot.get_analytics(days=7)
        
        if analytics:
            print("✅ Análise dos últimos 7 dias:")
            print(f"   Posts publicados: {analytics.get('total_posts', 0)}")
            print(f"   Engajamento total: {analytics.get('total_engagement', 0)}")
            print(f"   Taxa de engajamento: {analytics.get('engagement_rate', 0):.2f}%")
            print(f"   Melhor horário: {analytics.get('best_time', 'N/A')}")
            print(f"   Hashtags mais eficazes: {', '.join(analytics.get('top_hashtags', []))}")
        
        print("\n🎆 Exemplo avançado concluído!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if 'bot' in locals():
            await bot.stop()


def main():
    """Função principal"""
    print("🤖 SocialBot AI - Exemplos de Uso")
    print("\nEscolha um exemplo:")
    print("1. Exemplo Básico")
    print("2. Exemplo Avançado")
    
    choice = input("\nDigite sua escolha (1 ou 2): ").strip()
    
    if choice == "1":
        asyncio.run(exemplo_basico())
    elif choice == "2":
        asyncio.run(exemplo_avancado())
    else:
        print("❌ Escolha inválida!")


if __name__ == "__main__":
    main()
