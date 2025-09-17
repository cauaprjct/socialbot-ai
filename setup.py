#!/usr/bin/env python3
"""
Setup script para o SocialBot AI
"""

from setuptools import setup, find_packages
from pathlib import Path

# Lê o README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Lê os requirements
requirements = []
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="socialbot-ai",
    version="1.0.0",
    author="SocialBot AI Team",
    author_email="socialbot.ai@gmail.com",
    description="Bot de Automação para Redes Sociais com IA",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cauaprjct/socialbot-ai",
    project_urls={
        "Bug Tracker": "https://github.com/cauaprjct/socialbot-ai/issues",
        "Documentation": "https://github.com/cauaprjct/socialbot-ai/wiki",
        "Source Code": "https://github.com/cauaprjct/socialbot-ai",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Communications",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.21.1",
            "pytest-cov>=4.1.0",
            "black>=23.11.0",
            "flake8>=6.1.0",
            "mypy>=1.7.1",
            "pre-commit>=3.5.0",
        ],
        "docs": [
            "sphinx>=7.1.2",
            "sphinx-rtd-theme>=1.3.0",
            "myst-parser>=2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "socialbot-ai=src.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "socialbot-ai": [
            "*.md",
            "*.txt",
            "*.yml",
            "*.yaml",
            "*.json",
        ],
    },
    keywords=[
        "social media",
        "automation",
        "ai",
        "bot",
        "twitter",
        "instagram",
        "linkedin",
        "content generation",
        "machine learning",
        "nlp",
    ],
    zip_safe=False,
)