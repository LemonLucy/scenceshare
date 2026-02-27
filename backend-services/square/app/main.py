from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.api.routes import router

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Square Service",
    description="Community Discussion & Posts Service",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1/square", tags=["Square"])

@app.get("/")
def root():
    return {"service": "Square", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}
