from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI(
    title="SceneShare API Gateway",
    description="MSA Gateway for SceneShare Services",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service URLs
SERVICES = {
    "auth": "http://localhost:8004",
    "square": "http://localhost:8001",
    "critics": "http://localhost:8002",
    "archive": "http://localhost:8003",
    "movies": "http://localhost:8000",
}

@app.get("/")
def root():
    return {
        "gateway": "SceneShare API Gateway",
        "services": list(SERVICES.keys()),
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """모든 서비스 헬스 체크"""
    status = {}
    async with httpx.AsyncClient() as client:
        for service, url in SERVICES.items():
            try:
                response = await client.get(f"{url}/health", timeout=2.0)
                status[service] = "healthy" if response.status_code == 200 else "unhealthy"
            except:
                status[service] = "down"
    return status

# Square Service Proxy
@app.api_route("/api/v1/square/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def square_proxy(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        url = f"{SERVICES['square']}/api/v1/square/{path}"
        
        if request.method == "GET":
            response = await client.get(url, params=request.query_params)
        elif request.method == "POST":
            body = await request.json()
            response = await client.post(url, json=body)
        elif request.method == "PUT":
            body = await request.json()
            response = await client.put(url, json=body)
        elif request.method == "DELETE":
            response = await client.delete(url)
        
        return response.json()

# Critics Service Proxy
@app.api_route("/api/v1/critics/{path:path}", methods=["GET", "POST"])
async def critics_proxy(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        url = f"{SERVICES['critics']}/api/v1/critics/{path}"
        
        if request.method == "GET":
            response = await client.get(url, params=request.query_params)
        else:
            body = await request.json()
            response = await client.post(url, json=body)
        
        return response.json()

# Archive Service Proxy
@app.api_route("/api/v1/archive/{path:path}", methods=["GET", "POST"])
async def archive_proxy(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        url = f"{SERVICES['archive']}/api/v1/archive/{path}"
        
        if request.method == "GET":
            response = await client.get(url, params=request.query_params)
        else:
            body = await request.json()
            response = await client.post(url, json=body)
        
        return response.json()

# Movies Service Proxy (TMDB)
@app.api_route("/api/v1/movies/{path:path}", methods=["GET"])
async def movies_proxy(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        url = f"{SERVICES['movies']}/api/v1/movies/{path}"
        response = await client.get(url, params=request.query_params)
        return response.json()

# Auth Service Proxy
@app.api_route("/api/v1/auth/{path:path}", methods=["GET", "POST"])
async def auth_proxy(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        url = f"{SERVICES['auth']}/api/v1/auth/{path}"
        
        if request.method == "GET":
            response = await client.get(url, params=request.query_params)
        else:
            body = await request.json()
            response = await client.post(url, json=body)
        
        return response.json()
