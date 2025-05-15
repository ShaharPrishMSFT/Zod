"""
Tests for LlmModels unified configuration entry points.
"""

import os
import pytest

from ..models.llm_models import LlmModels

def test_fromopenai_explicit_config():
    config = {
        "provider": "openai",
        "model": "gpt-4.1",
        "api_key": "sk-test",
        "api_base": "https://api.openai.com/v1",
        "api_version": "2020-01-01"
    }
    result = LlmModels.FromOpenAi(config)
    assert result["provider"] == "openai"
    assert result["model"] == "gpt-4.1"
    assert result["api_key"] == "sk-test"
    assert result["api_base"] == "https://api.openai.com/v1"
    assert result["api_version"] == "2020-01-01"

def test_fromopenai_env(monkeypatch):
    monkeypatch.setenv("OPENAI_MODEL", "gpt-3.5-turbo")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-env")
    monkeypatch.setenv("OPENAI_API_BASE", "https://env.openai.com/v1")
    monkeypatch.setenv("OPENAI_API_VERSION", "2021-01-01")
    result = LlmModels.FromOpenAi()
    assert result["provider"] == "openai"
    assert result["model"] == "gpt-3.5-turbo"
    assert result["api_key"] == "sk-env"
    assert result["api_base"] == "https://env.openai.com/v1"
    assert result["api_version"] == "2021-01-01"

def test_fromopenai_defaults(monkeypatch):
    monkeypatch.delenv("OPENAI_MODEL", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    result = LlmModels.FromOpenAi()
    assert result["provider"] == "openai"
    assert result["model"] == "gpt-4.1"
    # api_key may be None if not set

def test_from_litellm_explicit_config():
    config = {
        "provider": "azure",
        "model": "azure/my-deployment",
        "api_key": "azure-key",
        "api_base": "https://azure.openai.com",
        "api_version": "2025-01-01",
        "deployment": "my-deployment"
    }
    result = LlmModels.From(config)
    assert result["provider"] == "azure"
    assert result["model"] == "azure/my-deployment"
    assert result["api_key"] == "azure-key"
    assert result["api_base"] == "https://azure.openai.com"
    assert result["api_version"] == "2025-01-01"
    assert result["deployment"] == "my-deployment"

def test_from_litellm_env(monkeypatch):
    monkeypatch.setenv("LITELLM_PROVIDER", "azure")
    monkeypatch.setenv("LITELLM_MODEL", "azure/env-deployment")
    monkeypatch.setenv("LITELLM_API_KEY", "env-azure-key")
    monkeypatch.setenv("LITELLM_API_BASE", "https://env.azure.com")
    monkeypatch.setenv("LITELLM_API_VERSION", "2026-01-01")
    monkeypatch.setenv("LITELLM_DEPLOYMENT", "env-deployment")
    result = LlmModels.From()
    assert result["provider"] == "azure"
    assert result["model"] == "azure/env-deployment"
    assert result["api_key"] == "env-azure-key"
    assert result["api_base"] == "https://env.azure.com"
    assert result["api_version"] == "2026-01-01"
    assert result["deployment"] == "env-deployment"

def test_from_litellm_env_fallback(monkeypatch):
    # Only set OPENAI_API_KEY and AZURE_DEPLOYMENT_NAME, should fallback
    monkeypatch.delenv("LITELLM_API_KEY", raising=False)
    monkeypatch.setenv("OPENAI_API_KEY", "fallback-key")
    monkeypatch.setenv("AZURE_DEPLOYMENT_NAME", "fallback-deployment")
    result = LlmModels.From()
    assert result["api_key"] == "fallback-key"
    assert result["deployment"] == "fallback-deployment"
