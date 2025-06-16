from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import uvicorn
import httpx
import os
import subprocess

from models import (
    VideoRequest, VideoResponse, ScriptResponse, StatusResponse,
    VideoStatus, TTSRequest, TTSResponse, SubtitleResponse
)
from config import settings
from script import VideoScriptGenerator

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
    gemini_api_key = settings.GEMINI_API_KEY
    if not gemini_api_key:
        raise HTTPException(status_code=500, detail="Gemini API key not configured.")

    # Gemini API endpoint and headers
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {"Content-Type": "application/json"}
    params = {"key": gemini_api_key}
    prompt = f"Write a clear, engaging educational script for the following topic. The script should be about 1 minute long (120-150 words): {request.prompt}" 
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, params=params, json=data)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Gemini API error: {response.text}")
        result = response.json()
        script = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        if not script:
            raise HTTPException(status_code=500, detail="No script returned from Gemini API.")
    video_id = f"script_{hash(request.prompt) % 10000}"
    return ScriptResponse(
        script=script,
        video_id=video_id,
        word_count=len(script.split())
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
    Generate Peter Griffin voice from script using ElevenLabs API
    """
    eleven_api_key = settings.TTS_API_KEY
    if not eleven_api_key:
        raise HTTPException(status_code=500, detail="ElevenLabs API key not configured.")

    voice_id = "EXAVITQu4vr4xnSDxMaL"  # Example: Peter Griffin voice ID (replace with your custom voice if needed)
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": eleven_api_key,
        "Content-Type": "application/json"
    }
    data = {
        "text": request.script,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.8}
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"ElevenLabs API error: {response.text}")
        audio_bytes = response.content

    # Save audio file
    audio_dir = settings.OUTPUT_DIR
    os.makedirs(audio_dir, exist_ok=True)
    video_id = f"tts_{hash(request.script) % 10000}"
    audio_path = os.path.join(audio_dir, f"{video_id}.mp3")
    with open(audio_path, "wb") as f:
        f.write(audio_bytes)

    # Optionally, calculate duration (requires extra libs, placeholder for now)
    duration = 0.0

    return TTSResponse(
        audio_url=f"/api/audio/{video_id}.mp3",
        duration=duration,
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

@app.post("/api/generate-all")
async def generate_all(request: VideoRequest):
    """
    Generate script, audio, and subtitles for a given topic in one call.
    """
    # 1. Generate script and save to outputs/topic.json
    generator = VideoScriptGenerator()
    script = generator.generate_script(request.prompt)
    generator.save_script(script)

    # 2. Generate audio (outputs/output.mp3)
    subprocess.run(["python", "audio.py"], check=True)

    # 3. Generate subtitles (outputs/subtitles.txt)
    subprocess.run(["python", "subtitles.py"], check=True)

    return {"message": "Script, audio, and subtitles generated.", "script_file": "outputs/topic.json", "audio_file": "outputs/output.mp3", "subtitles_file": "outputs/subtitles.txt"}

@app.post("/api/generate-video-full")
async def generate_video_full(request: VideoRequest, template_id: int = Body(..., embed=True)):
    """
    Generate script, audio, subtitles, and merge with selected video template.
    """
    # 1. Generate script and save to outputs/topic.json
    generator = VideoScriptGenerator()
    script = generator.generate_script(request.prompt)
    generator.save_script(script)

    # 2. Generate audio (outputs/output.mp3)
    import subprocess
    subprocess.run(["python", "audio.py"], check=True)

    # 3. Generate subtitles (outputs/subtitles.txt)
    subprocess.run(["python", "subtitles.py"], check=True)

    # 4. Select template
    template_path = f"templates/template{template_id}.mp4"
    if not os.path.exists(template_path):
        raise HTTPException(status_code=404, detail=f"Template {template_id} not found.")

    # 5. Merge audio with template using ffmpeg
    output_video = "outputs/final_video.mp4"
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-i", template_path,
        "-i", "outputs/output.mp3",
        "-c:v", "copy", "-c:a", "aac", "-shortest", output_video
    ]
    subprocess.run(ffmpeg_cmd, check=True)

    return {"message": "Video generated with template.", "video_file": output_video}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
