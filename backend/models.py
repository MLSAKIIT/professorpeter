from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime

class VideoStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    GENERATING_SCRIPT = "generating_script"
    VALIDATING_SCRIPT = "validating_script"
    GENERATING_VOICE = "generating_voice"
    GENERATING_SUBTITLES = "generating_subtitles"
    COMPILING_VIDEO = "compiling_video"
    COMPLETED = "completed"
    FAILED = "failed"

class VideoRequest(BaseModel):
    prompt: str = Field(..., description="The prompt/topic for video generation", min_length=1, max_length=500)
    topic: Optional[str] = Field(None, description="Optional topic categorization")
    duration: Optional[int] = Field(None, description="Desired video duration in seconds", gt=0, le=120)
    template_id: Optional[int] = Field(1, description="Template ID to use for video generation", ge=1, le=10)
    key_points: Optional[List[str]] = Field(None, description="Key points to cover in the video")

class VideoResponse(BaseModel):
    video_id: str = Field(..., description="Unique identifier for the video")
    status: VideoStatus = Field(..., description="Current status of video generation")
    message: str = Field(..., description="Human readable status message")
    created_at: Optional[str] = Field(None, description="ISO timestamp when video generation started")
    estimated_completion: Optional[str] = Field(None, description="Estimated completion time")

class ScriptRequest(BaseModel):
    prompt: str = Field(..., description="The prompt/topic for script generation", min_length=1, max_length=500)
    topic: Optional[str] = Field(None, description="Optional topic categorization")
    style: Optional[str] = Field("educational", description="Script style (educational, comedy, motivational)")

class ScriptResponse(BaseModel):
    script: str = Field(..., description="Generated script text")
    video_id: str = Field(..., description="Unique identifier for this script")
    word_count: int = Field(..., description="Number of words in the script")
    estimated_duration: Optional[float] = Field(None, description="Estimated reading duration in seconds")
    style: Optional[str] = Field(None, description="Script style used")

class TTSRequest(BaseModel):
    script: str = Field(..., description="Script text to convert to speech", min_length=1)
    voice_model: str = Field("peter_griffin", description="Voice model to use")
    speed: Optional[float] = Field(1.0, description="Speech speed multiplier", gt=0.5, le=2.0)
    pitch: Optional[float] = Field(1.0, description="Pitch adjustment", gt=0.5, le=2.0)

class TTSResponse(BaseModel):
    audio_url: str = Field(..., description="URL to access the generated audio file")
    duration: float = Field(..., description="Duration of the audio in seconds")
    video_id: str = Field(..., description="Unique identifier for this audio")
    file_size: Optional[int] = Field(None, description="File size in bytes")

class SubtitleSegment(BaseModel):
    start: float = Field(..., description="Start time in seconds")
    end: float = Field(..., description="End time in seconds")
    text: str = Field(..., description="Subtitle text")

class SubtitleResponse(BaseModel):
    subtitles: List[SubtitleSegment] = Field(..., description="List of subtitle segments")
    video_id: str = Field(..., description="Unique identifier for this subtitle set")
    total_duration: Optional[float] = Field(None, description="Total duration covered by subtitles")
    language: Optional[str] = Field("en", description="Language code")

class StatusResponse(BaseModel):
    video_id: str = Field(..., description="Unique identifier for the video")
    status: VideoStatus = Field(..., description="Current status of video generation")
    progress: int = Field(..., description="Progress percentage (0-100)", ge=0, le=100)
    message: str = Field(..., description="Human readable status message")
    created_at: Optional[str] = Field(None, description="ISO timestamp when generation started")
    completed_at: Optional[str] = Field(None, description="ISO timestamp when generation completed")
    estimated_remaining: Optional[int] = Field(None, description="Estimated seconds remaining")
    current_step: Optional[str] = Field(None, description="Current processing step")

class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Human readable error message")
    video_id: Optional[str] = Field(None, description="Associated video ID if applicable")
    timestamp: Optional[str] = Field(None, description="ISO timestamp when error occurred")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")

class GeneratedVideo(BaseModel):
    """Model matching frontend expectations"""
    id: str = Field(..., description="Unique video identifier")
    script: str = Field(..., description="Generated script text")
    videoUrl: Optional[str] = Field(None, description="URL to the generated video file")
    shareUrl: str = Field(..., description="Shareable URL for the video")
    status: str = Field("completed", description="Video status")
    created_at: Optional[str] = Field(None, description="Creation timestamp")
    duration: Optional[float] = Field(None, description="Video duration in seconds")

class HealthResponse(BaseModel):
    status: str = Field(..., description="Service health status")
    service: str = Field(..., description="Service name")
    timestamp: str = Field(..., description="Current timestamp")
    version: str = Field(..., description="API version")
    dependencies: Dict[str, bool] = Field(..., description="Status of external dependencies")

class VideoListResponse(BaseModel):
    videos: List[GeneratedVideo] = Field(..., description="List of generated videos")
    total: int = Field(..., description="Total number of videos")
    page: Optional[int] = Field(None, description="Current page number")
    page_size: Optional[int] = Field(None, description="Number of items per page")
    message: Optional[str] = Field(None, description="Additional information")
