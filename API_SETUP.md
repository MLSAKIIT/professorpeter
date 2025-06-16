# API Configuration Setup

The Professor Peter video generation system requires **real API keys** for both script generation and voice synthesis. No fallbacks or mock responses are provided.

## Required API Keys

### 1. Google Gemini API Key
**Purpose**: Script generation using AI
**Environment Variable**: `GEMINI_API_KEY`

**How to get it**:
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key

### 2. ElevenLabs API Key  
**Purpose**: Text-to-speech (Peter Griffin voice)
**Environment Variable**: `TTS_API_KEY`

**How to get it**:
1. Sign up at [ElevenLabs](https://elevenlabs.io/)
2. Go to your [Profile Settings](https://elevenlabs.io/docs/authentication)
3. Copy your API key

### 3. Voice ID Configuration
**Purpose**: Specify which voice to use for Peter Griffin
**Environment Variable**: `DEFAULT_VOICE_ID`
**Default Value**: `EXAVITQu4vr4xnSDxMaL` (Sample voice)

**How to find voice IDs**:
1. Use ElevenLabs Voice Library
2. Or use the API: `GET https://api.elevenlabs.io/v1/voices`

## Configuration Steps

### Option 1: Environment Variables (Recommended)
Create a `.env` file in the `backend/` directory:

```bash
# Copy from env.example and fill in your keys
cp backend/env.example backend/.env
```

Edit `backend/.env`:
```env
GEMINI_API_KEY=your_gemini_api_key_here
TTS_API_KEY=your_elevenlabs_api_key_here
DEFAULT_VOICE_ID=EXAVITQu4vr4xnSDxMaL
```

### Option 2: System Environment Variables
```bash
export GEMINI_API_KEY="your_gemini_api_key_here"
export TTS_API_KEY="your_elevenlabs_api_key_here"
export DEFAULT_VOICE_ID="EXAVITQu4vr4xnSDxMaL"
```

### Option 3: PowerShell (Windows)
```powershell
$env:GEMINI_API_KEY="your_gemini_api_key_here"
$env:TTS_API_KEY="your_elevenlabs_api_key_here"
$env:DEFAULT_VOICE_ID="EXAVITQu4vr4xnSDxMaL"
```

## Verification

After setting up the keys, verify they're working:

1. **Check API status**:
   ```bash
   curl http://localhost:8000/health
   ```

2. **Expected response**:
   ```json
   {
     "status": "healthy",
     "dependencies": {
       "gemini_api": true,
       "tts_api": true
     }
   }
   ```

3. **Check available templates**:
   ```bash
   curl http://localhost:8000/api/templates
   ```

## Error Messages

If API keys are not configured, you'll see clear error messages:

- ❌ `Gemini API key not configured. Please set GEMINI_API_KEY environment variable.`
- ❌ `TTS API key not configured. Please set TTS_API_KEY environment variable.`
- ❌ `Default voice ID not configured. Please set DEFAULT_VOICE_ID environment variable.`

## Cost Considerations

### Gemini API
- **Free tier**: 15 requests per minute
- **Paid**: $0.125 per 1K characters (input)

### ElevenLabs
- **Free tier**: 10,000 characters per month
- **Starter**: $5/month for 30,000 characters
- **Creator**: $22/month for 100,000 characters

## Security Notes

- ⚠️ **Never commit API keys to version control**
- ✅ Use `.env` files (already in `.gitignore`)
- ✅ Use environment variables in production
- ✅ Rotate keys regularly
- ✅ Monitor usage and billing

## Troubleshooting

### Common Issues

1. **"Invalid API key"**
   - Verify the key is correct
   - Check if the key has proper permissions
   - Ensure no extra spaces or characters

2. **"Voice ID not found"**
   - Use a valid ElevenLabs voice ID
   - Check available voices in your account

3. **"Rate limit exceeded"**
   - Wait and retry
   - Upgrade your API plan
   - Implement proper retry logic

### Testing Individual APIs

**Test Gemini**:
```bash
curl -X POST http://localhost:8000/api/generate-script \
  -H "Content-Type: application/json" \
  -d '{"prompt": "test prompt"}'
```

**Test ElevenLabs**:
```bash
curl -X POST http://localhost:8000/api/generate-tts \
  -H "Content-Type: application/json" \
  -d '{"script": "Hello, this is a test."}'
```

## Support

If you encounter issues:
1. Check the logs: `tail -f backend/logs/app.log`
2. Verify API key configuration
3. Test individual API endpoints
4. Check network connectivity
5. Review API documentation

---

**Remember**: This system now requires **real API keys** - no mock responses or fallbacks are provided to ensure you get actual AI-generated content and voice synthesis. 