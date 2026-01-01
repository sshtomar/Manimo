"""OpenAI GPT provider."""

from openai import AsyncOpenAI

from ..base import LLMClient


class OpenAIProvider(LLMClient):
    """OpenAI GPT LLM provider."""

    def __init__(self, api_key: str, model: str = "gpt-4-turbo-preview"):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model

    async def generate(
        self,
        system: str,
        user: str,
        skills: list[dict] | None = None,
        model_override: str | None = None,
        max_tokens: int = 4096,
    ) -> str:
        """Generate a response using GPT.

        Args:
            system: System prompt
            user: User message
            skills: Ignored for OpenAI (not supported)
            model_override: Optional model to use instead of the default
            max_tokens: Maximum tokens in response

        Returns:
            Generated text response
        """
        model = model_override or self.model

        response = await self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            max_tokens=max_tokens,
        )

        return response.choices[0].message.content or ""

