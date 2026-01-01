"""Base LLM client abstract class."""

from abc import ABC, abstractmethod


class LLMClient(ABC):
    """Abstract LLM client."""

    @abstractmethod
    async def generate(
        self,
        system: str,
        user: str,
        skills: list[dict] | None = None,
        model_override: str | None = None,
        max_tokens: int = 4096,
    ) -> str:
        """Generate a response.

        Args:
            system: System prompt
            user: User message
            skills: Optional list of skill configs (provider-specific format)
            model_override: Optional model to use instead of the default
            max_tokens: Maximum tokens in response

        Returns:
            Generated text response
        """
        pass

    async def verify_with_vision(
        self,
        system: str,
        user: str,
        image_base64: str,
        media_type: str = "image/png",
    ) -> str:
        """Verify output using vision capabilities.

        Args:
            system: System prompt
            user: User message/question about the image
            image_base64: Base64-encoded image data
            media_type: Image MIME type (default: image/png)

        Returns:
            Verification response text

        Raises:
            NotImplementedError: If provider doesn't support vision
        """
        raise NotImplementedError("Vision not supported by this provider")

