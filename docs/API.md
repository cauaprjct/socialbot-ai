# 📚 API Documentation - SocialBot AI

Esta documentação descreve as APIs e interfaces principais do SocialBot AI.

## 📋 Índice

- [Configuração](#configuração)
- [Bot Principal](#bot-principal)
- [Módulos de IA](#módulos-de-ia)
- [Dashboard](#dashboard)
- [Utilitários](#utilitários)

## ⚙️ Configuração

### Config

Classe principal para gerenciar configurações do sistema.

```python
from src.utils.config import Config

# Carrega configurações do .env
config = Config()

# Verifica plataformas configuradas
platforms = config.get_configured_platforms()
print(platforms)  # ['twitter', 'instagram']

# Valida configurações
is_valid = config.validate()
if is_valid:
    print("✅ Configurações válidas")
else:
    print("❌ Erro nas configurações")
```

#### Métodos Principais

| Método | Descrição | Retorno |
|--------|-------------|----------|
| `get_configured_platforms()` | Lista plataformas configuradas | `List[str]` |
| `is_configured(platform)` | Verifica se plataforma está configurada | `bool` |
| `validate()` | Valida todas as configurações | `Dict[str, List[str]]` |

### Configurações por Plataforma

#### TwitterConfig

```python
@dataclass
class TwitterConfig:
    api_key: str
    api_secret: str
    access_token: str
    access_token_secret: str
    bearer_token: str
    rate_limit_posts_per_hour: int = 50
```

#### AIConfig

```python
@dataclass
class AIConfig:
    huggingface_token: str
    openai_api_key: str
    openai_model: str = "gpt-3.5-turbo"
    model_name: str = "microsoft/DialoGPT-medium"
    max_length: int = 280
    temperature: float = 0.7
    top_p: float = 0.9
```

## 🤖 Bot Principal

### SocialBot

Classe principal que orquestra todas as funcionalidades.

```python
from src.bot.social_bot import SocialBot
from src.utils.config import Config

# Inicializa o bot
config = Config()
bot = SocialBot(config)
await bot.initialize()

# Publica um post
result = await bot.post_to_platforms(
    content="Olá mundo! 🤖",
    platforms=["twitter"]
)

print(result)
# {
#     "success": True,
#     "results": {
#         "twitter": {
#             "id": "1234567890",
#             "url": "https://twitter.com/user/status/1234567890"
#         }
#     }
# }
```

#### Métodos Principais

| Método | Descrição | Parâmetros | Retorno |
|--------|-------------|-------------|----------|
| `initialize()` | Inicializa o bot | - | `None` |
| `post_to_platforms()` | Publica em plataformas | `content`, `platforms` | `Dict` |
| `schedule_post()` | Agenda um post | `content`, `platforms`, `schedule_time` | `Dict` |
| `get_mentions()` | Obtém menções | `limit`, `since` | `List[Dict]` |
| `get_analytics()` | Obtém analytics | `days`, `platform` | `Dict` |
| `get_statistics()` | Obtém estatísticas | - | `Dict` |

### TwitterBot

Bot específico para Twitter/X.

```python
from src.bot.twitter_bot import TwitterBot

# Inicializa bot do Twitter
twitter_bot = TwitterBot(config.twitter)
await twitter_bot.initialize()

# Publica tweet
result = await twitter_bot.post_tweet("Meu primeiro tweet automatizado!")

# Publica thread
thread_tweets = [
    "Este é o primeiro tweet da thread 🧵",
    "Este é o segundo tweet da thread 🔗",
    "E este é o último! 🏁"
]
result = await twitter_bot.post_thread(thread_tweets)

# Responde a um tweet
result = await twitter_bot.reply_to_tweet(
    tweet_id="1234567890",
    reply_text="Obrigado pelo tweet! 🙏"
)
```

#### Métodos do TwitterBot

| Método | Descrição | Parâmetros | Retorno |
|--------|-------------|-------------|----------|
| `post_tweet()` | Publica tweet | `text`, `media` | `Dict` |
| `post_thread()` | Publica thread | `tweets` | `List[Dict]` |
| `reply_to_tweet()` | Responde tweet | `tweet_id`, `reply_text` | `Dict` |
| `get_mentions()` | Obtém menções | `count`, `since_id` | `List[Dict]` |
| `get_user_timeline()` | Obtém timeline | `user_id`, `count` | `List[Dict]` |
| `search_tweets()` | Busca tweets | `query`, `count` | `List[Dict]` |

## 🧠 Módulos de IA

### ContentGenerator

Gerador de conteúdo usando IA.

```python
from src.ai.content_generator import (
    ContentGenerator, 
    ContentRequest, 
    ContentTone, 
    ContentType
)

# Inicializa gerador
generator = ContentGenerator(config.ai)

# Cria requisição de conteúdo
request = ContentRequest(
    topic="inteligência artificial",
    platform="twitter",
    tone=ContentTone.PROFESSIONAL,
    content_type=ContentType.POST,
    max_length=280,
    include_hashtags=True,
    include_emojis=True
)

# Gera conteúdo
content = await generator.generate_content(request)

print(content.text)
print(content.hashtags)
print(f"Confiança: {content.confidence_score}")
```

#### ContentRequest

```python
@dataclass
class ContentRequest:
    topic: str
    platform: str
    tone: ContentTone = ContentTone.CASUAL
    content_type: ContentType = ContentType.POST
    max_length: int = 280
    include_hashtags: bool = True
    include_emojis: bool = True
    target_audience: Optional[str] = None
    keywords: List[str] = None
    context: Optional[str] = None
```

#### ContentTone (Enum)

- `PROFESSIONAL` - Tom profissional
- `CASUAL` - Tom casual
- `FUNNY` - Tom humorístico
- `INSPIRATIONAL` - Tom inspiracional
- `EDUCATIONAL` - Tom educativo
- `PROMOTIONAL` - Tom promocional

#### ContentType (Enum)

- `POST` - Post normal
- `CAPTION` - Legenda
- `THREAD` - Thread/sequência
- `STORY` - Story
- `REPLY` - Resposta

### SentimentAnalyzer

Analisador de sentimento para conteúdo.

```python
from src.ai.sentiment_analyzer import SentimentAnalyzer

# Inicializa analisador
analyzer = SentimentAnalyzer(config.ai)

# Analisa sentimento
result = await analyzer.analyze_sentiment(
    text="Estou muito feliz com este projeto!"
)

print(result)
# {
#     "sentiment": "positive",
#     "confidence": 0.95,
#     "scores": {
#         "positive": 0.95,
#         "negative": 0.03,
#         "neutral": 0.02
#     }
# }
```

### HashtagGenerator

Gerador de hashtags relevantes.

```python
from src.ai.hashtag_generator import HashtagGenerator

# Inicializa gerador
hashtag_gen = HashtagGenerator(config.ai)

# Gera hashtags
hashtags = await hashtag_gen.generate_hashtags(
    text="Aprendendo programação Python com IA",
    platform="twitter",
    max_hashtags=5
)

print(hashtags)
# ["#Python", "#IA", "#Programming", "#MachineLearning", "#Tech"]
```

## 🎨 Dashboard

### DashboardApp

Interface web para gerenciar o bot.

```python
from src.dashboard.app import DashboardApp

# Inicializa dashboard
dashboard = DashboardApp(config, bot)

# Inicia servidor
await dashboard.start()
# Dashboard disponível em http://localhost:8501
```

#### Funcionalidades do Dashboard

- 📋 **Visão Geral**: Status do bot e estatísticas
- 📝 **Criar Post**: Interface para criar e publicar posts
- 📅 **Agendamento**: Gerenciar posts agendados
- 📊 **Analytics**: Gráficos e métricas de performance
- ⚙️ **Configurações**: Gerenciar configurações do bot
- 📜 **Logs**: Visualizar logs do sistema

## 🔧 Utilitários

### Logger

Sistema de logging avançado.

```python
from src.utils.logger import Logger

# Obtém logger
logger = Logger().get_logger(__name__)

# Diferentes níveis de log
logger.debug("Mensagem de debug")
logger.info("ℹ️ Informação importante")
logger.warning("⚠️ Aviso")
logger.error("❌ Erro")
logger.critical("🚨 Erro crítico")

# Log com contexto
logger.info("Post publicado", extra={
    "platform": "twitter",
    "post_id": "1234567890",
    "user_id": "user123"
})
```

### Validators

Funções de validação.

```python
from src.utils.validators import (
    validate_social_media_config,
    validate_ai_config,
    validate_post_content
)

# Valida configuração de rede social
is_valid = validate_social_media_config(config.twitter)

# Valida configuração de IA
is_valid = validate_ai_config(config.ai)

# Valida conteúdo do post
is_valid = validate_post_content(
    text="Meu post",
    platform="twitter",
    max_length=280
)
```

### Helpers

Funções auxiliares.

```python
from src.utils.helpers import (
    format_datetime,
    sanitize_text,
    generate_uuid,
    extract_hashtags,
    count_characters
)

# Formata data/hora
formatted = format_datetime(datetime.now())
# "2024-01-15 14:30:00"

# Sanitiza texto
clean_text = sanitize_text("Texto com @menções e #hashtags")

# Gera UUID único
unique_id = generate_uuid()

# Extrai hashtags
hashtags = extract_hashtags("Post com #python e #ai")
# ["python", "ai"]

# Conta caracteres
count = count_characters("Meu texto", platform="twitter")
```

## 📊 Rate Limiting

### RateLimiter

Controle de taxa de requisições.

```python
from src.bot.rate_limiter import RateLimiter

# Cria rate limiter
limiter = RateLimiter(
    max_requests=50,  # Máximo 50 requisições
    time_window=3600  # Por hora (3600 segundos)
)

# Verifica se pode fazer requisição
if await limiter.can_make_request("twitter_post"):
    # Faz a requisição
    result = await make_api_call()
    
    # Registra a requisição
    await limiter.record_request("twitter_post")
else:
    print("⚠️ Rate limit atingido, aguarde...")
    wait_time = await limiter.get_wait_time("twitter_post")
    print(f"Aguarde {wait_time} segundos")
```

## 📅 Scheduler

### PostScheduler

Agendamento de posts.

```python
from src.bot.scheduler import PostScheduler, PostPriority
from datetime import datetime, timedelta

# Inicializa scheduler
scheduler = PostScheduler(config)

# Agenda post
schedule_id = await scheduler.schedule_post(
    content="Post agendado",
    platforms=["twitter"],
    schedule_time=datetime.now() + timedelta(hours=2),
    priority=PostPriority.NORMAL
)

# Lista posts agendados
scheduled_posts = await scheduler.get_scheduled_posts()

# Cancela post agendado
await scheduler.cancel_scheduled_post(schedule_id)
```

#### PostPriority (Enum)

- `LOW` - Baixa prioridade
- `NORMAL` - Prioridade normal
- `HIGH` - Alta prioridade
- `URGENT` - Urgente

## 📊 Analytics

### EngagementTracker

Rastreamento de engajamento.

```python
from src.analytics.engagement_tracker import EngagementTracker

# Inicializa tracker
tracker = EngagementTracker(config)

# Registra post
await tracker.track_post(
    post_id="1234567890",
    platform="twitter",
    content="Meu post",
    timestamp=datetime.now()
)

# Atualiza métricas
await tracker.update_metrics(
    post_id="1234567890",
    likes=10,
    retweets=5,
    replies=2
)

# Obtém relatório
report = await tracker.get_engagement_report(
    start_date=datetime.now() - timedelta(days=7),
    end_date=datetime.now()
)
```

## 🔒 Segurança

### Autenticação

Todas as APIs são protegidas por autenticação.

```python
# Configuração de segurança no .env
SECRET_KEY=sua-chave-secreta-super-segura
ADMIN_USERNAME=admin
ADMIN_PASSWORD=senha-forte

# JWT Token para APIs
JWT_SECRET_KEY=chave-jwt-secreta
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

### Validação de Entrada

Todos os inputs são validados.

```python
from src.utils.validators import validate_input

# Valida entrada do usuário
is_valid = validate_input(
    data={"content": "Meu post"},
    schema={
        "content": {"type": "string", "max_length": 280}
    }
)
```

## 🔍 Monitoramento

### Métricas Prometheus

```python
from src.utils.metrics import metrics

# Incrementa contador
metrics.posts_published.inc()

# Registra tempo de execução
with metrics.api_request_duration.time():
    result = await make_api_call()

# Registra gauge
metrics.active_connections.set(10)
```

### Health Checks

```bash
# Verifica saúde do sistema
curl http://localhost:8000/health

# Resposta:
{
    "status": "healthy",
    "timestamp": "2024-01-15T14:30:00Z",
    "version": "1.0.0",
    "components": {
        "database": "healthy",
        "redis": "healthy",
        "twitter_api": "healthy"
    }
}
```

## 🔧 Exemplos Práticos

### Exemplo Completo

```python
import asyncio
from src.main import SocialBotAI
from src.ai.content_generator import ContentRequest, ContentTone

async def exemplo_completo():
    # 1. Inicializa bot
    bot = SocialBotAI()
    await bot.initialize()
    
    # 2. Gera conteúdo
    request = ContentRequest(
        topic="programação Python",
        platform="twitter",
        tone=ContentTone.EDUCATIONAL
    )
    
    content = await bot.bot.ai_content_generator.generate_content(request)
    
    # 3. Publica conteúdo
    result = await bot.bot.post_to_platforms(
        content=content.text,
        platforms=["twitter"]
    )
    
    # 4. Monitora resultado
    if result["success"]:
        print(f"✅ Post publicado: {result['results']['twitter']['url']}")
    
    # 5. Para bot
    await bot.stop()

# Executa exemplo
asyncio.run(exemplo_completo())
```

## 🔗 Links Úteis

- [GitHub Repository](https://github.com/cauaprjct/socialbot-ai)
- [Documentação Completa](https://github.com/cauaprjct/socialbot-ai/wiki)
- [Exemplos](https://github.com/cauaprjct/socialbot-ai/tree/main/examples)
- [Issues](https://github.com/cauaprjct/socialbot-ai/issues)
- [Discussions](https://github.com/cauaprjct/socialbot-ai/discussions)

---

📝 **Documentação gerada automaticamente** | 🔄 **Última atualização**: 2024-01-15
