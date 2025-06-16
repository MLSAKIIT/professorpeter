from fastapi import FastAPI, HTTPException, Body, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from typing import Optional, List
import uvicorn
import httpx
import os
import subprocess
import json
import traceback
from datetime import datetime

from models import (
    VideoRequest, VideoResponse, ScriptResponse, StatusResponse,
    VideoStatus, TTSRequest, TTSResponse, SubtitleResponse, ErrorResponse
)
from config import settings
from script import VideoScriptGenerator
from video_compiler import overlay_image_on_video, merge_audio_with_video, burn_subtitles_on_video, transcript_txt_to_srt

app = FastAPI(
    title="Educational Video Generator API",
    description="Backend for creating educational videos with Peter Griffin voice",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Mount static files for serving generated content
app.mount("/static/outputs", StaticFiles(directory=settings.OUTPUT_DIR), name="outputs")
app.mount("/static/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal Server Error",
            message=str(exc)
        ).dict()
    )

# Health check endpoints
@app.get("/")
async def root():
    return {
        "message": "Educational Video Generator API is running",
        "version": "0.1.0",
        "status": "healthy",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "video-generator",
        "timestamp": datetime.now().isoformat(),
        "dependencies": {
            "gemini_api": bool(settings.GEMINI_API_KEY),
            "tts_api": bool(settings.TTS_API_KEY)
        }
    }

