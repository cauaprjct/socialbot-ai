"""
Gerenciador de configurações do SocialBot AI

Carrega e valida todas as configurações do arquivo .env e variáveis de ambiente.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from dotenv import load_dotenv


@dataclass
class TwitterConfig:
    """Configurações do Twitter/X"""
    api_key: str = ""
    api_secret: str = ""
    access_token: str = ""
    access_token_secret: str = ""
    bearer_token: str = ""
    rate_limit_posts_per_hour: int = 50


@dataclass
class InstagramConfig:
    """Configurações do Instagram"""
    access_token: str = ""
    business_account_id: str = ""
    app_id: str = ""
    app_secret: str = ""
    rate_limit_posts_per_hour: int = 25


@dataclass
class LinkedInConfig:
    """Configurações do LinkedIn"""
    client_id: str = ""
    client_secret: str = ""
    access_token: str = ""
    rate_limit_posts_per_hour: int = 20


@dataclass
class AIConfig:
    """Configurações de IA"""
    huggingface_token: str = ""
    openai_api_key: str = ""
    openai_model: str = "gpt-3.5-turbo"
    model_name: str = "microsoft/DialoGPT-medium"
    max_length: int = 280
    temperature: float = 0.7
    top_p: float = 0.9


@dataclass
class DatabaseConfig:
    """Configurações do banco de dados"""
    url: str = "sqlite:///socialbot.db"
    redis_url: str = "redis://localhost:6379/0"


@dataclass
class DashboardConfig:
    """Configurações do dashboard"""
    streamlit_port: int = 8501
    streamlit_host: str = "0.0.0.0"
    fastapi_port: int = 8000
    fastapi_host: str = "0.0.0.0"
    secret_key: str = "change-this-secret-key"
    admin_username: str = "admin"
    admin_password: str = "change-this-password"


@dataclass
class GoogleConfig:
    """Configurações das APIs do Google"""
    calendar_credentials_path: str = "credentials/google_calendar_credentials.json"
    calendar_id: str = ""
    sheets_credentials_path: str = "credentials/google_sheets_credentials.json"
    sheets_spreadsheet_id: str = ""


class Config:
    """Gerenciador principal de configurações"""
    
    def __init__(self, env_file: Optional[str] = None):
        """
        Inicializa as configurações
        
        Args:
            env_file: Caminho para o arquivo .env (opcional)
        """
        # Carrega variáveis de ambiente
        if env_file:
            load_dotenv(env_file)
        else:
            # Procura por .env no diretório atual e nos pais
            current_dir = Path.cwd()
            for parent in [current_dir] + list(current_dir.parents):
                env_path = parent / ".env"
                if env_path.exists():
                    load_dotenv(env_path)
                    break
        
        # Inicializa configurações
        self.twitter = self._load_twitter_config()
        self.instagram = self._load_instagram_config()
        self.linkedin = self._load_linkedin_config()
        self.ai = self._load_ai_config()
        self.database = self._load_database_config()
        self.dashboard = self._load_dashboard_config()
        self.google = self._load_google_config()
        
        # Configurações gerais
        self.bot_name = os.getenv("BOT_NAME", "SocialBot AI")
        self.bot_version = os.getenv("BOT_VERSION", "1.0.0")
        self.debug = os.getenv("DEBUG", "false").lower() == "true"
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.timezone = os.getenv("TIMEZONE", "America/Sao_Paulo")
        
        # Configurações de conteúdo
        self.default_hashtags = os.getenv("DEFAULT_HASHTAGS", "#AI #automation #socialmedia").split()
        self.preferred_post_times = self._parse_post_times(
            os.getenv("PREFERRED_POST_TIMES", "09:00,12:00,15:00,18:00,21:00")
        )
        
        # Webhooks e integrações
        self.webhook_url = os.getenv("WEBHOOK_URL", "")
        self.webhook_secret = os.getenv("WEBHOOK_SECRET", "")
        self.notion_token = os.getenv("NOTION_TOKEN", "")
        self.trello_api_key = os.getenv("TRELLO_API_KEY", "")
        
        # Monitoramento
        self.sentry_dsn = os.getenv("SENTRY_DSN", "")
        self.prometheus_port = int(os.getenv("PROMETHEUS_PORT", "9090"))
    
    def _load_twitter_config(self) -> TwitterConfig:
        """Carrega configurações do Twitter"""
        return TwitterConfig(
            api_key=os.getenv("TWITTER_API_KEY", ""),
            api_secret=os.getenv("TWITTER_API_SECRET", ""),
            access_token=os.getenv("TWITTER_ACCESS_TOKEN", ""),
            access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET", ""),
            bearer_token=os.getenv("TWITTER_BEARER_TOKEN", ""),
            rate_limit_posts_per_hour=int(os.getenv("TWITTER_RATE_LIMIT_POSTS_PER_HOUR", "50"))
        )
    
    def _load_instagram_config(self) -> InstagramConfig:
        """Carrega configurações do Instagram"""
        return InstagramConfig(
            access_token=os.getenv("INSTAGRAM_ACCESS_TOKEN", ""),
            business_account_id=os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID", ""),
            app_id=os.getenv("FACEBOOK_APP_ID", ""),
            app_secret=os.getenv("FACEBOOK_APP_SECRET", ""),
            rate_limit_posts_per_hour=int(os.getenv("INSTAGRAM_RATE_LIMIT_POSTS_PER_HOUR", "25"))
        )
    
    def _load_linkedin_config(self) -> LinkedInConfig:
        """Carrega configurações do LinkedIn"""
        return LinkedInConfig(
            client_id=os.getenv("LINKEDIN_CLIENT_ID", ""),
            client_secret=os.getenv("LINKEDIN_CLIENT_SECRET", ""),
            access_token=os.getenv("LINKEDIN_ACCESS_TOKEN", ""),
            rate_limit_posts_per_hour=int(os.getenv("LINKEDIN_RATE_LIMIT_POSTS_PER_HOUR", "20"))
        )
    
    def _load_ai_config(self) -> AIConfig:
        """Carrega configurações de IA"""
        return AIConfig(
            huggingface_token=os.getenv("HUGGINGFACE_TOKEN", ""),
            openai_api_key=os.getenv("OPENAI_API_KEY", ""),
            openai_model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
            model_name=os.getenv("AI_MODEL_NAME", "microsoft/DialoGPT-medium"),
            max_length=int(os.getenv("AI_MAX_LENGTH", "280")),
            temperature=float(os.getenv("AI_TEMPERATURE", "0.7")),
            top_p=float(os.getenv("AI_TOP_P", "0.9"))
        )
    
    def _load_database_config(self) -> DatabaseConfig:
        """Carrega configurações do banco de dados"""
        return DatabaseConfig(
            url=os.getenv("DATABASE_URL", "sqlite:///socialbot.db"),
            redis_url=os.getenv("REDIS_URL", "redis://localhost:6379/0")
        )
    
    def _load_dashboard_config(self) -> DashboardConfig:
        """Carrega configurações do dashboard"""
        return DashboardConfig(
            streamlit_port=int(os.getenv("STREAMLIT_PORT", "8501")),
            streamlit_host=os.getenv("STREAMLIT_HOST", "0.0.0.0"),
            fastapi_port=int(os.getenv("FASTAPI_PORT", "8000")),
            fastapi_host=os.getenv("FASTAPI_HOST", "0.0.0.0"),
            secret_key=os.getenv("SECRET_KEY", "change-this-secret-key"),
            admin_username=os.getenv("ADMIN_USERNAME", "admin"),
            admin_password=os.getenv("ADMIN_PASSWORD", "change-this-password")
        )
    
    def _load_google_config(self) -> GoogleConfig:
        """Carrega configurações do Google"""
        return GoogleConfig(
            calendar_credentials_path=os.getenv("GOOGLE_CALENDAR_CREDENTIALS_PATH", "credentials/google_calendar_credentials.json"),
            calendar_id=os.getenv("GOOGLE_CALENDAR_ID", ""),
            sheets_credentials_path=os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH", "credentials/google_sheets_credentials.json"),
            sheets_spreadsheet_id=os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID", "")
        )
    
    def _parse_post_times(self, times_str: str) -> List[str]:
        """Parse dos horários preferenciais para posts"""
        try:
            return [time.strip() for time in times_str.split(",")]
        except:
            return ["09:00", "12:00", "15:00", "18:00", "21:00"]
    
    def is_configured(self, platform: str) -> bool:
        """Verifica se uma plataforma está configurada"""
        if platform.lower() == "twitter":
            return bool(self.twitter.api_key and self.twitter.api_secret)
        elif platform.lower() == "instagram":
            return bool(self.instagram.access_token)
        elif platform.lower() == "linkedin":
            return bool(self.linkedin.client_id and self.linkedin.client_secret)
        return False
    
    def get_configured_platforms(self) -> List[str]:
        """Retorna lista de plataformas configuradas"""
        platforms = []
        if self.is_configured("twitter"):
            platforms.append("twitter")
        if self.is_configured("instagram"):
            platforms.append("instagram")
        if self.is_configured("linkedin"):
            platforms.append("linkedin")
        return platforms
    
    def validate(self) -> Dict[str, List[str]]:
        """Valida todas as configurações e retorna erros encontrados"""
        errors = {
            "twitter": [],
            "instagram": [],
            "linkedin": [],
            "ai": [],
            "general": []
        }
        
        # Validação Twitter
        if self.twitter.api_key and not self.twitter.api_secret:
            errors["twitter"].append("API Secret é obrigatório quando API Key está definida")
        
        # Validação Instagram
        if self.instagram.access_token and not self.instagram.business_account_id:
            errors["instagram"].append("Business Account ID é obrigatório")
        
        # Validação LinkedIn
        if self.linkedin.client_id and not self.linkedin.client_secret:
            errors["linkedin"].append("Client Secret é obrigatório quando Client ID está definido")
        
        # Validação IA
        if not self.ai.huggingface_token and not self.ai.openai_api_key:
            errors["ai"].append("Pelo menos um token de IA (Hugging Face ou OpenAI) é necessário")
        
        # Remove categorias sem erros
        return {k: v for k, v in errors.items() if v}
    
    def __str__(self) -> str:
        """Representação string das configurações (sem dados sensíveis)"""
        return f"""SocialBot AI Configuration:
- Bot: {self.bot_name} v{self.bot_version}
- Debug: {self.debug}
- Timezone: {self.timezone}
- Configured Platforms: {', '.join(self.get_configured_platforms())}
- Database: {self.database.url.split('://')[0]}://...
- Dashboard: {self.dashboard.streamlit_host}:{self.dashboard.streamlit_port}
"""
