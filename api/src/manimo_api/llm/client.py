"""LLM client factory."""

from ..config import settings
from .base import LLMClient
from .providers.anthropic import AnthropicProvider
from .providers.openai import OpenAIProvider


def get_llm_client() -> LLMClient:
    """Get the configured LLM client."""
    provider = settings.DEFAULT_LLM_PROVIDER

    if provider == "anthropic":
        return AnthropicProvider(
            api_key=settings.ANTHROPIC_API_KEY,
            model=settings.DEFAULT_MODEL,
        )
    elif provider == "openai":
        return OpenAIProvider(
            api_key=settings.OPENAI_API_KEY,
            model=settings.DEFAULT_MODEL,
        )
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")

