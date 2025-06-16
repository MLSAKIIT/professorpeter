#!/bin/bash

# Professor Peter's Students - Development Startup Script
# This script starts both the backend and frontend in development mode

echo "🚀 Starting Professor Peter's Students Development Environment..."
echo ""

# Function to kill background processes on script exit
cleanup() {
    echo ""
    echo "🛑 Shutting down services..."
    kill $backend_pid 2>/dev/null
    kill $frontend_pid 2>/dev/null
    exit 0
}

# Set up cleanup trap
trap cleanup SIGINT SIGTERM

# Check if backend directory exists
if [ ! -d "backend" ]; then
    echo "❌ Backend directory not found!"
    echo "Please run this script from the project root directory."
    exit 1
fi

# Check if frontend directory exists
if [ ! -d "client" ]; then
    echo "❌ Frontend directory not found!"
    echo "Please run this script from the project root directory."
    exit 1
fi

# Start Backend
echo "🔧 Starting Backend (FastAPI)..."
cd backend

# Check if .env exists, if not copy from example
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "✅ Please edit backend/.env with your API keys (optional for demo mode)"
fi

# Check if uv is available
if command -v uv >/dev/null 2>&1; then
    echo "🐍 Using uv to start backend..."
    uv run start.py &
    backend_pid=$!
else
    echo "🐍 Using python to start backend..."
    python start.py &
    backend_pid=$!
fi

cd ..

# Wait a moment for backend to start
echo "⏳ Waiting for backend to initialize..."
sleep 3

# Start Frontend
echo "🎨 Starting Frontend (Next.js)..."
cd client

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
fi

echo "🚀 Starting Next.js development server..."
npm run dev &
frontend_pid=$!

cd ..

echo ""
echo "✅ Both services are starting!"
echo ""
echo "📍 Service URLs:"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "🔄 Backend Status: Check the frontend for connection indicator"
echo "📱 Demo Mode: Works without API keys"
echo "🔑 Production: Add API keys to backend/.env"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for background processes
wait 