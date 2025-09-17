"""
Sistema de Exceções Customizadas do SocialBot AI

Hierarquia robusta de exceções para melhor tratamento de erros,
debugging e monitoramento do sistema.
"""

from typing import Dict, Any, Optional, List
from enum import Enum
import traceback
from datetime import datetime


class ErrorCode(Enum):
    """Códigos de erro padronizados"""
    
    # Erros de Configuração (1000-1099)
    CONFIG_MISSING = 1000
    CONFIG_INVALID = 1001
    CONFIG_API_KEY_MISSING = 1002
    CONFIG_API_KEY_INVALID = 1003
    
    # Erros de API (2000-2099)
    API_CONNECTION_FAILED = 2000
    API_AUTHENTICATION_FAILED = 2001
    API_RATE_LIMIT_EXCEEDED = 2002
    API_QUOTA_EXCEEDED = 2003
    API_INVALID_REQUEST = 2004
    API_SERVER_ERROR = 2005
    API_TIMEOUT = 2006
    
    # Erros de Conteúdo (3000-3099)
    CONTENT_GENERATION_FAILED = 3000
    CONTENT_TOO_LONG = 3001
    CONTENT_INVALID_FORMAT = 3002
    CONTENT_MODERATION_FAILED = 3003
    
    # Erros de Agendamento (4000-4099)
    SCHEDULE_INVALID_TIME = 4000
    SCHEDULE_CONFLICT = 4001
    SCHEDULE_EXECUTION_FAILED = 4002
    
    # Erros de Banco de Dados (5000-5099)
    DATABASE_CONNECTION_FAILED = 5000
    DATABASE_QUERY_FAILED = 5001
    DATABASE_CONSTRAINT_VIOLATION = 5002
    
    # Erros de Cache (6000-6099)
    CACHE_CONNECTION_FAILED = 6000
    CACHE_OPERATION_FAILED = 6001
    
    # Erros de IA (7000-7099)
    AI_MODEL_NOT_AVAILABLE = 7000
    AI_GENERATION_FAILED = 7001
    AI_QUOTA_EXCEEDED = 7002
    
    # Erros de Sistema (8000-8099)
    SYSTEM_RESOURCE_EXHAUSTED = 8000
    SYSTEM_DEPENDENCY_UNAVAILABLE = 8001
    SYSTEM_INTERNAL_ERROR = 8002


