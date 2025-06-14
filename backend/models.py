from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

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
    prompt: str
    topic: Optional[str] = None
    duration: Optional[int] = None  # in seconds

class VideoResponse(BaseModel):
    video_id: str
    status: VideoStatus
    message: str

class ScriptRequest(BaseModel):
    prompt: str
    topic: Optional[str] = None

class ScriptResponse(BaseModel):
    script: str
    video_id: str
    word_count: int

class TTSRequest(BaseModel):
    script: str
    voice_model: str = "peter_griffin"

class TTSResponse(BaseModel):
    audio_url: str
    duration: float
    video_id: str

class SubtitleResponse(BaseModel):
    subtitles: List[dict]
    video_id: str

class StatusResponse(BaseModel):
    video_id: str
    status: VideoStatus
    progress: int
    message: str
    created_at: Optional[str] = None
    completed_at: Optional[str] = None

class ErrorResponse(BaseModel):
    error: str
    message: str
    video_id: Optional[str] = None
