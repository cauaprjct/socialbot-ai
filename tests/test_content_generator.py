"""
Testes para o módulo ContentGenerator

Testa a geração de conteúdo usando IA.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.ai.content_generator import (
    ContentGenerator, 
    ContentRequest, 
    ContentTone, 
    ContentType,
    GeneratedContent
)
from src.utils.config import AIConfig


@pytest.fixture
def ai_config():
    """Fixture para configuração de IA"""
    return AIConfig(
        huggingface_token="test_token",
        openai_api_key="test_key",
        temperature=0.7,
        top_p=0.9,
        max_length=100
    )


@pytest.fixture
def content_generator(ai_config):
    """Fixture para ContentGenerator"""
    return ContentGenerator(ai_config)


@pytest.fixture
def sample_request():
    """Fixture para requisição de conteúdo"""
    return ContentRequest(
        topic="Python Programming",
        tone=ContentTone.CASUAL,
        content_type=ContentType.POST,
        platform="twitter",
        max_length=280,
        include_hashtags=True,
        include_emojis=True
    )


class TestContentGenerator:
    """Testes para a classe ContentGenerator"""
    
    def test_init(self, ai_config):
        """Testa inicialização do ContentGenerator"""
        generator = ContentGenerator(ai_config)
        
        assert generator.config == ai_config
        assert generator.logger is not None
        assert hasattr(generator, 'huggingface_pipeline')
        assert hasattr(generator, 'openai_client')
    
    def test_content_request_creation(self):
        """Testa criação de ContentRequest"""
        request = ContentRequest(
            topic="Test Topic",
            platform="twitter"
        )
        
        assert request.topic == "Test Topic"
        assert request.platform == "twitter"
        assert request.tone == ContentTone.CASUAL  # Valor padrão
        assert request.content_type == ContentType.POST  # Valor padrão
        assert request.max_length == 280  # Valor padrão
        assert request.include_hashtags is True
        assert request.include_emojis is True
    
    @pytest.mark.asyncio
    async def test_generate_content_success(self, content_generator, sample_request):
        """Testa geração de conteúdo bem-sucedida"""
        # Mock da resposta da IA
        mock_response = {
            "text": "Python é uma linguagem incrível! 🐍",
            "hashtags": ["#Python", "#Programming", "#Code"],
            "confidence": 0.95
        }
        
        with patch.object(content_generator, '_generate_with_openai', 
                         return_value=mock_response) as mock_openai:
            
            result = await content_generator.generate_content(sample_request)
            
            assert isinstance(result, GeneratedContent)
            assert result.text == mock_response["text"]
            assert result.hashtags == mock_response["hashtags"]
            assert result.confidence_score == mock_response["confidence"]
            assert result.platform == sample_request.platform
            assert result.tone == sample_request.tone
            
            mock_openai.assert_called_once_with(sample_request)
    
    @pytest.mark.asyncio
    async def test_generate_content_fallback_to_huggingface(self, content_generator, sample_request):
        """Testa fallback para Hugging Face quando OpenAI falha"""
        mock_hf_response = {
            "text": "Conteúdo gerado pelo Hugging Face",
            "hashtags": ["#AI", "#HuggingFace"],
            "confidence": 0.85
        }
        
        with patch.object(content_generator, '_generate_with_openai', 
                         side_effect=Exception("OpenAI Error")) as mock_openai, \
             patch.object(content_generator, '_generate_with_huggingface', 
                         return_value=mock_hf_response) as mock_hf:
            
            result = await content_generator.generate_content(sample_request)
            
            assert isinstance(result, GeneratedContent)
            assert result.text == mock_hf_response["text"]
            assert result.hashtags == mock_hf_response["hashtags"]
            assert result.confidence_score == mock_hf_response["confidence"]
            
            mock_openai.assert_called_once_with(sample_request)
            mock_hf.assert_called_once_with(sample_request)
    
    @pytest.mark.asyncio
    async def test_generate_content_failure(self, content_generator, sample_request):
        """Testa falha na geração de conteúdo"""
        with patch.object(content_generator, '_generate_with_openai', 
                         side_effect=Exception("OpenAI Error")), \
             patch.object(content_generator, '_generate_with_huggingface', 
                         side_effect=Exception("HuggingFace Error")):
            
            result = await content_generator.generate_content(sample_request)
            
            assert result is None
    
    def test_validate_request_valid(self, content_generator, sample_request):
        """Testa validação de requisição válida"""
        is_valid = content_generator._validate_request(sample_request)
        assert is_valid is True
    
    def test_validate_request_invalid_topic(self, content_generator):
        """Testa validação com tópico inválido"""
        request = ContentRequest(
            topic="",  # Tópico vazio
            platform="twitter"
        )
        
        is_valid = content_generator._validate_request(request)
        assert is_valid is False
    
    def test_validate_request_invalid_platform(self, content_generator):
        """Testa validação com plataforma inválida"""
        request = ContentRequest(
            topic="Valid Topic",
            platform="invalid_platform"
        )
        
        is_valid = content_generator._validate_request(request)
        assert is_valid is False
    
    def test_build_prompt_twitter(self, content_generator, sample_request):
        """Testa construção de prompt para Twitter"""
        prompt = content_generator._build_prompt(sample_request)
        
        assert sample_request.topic in prompt
        assert "Twitter" in prompt or "twitter" in prompt
        assert str(sample_request.max_length) in prompt
        assert "hashtags" in prompt.lower()
        assert "emojis" in prompt.lower()
    
    def test_build_prompt_professional_tone(self, content_generator):
        """Testa construção de prompt com tom profissional"""
        request = ContentRequest(
            topic="Business Strategy",
            platform="linkedin",
            tone=ContentTone.PROFESSIONAL
        )
        
        prompt = content_generator._build_prompt(request)
        
        assert "professional" in prompt.lower() or "profissional" in prompt.lower()
        assert "business" in prompt.lower() or "negócios" in prompt.lower()
    
    def test_extract_hashtags(self, content_generator):
        """Testa extração de hashtags"""
        text = "Este é um post sobre #Python e #AI com #MachineLearning!"
        
        hashtags = content_generator._extract_hashtags(text)
        
        expected_hashtags = ["#Python", "#AI", "#MachineLearning"]
        assert hashtags == expected_hashtags
    
    def test_extract_hashtags_no_hashtags(self, content_generator):
        """Testa extração quando não há hashtags"""
        text = "Este é um post sem hashtags."
        
        hashtags = content_generator._extract_hashtags(text)
        
        assert hashtags == []
    
    def test_extract_emojis(self, content_generator):
        """Testa extração de emojis"""
        text = "Olá mundo! 😀 Python é incrível! 🐍✨"
        
        emojis = content_generator._extract_emojis(text)
        
        expected_emojis = ["😀", "🐍", "✨"]
        assert emojis == expected_emojis
    
    def test_extract_emojis_no_emojis(self, content_generator):
        """Testa extração quando não há emojis"""
        text = "Este e um post sem emojis."
        
        emojis = content_generator._extract_emojis(text)
        
        assert emojis == []
    
    def test_calculate_confidence_high(self, content_generator):
        """Testa cálculo de confiança alta"""
        text = "Este é um post bem estruturado com #hashtags e emojis! 🚀"
        request = ContentRequest(
            topic="estrutura",
            platform="twitter",
            include_hashtags=True,
            include_emojis=True
        )
        
        confidence = content_generator._calculate_confidence(text, request)
        
        assert confidence > 0.8  # Alta confiança
    
    def test_calculate_confidence_low(self, content_generator):
        """Testa cálculo de confiança baixa"""
        text = "Post simples."
        request = ContentRequest(
            topic="complexidade",
            platform="twitter",
            include_hashtags=True,
            include_emojis=True
        )
        
        confidence = content_generator._calculate_confidence(text, request)
        
        assert confidence < 0.5  # Baixa confiança
    
    def test_adjust_content_for_platform_twitter(self, content_generator):
        """Testa ajuste de conteúdo para Twitter"""
        long_text = "Este é um texto muito longo que excede o limite do Twitter " * 10
        
        adjusted = content_generator._adjust_content_for_platform(long_text, "twitter")
        
        assert len(adjusted) <= 280
        assert adjusted.endswith("...")
    
    def test_adjust_content_for_platform_linkedin(self, content_generator):
        """Testa ajuste de conteúdo para LinkedIn"""
        text = "Conteúdo profissional para LinkedIn."
        
        adjusted = content_generator._adjust_content_for_platform(text, "linkedin")
        
        # LinkedIn permite textos mais longos
        assert len(adjusted) <= 3000
        assert adjusted == text  # Não deve ser truncado
    
    @pytest.mark.asyncio
    async def test_generate_variations(self, content_generator, sample_request):
        """Testa geração de variações de conteúdo"""
        mock_responses = [
            {
                "text": "Variação 1 do conteúdo",
                "hashtags": ["#Python"],
                "confidence": 0.9
            },
            {
                "text": "Variação 2 do conteúdo",
                "hashtags": ["#Code"],
                "confidence": 0.85
            }
        ]
        
        with patch.object(content_generator, '_generate_with_openai', 
                         side_effect=mock_responses):
            
            variations = await content_generator.generate_variations(
                sample_request, 
                count=2
            )
            
            assert len(variations) == 2
            assert all(isinstance(v, GeneratedContent) for v in variations)
            assert variations[0].text == mock_responses[0]["text"]
            assert variations[1].text == mock_responses[1]["text"]
    
    @pytest.mark.asyncio
    async def test_optimize_for_engagement(self, content_generator):
        """Testa otimização para engajamento"""
        base_content = GeneratedContent(
            text="Conteúdo base",
            hashtags=["#test"],
            emojis=[],
            tone=ContentTone.CASUAL,
            platform="twitter",
            confidence_score=0.7,
            metadata={}
        )
        
        optimized = await content_generator.optimize_for_engagement(
            base_content,
            target_audience="developers"
        )
        
        assert isinstance(optimized, GeneratedContent)
        assert optimized.confidence_score >= base_content.confidence_score
    
    def test_content_tone_enum(self):
        """Testa enum ContentTone"""
        assert ContentTone.PROFESSIONAL.value == "professional"
        assert ContentTone.CASUAL.value == "casual"
        assert ContentTone.FUNNY.value == "funny"
        assert ContentTone.INSPIRATIONAL.value == "inspirational"
        assert ContentTone.EDUCATIONAL.value == "educational"
        assert ContentTone.PROMOTIONAL.value == "promotional"
    
    def test_content_type_enum(self):
        """Testa enum ContentType"""
        assert ContentType.POST.value == "post"
        assert ContentType.CAPTION.value == "caption"
        assert ContentType.THREAD.value == "thread"
        assert ContentType.STORY.value == "story"
        assert ContentType.REPLY.value == "reply"


class TestGeneratedContent:
    """Testes para a classe GeneratedContent"""
    
    def test_generated_content_creation(self):
        """Testa criação de GeneratedContent"""
        content = GeneratedContent(
            text="Conteúdo de teste",
            hashtags=["#test", "#python"],
            emojis=["🚀", "🐍"],
            tone=ContentTone.CASUAL,
            platform="twitter",
            confidence_score=0.95,
            metadata={"source": "openai"}
        )
        
        assert content.text == "Conteúdo de teste"
        assert content.hashtags == ["#test", "#python"]
        assert content.emojis == ["🚀", "🐍"]
        assert content.tone == ContentTone.CASUAL
        assert content.platform == "twitter"
        assert content.confidence_score == 0.95
        assert content.metadata["source"] == "openai"
    
    def test_generated_content_str_representation(self):
        """Testa representação string de GeneratedContent"""
        content = GeneratedContent(
            text="Teste",
            hashtags=["#test"],
            emojis=["🚀"],
            tone=ContentTone.CASUAL,
            platform="twitter",
            confidence_score=0.9,
            metadata={}
        )
        
        str_repr = str(content)
        assert "Teste" in str_repr
        assert "twitter" in str_repr
        assert "0.9" in str_repr


# Testes de integração
class TestContentGeneratorIntegration:
    """Testes de integração para ContentGenerator"""
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_full_content_generation_flow(self, ai_config):
        """Testa fluxo completo de geração de conteúdo"""
        # Este teste requer configurações reais de API
        # Pule se não estiver em ambiente de integração
        if not ai_config.openai_api_key or ai_config.openai_api_key == "test_key":
            pytest.skip("Teste de integração requer API key real")
        
        generator = ContentGenerator(ai_config)
        
        request = ContentRequest(
            topic="inteligência artificial",
            platform="twitter",
            tone=ContentTone.EDUCATIONAL,
            max_length=280
        )
        
        content = await generator.generate_content(request)
        
        assert content is not None
        assert isinstance(content, GeneratedContent)
        assert len(content.text) <= 280
        assert content.confidence_score > 0
        assert content.platform == "twitter"
        assert content.tone == ContentTone.EDUCATIONAL


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
