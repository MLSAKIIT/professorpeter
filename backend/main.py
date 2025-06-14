from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import uvicorn

from models import (
    VideoRequest, VideoResponse, ScriptResponse, StatusResponse,
    VideoStatus, TTSRequest, TTSResponse, SubtitleResponse
)
from config import settings

app = FastAPI(
    title="Educational Video Generator API",
    description="Backend for creating educational videos with Peter Griffin voice",
    version="0.1.0"
)

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "Educational Video Generator API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "video-generator"}

# Video generation endpoints
@app.post("/api/generate-video", response_model=VideoResponse)
async def generate_video(request: VideoRequest):
    """
    Main endpoint to start video generation process
    """
    # Placeholder for video generation logic
    video_id = f"video_{hash(request.prompt) % 10000}"
    
    return VideoResponse(
        video_id=video_id,
        status=VideoStatus.PROCESSING,
        message="Video generation started"
    )

@app.post("/api/generate-script", response_model=ScriptResponse)
async def generate_script(request: VideoRequest):
    """
    Generate script from user prompt using Gemini API
    """
    # Placeholder for Gemini API integration
    video_id = f"script_{hash(request.prompt) % 10000}"
    
    return ScriptResponse(
        script="This is a placeholder script for: " + request.prompt,
        video_id=video_id,
        word_count=len(request.prompt.split())
    )

@app.get("/api/video/{video_id}/status", response_model=StatusResponse)
async def get_video_status(video_id: str):
    """
    Check the status of video generation
    """
    # Placeholder for status checking logic
    return StatusResponse(
        video_id=video_id,
        status=VideoStatus.PROCESSING,
        progress=50,
        message="Generating voice with Peter Griffin TTS"
    )

@app.get("/api/video/{video_id}/download")
async def download_video(video_id: str):
    """
    Download the generated video file
    """
    # Placeholder for file serving logic
    raise HTTPException(status_code=404, detail="Video not found or not ready")

@app.post("/api/generate-tts", response_model=TTSResponse)
async def generate_tts(request: TTSRequest):
    """
    Generate Peter Griffin voice from script
    """
    # Placeholder for TTS API integration
    video_id = f"tts_{hash(request.script) % 10000}"
    
    return TTSResponse(
        audio_url=f"/api/audio/{video_id}.mp3",
        duration=30.5,  # placeholder duration
        video_id=video_id
    )

@app.post("/api/generate-subtitles", response_model=SubtitleResponse)
async def generate_subtitles(video_id: str):
    """
    Generate subtitles from script
    """
    # Placeholder for subtitle generation logic
    sample_subtitles = [
        {"start": 0.0, "end": 2.5, "text": "Hey there, folks!"},
        {"start": 2.5, "end": 5.0, "text": "Welcome to another educational video"},
        {"start": 5.0, "end": 8.0, "text": "with your favorite Griffin!"}
    ]
    
    return SubtitleResponse(
        subtitles=sample_subtitles,
        video_id=video_id
    )

@app.get("/api/videos")
async def list_videos():
    """
    List all generated videos
    """
    # Placeholder for database query
    return {"videos": [], "total": 0}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