class SocialBotError(Exception):
    """
    Exceção base do SocialBot AI
    
    Fornece contexto rico para debugging e monitoramento.
    """
    
    def __init__(
        self,
        message: str,
        error_code: ErrorCode,
        details: Optional[Dict[str, Any]] = None,
        cause: Optional[Exception] = None,
        user_message: Optional[str] = None,
        retry_after: Optional[int] = None
    ):
        """
        Inicializa exceção customizada
        
        Args:
            message: Mensagem técnica detalhada
            error_code: Código de erro padronizado
            details: Contexto adicional para debugging
            cause: Exceção original que causou este erro
            user_message: Mensagem amigável para o usuário
            retry_after: Segundos para tentar novamente (se aplicável)
        """
        super().__init__(message)
        
        self.error_code = error_code
        self.details = details or {}
        self.cause = cause
        self.user_message = user_message or self._get_default_user_message()
        self.retry_after = retry_after
        self.timestamp = datetime.utcnow()
        self.traceback_str = traceback.format_exc()
        
        # Adiciona informações da exceção original
        if cause:
            self.details["original_error"] = str(cause)
            self.details["original_type"] = type(cause).__name__
    
    def _get_default_user_message(self) -> str:
        """Gera mensagem padrão amigável para o usuário"""
        category = self.error_code.value // 1000
        
        messages = {
            1: "Erro de configuração. Verifique suas credenciais.",
            2: "Erro de conexão com a API. Tente novamente em alguns minutos.",
            3: "Erro na geração de conteúdo. Tente com um tópico diferente.",
            4: "Erro no agendamento. Verifique a data e horário.",
            5: "Erro interno do sistema. Nossa equipe foi notificada.",
            6: "Erro temporário. Tente novamente em alguns segundos.",
            7: "Serviço de IA temporariamente indisponível.",
            8: "Erro interno do sistema. Nossa equipe foi notificada."
        }
        
        return messages.get(category, "Erro inesperado. Tente novamente.")
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte exceção para dicionário para logging/serialização"""
        return {
            "error_code": self.error_code.value,
            "error_name": self.error_code.name,
            "message": str(self),
            "user_message": self.user_message,
            "details": self.details,
            "timestamp": self.timestamp.isoformat(),
            "retry_after": self.retry_after,
            "cause": str(self.cause) if self.cause else None
        }
    
    def __str__(self) -> str:
        """String representation com código de erro"""
        return f"[{self.error_code.name}] {super().__str__()}"


# Exceções específicas por categoria

class ConfigurationError(SocialBotError):
    """Erros relacionados à configuração do sistema"""
    
    def __init__(self, message: str, config_key: Optional[str] = None, **kwargs):
        if config_key:
            kwargs.setdefault("details", {})["config_key"] = config_key
        
        super().__init__(
            message=message,
            error_code=kwargs.pop("error_code", ErrorCode.CONFIG_INVALID),
            **kwargs
        )


class APIError(SocialBotError):
    """Erros relacionados a APIs externas"""
    
    def __init__(
        self,
        message: str,
        platform: Optional[str] = None,
        status_code: Optional[int] = None,
        response_body: Optional[str] = None,
        **kwargs
    ):
        details = kwargs.setdefault("details", {})
        if platform:
            details["platform"] = platform
        if status_code:
            details["status_code"] = status_code
        if response_body:
            details["response_body"] = response_body[:1000]  # Limita tamanho
        
        super().__init__(
            message=message,
            error_code=kwargs.pop("error_code", ErrorCode.API_CONNECTION_FAILED),
            **kwargs
        )


class RateLimitError(APIError):
    """Erro específico de rate limiting"""
    
    def __init__(self, message: str, retry_after: int = 60, **kwargs):
        super().__init__(
            message=message,
            error_code=ErrorCode.API_RATE_LIMIT_EXCEEDED,
            retry_after=retry_after,
            user_message=f"Limite de requisições atingido. Tente novamente em {retry_after} segundos.",
            **kwargs
        )


class AuthenticationError(APIError):
    """Erro de autenticação com APIs"""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message=message,
            error_code=ErrorCode.API_AUTHENTICATION_FAILED,
            user_message="Credenciais inválidas. Verifique suas chaves de API.",
            **kwargs
        )


class ContentError(SocialBotError):
    """Erros relacionados à geração e processamento de conteúdo"""
    
    def __init__(self, message: str, content_type: Optional[str] = None, **kwargs):
        if content_type:
            kwargs.setdefault("details", {})["content_type"] = content_type
        
        super().__init__(
            message=message,
            error_code=kwargs.pop("error_code", ErrorCode.CONTENT_GENERATION_FAILED),
            **kwargs
        )


class SchedulingError(SocialBotError):
    """Erros relacionados ao agendamento de posts"""
    
    def __init__(self, message: str, schedule_time: Optional[str] = None, **kwargs):
        if schedule_time:
            kwargs.setdefault("details", {})["schedule_time"] = schedule_time
        
        super().__init__(
            message=message,
            error_code=kwargs.pop("error_code", ErrorCode.SCHEDULE_INVALID_TIME),
            **kwargs
        )


class DatabaseError(SocialBotError):
    """Erros relacionados ao banco de dados"""
    
    def __init__(self, message: str, query: Optional[str] = None, **kwargs):
        if query:
            kwargs.setdefault("details", {})["query"] = query[:500]  # Limita tamanho
        
        super().__init__(
            message=message,
            error_code=kwargs.pop("error_code", ErrorCode.DATABASE_CONNECTION_FAILED),
            **kwargs
        )


class AIError(SocialBotError):
    """Erros relacionados aos serviços de IA"""
    
    def __init__(self, message: str, model_name: Optional[str] = None, **kwargs):
        if model_name:
            kwargs.setdefault("details", {})["model_name"] = model_name
        
        super().__init__(
            message=message,
            error_code=kwargs.pop("error_code", ErrorCode.AI_MODEL_NOT_AVAILABLE),
            **kwargs
        )


class SystemError(SocialBotError):
    """Erros de sistema e recursos"""
    
    def __init__(self, message: str, resource: Optional[str] = None, **kwargs):
        if resource:
            kwargs.setdefault("details", {})["resource"] = resource
        
        super().__init__(
            message=message,
            error_code=kwargs.pop("error_code", ErrorCode.SYSTEM_INTERNAL_ERROR),
            **kwargs
        )


# Utilitários para tratamento de exceções

def handle_api_response(response, platform: str = "unknown"):
    """
    Analisa resposta de API e levanta exceção apropriada se necessário
    
    Args:
        response: Objeto de resposta HTTP
        platform: Nome da plataforma (Twitter, Instagram, etc.)
        
    Raises:
        APIError: Se a resposta indica erro
    """
    if response.status_code == 200:
        return
    
    error_map = {
        401: AuthenticationError,
        403: AuthenticationError,
        429: RateLimitError,
        500: APIError,
        502: APIError,
        503: APIError,
        504: APIError
    }
    
    error_class = error_map.get(response.status_code, APIError)
    
    # Extrai retry_after do header se disponível
    retry_after = None
    if response.status_code == 429:
        retry_after = int(response.headers.get("Retry-After", 60))
    
    raise error_class(
        message=f"API request failed: {response.status_code} {response.reason}",
        platform=platform,
        status_code=response.status_code,
        response_body=response.text,
        retry_after=retry_after
    )


def log_exception(logger, exception: Exception, context: Optional[Dict[str, Any]] = None):
    """
    Loga exceção com contexto estruturado
    
    Args:
        logger: Logger instance
        exception: Exceção para logar
        context: Contexto adicional
    """
    if isinstance(exception, SocialBotError):
        log_data = exception.to_dict()
        if context:
            log_data["context"] = context
        
        logger.error(
            f"SocialBot Error: {exception.error_code.name}",
            extra=log_data
        )
    else:
        logger.error(
            f"Unexpected error: {type(exception).__name__}: {exception}",
            extra={
                "exception_type": type(exception).__name__,
                "exception_message": str(exception),
                "context": context or {},
                "traceback": traceback.format_exc()
            }
        )


def is_retryable_error(exception: Exception) -> bool:
    """
    Determina se um erro é passível de retry
    
    Args:
        exception: Exceção para analisar
        
    Returns:
        True se o erro pode ser tentado novamente
    """
    if isinstance(exception, SocialBotError):
        retryable_codes = {
            ErrorCode.API_CONNECTION_FAILED,
            ErrorCode.API_TIMEOUT,
            ErrorCode.API_SERVER_ERROR,
            ErrorCode.DATABASE_CONNECTION_FAILED,
            ErrorCode.CACHE_CONNECTION_FAILED,
            ErrorCode.SYSTEM_RESOURCE_EXHAUSTED
        }
        return exception.error_code in retryable_codes
    
    # Exceções padrão que são retryable
    retryable_types = (
        ConnectionError,
        TimeoutError,
        OSError
    )
    
    return isinstance(exception, retryable_types)


def get_retry_delay(exception: Exception, attempt: int) -> int:
    """
    Calcula delay para retry baseado na exceção e tentativa
    
    Args:
        exception: Exceção que causou a falha
        attempt: Número da tentativa (1-based)
        
    Returns:
        Delay em segundos
    """
    if isinstance(exception, RateLimitError) and exception.retry_after:
        return exception.retry_after
    
    # Backoff exponencial com jitter
    base_delay = min(2 ** attempt, 300)  # Max 5 minutos
    jitter = base_delay * 0.1  # 10% de jitter
    
    import random
    return int(base_delay + random.uniform(-jitter, jitter))