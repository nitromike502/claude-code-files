#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "google-cloud-texttospeech",
#     "python-dotenv",
#     "pygame",
# ]
# ///

import argparse
import os
import sys
import tempfile
from pathlib import Path
from dotenv import load_dotenv

# Fix Windows Unicode encoding issues
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

def setup_google_credentials():
    """
    Set up Google Cloud credentials for both WSL and Windows environments.
    Converts WSL paths to Windows paths when running from Windows executable.
    """
    google_creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

    if google_creds_path:
        # Check if the current path exists
        if os.path.exists(google_creds_path):
            return google_creds_path

        # If WSL path doesn't exist from Windows context, try converting to Windows path
        if google_creds_path.startswith('/'):
            # Convert WSL path to Windows UNC path
            windows_path = google_creds_path.replace('/', '\\')
            windows_path = f"\\\\wsl.localhost\\Ubuntu{windows_path}"

            # Set the converted path in environment
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = windows_path

            # Verify the converted path exists
            if os.path.exists(windows_path):
                print(f"SUCCESS: Using converted Windows credential path: {windows_path}")
                return windows_path
            else:
                print(f"WARNING: Credential file not found at WSL path: {google_creds_path}")
                print(f"WARNING: Credential file not found at Windows path: {windows_path}")
                return None

        # If Windows path doesn't exist, try converting to WSL path
        elif '\\\\wsl.localhost\\Ubuntu\\' in google_creds_path:
            # Convert Windows UNC path to WSL path
            wsl_path = google_creds_path.replace('\\\\wsl.localhost\\Ubuntu\\', '/')
            wsl_path = wsl_path.replace('\\', '/')

            # Set the converted path in environment
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = wsl_path

            # Verify the converted path exists
            if os.path.exists(wsl_path):
                return wsl_path
            else:
                print(f"WARNING: Credential file not found at Windows path: {google_creds_path}")
                print(f"WARNING: Credential file not found at WSL path: {wsl_path}")
                return None

    return google_creds_path

