"""Anthropic Claude provider."""

import json
import os
from datetime import datetime

import logfire
from anthropic import AsyncAnthropic

from ...config import settings
from ..base import LLMClient


class AnthropicProvider(LLMClient):
    """Anthropic Claude LLM provider with dual-model support."""

    def __init__(self, api_key: str, model: str = "claude-haiku-4-5-20251001"):
        self.client = AsyncAnthropic(api_key=api_key)
        self.model = model

        self.log_dir = "llm_logs"
        os.makedirs(self.log_dir, exist_ok=True)

    async def generate(
        self,
        system: str,
        user: str,
        skills: list[dict] | None = None,
        model_override: str | None = None,
        max_tokens: int = 4096,
    ) -> str:
        """Generate a response using Claude with optional skills.

        Args:
            system: System prompt
            user: User message
            skills: Optional list of skill configs in format:
                    [{"type": "custom", "skill_id": "skill_...", "version": "..."}]
            model_override: Optional model to use instead of the default
            max_tokens: Maximum tokens in response

        Returns:
            Generated text response
        """
        model = model_override or self.model
        timestamp = datetime.now().isoformat()

        with logfire.span(
            "llm.generate",
            model=model,
            system_length=len(system),
            user_length=len(user),
            skills_count=len(skills) if skills else 0,
        ) as span:
            logfire.info(
                "LLM Request",
                model=model,
                system_prompt=system,
                user_prompt=user,
                skills=skills,
            )

            api_params = {
                "model": model,
                "max_tokens": max_tokens,
                "system": system,
                "messages": [
                    {"role": "user", "content": user},
                ],
            }

            if skills:
                api_params["extra_body"] = {
                    "container": {"skills": skills}
                }
                api_params["extra_headers"] = {
                    "anthropic-beta": "skills-2025-10-02,code-execution-2025-08-25,files-api-2025-04-14"
                }
                api_params["tools"] = [
                    {
                        "type": "code_execution_20250825",
                        "name": "code_execution",
                    }
                ]

            message = await self.client.messages.create(**api_params)

            response_text = message.content[0].text

            logfire.info(
                "LLM Response",
                model=model,
                response=response_text,
                input_tokens=message.usage.input_tokens,
                output_tokens=message.usage.output_tokens,
                total_tokens=message.usage.input_tokens + message.usage.output_tokens,
            )

            span.set_attribute("input_tokens", message.usage.input_tokens)
            span.set_attribute("output_tokens", message.usage.output_tokens)
            span.set_attribute("response_length", len(response_text))

            log_entry = {
                "timestamp": timestamp,
                "model": model,
                "request": {
                    "system": system,
                    "user": user,
                },
                "response": {
                    "text": response_text,
                    "usage": {
                        "input_tokens": message.usage.input_tokens,
                        "output_tokens": message.usage.output_tokens,
                    }
                }
            }

            log_file = os.path.join(
                self.log_dir,
                f"llm_call_{timestamp.replace(':', '-')}.json"
            )
            with open(log_file, "w") as f:
                json.dump(log_entry, f, indent=2)

            return response_text

    async def verify_with_vision(
        self,
        system: str,
        user: str,
        image_base64: str,
        media_type: str = "image/png",
    ) -> str:
        """Verify output using vision capabilities.

        Always uses Sonnet for vision tasks (fast and vision-capable).

        Args:
            system: System prompt
            user: User message/question about the image
            image_base64: Base64-encoded image data
            media_type: Image MIME type (default: image/png)

        Returns:
            Verification response text
        """
        with logfire.span(
            "llm.verify_with_vision",
            model=settings.SONNET_MODEL,
            system_length=len(system),
            user_length=len(user),
        ) as span:
            message = await self.client.messages.create(
                model=settings.SONNET_MODEL,
                max_tokens=2048,
                system=system,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": media_type,
                                    "data": image_base64,
                                },
                            },
                            {"type": "text", "text": user},
                        ],
                    }
                ],
            )

            response_text = message.content[0].text

            span.set_attribute("input_tokens", message.usage.input_tokens)
            span.set_attribute("output_tokens", message.usage.output_tokens)

            logfire.info(
                "Vision Verification Response",
                model=settings.SONNET_MODEL,
                response=response_text,
                input_tokens=message.usage.input_tokens,
                output_tokens=message.usage.output_tokens,
            )

            return response_text

