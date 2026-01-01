# Manimo

**AI-Native Notebook Workspace for Mathematical Animations**

Manimo is a collaborative animation platform that combines Marimo's reactive Python notebooks with a skills-based AI system to help creators build high-quality mathematical animations using Manim.

## Features

- **Skills-Based AI System**: Single-agent architecture with Manim-focused skills for reliable animation code generation
- **Marimo Notebooks**: Python-first notebooks with reactive execution
- **Modal Execution**: Isolated sandboxes for video rendering
- **Animation Focus**: Built-in support for mathematical visualization, educational animations, and video rendering
- **R2 Storage**: Persistent notebooks, assets, and rendered videos with versioning

## Architecture

```
┌─────────────────┐
│  Next.js UI     │
│  (Frontend)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────┐
│  FastAPI        │◄────►│ LLM Provider │
│  Orchestrator   │      │ (Claude/GPT) │
│  (API)          │      └──────────────┘
└────────┬────────┘
         │
    ┌────┴────┬─────────────┐
    ▼         ▼             ▼
┌────────┐ ┌──────┐  ┌────────────┐
│   R2   │ │Modal │  │ Skills-Based│
│Storage │ │ Exec │  │    Agent    │
└────────┘ └──────┘  └────────────┘
```

### Skills-Based System

1. **Skill Selection**: Agent analyzes task and selects relevant Manim skills
2. **Code Generation**: Agent generates animation code following ALL skill requirements
3. **Video Rendering**: Modal sandboxes render videos and upload to R2

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20+
- API keys:
  - Anthropic (Claude) or OpenAI (GPT)
  - Cloudflare R2
  - Modal

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/manimo.git
   cd manimo
   ```

2. **Run setup script**
   ```bash
   ./scripts/setup.sh
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Start development servers**
   ```bash
   ./scripts/dev.sh
   ```

5. **Open your browser**
   - Frontend: http://localhost:3000
   - API docs: http://localhost:8000/docs

## Repository Structure

```
manimo/
├── frontend/          # Next.js application
├── api/              # FastAPI orchestrator
│   ├── src/manimo_api/
│   ├── prompts/      # Agent prompts
│   └── routes/       # API endpoints
├── modal/            # Modal execution sandboxes
├── shared/           # Shared utilities
├── skills/           # Manim-focused skills
├── examples/         # Example notebooks & animations
├── infra/            # Infrastructure as Code
│   ├── terraform/    # Terraform configs
│   └── docker/       # Docker configs
├── scripts/          # Development scripts
└── docs/             # Documentation
```

## Skills

Manimo includes skills for creating high-quality animations:

- **Core Animation Principles**: Timing, easing, scene composition
- **Manim API Patterns**: Scene, Mobject, Animation classes
- **Mathematical Visualization**: Best practices for math animations
- **Video Rendering**: Optimization, quality settings, formats
- **Educational Animation**: Pedagogical design principles
- **Manimo Notebook**: Marimo-specific patterns for Manim

## Documentation

- [System Overview](docs/overview.md)
- [Architecture](docs/architecture.md)
- [Local Development](docs/local-development.md)

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- [Manim](https://www.manim.community/) - Mathematical animation engine
- [Marimo](https://marimo.io) - Reactive Python notebooks
- [Modal](https://modal.com) - Serverless compute platform
- [Cloudflare R2](https://www.cloudflare.com/products/r2/) - Object storage
- [FastAPI](https://fastapi.tiangolo.com) - API framework
- [Next.js](https://nextjs.org) - React framework

