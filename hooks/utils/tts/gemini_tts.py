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

    Available voice names: aoede, puck, charon, kore, fenrir, leda, orus, zephyr, sulafat
    Environment variable: GEMINI_VOICE (voice name or full voice ID)
    Environment file: .claude/.env (preferred) or .env (fallback)

    Features:
    - High-quality Chirp 3 HD voice synthesis
    - Natural, expressive speech generation
    - Multiple voice personalities
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
    args = parser.parse_args()

    # Check for required authentication
    # Google Cloud uses Application Default Credentials or GOOGLE_APPLICATION_CREDENTIALS
    google_creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
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

        # Initialize client
        client = texttospeech.TextToSpeechClient()

        print("🎙️  Google Gemini Chirp 3 HD TTS")
        print("=" * 40)

        # Get text from arguments or use default
        if args.text:
            text = " ".join(args.text)
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
                audio_encoding=texttospeech.AudioEncoding.MP3
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

            # Clean up temporary file
            os.unlink(temp_audio_path)

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
                    os.unlink(temp_audio_path)
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