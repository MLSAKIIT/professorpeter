# Educational Video Generator Backend

A FastAPI backend for generating educational videos with Peter Griffin voice.

## Features

- **Script Generation**: Convert user prompts to educational scripts using Gemini API
- **Voice Generation**: Text-to-speech with Peter Griffin voice
- **Subtitle Generation**: Automatic subtitle creation from scripts
- **Video Compilation**: Combine voice, subtitles, and video content
- **Status Tracking**: Real-time progress monitoring

## Setup

### Prerequisites

- Python 3.12+
- uv package manager

### Installation

1. Install dependencies:
```bash
uv sync
```

2. Copy environment variables:
```bash
cp .env.example .env
```

3. Update `.env` with your API keys:
   - `GEMINI_API_KEY`: Your Google Gemini API key
   - `TTS_API_KEY`: Your TTS service API key

### Running the Server

Development mode:
```bash
uv run python main.py
```

Or using uvicorn directly:
```bash
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### API Documentation

Once running, visit:
- API Docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Core Endpoints

- `POST /api/generate-video` - Start video generation process
- `POST /api/generate-script` - Generate script from prompt
- `POST /api/generate-tts` - Convert script to Peter Griffin voice
- `POST /api/generate-subtitles` - Generate subtitles from script
- `GET /api/video/{video_id}/status` - Check generation status
- `GET /api/video/{video_id}/download` - Download completed video
- `GET /api/videos` - List all videos

### Health Check

- `GET /` - API status
- `GET /health` - Health check

## Deployment

### Railway

1. Connect your repository to Railway
2. Set environment variables in Railway dashboard
3. Deploy automatically on push to main branch

### Environment Variables

Required for production:
- `GEMINI_API_KEY`
- `TTS_API_KEY`
- `HOST` (default: 0.0.0.0)
- `PORT` (default: 8000)
- `DEBUG` (default: True)

## Project Structure

```
backend/
├── main.py           # FastAPI application
├── models.py         # Pydantic models
├── config.py         # Configuration settings
├── pyproject.toml    # Project dependencies
├── .env.example      # Environment template
└── README.md         # This file
```

## Development

The backend is structured to be easily extensible. Key areas for implementation:

1. **Gemini API Integration** - Add actual AI script generation
2. **TTS Service** - Integrate Peter Griffin voice synthesis
3. **Video Processing** - Add video compilation logic
4. **Database** - Add persistence for video metadata
5. **File Storage** - Implement file upload/download handling

## License

MIT License