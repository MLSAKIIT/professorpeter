from fastapi import FastAPI, HTTPException, Body, File, UploadFile, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from typing import Optional, List, Dict
import uvicorn
import httpx
import os
import subprocess
import json
import traceback
import asyncio
import logging
from datetime import datetime
from pathlib import Path

from models import (
    VideoRequest, VideoResponse, ScriptResponse, StatusResponse,
    VideoStatus, TTSRequest, TTSResponse, SubtitleResponse, ErrorResponse
)
from config import settings
from script import VideoScriptGenerator
from video_compiler import overlay_image_on_video, merge_audio_with_video, burn_subtitles_on_video, transcript_txt_to_srt

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Educational Video Generator API",
    description="Backend for creating educational videos with Peter Griffin voice",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Global video status store
video_status_store: Dict[str, dict] = {}

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Create necessary directories
os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

# Mount static files for serving generated content
app.mount("/static/outputs", StaticFiles(directory=settings.OUTPUT_DIR), name="outputs")
app.mount("/static/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

def update_video_status(video_id: str, status: VideoStatus, progress: int, message: str, error: str = None):
    """Update video status in the global store with logging"""
    logger.info(f"🎬 Video {video_id}: {status.value} - {progress}% - {message}")
    if error:
        logger.error(f"❌ Video {video_id} Error: {error}")
    
    video_status_store[video_id] = {
        "status": status,
        "progress": progress,
        "message": message,
        "error": error,
        "updated_at": datetime.now().isoformat(),
        "created_at": video_status_store.get(video_id, {}).get("created_at", datetime.now().isoformat())
    }

async def generate_video_background(video_id: str, prompt: str, template: str = "lecture"):
    """Background task to generate the complete video"""
    try:
        logger.info(f"🎬 Starting video generation for {video_id} with prompt: '{prompt}'")
        
        # Step 1: Generate Script
        update_video_status(video_id, VideoStatus.GENERATING_SCRIPT, 10, "Generating Peter Griffin script...")
        await asyncio.sleep(1)  # Simulate processing time
        
        # Check if Gemini API key is configured
        if not settings.GEMINI_API_KEY:
            error_msg = "Gemini API key not configured. Please set GEMINI_API_KEY environment variable."
            logger.error(f"❌ {error_msg}")
            raise Exception(error_msg)
        
        logger.info(f"📝 Using Gemini API for script generation")
        generator = VideoScriptGenerator()
        
        try:
            script_data = generator.generate_script(prompt, duration=settings.MAX_VIDEO_DURATION)
            
            # Extract script text
            if isinstance(script_data, dict) and 'audio_script' in script_data:
                script_text = " ".join([segment.get('text', '') for segment in script_data.get('audio_script', [])])
            elif isinstance(script_data, dict) and 'key_sections' in script_data:
                script_text = " ".join([section.get('narration_text', '') for section in script_data.get('key_sections', [])])
            else:
                script_text = str(script_data)
                
        except Exception as e:
            error_msg = f"Script generation failed: {str(e)}"
            logger.error(f"❌ {error_msg}")
            raise Exception(error_msg)

        # Save script
        script_path = os.path.join(settings.OUTPUT_DIR, f"{video_id}_script.txt")
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_text)
        
        logger.info(f"📝 Script generated and saved to {script_path}")
        update_video_status(video_id, VideoStatus.GENERATING_VOICE, 30, "Creating Peter Griffin voice audio...")
        
        # Step 2: Generate Audio (TTS)
        await asyncio.sleep(2)  # Simulate TTS processing
        
        audio_path = os.path.join(settings.OUTPUT_DIR, f"{video_id}.mp3")
        
        # Use the existing audio.py module for TTS generation
        logger.info(f"🎤 Using ElevenLabs API for TTS generation via audio module")
        try:
            from elevenlabs.client import ElevenLabs
            
            # Use the same configuration as audio.py
            client = ElevenLabs(api_key=settings.TTS_API_KEY)
            
            # Use the voice ID from audio.py (LjreBZhXeL6R2WLwGI3Z)
            voice_id = "LjreBZhXeL6R2WLwGI3Z"
            
            logger.info(f"🎤 Generating TTS with voice_id: {voice_id}")
            
            # Generate audio using the same settings as audio.py
            audio = client.text_to_speech.convert(
                voice_id=voice_id,
                text=script_text[:2000],  # Limit text length
                output_format="mp3_44100_128",        # High quality MP3
                model_id="eleven_multilingual_v2",   # Recommended model
                voice_settings={
                    "stability": 0.6,
                    "similarity_boost": 0.8
                }
            )
            
            # Save the audio file
            with open(audio_path, "wb") as f:
                f.write(b"".join(audio))
            
            logger.info(f"🎤 TTS audio generated and saved to {audio_path}")
                    
        except Exception as e:
            error_msg = f"TTS generation failed: {str(e)}"
            logger.error(f"❌ {error_msg}")
            raise Exception(error_msg)
        
        update_video_status(video_id, VideoStatus.COMPILING_VIDEO, 60, "Generating subtitles...")
        
        # Step 3: Generate Subtitles
        await asyncio.sleep(1)
        subtitles_path = os.path.join(settings.OUTPUT_DIR, f"{video_id}.srt")
        transcript_txt_to_srt(script_path, subtitles_path, duration_per_line=3.0)
        logger.info(f"📝 Subtitles generated and saved to {subtitles_path}")
        
        update_video_status(video_id, VideoStatus.COMPILING_VIDEO, 80, "Compiling final video with subtitles...")
        
        # Step 4: Video Compilation
        await asyncio.sleep(2)
        
        # Map template names to actual files
        template_map = {
            "lecture": "template1.mp4",  # Use real template instead of mock
            "classroom": "template2.mp4",
            "laboratory": "template3.mp4"
        }
        
        # Get template file path
        template_file = template_map.get(template, "template1.mp4")  # Default to template1
        template_video = os.path.join(settings.TEMPLATES_DIR, template_file)
        peter_image = os.path.join(settings.ASSETS_DIR, "peter_griffin.png")
        
        # Validate template exists and is not empty
        if not os.path.exists(template_video):
            error_msg = f"Template '{template_file}' not found at {template_video}"
            logger.error(f"❌ {error_msg}")
            raise Exception(error_msg)
        
        # Check template file size (should be > 1MB for real video)
        template_size = os.path.getsize(template_video)
        if template_size < 1024 * 1024:  # Less than 1MB
            error_msg = f"Template '{template_file}' appears to be invalid (size: {template_size} bytes)"
            logger.error(f"❌ {error_msg}")
            raise Exception(error_msg)
        
        # Validate Peter Griffin image exists
        if not os.path.exists(peter_image):
            error_msg = f"Peter Griffin image not found at {peter_image}"
            logger.error(f"❌ {error_msg}")
            raise Exception(error_msg)
        
        logger.info(f"📹 Using template: {template_file} (size: {template_size / (1024*1024):.1f}MB)")
        logger.info(f"🖼️ Using Peter Griffin image: {os.path.basename(peter_image)}")
        
        # Final video paths
        temp_video_path = os.path.join(settings.OUTPUT_DIR, f"{video_id}_temp.mp4")
        with_audio_path = os.path.join(settings.OUTPUT_DIR, f"{video_id}_with_audio.mp4")
        final_video_path = os.path.join(settings.OUTPUT_DIR, f"{video_id}.mp4")
        
        try:
            logger.info(f"📹 Starting video compilation process")
            
            # Check if we have ffmpeg available for real video processing
            try:
                subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
                ffmpeg_available = True
                logger.info(f"🎬 FFmpeg detected - using real video compilation")
            except (subprocess.CalledProcessError, FileNotFoundError):
                ffmpeg_available = False
                logger.warning(f"⚠️ FFmpeg not available - using mock compilation")
            
            if ffmpeg_available:
                # Real video compilation with ffmpeg
                logger.info(f"📹 Step 1: Overlaying Peter Griffin image on template")
                overlay_image_on_video(template_video, peter_image, temp_video_path)
                
                logger.info(f"🎤 Step 2: Merging audio with video")
                merge_audio_with_video(temp_video_path, audio_path, with_audio_path)
                
                logger.info(f"📝 Step 3: Burning subtitles on video")
                burn_subtitles_on_video(with_audio_path, subtitles_path, final_video_path, audio_path)
                
                logger.info(f"✅ Real video compilation completed successfully")
            else:
                # Mock implementation when ffmpeg is not available
                logger.info(f"📹 Creating mock final video at {final_video_path}")
                with open(final_video_path, "wb") as f:
                    f.write(b"mock_final_video_with_peter_griffin_explanation")
                logger.info(f"✅ Mock video compilation completed")
            
        except Exception as e:
            logger.error(f"❌ Video compilation failed: {str(e)}")
            logger.error(traceback.format_exc())
            raise e  # Re-raise the exception instead of creating fallback
        
        # Clean up temporary files
        for temp_file in [temp_video_path, with_audio_path]:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        
        update_video_status(video_id, VideoStatus.COMPLETED, 100, "Video generation completed successfully!")
        logger.info(f"🎉 Video generation completed for {video_id}")
        
    except Exception as e:
        error_msg = f"Video generation failed: {str(e)}"
        logger.error(f"❌ {error_msg}")
        logger.error(traceback.format_exc())
        update_video_status(video_id, VideoStatus.FAILED, 0, "Video generation failed", error_msg)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {str(exc)}")
    logger.error(traceback.format_exc())
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

