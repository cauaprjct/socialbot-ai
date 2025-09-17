# 🤝 Contribuindo para o SocialBot AI

Obrigado por considerar contribuir para o SocialBot AI! Este documento fornece diretrizes para contribuições.

## 🎯 Como Contribuir

### 🐛 Reportando Bugs

1. **Verifique** se o bug já foi reportado nas [Issues](https://github.com/cauaprjct/socialbot-ai/issues)
2. **Crie uma nova issue** com:
   - Título claro e descritivo
   - Descrição detalhada do problema
   - Passos para reproduzir
   - Comportamento esperado vs atual
   - Screenshots (se aplicável)
   - Informações do ambiente (OS, Python version, etc.)

### 💡 Sugerindo Features

1. **Verifique** se a feature já foi sugerida
2. **Crie uma issue** com:
   - Título claro
   - Descrição detalhada da feature
   - Justificativa (por que seria útil)
   - Exemplos de uso
   - Mockups ou diagramas (se aplicável)

### 🔧 Contribuindo com Código

#### Configuração do Ambiente

```bash
# 1. Fork o repositório
# 2. Clone seu fork
git clone https://github.com/SEU_USERNAME/socialbot-ai.git
cd socialbot-ai

# 3. Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 4. Instale dependências
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 5. Configure pre-commit hooks
pre-commit install

# 6. Execute testes
pytest
```

#### Processo de Desenvolvimento

1. **Crie uma branch** para sua feature/fix:
   ```bash
   git checkout -b feature/nome-da-feature
   # ou
   git checkout -b fix/nome-do-bug
   ```

2. **Desenvolva** seguindo as diretrizes de código

3. **Teste** suas mudanças:
   ```bash
   # Testes unitários
   pytest tests/
   
   # Testes de integração
   pytest tests/integration/
   
   # Cobertura
   pytest --cov=src tests/
   ```

4. **Commit** suas mudanças:
   ```bash
   git add .
   git commit -m "feat: adiciona nova funcionalidade X"
   ```

5. **Push** para seu fork:
   ```bash
   git push origin feature/nome-da-feature
   ```

6. **Crie um Pull Request**

## 📝 Diretrizes de Código

### Estilo de Código

- **Python**: Seguimos PEP 8
- **Formatação**: Usamos Black
- **Linting**: Usamos Flake8
- **Type hints**: Obrigatórios para funções públicas
- **Docstrings**: Formato Google Style

### Estrutura de Commits

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

```
type(scope): description

[optional body]

[optional footer]
```

**Tipos:**
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `style`: Formatação
- `refactor`: Refatoração
- `test`: Testes
- `chore`: Tarefas de manutenção

**Exemplos:**
```
feat(twitter): adiciona suporte a threads
fix(ai): corrige geração de hashtags
docs(readme): atualiza instruções de instalação
```

### Testes

- **Cobertura mínima**: 80%
- **Testes unitários**: Para toda lógica de negócio
- **Testes de integração**: Para APIs externas
- **Mocks**: Para dependências externas

```python
# Exemplo de teste
import pytest
from unittest.mock import Mock, patch

from src.bot.twitter_bot import TwitterBot

@pytest.mark.asyncio
async def test_twitter_bot_post():
    """Testa publicação no Twitter"""
    bot = TwitterBot(mock_config)
    
    with patch('tweepy.Client') as mock_client:
        mock_client.create_tweet.return_value = Mock(data={'id': '123'})
        
        result = await bot.post("Test message")
        
        assert result.success is True
        assert result.post_id == '123'
```

### Documentação

- **Docstrings**: Para todas as classes e funções públicas
- **README**: Mantenha atualizado
- **Changelog**: Documente mudanças importantes
- **Exemplos**: Adicione exemplos de uso

```python
def generate_content(topic: str, style: str = "casual") -> str:
    """
    Gera conteúdo usando IA.
    
    Args:
        topic: Tópico para o conteúdo
        style: Estilo do conteúdo (casual, formal, etc.)
        
    Returns:
        Conteúdo gerado
        
    Raises:
        ContentGenerationError: Se falhar na geração
        
    Example:
        >>> content = generate_content("IA", "profissional")
        >>> print(content)
        "A inteligência artificial está revolucionando..."
    """
```

## 🏗️ Arquitetura

### Princípios

- **SOLID**: Seguimos os princípios SOLID
- **Clean Architecture**: Separação clara de responsabilidades
- **Dependency Injection**: Para testabilidade
- **Async/Await**: Para operações I/O

### Estrutura de Pastas

```
src/
├── bot/           # Bots das plataformas
├── ai/            # Módulos de IA
├── analytics/     # Sistema de analytics
├── dashboard/     # Interface web
├── integrations/  # Integrações externas
├── interfaces/    # Interfaces e contratos
└── utils/         # Utilitários
```

### Padrões

- **Repository Pattern**: Para acesso a dados
- **Factory Pattern**: Para criação de objetos
- **Observer Pattern**: Para eventos
- **Circuit Breaker**: Para resiliência

## 🚀 Deploy e CI/CD

### GitHub Actions

Temos workflows para:
- **Testes**: Executados em PRs
- **Linting**: Verificação de código
- **Security**: Scan de vulnerabilidades
- **Deploy**: Automático na main

### Docker

- **Multi-stage builds**: Para otimização
- **Health checks**: Para monitoramento
- **Security**: Non-root user

## 📋 Checklist para PRs

- [ ] Código segue as diretrizes de estilo
- [ ] Testes passam (unitários e integração)
- [ ] Cobertura de testes mantida/melhorada
- [ ] Documentação atualizada
- [ ] Changelog atualizado (se necessário)
- [ ] Commits seguem padrão conventional
- [ ] PR tem descrição clara
- [ ] Breaking changes documentadas

## 🎖️ Reconhecimento

Contribuições são reconhecidas:
- **Contributors**: Listados no README
- **Hall of Fame**: Para contribuições significativas
- **Badges**: Para diferentes tipos de contribuição

## 📞 Suporte

- **Discord**: [Link do servidor](https://discord.gg/socialbot-ai)
- **Discussions**: [GitHub Discussions](https://github.com/cauaprjct/socialbot-ai/discussions)
- **Email**: socialbot.ai@gmail.com

## 📄 Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a [MIT License](LICENSE).

---

**Obrigado por contribuir! 🙏**