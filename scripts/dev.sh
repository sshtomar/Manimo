#!/bin/bash
# Development script for Manimo

set -e

echo "Starting Manimo development servers..."

# Start API server
echo "Starting API server..."
cd api && source venv/bin/activate && uvicorn manimo_api.main:app --reload --port 8000 &
API_PID=$!
cd ..

# Start frontend
echo "Starting frontend..."
if [ -d "frontend" ]; then
    cd frontend && pnpm dev &
    FRONTEND_PID=$!
    cd ..
else
    echo "⚠️  Frontend directory not found, skipping..."
    FRONTEND_PID=""
fi

echo "✅ Development servers started!"
echo "API: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for interrupt
if [ -n "$FRONTEND_PID" ]; then
    trap "kill $API_PID $FRONTEND_PID 2>/dev/null" EXIT
else
    trap "kill $API_PID 2>/dev/null" EXIT
fi
wait

