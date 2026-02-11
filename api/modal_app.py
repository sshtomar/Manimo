"""Modal deployment for Manimo API.

Deploys the FastAPI application to Modal with E2B sandbox integration
for notebook execution and Manim rendering.

Deploy:
  modal deploy api/modal_app.py

Dev (hot-reload):
  modal serve api/modal_app.py
"""

import modal

api_image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        # Core API
        "fastapi>=0.110.0",
        "pydantic>=2.6.0",
        "pydantic-settings>=2.2.0",
        "uvicorn[standard]>=0.28.0",
        "python-multipart>=0.0.9",
        # Auth
        "python-jose[cryptography]>=3.3.0",
        "passlib[bcrypt]>=1.7.4",
        # Storage
        "boto3>=1.34.0",
        # AI/LLM
        "anthropic>=0.25.0",
        "openai>=1.14.0",
        # Sandbox
        "e2b-code-interpreter>=0.15.0",
        # Monitoring
        "logfire>=0.0.1",
        # Utilities
        "python-dotenv>=1.2.1",
        "httpx>=0.27.0",
    )
    .add_local_dir("src", "/app/src")
    .add_local_file("skills_config.py", "/app/skills_config.py")
)

app = modal.App("manimo-api")

secrets = [
    modal.Secret.from_name("r2-credentials"),
    modal.Secret.from_name("anthropic-api-key"),
    modal.Secret.from_name("e2b-api-key"),
]


@app.function(
    image=api_image,
    secrets=secrets,
    scaledown_window=300,
    cpu=2.0,
    memory=2048,
)
@modal.asgi_app()
def manimo_api():
    """Deploy the Manimo API as a Modal ASGI app."""
    import os
    import sys

    sys.path.insert(0, "/app/src")
    sys.path.insert(0, "/app")

    os.environ.setdefault("ALLOWED_ORIGINS", "*")
    os.environ.setdefault("USE_LOCAL_STORAGE", "false")
    os.environ.setdefault("DEFAULT_MODEL", "claude-haiku-4-5-20251001")

    from manimo_api.main import app

    return app
