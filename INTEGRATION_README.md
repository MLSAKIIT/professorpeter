# Professor Peter's Students - Integration Guide

## 🚀 Quick Start

This application consists of a **Next.js frontend** and a **FastAPI backend** that work together to create AI-powered educational videos with Peter Griffin's personality.

### Prerequisites

- **Frontend**: Node.js 18+ and npm
- **Backend**: Python 3.8+ and uv (or pip)
- **Optional**: Google Gemini API key and ElevenLabs API key for production

## 🛠️ Setup Instructions

### 1. Backend Setup

```bash
cd backend

# Install dependencies using uv (recommended)
uv install

# Or using pip
pip install -r requirements.txt

# Copy environment template
cp env.example .env

# Edit .env file with your API keys (optional for demo mode)
# GEMINI_API_KEY=your_google_gemini_api_key_here
# TTS_API_KEY=your_elevenlabs_api_key_here

# Run setup script (creates directories, validates config)
python setup.py

# Start the backend server
uv run start.py
# Or: python start.py
```

The backend will be available at: http://localhost:8000

### 2. Frontend Setup

```bash
cd client

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will be available at: http://localhost:3000

## 🔄 Integration Features

### Automatic Backend Detection

The frontend automatically detects if the backend is running:

- **✅ Backend Online**: Uses real API endpoints for video generation
- **⚠️ Backend Offline**: Falls back to mock responses for demo purposes

### Real-time Status Updates

When the backend is connected:
- Real-time video generation progress
- Status polling every 3 seconds
- Dynamic UI updates based on generation state

### Seamless Fallback

If the backend is unavailable:
- Graceful degradation to mock mode
- Peter Griffin-style demo responses
- Full UI functionality maintained

## 📡 API Integration Points

### Core Endpoints

| Endpoint | Purpose | Frontend Usage |
|----------|---------|----------------|
| `GET /health` | Backend status check | Connection detection |
| `POST /api/generate-script` | Generate Peter Griffin script | Script creation |
| `POST /api/generate-video` | Start video generation | Video processing |
| `GET /api/video/{id}/status` | Check generation progress | Status polling |
| `GET /api/video/{id}/download` | Download completed video | Video serving |

### Status Flow

1. **Script Generation**: POST to `/api/generate-script`
2. **Video Processing**: POST to `/api/generate-video` 
3. **Status Polling**: GET `/api/video/{id}/status` (every 3s)
4. **Completion**: Status changes to 'completed'
5. **Download**: GET `/api/video/{id}/download`

## 🎯 Development Workflow

### Running Both Services

**Terminal 1 (Backend):**
```bash
cd backend
uv run start.py
```

**Terminal 2 (Frontend):**
```bash
cd client
npm run dev
```

### Backend-Only Development

The frontend works independently with mock responses:
```bash
cd client
npm run dev
# Backend connection will show as "offline" but functionality is preserved
```

### Production Deployment

1. **Backend**: Configure environment variables and deploy FastAPI app
2. **Frontend**: Set `NEXT_PUBLIC_API_URL` to your backend URL
3. **CORS**: Backend is configured to allow frontend origins

## 🔧 Configuration

### Environment Variables

**Backend (.env):**
```bash
GEMINI_API_KEY=your_google_gemini_api_key_here
TTS_API_KEY=your_elevenlabs_api_key_here
FRONTEND_URL=http://localhost:3000
```

**Frontend (.env.local):**
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Mock Mode vs Production Mode

**Mock Mode** (no API keys):
- Uses simulated responses
- Instant "video generation"
- Peter Griffin personality preserved
- Perfect for development and demos

**Production Mode** (with API keys):
- Real AI-generated scripts using Google Gemini
- Actual text-to-speech using ElevenLabs
- Video compilation with subtitles
- Full production pipeline

## 🐛 Troubleshooting

### Common Issues

**Backend not starting:**
```bash
# Check Python version
python --version

# Install missing dependencies
uv install
# or: pip install -r requirements.txt

# Check port availability
lsof -i :8000
```

**Frontend API connection issues:**
```bash
# Check backend is running
curl http://localhost:8000/health

# Verify environment variables
echo $NEXT_PUBLIC_API_URL
```

**CORS errors:**
- Backend is pre-configured for localhost:3000
- For different ports, update `FRONTEND_URL` in backend/.env

### Logs and Debugging

**Backend logs:**
- Check console output for API errors
- Health endpoint shows dependency status

**Frontend logs:**
- Check browser console for API calls
- Network tab shows request/response details

## 🎨 Features Overview

### Frontend Features
- Modern glassmorphism design with black theme
- Grid pattern background
- Template selection (Educational, Comedy, Motivational)
- Real-time status updates
- Video preview and download
- Social sharing functionality
- Responsive design

### Backend Features
- FastAPI with automatic OpenAPI docs
- Google Gemini AI integration
- ElevenLabs text-to-speech
- Video compilation with MoviePy
- Status tracking and progress updates
- File serving and download endpoints
- Mock mode for development

## 📊 Performance

- **Mock Mode**: Instant responses (2-3 second simulated delay)
- **Production Mode**: 30-60 seconds for full video generation
- **Status Updates**: Real-time polling every 3 seconds
- **File Sizes**: Videos typically 5-15MB depending on length

## 🚀 Next Steps

1. **API Keys**: Add your Gemini and ElevenLabs keys for production
2. **Deployment**: Deploy both services to your preferred platform
3. **Customization**: Modify templates and personalities
4. **Monitoring**: Add logging and analytics
5. **Scaling**: Implement queue system for high-volume usage

---

**Happy Coding!** 🎬✨ 