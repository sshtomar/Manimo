"""Modal deployment for Manimo API.

This deploys the FastAPI application to Modal, making it publicly accessible
for notebooks to use the skills-based code generation.
"""

import modal

# Build the container image with all API dependencies and copy source code
api_image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        # Core dependencies
        "fastapi>=0.110.0",
        "pydantic>=2.6.0",
        "pydantic-settings>=2.0.0",
        "uvicorn[standard]>=0.27.0",
        "python-multipart>=0.0.9",

        # Storage and cloud
        "boto3>=1.34.0",
        "httpx>=0.26.0",

        # AI/LLM
        "anthropic>=0.21.0",
        "openai>=1.12.0",

        # Utilities
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0.0",
    )
    # Copy source code into the image at build time
    .add_local_dir("src", "/app/src")
    .add_local_file("skills_config.py", "/app/skills_config.py")
)

app = modal.App("manimo-api")

# Secrets required for the API
secrets = [
    modal.Secret.from_name("r2-credentials"),
    modal.Secret.from_name("anthropic-api-key"),
]

@app.function(
    image=api_image,
    secrets=secrets,
    scaledown_window=300,
    cpu=2.0,
    memory=2048,
    max_containers=100,
)
@modal.asgi_app()
def manimo_api():
    """Deploy the Manimo API as a Modal ASGI app."""
    import os
    import sys

    sys.path.insert(0, "/app/src")
    sys.path.insert(0, "/app")

    os.environ["ALLOWED_ORIGINS"] = "*"
    os.environ["USE_LOCAL_STORAGE"] = "false"

    if not os.environ.get("DEFAULT_MODEL"):
        os.environ["DEFAULT_MODEL"] = "claude-haiku-4-5-20251001"

    from manimo_api.main import app

    return app


@app.function()
def get_api_url():
    """Get the deployed API URL."""
    return "https://your-workspace--manimo-api-manimo-api.modal.run"


if __name__ == "__main__":
    import modal.runner
    with modal.runner.deploy_app(app):
        url = get_api_url.remote()
        print(f"\n✅ Manimo API deployed at: {url}")
        print(f"📊 API Documentation: {url}/docs")
        print(f"\nTo use with notebooks, set this environment variable in Modal:")
        print(f"MANIMO_API_URL={url}/api")

