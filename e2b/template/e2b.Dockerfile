# E2B Template for Manimo Notebooks
# Based on e2b code interpreter base image with full data science stack

FROM e2bdev/code-interpreter:latest

# Install system dependencies for Manim and LaTeX
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    texlive \
    texlive-latex-extra \
    texlive-fonts-extra \
    texlive-latex-recommended \
    libcairo2-dev \
    libpango1.0-dev \
    pkg-config \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast package management
RUN pip install --no-cache-dir uv

# Create workspace directory structure
RUN mkdir -p /home/user/workspace/data /home/user/workspace/images

# Create virtual environment and install packages
RUN uv venv /home/user/.venv && \
    VIRTUAL_ENV=/home/user/.venv uv pip install \
    # Core
    marimo>=0.17.8 \
    boto3>=1.34.0 \
    manim>=0.18.0 \
    # AI/LLM
    anthropic>=0.25.0 \
    openai>=1.12.0 \
    # Web server for AI integration
    fastapi>=0.109.0 \
    uvicorn>=0.27.0 \
    httpx>=0.26.0 \
    pydantic>=2.5.0 \
    # Data science
    pandas>=2.1.0 \
    numpy>=1.26.0 \
    polars>=0.20.0 \
    scipy>=1.12.0 \
    statsmodels>=0.14.0 \
    scikit-learn>=1.4.0 \
    # Visualization
    matplotlib>=3.8.0 \
    seaborn>=0.13.0 \
    plotly>=5.18.0 \
    altair>=5.2.0 \
    # Excel support
    openpyxl>=3.1.0 \
    xlsxwriter>=3.1.0 \
    # Utilities
    requests>=2.31.0

# Set permissions
RUN chmod -R 777 /home/user/workspace

# Create Marimo config directory
RUN mkdir -p /home/user/.config/marimo

WORKDIR /home/user/workspace

# Configure venv in PATH
ENV PATH="/home/user/.venv/bin:$PATH"
ENV VIRTUAL_ENV="/home/user/.venv"
