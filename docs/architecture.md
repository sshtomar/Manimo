# Manimo Architecture

This document provides a detailed overview of Manimo's architecture and design decisions.

## System Components

### Frontend (Next.js)

**Location**: `frontend/`

The Next.js application provides the user interface for creating and editing Manim animation notebooks.

**Key Features**:
- Notebook launcher UI
- Video player for rendered animations
- Rendering controls and status
- Dashboard for managing animations

**Technology Stack**:
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- Video.js for video playback
- pnpm

### API Orchestrator (FastAPI)

**Location**: `api/`

The FastAPI backend coordinates the skills-based agent system and manages interactions with storage and execution services.

**Key Responsibilities**:
- Run skills-based agent (skill selection → code generation)
- Manage LLM provider calls
- Handle R2 storage operations
- Trigger Modal execution jobs for video rendering

**Endpoints**:
- `POST /api/ask_ai` - Generate animation code with skills
- `GET/PUT /api/notebook/{id}` - Notebook CRUD
- `POST /api/render` - Trigger video rendering
- `GET /api/notebook/{id}/videos` - List rendered videos

### Modal Execution

**Location**: `modal/`

Modal provides isolated sandboxes for notebook execution and video rendering.

**Execution Flow**:
1. Download notebook from R2
2. Launch Marimo server for editing
3. Render Manim scenes to video
4. Upload videos back to R2

**Features**:
- Ephemeral containers (no state persistence)
- GPU support for video rendering
- Pre-built images with Manim and dependencies
- Structured logging

### Storage (Cloudflare R2)

**Purpose**: Persistent storage for notebooks, rendered videos, and assets

**Layout**:
```
{user_id}/{notebook_id}/
  notebook.py              # Current version
  versions/                # Historical versions
  videos/                  # Rendered videos (.mp4)
  assets/                  # Images, SVGs, etc.
  logs/                    # Rendering logs
```

## Skills-Based System

### Agent Flow

```
User Prompt
    ↓
Pass 0: Parse notebook, build context
    ↓
Pass 1: Skill Selection (LLM call)
    ↓
Pass 2: Code Generation with Skills (LLM call)
    ↓
Return Manim code
```

### Skills

1. **core-animation-principles**: Timing, easing, scene composition
2. **manim-api-patterns**: Scene, Mobject, Animation classes
3. **mathematical-visualization**: Best practices for math animations
4. **video-rendering**: Optimization, quality settings, formats
5. **educational-animation**: Pedagogical design principles
6. **manimo-notebook**: Marimo-specific patterns for Manim

## Key Differences from Inquiro

1. **Output**: Videos instead of statistical plots
2. **Skills**: Animation principles instead of statistical methods
3. **Execution**: Video rendering instead of data analysis
4. **Storage**: Video files instead of CSV/plots
5. **Frontend**: Video player instead of plot viewer
6. **Agent focus**: Animation quality vs. statistical rigor