def main():
    """
    Google Gemini Chirp 3 HD TTS Script

    Uses Google Cloud Text-to-Speech API with Chirp 3 HD voices for high-quality speech synthesis.
    Accepts optional text prompt and voice selection as command-line arguments.

    Usage:
    - ./gemini_tts.py                                        # Uses default text and voice
    - ./gemini_tts.py "Your custom text"                     # Uses provided text with default voice
    - ./gemini_tts.py "Text" --voice sulafat                 # Uses Sulafat voice
    - ./gemini_tts.py "Text" --voice-id en-US-Chirp3-HD-Kore # Uses specific voice ID
    - ./gemini_tts.py "Text" --speed 1.5                     # Uses 1.5x speaking rate

    Available voice names: aoede, puck, charon, kore, fenrir, leda, orus, zephyr, sulafat
    Environment variable: GEMINI_VOICE (voice name or full voice ID)
    Environment file: .claude/.env (preferred) or .env (fallback)

    Features:
    - High-quality Chirp 3 HD voice synthesis
    - Natural, expressive speech generation
    - Multiple voice personalities
    - Adjustable speaking rate (0.25x to 2.0x speed)
    - Support for 40+ languages
    - Cost-effective for production use
    """

    # Load environment variables
    # First try .claude/.env, then fall back to current directory .env
    # Find the .claude directory by going up from the script location
    current = Path(__file__).parent
    while current.name != ".claude" and current.parent != current:
        current = current.parent
    if current.name == ".claude":
        claude_env = current / ".env"
        if claude_env.exists():
            load_dotenv(claude_env)
        else:
            load_dotenv()  # Fall back to current directory
    else:
        load_dotenv()  # Fall back to current directory

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Google Gemini Chirp 3 HD TTS with voice selection')
    parser.add_argument('text', nargs='*', help='Text to convert to speech')
    parser.add_argument('--voice', choices=['aoede', 'puck', 'charon', 'kore', 'fenrir', 'leda', 'orus', 'zephyr', 'sulafat'],
                       help='Voice name to use')
    parser.add_argument('--voice-id', help='Specific voice ID to use (e.g., en-US-Chirp3-HD-Sulafat)')
    parser.add_argument('--speed', type=float, default=1.0, help='Speaking rate (0.25-2.0, default: 1.0)')
    parser.add_argument('--stdin', action='store_true', help='Read text from stdin instead of arguments')
    args = parser.parse_args()

    # Validate speed parameter
    if not (0.25 <= args.speed <= 2.0):
        print("❌ Error: Speed must be between 0.25 and 2.0")
        sys.exit(1)

    # Set up Google Cloud credentials for both WSL and Windows environments
    google_creds_path = setup_google_credentials()

    # Check for required authentication
    if not google_creds_path and not os.getenv('GOOGLE_CLOUD_PROJECT'):
        # Check if we can use Application Default Credentials
        try:
            import google.auth
            credentials, project = google.auth.default()
        except Exception:
            print("❌ Error: Google Cloud authentication not configured")
            print("Please set up authentication by either:")
            print("1. Setting GOOGLE_APPLICATION_CREDENTIALS environment variable to your service account key file")
            print("2. Running 'gcloud auth application-default login' for Application Default Credentials")
            print("3. Setting GOOGLE_CLOUD_PROJECT if using other authentication methods")
            print("See: https://cloud.google.com/docs/authentication/getting-started")
            sys.exit(1)

    # Voice ID mapping for Chirp 3 HD voices
    voice_mapping = {
        'aoede': 'en-US-Chirp3-HD-Aoede',
        'puck': 'en-US-Chirp3-HD-Puck',
        'charon': 'en-US-Chirp3-HD-Charon',
        'kore': 'en-US-Chirp3-HD-Kore',
        'fenrir': 'en-US-Chirp3-HD-Fenrir',
        'leda': 'en-US-Chirp3-HD-Leda',
        'orus': 'en-US-Chirp3-HD-Orus',
        'zephyr': 'en-US-Chirp3-HD-Zephyr',
        'sulafat': 'en-US-Chirp3-HD-Sulafat',
    }

    try:
        from google.cloud import texttospeech
        import pygame
        from google.oauth2 import service_account

        # Initialize client with explicit credentials
        # Try multiple credential paths
        credentials_paths = [
            "C:\\Users\\nitro\\.claude\\hooks\\utils\\tts\\gen-lang-client-0718398491-6186cfe2ae0c.local.json",
            "/mnt/c/Users/nitro/.claude/hooks/utils/tts/gen-lang-client-0718398491-6186cfe2ae0c.local.json",
            "/home/meckert/.claude/hooks/utils/tts/gen-lang-client-0718398491-6186cfe2ae0c.local.json"
        ]

        client = None
        for cred_path in credentials_paths:
            try:
                if os.path.exists(cred_path):
                    credentials = service_account.Credentials.from_service_account_file(cred_path)
                    client = texttospeech.TextToSpeechClient(credentials=credentials)
                    print(f"✅ Using credentials from: {cred_path}")
                    break
            except Exception as e:
                continue

        if not client:
            # Fall back to default client
            client = texttospeech.TextToSpeechClient()

        print("🎙️  Google Gemini Chirp 3 HD TTS")
        print("=" * 40)

        # Get text from stdin, arguments, or use default
        if args.stdin:
            # Read from stdin
            try:
                text = sys.stdin.read().strip()
                if not text:
                    text = "The first move is what sets everything in motion."
            except Exception:
                text = "The first move is what sets everything in motion."
        elif args.text:
            text = " ".join(args.text)
        elif not sys.stdin.isatty():
            # Automatically detect piped input even without --stdin flag
            try:
                text = sys.stdin.read().strip()
                if not text:
                    text = "The first move is what sets everything in motion."
            except Exception:
                text = "The first move is what sets everything in motion."
        else:
            text = "The first move is what sets everything in motion."

        # Determine voice ID to use
        voice_id = None
        voice_name = "default"

        if args.voice_id:
            # Use specific voice ID from argument
            voice_id = args.voice_id
            voice_name = f"custom ({voice_id})"
        elif args.voice:
            # Use voice name from argument
            voice_id = voice_mapping[args.voice]
            voice_name = args.voice
        elif os.getenv('GEMINI_VOICE'):
            # Use voice from environment variable
            env_voice = os.getenv('GEMINI_VOICE').lower()
            if env_voice in voice_mapping:
                voice_id = voice_mapping[env_voice]
                voice_name = env_voice
            else:
                # Assume it's a custom voice ID
                voice_id = env_voice
                voice_name = f"env custom ({voice_id})"
        else:
            # Default to Sulafat voice as requested
            voice_id = voice_mapping['sulafat']
            voice_name = 'sulafat'

        print(f"🎯 Text: {text}")
        print(f"🎤 Voice: {voice_name}")
        print(f"⚡ Speed: {args.speed}x")
        print("🔊 Generating and playing...")

        try:
            # Set up the synthesis input
            synthesis_input = texttospeech.SynthesisInput(text=text)

            # Set up voice parameters
            voice = texttospeech.VoiceSelectionParams(
                language_code="en-US",
                name=voice_id
            )

            # Set up audio configuration
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=args.speed
            )

            # Generate speech
            response = client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )

            # Create temporary file for audio playback
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_audio:
                temp_audio.write(response.audio_content)
                temp_audio_path = temp_audio.name

            # Initialize pygame mixer for audio playback
            pygame.mixer.init()
            pygame.mixer.music.load(temp_audio_path)
            pygame.mixer.music.play()

            # Wait for playback to complete
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)

            # Clean up
            pygame.mixer.quit()
            try:
                os.unlink(temp_audio_path)
            except (OSError, PermissionError):
                # File might still be in use, try again after a short delay
                pygame.time.wait(500)
                try:
                    os.unlink(temp_audio_path)
                except (OSError, PermissionError):
                    pass  # Leave the temp file if we can't delete it

            print("✅ Playback complete!")

        except Exception as e:
            error_msg = str(e)
            if "permission" in error_msg.lower() or "authentication" in error_msg.lower():
                print("❌ Authentication error. Please check your Google Cloud credentials.")
                print("Make sure you have Text-to-Speech API enabled and proper permissions.")
            elif "not found" in error_msg.lower() and voice_id:
                print(f"⚠️  Voice '{voice_name}' not found. Trying default voice...")
                # Retry with default voice
                try:
                    voice = texttospeech.VoiceSelectionParams(
                        language_code="en-US",
                        name="en-US-Chirp3-HD-Charon"  # Fallback to Charon
                    )
                    # Use the same audio config with speed for fallback
                    response = client.synthesize_speech(
                        input=synthesis_input,
                        voice=voice,
                        audio_config=audio_config
                    )
                    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_audio:
                        temp_audio.write(response.audio_content)
                        temp_audio_path = temp_audio.name

                    pygame.mixer.music.load(temp_audio_path)
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy():
                        pygame.time.wait(100)

                    # Clean up
                    pygame.mixer.quit()
                    try:
                        os.unlink(temp_audio_path)
                    except (OSError, PermissionError):
                        pygame.time.wait(500)
                        try:
                            os.unlink(temp_audio_path)
                        except (OSError, PermissionError):
                            pass
                    print("✅ Playback complete with fallback voice!")
                except Exception as fallback_error:
                    print(f"❌ Error with fallback voice: {fallback_error}")
            else:
                print(f"❌ Error: {e}")

    except ImportError as import_error:
        missing_package = str(import_error).split("'")[1] if "'" in str(import_error) else "required package"
        print(f"❌ Error: {missing_package} not installed")
        print("This script uses UV to auto-install dependencies.")
        print("Make sure UV is installed: https://docs.astral.sh/uv/")
        print("\nRequired packages:")
        print("- google-cloud-texttospeech")
        print("- pygame")
        print("- python-dotenv")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()