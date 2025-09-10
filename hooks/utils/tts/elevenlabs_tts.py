#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "elevenlabs",
#     "python-dotenv",
# ]
# ///

import argparse
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def main():
    """
    ElevenLabs Turbo v2.5 TTS Script

    Uses ElevenLabs' Turbo v2.5 model for fast, high-quality text-to-speech.
    Accepts optional text prompt and voice selection as command-line arguments.

    Usage:
    - ./elevenlabs_tts.py                                    # Uses default text and voice
    - ./elevenlabs_tts.py "Your custom text"                 # Uses provided text with default voice
    - ./elevenlabs_tts.py "Text" --voice rachel              # Uses Rachel voice
    - ./elevenlabs_tts.py "Text" --voice-id pNInz6obpgDQGcFmaJgB # Uses specific voice ID

    Available voice names: adam, rachel, domi, bella
    Environment variable: ELEVENLABS_VOICE (adam, rachel, domi, bella, or voice ID)
    Environment file: .claude/.env (preferred) or .env (fallback)

    Features:
    - Fast generation (optimized for real-time use)
    - High-quality voice synthesis
    - Stable production model
    - Cost-effective for high-volume usage
    - Voice selection via argument or environment variable
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
    parser = argparse.ArgumentParser(description='ElevenLabs TTS with voice selection')
    parser.add_argument('text', nargs='*', help='Text to convert to speech')
    parser.add_argument('--voice', choices=['adam', 'rachel', 'domi', 'bella', 'arabella', 'bellab'],
                       help='Voice name to use')
    parser.add_argument('--voice-id', help='Specific voice ID to use')
    args = parser.parse_args()

    # Get API key from environment
    api_key = os.getenv('ELEVENLABS_API_KEY')
    if not api_key:
        print("❌ Error: ELEVENLABS_API_KEY not found in environment variables")
        print("Please add your ElevenLabs API key to .env file:")
        print("ELEVENLABS_API_KEY=your_api_key_here")
        sys.exit(1)

    # Voice ID mapping
    voice_mapping = {
        'adam': 'pNInz6obpgDQGcFmaJgB',
        'rachel': '21m00Tcm4TlvDq8ikWAM',
        'domi': 'AZnzlk1XvdvUeBnXmlld',
        'bella': 'EXAVITQu4vr4xnSDxMaL',
        'arabella': 'aEO01A4wXwd1O8GPgGlF',
        'bellab': 'cNYrMw9glwJZXR8RwbuR',
    }

    try:
        from elevenlabs.client import ElevenLabs
        from elevenlabs.play import play

        # Initialize client
        client = ElevenLabs(api_key=api_key)

        print("🎙️  ElevenLabs Turbo v2.5 TTS")
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
        elif os.getenv('ELEVENLABS_VOICE'):
            # Use voice from environment variable
            env_voice = os.getenv('ELEVENLABS_VOICE').lower()
            if env_voice in voice_mapping:
                voice_id = voice_mapping[env_voice]
                voice_name = env_voice
            else:
                # Assume it's a custom voice ID
                voice_id = env_voice
                voice_name = f"env custom ({voice_id})"

        print(f"🎯 Text: {text}")
        print(f"🎤 Voice: {voice_name}")
        print("🔊 Generating and playing...")

        try:
            # Generate and play audio directly
            if voice_id:
                # Use specified voice
                try:
                    audio = client.text_to_speech.convert(
                        text=text,
                        voice_id=voice_id,
                        model_id="eleven_turbo_v2_5"
                    )
                except Exception as e:
                    print(f"⚠️  Specified voice failed ({voice_name}), trying fallbacks...")
                    voice_id = None

            if not voice_id:
                # Try common voice IDs as fallback
                common_voice_ids = [
                    "pNInz6obpgDQGcFmaJgB",  # Adam
                    "21m00Tcm4TlvDq8ikWAM",  # Rachel
                    "AZnzlk1XvdvUeBnXmlld",  # Domi
                    "EXAVITQu4vr4xnSDxMaL"   # Bella
                    "aEO01A4wXwd1O8GPgGlF"   # arabella
                    'cNYrMw9glwJZXR8RwbuR'   # bellab
                ]

                audio = None
                for fallback_voice_id in common_voice_ids:
                    try:
                        audio = client.text_to_speech.convert(
                            text=text,
                            voice_id=fallback_voice_id,
                            model_id="eleven_turbo_v2_5"
                        )
                        break
                    except Exception as e:
                        continue

                if audio is None:
                    raise Exception("No available voices found")

            play(audio)
            print("✅ Playback complete!")

        except Exception as e:
            print(f"❌ Error: {e}")


    except ImportError:
        print("❌ Error: elevenlabs package not installed")
        print("This script uses UV to auto-install dependencies.")
        print("Make sure UV is installed: https://docs.astral.sh/uv/")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
