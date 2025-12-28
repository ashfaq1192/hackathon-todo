#!/bin/bash
# Start Backend Server
# This script starts the FastAPI backend server on port 8000

cd backend
echo "🚀 Starting Backend Server (FastAPI) on http://localhost:8000"
echo "📚 API Docs available at http://localhost:8000/docs"
echo ""
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
