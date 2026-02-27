#!/bin/bash

# MSA 서비스 실행 스크립트

echo "🚀 Starting SceneShare MSA Services..."

# Movies Service (Port 8000)
cd /home/lucy/Q/movie/backend-services/movies
python3 -m venv venv 2>/dev/null
source venv/bin/activate
pip install -q -r requirements.txt
export TMDB_API_KEY=7394c0d4d8e4eb4b65728ea9d83ff3d8
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > /tmp/movies.log 2>&1 &
echo "✅ Movies Service started on port 8000"

# Square Service (Port 8001)
cd /home/lucy/Q/movie/backend-services/square
python3 -m venv venv 2>/dev/null
source venv/bin/activate
pip install -q -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload > /tmp/square.log 2>&1 &
echo "✅ Square Service started on port 8001"

# Critics Service (Port 8002)
cd /home/lucy/Q/movie/backend-services/critics
python3 -m venv venv 2>/dev/null
source venv/bin/activate
pip install -q -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload > /tmp/critics.log 2>&1 &
echo "✅ Critics Service started on port 8002"

# Archive Service (Port 8003)
cd /home/lucy/Q/movie/backend-services/archive
python3 -m venv venv 2>/dev/null
source venv/bin/activate
pip install -q -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload > /tmp/archive.log 2>&1 &
echo "✅ Archive Service started on port 8003"

# API Gateway (Port 9000)
cd /home/lucy/Q/movie/backend-services/gateway
python3 -m venv venv 2>/dev/null
source venv/bin/activate
pip install -q -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 9000 --reload > /tmp/gateway.log 2>&1 &
echo "✅ API Gateway started on port 9000"

echo ""
echo "🎉 All services started!"
echo ""
echo "📍 Service URLs:"
echo "   - Gateway:  http://localhost:9000"
echo "   - Movies:   http://localhost:8000"
echo "   - Square:   http://localhost:8001"
echo "   - Critics:  http://localhost:8002"
echo "   - Archive:  http://localhost:8003"
echo ""
echo "📚 API Docs:"
echo "   - Gateway:  http://localhost:9000/docs"
echo ""
echo "📊 Health Check:"
echo "   curl http://localhost:9000/health"
