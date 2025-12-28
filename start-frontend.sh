#!/bin/bash
# Start Frontend Server
# This script starts the Next.js frontend server on port 3000

cd frontend
echo "🚀 Starting Frontend Server (Next.js) on http://localhost:3000"
echo "🔐 Make sure backend is running on http://localhost:8000"
echo ""
npm run dev
