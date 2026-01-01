#!/bin/bash
# Setup script for Manimo

set -e

echo "Setting up Manimo..."

# Create virtual environments
echo "Creating virtual environments..."
cd api && python -m venv venv && cd ..
cd modal && python -m venv venv && cd ..
cd shared && python -m venv venv && cd ..

# Install dependencies
echo "Installing API dependencies..."
cd api && source venv/bin/activate && pip install -e . && cd ..

echo "Installing Modal dependencies..."
cd modal && source venv/bin/activate && pip install -e . && cd ..

echo "Installing shared dependencies..."
cd shared && source venv/bin/activate && pip install -e . && cd ..

# Frontend setup
echo "Installing frontend dependencies..."
cd frontend && pnpm install && cd ..

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Copy .env.example to .env and configure API keys"
echo "2. Run './scripts/dev.sh' to start development servers"