# Enhanced video generation endpoint that matches frontend expectations
@app.post("/api/generate-video", response_model=VideoResponse)
async def generate_video(request: VideoRequest):
    """
    Main endpoint to start video generation process
    """
    try:
        if not request.prompt or len(request.prompt.strip()) == 0:
            raise HTTPException(status_code=400, detail="Prompt cannot be empty")
        
        if len(request.prompt) > 500:
            raise HTTPException(status_code=400, detail="Prompt too long (max 500 characters)")
        
        video_id = f"video_{abs(hash(request.prompt)) % 100000}"
        
        return VideoResponse(
            video_id=video_id,
            status=VideoStatus.PENDING,
            message="Video generation request received and queued"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start video generation: {str(e)}")

@app.post("/api/generate-script", response_model=ScriptResponse)
async def generate_script(request: VideoRequest):
    """
    Generate script from user prompt using the VideoScriptGenerator
    """
    try:
        if not request.prompt or len(request.prompt.strip()) == 0:
            raise HTTPException(status_code=400, detail="Prompt cannot be empty")
        
        # Check if API key is configured
        if not settings.GEMINI_API_KEY:
            # For demo purposes, return a mock script
            video_id = f"script_{abs(hash(request.prompt)) % 100000}"
            mock_script = f"""Hey there, folks! Peter Griffin here with another mind-blowing explanation about "{request.prompt}". 

Now, I know what you're thinking - "Peter, how do you know so much about this stuff?" Well, let me tell you, it's because I once saw a documentary about it while eating a sandwich. 

So basically, {request.prompt} is like when you're trying to explain something to Meg, but she just doesn't get it, you know? It's all about the science and stuff. 

The key thing to understand is that {request.prompt} works in a very specific way - kinda like how my brain works, but actually functional. Trust me on this one, I'm basically an expert now.

And that's pretty much everything you need to know about {request.prompt}. Remember, if Peter Griffin can understand it, so can you!"""
            
            return ScriptResponse(
                script=mock_script,
                video_id=video_id,
                word_count=len(mock_script.split())
            )
        
        # Use the actual VideoScriptGenerator
        generator = VideoScriptGenerator()
        script_data = generator.generate_script(request.prompt, duration=settings.MAX_VIDEO_DURATION)
        video_id = f"script_{abs(hash(request.prompt)) % 100000}"
        
        # Extract script text from the generated data
        if isinstance(script_data, dict) and 'audio_script' in script_data:
            # If it's the full segmented script, extract the text
            script_text = " ".join([segment.get('text', '') for segment in script_data.get('audio_script', [])])
        elif isinstance(script_data, dict) and 'key_sections' in script_data:
            # If it's the initial script format
            script_text = " ".join([section.get('narration_text', '') for section in script_data.get('key_sections', [])])
        else:
            script_text = str(script_data)
        
        return ScriptResponse(
            script=script_text,
            video_id=video_id,
            word_count=len(script_text.split())
        )
        
    except Exception as e:
        print(f"Script generation error: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to generate script: {str(e)}")

@app.get("/api/video/{video_id}/status", response_model=StatusResponse)
async def get_video_status(video_id: str):
    """
    Check the status of video generation
    """
    try:
        # For demo purposes, simulate different statuses
        import time
        
        # Simple simulation based on time
        creation_time = abs(hash(video_id)) % 100
        elapsed = int(time.time()) % 120  # 2 minute cycle
        
        if elapsed < 30:
            status = VideoStatus.GENERATING_SCRIPT
            progress = min(30, elapsed * 3)
            message = "Generating Peter Griffin script..."
        elif elapsed < 60:
            status = VideoStatus.GENERATING_VOICE
            progress = min(60, 30 + (elapsed - 30) * 2)
            message = "Creating Peter Griffin voice audio..."
        elif elapsed < 90:
            status = VideoStatus.COMPILING_VIDEO
            progress = min(90, 60 + (elapsed - 60))
            message = "Compiling final video with subtitles..."
        else:
            status = VideoStatus.COMPLETED
            progress = 100
            message = "Video generation completed successfully!"
        
        return StatusResponse(
            video_id=video_id,
            status=status,
            progress=progress,
            message=message,
            created_at=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get video status: {str(e)}")

@app.get("/api/video/{video_id}/download")
async def download_video(video_id: str):
    """
    Download the generated video file
    """
    try:
        # Check if video file exists
        video_path = os.path.join(settings.OUTPUT_DIR, f"{video_id}.mp4")
        
        if not os.path.exists(video_path):
            # For demo, return a placeholder response
            raise HTTPException(
                status_code=404, 
                detail="Video not found or still processing. Please check the status endpoint."
            )
        
        return FileResponse(
            video_path,
            media_type="video/mp4",
            filename=f"peter_explains_{video_id}.mp4"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download video: {str(e)}")

@app.post("/api/generate-tts", response_model=TTSResponse)
async def generate_tts(request: TTSRequest):
    """
    Generate Peter Griffin voice from script using ElevenLabs API
    """
    try:
        if not settings.TTS_API_KEY:
            raise HTTPException(
                status_code=503, 
                detail="TTS service not configured. Please set TTS_API_KEY environment variable."
            )

        voice_id = settings.DEFAULT_VOICE_ID
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "xi-api-key": settings.TTS_API_KEY,
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
        video_id = f"tts_{abs(hash(request.script)) % 100000}"
        audio_path = os.path.join(settings.OUTPUT_DIR, f"{video_id}.mp3")
        
        with open(audio_path, "wb") as f:
            f.write(audio_bytes)

        return TTSResponse(
            audio_url=f"/static/outputs/{video_id}.mp3",
            duration=len(request.script) * 0.1,  # Rough estimate
            video_id=video_id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate TTS: {str(e)}")

@app.post("/api/generate-subtitles", response_model=SubtitleResponse)
async def generate_subtitles(video_id: str = Body(..., embed=True)):
    """
    Generate subtitles from script
    """
    try:
        # For demo purposes, return sample subtitles
        sample_subtitles = [
            {"start": 0.0, "end": 3.5, "text": "Hey there, folks! Peter Griffin here!"},
            {"start": 3.5, "end": 7.0, "text": "Welcome to another educational video"},
            {"start": 7.0, "end": 10.5, "text": "where I explain stuff in my own special way!"},
            {"start": 10.5, "end": 14.0, "text": "Now, let me break this down for you..."}
        ]
        
        return SubtitleResponse(
            subtitles=sample_subtitles,
            video_id=video_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate subtitles: {str(e)}")

@app.get("/api/videos")
async def list_videos():
    """
    List all generated videos
    """
    try:
        # For demo purposes, return empty list
        return {"videos": [], "total": 0, "message": "Video history feature coming soon!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list videos: {str(e)}")

@app.post("/api/generate-all")
async def generate_all(request: VideoRequest):
    """
    Generate script, audio, and subtitles for a given topic in one call.
    """
    try:
        if not request.prompt or len(request.prompt.strip()) == 0:
            raise HTTPException(status_code=400, detail="Prompt cannot be empty")
        
        video_id = f"full_{abs(hash(request.prompt)) % 100000}"
        
        # 1. Generate script
        generator = VideoScriptGenerator()
        script_data = generator.generate_script(request.prompt)
        
        # Save script to file
        script_file = os.path.join(settings.OUTPUT_DIR, f"{video_id}_script.json")
        with open(script_file, 'w', encoding='utf-8') as f:
            json.dump(script_data, f, indent=2, ensure_ascii=False)
        
        # For demo, we'll skip the actual audio and subtitle generation
        # as it requires external APIs and processing
        
        return {
            "message": "Full video generation started",
            "video_id": video_id,
            "script_file": f"static/outputs/{video_id}_script.json",
            "status": "processing"
        }
        
    except Exception as e:
        print(f"Generate all error: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to generate full video: {str(e)}")

# Development endpoint to test script generation
@app.get("/api/test-script/{prompt}")
async def test_script_generation(prompt: str):
    """
    Test endpoint for script generation
    """
    try:
        request = VideoRequest(prompt=prompt)
        result = await generate_script(request)
        return result
    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}

if __name__ == "__main__":
    print(f"Starting server on {settings.HOST}:{settings.PORT}")
    print(f"Debug mode: {settings.DEBUG}")
    print(f"Frontend URL: {settings.FRONTEND_URL}")
    print(f"Docs available at: http://{settings.HOST}:{settings.PORT}/docs")
    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
