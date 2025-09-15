# Google Gemini Chirp 3 HD TTS Setup Guide

This guide helps you configure Google Gemini Text-to-Speech with Chirp 3 HD voices for your Claude Code TTS notifications.

## Prerequisites

1. **Google Cloud Account**: You need an active Google Cloud account
2. **Google Cloud Project**: A project with Text-to-Speech API enabled
3. **Authentication**: Service Account or Application Default Credentials

## Setup Steps

### 1. Enable Text-to-Speech API

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Select or create a project
3. Navigate to **APIs & Services > Library**
4. Search for "Cloud Text-to-Speech API"
5. Click "Enable"

### 2. Authentication Options

#### Option A: Service Account Key (Recommended for Production)

1. Go to **IAM & Admin > Service Accounts**
2. Click "Create Service Account"
3. Give it a name (e.g., "claude-tts-service")
4. Grant the role: **Cloud Text-to-Speech Client** or **Text-to-Speech User**
5. Create and download the JSON key file
6. Set the environment variable:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
   ```

#### Option B: Application Default Credentials (Development)

1. Install the Google Cloud CLI: https://cloud.google.com/sdk/docs/install
2. Authenticate with your Google account:
   ```bash
   gcloud auth application-default login
   ```
3. Set your project ID:
   ```bash
   export GOOGLE_CLOUD_PROJECT="your-project-id"
   ```

### 3. Environment Variables

Add these to your `.claude/.env` file:

```bash
# Required: One of these authentication methods
GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
# OR
GOOGLE_CLOUD_PROJECT="your-project-id"

# Optional: Default voice selection
GEMINI_VOICE="sulafat"  # or any supported voice name
```

## Available Voices

The script supports these Chirp 3 HD voice personalities:

### Female Voices
- **aoede**: Natural, conversational
- **kore**: Clear, professional
- **leda**: Warm, friendly
- **zephyr**: Bright, energetic
- **sulafat**: Expressive, dynamic (your requested voice)

### Male Voices
- **puck**: Playful, youthful
- **charon**: Deep, authoritative
- **fenrir**: Strong, confident
- **orus**: Smooth, sophisticated

## Usage Examples

### Command Line Usage

```bash
# Use default voice (Sulafat)
./gemini_tts.py "Hello, this is a test"

# Use specific voice
./gemini_tts.py "Hello, this is a test" --voice sulafat

# Use full voice ID
./gemini_tts.py "Hello, this is a test" --voice-id en-US-Chirp3-HD-Sulafat
```

### Integration with Notification System

The notification.py script will automatically detect Google Cloud credentials and use Gemini TTS in this priority order:

1. **ElevenLabs** (if ELEVENLABS_API_KEY exists)
2. **Gemini** (if Google Cloud credentials exist) ← Your new option
3. **OpenAI** (if OPENAI_API_KEY exists)
4. **pyttsx3** (local fallback)

## Troubleshooting

### Authentication Errors
- Verify your service account has Text-to-Speech permissions
- Check that the JSON key file path is correct
- Ensure the Text-to-Speech API is enabled in your project

### Voice Not Found Errors
- The script will fall back to 'Charon' voice if the specified voice isn't available
- Check that you're using a supported voice name from the list above

### Import Errors
- The script uses UV to auto-install dependencies
- Required packages: `google-cloud-texttospeech`, `pygame`, `python-dotenv`

### Audio Playback Issues
- Ensure your system has audio output configured
- The script uses pygame for audio playback
- On Linux, you may need `sudo apt install python3-pygame` or similar

## Cost Considerations

- Chirp 3 HD voices are charged per character
- Current pricing: ~$16 per 1M characters
- Consider setting usage alerts in Google Cloud Console
- See: https://cloud.google.com/text-to-speech/pricing

## Security Notes

- Keep your service account key file secure
- Don't commit credentials to version control
- Use IAM roles with minimal required permissions
- Consider using Application Default Credentials for development

## Support

- [Google Cloud Text-to-Speech Documentation](https://cloud.google.com/text-to-speech/docs)
- [Chirp 3 HD Voices Documentation](https://cloud.google.com/text-to-speech/docs/chirp3-hd)
- [Authentication Guide](https://cloud.google.com/docs/authentication)