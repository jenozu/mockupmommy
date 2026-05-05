from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from routes.upload import router as upload_router

# Load environment variables
load_dotenv()

app = FastAPI(title="Mockup Mommy API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local development
        "https://v0-modern-ui-mockup-design.vercel.app",  # Vercel frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to Mockup Mommy API"} 