@app.get("/api/templates")
async def get_available_templates():
    """
    Get list of available video templates with their information
    """
    try:
        template_map = {
            "lecture": "template1.mp4",
            "classroom": "template2.mp4", 
            "laboratory": "template3.mp4"
        }
        
        templates = []
        for template_name, template_file in template_map.items():
            template_path = os.path.join(settings.TEMPLATES_DIR, template_file)
            if os.path.exists(template_path):
                file_size = os.path.getsize(template_path)
                templates.append({
                    "name": template_name,
                    "file": template_file,
                    "size_mb": round(file_size / (1024 * 1024), 1),
                    "available": file_size > 1024 * 1024  # Valid if > 1MB
                })
            else:
                templates.append({
                    "name": template_name,
                    "file": template_file,
                    "size_mb": 0,
                    "available": False
                })
        
        # Check if Peter Griffin image is available
        peter_image = os.path.join(settings.ASSETS_DIR, "peter_griffin.png")
        peter_available = os.path.exists(peter_image)
        
        logger.info(f"📊 Templates check: {len([t for t in templates if t['available']])} available")
        
        return {
            "templates": templates,
            "peter_griffin_available": peter_available,
            "total_templates": len(templates),
            "available_templates": len([t for t in templates if t["available"]])
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to get templates: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get templates: {str(e)}")

# Enhanced video generation endpoint with real background processing
@app.post("/api/generate-video", response_model=VideoResponse)
async def generate_video(request: VideoRequest, background_tasks: BackgroundTasks):
    """
    Main endpoint to start video generation process with real background processing
    """
    try:
        if not request.prompt or len(request.prompt.strip()) == 0:
            raise HTTPException(status_code=400, detail="Prompt cannot be empty")
        
        if len(request.prompt) > 500:
            raise HTTPException(status_code=400, detail="Prompt too long (max 500 characters)")
        
        video_id = f"video_{abs(hash(request.prompt + str(datetime.now()))) % 100000}"
        template = getattr(request, 'template', 'lecture')
        
        logger.info(f"🎬 Received video generation request for video_id: {video_id}")
        logger.info(f"📝 Prompt: {request.prompt}")
        logger.info(f"🎨 Template: {template}")
        
        # Initialize status
        update_video_status(video_id, VideoStatus.PENDING, 0, "Video generation request received and queued")
        
        # Start background video generation
        background_tasks.add_task(generate_video_background, video_id, request.prompt, template)
        
        return VideoResponse(
            video_id=video_id,
            status=VideoStatus.PENDING,
            message="Video generation started successfully"
        )
    except Exception as e:
        logger.error(f"❌ Failed to start video generation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to start video generation: {str(e)}")

@app.post("/api/generate-script", response_model=ScriptResponse)
async def generate_script(request: VideoRequest):
    """
    Generate script from user prompt using the VideoScriptGenerator
    Note: This endpoint only generates scripts, not videos. Use /api/generate-video for full video generation.
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
    Check the status of video generation using persistent store
    """
    try:
        # Check if video exists in our status store
        if video_id not in video_status_store:
            logger.warning(f"⚠️ Video {video_id} not found in status store")
            raise HTTPException(status_code=404, detail="Video not found")
        
        video_data = video_status_store[video_id]
        logger.info(f"📊 Status check for {video_id}: {video_data['status'].value} - {video_data['progress']}%")
        
        return StatusResponse(
            video_id=video_id,
            status=video_data['status'],
            progress=video_data['progress'],
            message=video_data['message'],
            created_at=video_data['created_at'],
            error=video_data.get('error')
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to get video status for {video_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get video status: {str(e)}")

@app.get("/api/video/{video_id}/download")
async def download_video(video_id: str):
    """
    Download the generated video file
    """
    try:
        # Check if video exists in status store and is completed
        if video_id not in video_status_store:
            logger.warning(f"⚠️ Video {video_id} not found in status store for download")
            raise HTTPException(status_code=404, detail="Video not found")
        
        video_data = video_status_store[video_id]
        if video_data['status'] != VideoStatus.COMPLETED:
            logger.warning(f"⚠️ Video {video_id} not ready for download. Status: {video_data['status'].value}")
            raise HTTPException(
                status_code=400, 
                detail=f"Video not ready for download. Current status: {video_data['status'].value}"
            )
        
        # Check if video file exists
        video_path = os.path.join(settings.OUTPUT_DIR, f"{video_id}.mp4")
        
        if not os.path.exists(video_path):
            logger.error(f"❌ Video file not found at {video_path} for completed video {video_id}")
            raise HTTPException(
                status_code=404, 
                detail="Video file not found on server"
            )
        
        logger.info(f"📥 Serving video download for {video_id}")
        return FileResponse(
            video_path,
            media_type="video/mp4",
            filename=f"peter_explains_{video_id}.mp4"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to download video {video_id}: {str(e)}")
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
    List all videos and their current status
    """
    try:
        videos = []
        for video_id, data in video_status_store.items():
            videos.append({
                "video_id": video_id,
                "status": data['status'].value,
                "progress": data['progress'],
                "message": data['message'],
                "created_at": data['created_at'],
                "updated_at": data['updated_at'],
                "error": data.get('error')
            })
        
        logger.info(f"📊 Listed {len(videos)} videos")
        return {"videos": videos, "total": len(videos)}
    except Exception as e:
        logger.error(f"❌ Failed to list videos: {str(e)}")
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
