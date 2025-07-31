#!/bin/bash

echo "🚀 Starting Jewelry 3D Platform..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed."
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "📝 Please edit .env file and add your OpenAI API key"
    else
        echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
        echo "📝 Please edit .env file and add your OpenAI API key"
    fi
fi

# Install frontend dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
fi

# Install backend dependencies if not already installed
if [ ! -d "backend/__pycache__" ]; then
    echo "📦 Installing backend dependencies..."
    cd backend
    pip install -r requirements.txt
    cd ..
fi

# Start backend server in background
echo "🔧 Starting backend server..."
cd backend
python main.py &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Start frontend server
echo "🎨 Starting frontend server..."
npm run dev

# Cleanup on exit
trap "echo '🛑 Shutting down...'; kill $BACKEND_PID 2>/dev/null; exit" INT TERM 