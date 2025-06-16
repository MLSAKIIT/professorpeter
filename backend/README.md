# Educational Video Generator Backend

🎬 Backend API for generating educational videos with Peter Griffin's voice and personality.

## ✨ Features

- **AI Script Generation**: Uses Google's Gemini models to create Peter Griffin-style educational scripts
- **Text-to-Speech**: Converts scripts to audio using ElevenLabs API
- **Video Compilation**: Merges audio with video templates and adds subtitles
- **REST API**: Comprehensive API for frontend integration
- **Mock Responses**: Works without API keys for development/testing

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Clone and navigate to backend directory
cd backend

# Run the setup script
python setup.py
```

### 2. Configure API Keys (Optional)

Edit the `.env` file with your API keys:

```bash
# For actual AI generation (optional)
GEMINI_API_KEY=your_google_gemini_api_key_here
TTS_API_KEY=your_elevenlabs_api_key_here

# Server settings
HOST=0.0.0.0
PORT=8000
DEBUG=True
FRONTEND_URL=http://localhost:3000
```

### 3. Start the Server

```bash
python start.py
```

The API will be available at:
- **Server**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 📚 API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API status and info |
| `GET` | `/health` | Health check with dependencies |
| `POST` | `/api/generate-script` | Generate Peter Griffin script |
| `POST` | `/api/generate-video` | Start video generation |
| `GET` | `/api/video/{id}/status` | Check generation status |
| `GET` | `/api/video/{id}/download` | Download completed video |

### Additional Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/generate-tts` | Convert script to speech |
| `POST` | `/api/generate-subtitles` | Generate subtitles |
| `POST` | `/api/generate-all` | Full pipeline generation |
| `GET` | `/api/videos` | List all videos |

## 🔧 Configuration

### Environment Variables

```bash
# Required for AI features
GEMINI_API_KEY=           # Google Gemini API key
TTS_API_KEY=             # ElevenLabs API key

# Server Configuration
HOST=0.0.0.0            # Server host
PORT=8000               # Server port
DEBUG=True              # Debug mode
FRONTEND_URL=           # Frontend URL for CORS

# Directories
UPLOAD_DIR=./uploads    # Upload directory
OUTPUT_DIR=./outputs    # Output directory
TEMPLATES_DIR=./templates # Video templates

# Video Settings
MAX_VIDEO_DURATION=60   # Maximum video length
DEFAULT_VOICE_ID=       # ElevenLabs voice ID
```

### Directory Structure

```
backend/
├── main.py              # FastAPI application
├── models.py            # Pydantic models
├── config.py            # Configuration settings
├── script.py            # Script generation logic
├── start.py             # Server startup script
├── setup.py             # Setup automation
├── requirements.txt     # Python dependencies
├── pyproject.toml       # Project configuration
├── env.example          # Environment template
├── outputs/             # Generated content
├── uploads/             # User uploads
└── templates/           # Video templates
```

## 🧪 Development Mode

The backend works without API keys for development:

- **Script Generation**: Returns mock Peter Griffin responses
- **Status Simulation**: Simulates video generation progress
- **File Serving**: Serves static content from outputs directory

## 🔑 Getting API Keys

### Google Gemini API
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add to `.env` as `GEMINI_API_KEY`

### ElevenLabs API
1. Sign up at [ElevenLabs](https://elevenlabs.io)
2. Go to Profile → API Keys
3. Create a new API key
4. Add to `.env` as `TTS_API_KEY`

## 📝 Usage Examples

### Generate Script

```bash
curl -X POST "http://localhost:8000/api/generate-script" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "quantum physics"}'
```

### Check Status

```bash
curl "http://localhost:8000/api/video/video_12345/status"
```

### Health Check

```bash
curl "http://localhost:8000/health"
```

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Change port in .env file
   PORT=8001
   ```

2. **Dependencies Installation Failed**
   ```bash
   # Install manually
   pip install fastapi uvicorn python-dotenv
   ```

3. **API Keys Not Working**
   - Verify keys are correctly set in `.env`
   - Check API key permissions and quotas
   - API will work in mock mode without keys

4. **CORS Issues**
   - Ensure `FRONTEND_URL` is set correctly
   - Check frontend is running on expected port

### Debug Mode

Enable detailed logging:

```bash
DEBUG=True python start.py
```

## 🔒 Security Notes

- **API Keys**: Never commit `.env` file to version control
- **CORS**: Configure `FRONTEND_URL` properly for production
- **File Access**: Generated files are served statically
- **Input Validation**: All inputs are validated via Pydantic models

## 🚀 Production Deployment

1. Set `DEBUG=False` in environment
2. Configure proper `FRONTEND_URL`
3. Use environment variables instead of `.env` file
4. Consider using a reverse proxy (nginx)
5. Set up proper logging and monitoring

## 📊 API Response Examples

### Script Generation Response
```json
{
  "script": "Hey there, folks! Peter Griffin here...",
  "video_id": "script_12345",
  "word_count": 150,
  "estimated_duration": 45.2
}
```

### Status Response
```json
{
  "video_id": "video_12345",
  "status": "generating_voice",
  "progress": 65,
  "message": "Creating Peter Griffin voice audio...",
  "created_at": "2024-01-01T12:00:00Z"
}
```

## 🤝 Contributing

1. Follow the existing code style
2. Add tests for new features
3. Update documentation
4. Ensure all endpoints work in mock mode

## 📄 License

This project is part of the Prof. Peter's Students educational video generator.