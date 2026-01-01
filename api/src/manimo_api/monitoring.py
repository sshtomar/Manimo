"""Monitoring and observability configuration using Pydantic Logfire."""

import os

import logfire
from .config import settings


def configure_logfire():
    """
    Configure Pydantic Logfire for monitoring LLM calls and agent interactions.
    """

    if settings.LOGFIRE_TOKEN:
        os.environ["LOGFIRE_TOKEN"] = settings.LOGFIRE_TOKEN

    logfire.configure(
        service_name="manimo-api",
        service_version="0.1.0",
        send_to_logfire=bool(settings.LOGFIRE_TOKEN),
        console=logfire.ConsoleOptions(verbose=True),
    )

    if settings.DEFAULT_LLM_PROVIDER == "anthropic":
        logfire.instrument_anthropic()
        logfire.info("Instrumented Anthropic client for monitoring")
    elif settings.DEFAULT_LLM_PROVIDER == "openai":
        logfire.instrument_openai()
        logfire.info("Instrumented OpenAI client for monitoring")

    logfire.info(
        "Logfire monitoring configured",
        provider=settings.DEFAULT_LLM_PROVIDER,
        model=settings.DEFAULT_MODEL,
    )

