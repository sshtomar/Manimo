# E2B Integration Guide

Complete guide for the E2B sandbox infrastructure that powers Inquiro's isolated notebook environments.

## Overview

E2B provides isolated sandbox environments for running Marimo notebooks. Each notebook launch creates a dedicated container with:
- Pre-installed data science packages
- R2 storage sync for persistence
- Marimo server with AI integration
- Virtual environment for runtime package installation

### Performance

| Metric | Time |
|--------|------|
| Sandbox creation | ~2.8s |
| R2 download | ~4.7s |
| **Total launch** | **~9.5s** |

## Prerequisites

### 1. E2B Account & API Key

1. Sign up at [e2b.dev](https://e2b.dev)
2. Get API key from [Dashboard > Keys](https://e2b.dev/dashboard?tab=keys)
3. Export the key:
   ```bash
   export E2B_API_KEY=e2b_xxx
   ```

### 2. R2 Storage Credentials

Cloudflare R2 stores notebooks and data files:

```bash
export R2_ENDPOINT=https://xxx.r2.cloudflarestorage.com
export R2_ACCESS_KEY_ID=xxx
export R2_SECRET_ACCESS_KEY=xxx
```

### 3. Python Environment

```bash
cd e2b
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Inquiro Frontend                        │
└─────────────────────────┬───────────────────────────────────┘
                          │ POST /launch
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    E2B FastAPI Server                        │
│                   (e2b/src/inquiro_e2b/server.py)           │
└─────────────────────────┬───────────────────────────────────┘
                          │ Sandbox.create()
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                     E2B Sandbox                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Template: inquiro-notebook                            │ │
│  │  - marimo, pandas, numpy, statsmodels pre-installed    │ │
│  │  - Venv at /home/user/.venv                           │ │
│  │  - Workspace at /home/user/workspace                   │ │
│  └────────────────────────────────────────────────────────┘ │
│                          │                                   │
│  ┌───────────────────────┼────────────────────────────────┐ │
│  │                       ▼                                │ │
│  │  1. Download notebook from R2                          │ │
│  │  2. Configure Marimo AI (Inquiro API)                  │ │
│  │  3. Start auto-sync to R2 (every 5s)                   │ │
│  │  4. Launch Marimo server on port 8080                  │ │
│  └────────────────────────────────────────────────────────┘ │
│                          │                                   │
│                          ▼                                   │
│              https://8080-{sandbox_id}.e2b.app              │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    Cloudflare R2                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  {user_id}/{notebook_id}/                              │ │
│  │  ├── notebook.py          # Marimo source              │ │
│  │  ├── data/                # Uploaded datasets          │ │
│  │  │   ├── survey.csv                                    │ │
│  │  │   └── results.xlsx                                  │ │
│  │  └── chat_history.json    # AI conversation            │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## API Reference

### Launch Notebook Sandbox

```bash
POST /launch
Content-Type: application/json

{
  "notebook_key": "user123/analysis-abc/notebook.py",
  "r2_bucket": "ai-notebooks-dev",
  "timeout_minutes": 30
}
```

**Response:**
```json
{
  "marimo_url": "https://8080-abc123xyz.e2b.app",
  "notebook_key": "user123/analysis-abc/notebook.py",
  "sandbox_id": "abc123xyz",
  "status": "launching",
  "auto_sync": true,
  "sync_interval": 5,
  "syncs_data_files": true
}
```

### Create New Notebook

```bash
POST /notebook
Content-Type: application/json

{
  "notebook_id": "my-analysis",
  "user_id": "user123",
  "title": "Regression Analysis",
  "r2_bucket": "ai-notebooks-dev"
}
```

**Response:**
```json
{
  "notebook_id": "my-analysis",
  "notebook_key": "user123/my-analysis/notebook.py",
  "status": "created",
  "title": "Regression Analysis"
}
```

### Health Check

```bash
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "inquiro-e2b",
  "e2b_configured": true
}
```

## Running the Server

### Development

```bash
cd e2b
source .venv/bin/activate
uvicorn inquiro_e2b.server:app --reload --port 8000
```

### Production

```bash
uvicorn inquiro_e2b.server:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY e2b/ .
RUN pip install -e .
CMD ["uvicorn", "inquiro_e2b.server:app", "--host", "0.0.0.0", "--port", "8000"]
```

## E2B Template Management

### Current Template

- **Alias**: `inquiro-notebook`
- **Template ID**: `2r0ttyrrcln7v7udxtl7`

### Pre-installed Packages

| Package | Purpose |
|---------|---------|
| marimo | Notebook runtime |
| boto3 | R2/S3 storage access |
| pandas | Data manipulation |
| numpy | Numerical computing |
| matplotlib | Plotting |
| statsmodels | Statistical models |
| scikit-learn | Machine learning |
| scipy | Scientific computing |
| seaborn | Statistical visualization |
| plotly | Interactive plots |
| openpyxl | Excel read/write |
| xlrd | Legacy Excel support |
| pyarrow | Parquet files |
| openai | AI API client |

### Rebuilding the Template

If you need to add packages or modify the template:

```bash
cd e2b/template

# Edit e2b.Dockerfile to add packages
vim e2b.Dockerfile

# Build new template
E2B_API_KEY=e2b_xxx python build_template.py
```

The build script outputs:
```
Building E2B template: inquiro-notebook
==================================================
... build logs ...
==================================================
Template built successfully!
Template ID: abc123xyz
Alias: inquiro-notebook

Use in code:
  sandbox = Sandbox.create("inquiro-notebook")
```

### Template Dockerfile

```dockerfile
FROM e2bdev/code-interpreter:latest

# Install uv for fast package management
RUN pip install --no-cache-dir uv

# Create workspace directory structure
RUN mkdir -p /home/user/workspace/data /home/user/workspace/images

# Create venv and install packages
RUN uv venv /home/user/.venv && \
    VIRTUAL_ENV=/home/user/.venv uv pip install \
    marimo boto3 pandas numpy matplotlib statsmodels scikit-learn \
    scipy seaborn plotly openpyxl xlrd pyarrow openai

# Set permissions
RUN chmod -R 777 /home/user/workspace

WORKDIR /home/user/workspace

# Configure venv in PATH
ENV PATH="/home/user/.venv/bin:$PATH"
ENV VIRTUAL_ENV="/home/user/.venv"
```

## Sandbox Internals

### Directory Structure

```
/home/user/
├── .venv/                    # Python virtual environment
│   └── bin/
│       ├── python
│       ├── pip
│       └── marimo
├── .config/
│   └── marimo/
│       └── marimo.toml       # AI configuration
└── workspace/                # Working directory
    ├── notebook.py           # Current notebook
    ├── data/                 # Data files
    └── images/               # Generated plots
```

### Marimo AI Configuration

The sandbox automatically configures Marimo to use Inquiro's API:

```toml
[ai]
mode = "ask"

[ai.models]
chat_model = "inquiro/statistical-v1"
edit_model = "inquiro/statistical-v1"
autocomplete_model = "inquiro/statistical-v1"

[ai.open_ai_compatible]
api_key = "inquiro-key"
base_url = "https://autodidact24--inquiro-api-inquiro-api.modal.run/api/v1"

[completion]
copilot = "custom"

[package_management]
manager = "uv"
```

### Auto-Sync Behavior

The sync process runs every 5 seconds and uploads:

| File Type | Synced | Destination |
|-----------|--------|-------------|
| `notebook.py` | Yes | `{notebook_key}` |
| `.csv`, `.xlsx`, `.json`, `.parquet` | Yes | `{base_path}/data/{filename}` |
| `chat_history.json` | Yes | `{base_path}/data/chat_history.json` |
| Hidden files (`.*`) | No | - |
| Temp files (`_*`) | No | - |

## Testing

### Run Test Script

```bash
cd e2b
source .venv/bin/activate

# Set environment variables
export E2B_API_KEY=e2b_xxx
export R2_ENDPOINT=https://xxx.r2.cloudflarestorage.com
export R2_ACCESS_KEY_ID=xxx
export R2_SECRET_ACCESS_KEY=xxx

# Run test
python test_launch.py
```

Expected output:
```
E2B Notebook Launcher Test
========================================

1. Creating notebook: test-abc123
   Created: {'notebook_id': 'test-abc123', ...}

2. Spawning sandbox for: test-user/test-abc123/notebook.py
[T+0.0s] Creating E2B sandbox...
[T+2.8s] Sandbox created in 2.8s: xyz789
[T+9.5s] Marimo starting, returning URL
TIMING: Sandbox=2.8s, Download=4.7s, Total=9.5s

   Result:
   - Sandbox ID: xyz789
   - Marimo URL: https://8080-xyz789.e2b.app
   - Status: launching

========================================
Test completed!

Open Marimo at: https://8080-xyz789.e2b.app
```

### Verify Marimo is Running

```bash
# Wait 5 seconds for Marimo to start
sleep 5

# Check HTTP status
curl -s -o /dev/null -w "%{http_code}" https://8080-xyz789.e2b.app
# Should return: 200
```

## Migration from Modal

### Key Differences

| Feature | Modal | E2B |
|---------|-------|-----|
| Sandbox creation | `modal.Sandbox.create()` | `Sandbox.create()` |
| Port exposure | `sandbox.tunnels()[port].url` | `sandbox.get_host(port)` |
| File operations | `sandbox.exec()` | `sandbox.files.write()` |
| Background processes | `sandbox.exec(..., background=True)` | `sandbox.commands.run(..., background=True)` |
| Startup time | ~7-10s | ~3s |
| Package install | Runtime (slow) | Pre-built template (instant) |

### Code Changes

**Modal (before):**
```python
import modal

sandbox = modal.Sandbox.create(
    "sleep", "infinity",
    encrypted_ports=[8080],
    timeout=30 * 60,
    image=notebook_image,
)
tunnel = sandbox.tunnels()[8080]
marimo_url = tunnel.url
```

**E2B (after):**
```python
from e2b_code_interpreter import Sandbox

sandbox = Sandbox.create(
    template="inquiro-notebook",
    timeout=30 * 60,
    envs={"R2_ENDPOINT": "...", ...},
)
marimo_host = sandbox.get_host(8080)
marimo_url = f"https://{marimo_host}"
```

## Troubleshooting

### Sandbox Not Found

```
Error: Sandbox Not Found - The sandbox xyz wasn't found.
```

**Cause**: Sandbox timed out or was terminated.
**Solution**: Launch a new sandbox. Default timeout is 30 minutes.

### Port Not Open

```
Error: Closed Port - No service running on port 8080.
```

**Cause**: Marimo hasn't started yet or crashed.
**Solution**:
1. Wait 5-10 seconds for Marimo to start
2. Check sandbox logs for errors
3. Verify template has marimo installed

### R2 Download Failed

```
Error: Download error: NoSuchKey
```

**Cause**: Notebook doesn't exist in R2.
**Solution**: Create the notebook first with `POST /notebook`.

### Template Not Found

```
Error: Template 'inquiro-notebook' not found
```

**Cause**: Template not built or wrong E2B account.
**Solution**:
1. Verify E2B_API_KEY is correct
2. Rebuild template: `python template/build_template.py`

## Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `E2B_API_KEY` | Yes | E2B API key from dashboard |
| `R2_ENDPOINT` | Yes | Cloudflare R2 endpoint URL |
| `R2_ACCESS_KEY_ID` | Yes | R2 access key |
| `R2_SECRET_ACCESS_KEY` | Yes | R2 secret key |

## Resources

- [E2B Documentation](https://e2b.dev/docs)
- [E2B Python SDK](https://pypi.org/project/e2b-code-interpreter/)
- [E2B GitHub](https://github.com/e2b-dev/E2B)
- [Marimo Documentation](https://docs.marimo.io/)
