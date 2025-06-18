<p align="center">
  <a href="" rel="noopener">
 <img width=250px height=250px src="backend/assets/peter_griffin.png" alt="professorpeter"></a>
</p>

<h1 align="center">Professor Peter 🎓🎬</h1>

> *"Hey Lois, remember when I became an AI-powered educational content creator? Nyehehehe!"*

Welcome to **Professor Peter** - the most ridiculous yet surprisingly effective educational video generator on the internet! 🚀

## What the heck is this thing? 🤔

Professor Peter is an AI-powered educational video generator that creates hilarious yet informative content using **Peter Griffin's voice and personality**. Because nothing says "quality education" quite like having a cartoon dad from Rhode Island explain quantum physics, right?

### The Magic Behind the Madness ✨

- 🧠 **AI Script Generation**: Uses Google's Gemini AI to create Peter Griffin-style educational scripts
- 🎤 **Voice Synthesis**: Converts scripts to audio using ElevenLabs TTS (with Peter's unmistakable voice)
- 🎬 **Video Compilation**: Merges everything with video templates and subtitles
- 🎨 **Beautiful UI**: A sleek Next.js frontend that doesn't look like it was designed by Peter himself
- 🚀 **Full-Stack Magic**: FastAPI backend + Next.js frontend = Chef's kiss

### Why would anyone make this? 🤷‍♂️

Great question! Sometimes the best way to learn complex topics is through humor and memorable characters. Plus, who doesn't want to hear Peter Griffin explain the intricacies of machine learning or the fundamentals of calculus?

*"Hey Brian, did you know that neural networks are like my brain, but actually functional?"*

## Quick Start (For the Impatient) ⚡

**Want to get this thing running ASAP?** We got you covered:

```bash
git clone <your-repo-url>
cd ProfessorPeters
chmod +x start-dev.sh
./start-dev.sh
```

Then visit `http://localhost:3000` and watch the magic happen! 🎪

## Detailed Setup (For the Thorough) 📚

### Prerequisites 📋

- **Python 3.12+** (because we're fancy like that)
- **Node.js 18+** (for the frontend goodness)
- **uv** (Python package manager - recommended)
- **Git** (obviously)
  
## 🎞 FFmpeg Installation & Setup

FFmpeg is required to process and merge audio and video.

### 🪟 Windows

1. Download FFmpeg from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)  
   (or directly from [gyan.dev builds](https://www.gyan.dev/ffmpeg/builds/))
2. Extract the ZIP to a folder like `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to your system `PATH`:
   - Open *System Properties → Environment Variables*
   - Under *System Variables*, find `Path`, click *Edit*, and add:  
     `C:\ffmpeg\bin`
4. Verify installation:
   ```bash
   ffmpeg -version
   ```

### 🐧 Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install ffmpeg
ffmpeg -version
```

### 🍎 macOS (Homebrew)

```bash
brew install ffmpeg
ffmpeg -version
```

> ✅ Ensure `ffmpeg` is accessible in your system PATH for video generation to work properly.

### Backend Setup 🐍

The backend is where all the Peter Griffin magic happens!

```bash
# Navigate to the backend directory
cd backend

# Install uv if you haven't already (highly recommended!)
# On macOS/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows:
# powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Add dependencies to your project
uv add fastapi uvicorn python-dotenv httpx google-generativeai elevenlabs

# Sync your environment (installs all dependencies)
uv sync

# Create your environment file
cp env.example .env

# Run the backend
uv run start.py
```

**Backend will be available at:**
- 🌐 API Server: `http://localhost:8000`
- 📖 Interactive Docs: `http://localhost:8000/docs`
- 📋 Alternative Docs: `http://localhost:8000/redoc`

### Frontend Setup 🎨

The frontend is where users interact with our Peter Griffin professor!

```bash
# Navigate to the frontend directory
cd client

# Install dependencies
npm install

# Start the development server
npm run dev
```

**Frontend will be available at:**
- 🎨 Web App: `http://localhost:3000`

### Environment Configuration 🔧

Edit `backend/.env` with your API keys (optional for demo mode):

```bash
# AI Magic (Optional - works in demo mode without these)
GEMINI_API_KEY=your_google_gemini_api_key_here
TTS_API_KEY=your_elevenlabs_api_key_here

# Server Settings
HOST=0.0.0.0
PORT=8000
DEBUG=true
FRONTEND_URL=http://localhost:3000

# Video Settings
MAX_VIDEO_DURATION=60
```

## Getting API Keys 🔑

### Google Gemini API (For Script Generation)
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` as `GEMINI_API_KEY`

### ElevenLabs API (For Peter's Voice)
1. Sign up at [ElevenLabs](https://elevenlabs.io)
2. Go to Profile → API Keys
3. Create a new API key
4. Add it to your `.env` as `TTS_API_KEY`

**Don't have API keys?** No problem! The app works in demo mode with mock responses.

## How to Use This Beast 🎯

### For New Users (Complete Noobs Welcome!) 👶

1. **Clone the Repository**
   ```bash
   git clone <your-repo-url>
   cd ProfessorPeters
   ```

2. **One-Command Setup** (The lazy way)
   ```bash
   ./start-dev.sh
   ```
   This script handles everything automatically!

3. **Manual Setup** (The control-freak way)
   ```bash
   # Backend
   cd backend
   uv sync
   uv run start.py &
   
   # Frontend (in another terminal)
   cd client
   npm install
   npm run dev
   ```

4. **Start Creating!**
   - Open `http://localhost:3000`
   - Enter a topic (e.g., "quantum physics" or "how to make a sandwich")
   - Watch Peter Griffin explain it like only he can!

### For Developers 🛠️

```bash
# Install everything
uv add <package-name>        # Add Python packages
uv sync                      # Install all dependencies
uv run <script>             # Run Python scripts

# Development commands
cd backend && uv run start.py              # Start backend
cd client && npm run dev                   # Start frontend
cd client && npm run build                 # Build for production
```

## Project Structure 🏗️

```
ProfessorPeters/
├── 📁 backend/                 # FastAPI backend
│   ├── 🐍 main.py             # API routes & magic
│   ├── 🎭 models.py           # Pydantic models
│   ├── ⚙️ config.py           # Configuration
│   ├── 📝 script.py           # AI script generation
│   ├── 🎬 video_compiler.py   # Video processing
│   ├── 🎤 audio.py           # TTS generation
│   ├── 📦 pyproject.toml     # Python dependencies
│   └── 🔧 requirements.txt   # Backup dependencies
├── 📁 client/                 # Next.js frontend
│   ├── 📁 src/app/           # App router pages
│   ├── 📁 src/components/    # React components
│   ├── 🎨 globals.css       # Global styles
│   └── 📦 package.json      # Node dependencies
├── 🚀 start-dev.sh          # Development startup script
└── 📖 README.md             # You are here!
```

## API Endpoints 🔌

The backend provides a comprehensive REST API:

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/generate-video` | Create a Peter Griffin educational video |
| `GET` | `/api/video/{id}/status` | Check video generation progress |
| `GET` | `/api/video/{id}/download` | Download your masterpiece |
| `POST` | `/api/generate-script` | Just the script, please |
| `GET` | `/api/templates` | Available video templates |
| `GET` | `/health` | Is this thing working? |

## Troubleshooting 🔧

### Common Issues & Solutions

**"The backend won't start!"**
- Check if port 8000 is already in use
- Make sure you're in the `backend` directory
- Try `uv sync` to reinstall dependencies

**"The frontend is broken!"**
- Delete `node_modules` and run `npm install` again
- Check if port 3000 is available
- Make sure you're in the `client` directory

**"My videos are terrible!"**
- That's not a bug, that's Peter Griffin being Peter Griffin
- Try different prompts for better results
- Check your API keys are working

**"I don't have API keys!"**
- No worries! The app works in demo mode
- You'll get mock responses that are still entertaining

### Getting Help 🆘

1. Check the logs in your terminal
2. Visit `http://localhost:8000/docs` for API documentation
3. Try the `/health` endpoint to check system status
4. When all else fails, ask yourself: "What would Peter do?"

## Contributing 🤝

Want to make Professor Peter even more ridiculous? We welcome contributions!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test everything works
5. Submit a pull request

## License 📄

This project is licensed under the "Please Don't Sue Us, We're Just Having Fun" license. 

Actually, check the LICENSE file for real legal stuff.

## Acknowledgments 🙏

- **Peter Griffin** - For being the inspiration (and hopefully not suing us)
- **Google Gemini** - For making AI script generation possible
- **ElevenLabs** - For incredible voice synthesis technology
- **FastAPI & Next.js** - For making web development not completely terrible
- **The Internet** - For being weird enough that this project makes sense

---

*"Hey Lois, I think I just revolutionized education! Nyehehehe!"* 🎓

Made with ❤️ and way too much caffeine by **Team Prof. Peters Students** for **MLSA Internal Hackathon 2025**.

## Team 👥

**Mentor:**
- Soham Roy

**Members:**
- Kartikeya Trivedi
- Vaibhav Deep Srivastava
- Yash Raj Gupta
- Vaibhav Raj
- Aditya Shukla
- Sidhi Kumari 
