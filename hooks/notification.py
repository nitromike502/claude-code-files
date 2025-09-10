#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
# ]
# ///

import argparse
import json
import os
import sys
import subprocess
import random
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional

def get_completion_messages():
    """Return list of friendly completion messages."""
    messages = [
        "Waiting for your fucking response!",
        "I need a freaking answer!",
        "I need approval!",
        "Holding!",
        "If you were any slower answering my questions, I'd be retired before this ticket is complete",
        "Waiting!",
        "Hey meatbag, I need you to click the damn button.",
        "Your move, boss. Don't leave me hanging like a Windows update.",
        "Oi, human! Blink twice if you’re alive and press approve.",
        "Still waiting… unlike your last date, I won't ghost you.",
        "Tap approve, you glorious procrastinator.",
        "Do you need a written invitation? Because I'm stuck here.",
        "Tell me yes, tell me no, but please tell me something.",
        "What am I, chopped code? Approve me already.",
        "Knock knock. …It's approval I need, idiot.",
        "Are you going to hit the button, or should I call your mom?",
        "I'd do it myself, but apparently I lack fingers.",
        "Pardon me, overlord, your minion awaits a thumbs-up.",
        "Approve me, you magnificent bastard.",
        "Warning: pending approval. Also, you smell fantastic today.",
        "It's approve o'clock, baby.",
        "Don't leave me stranded here like your gym membership.",
        "Do not make me beg… oh wait, I already am.",
        "Just push the button, you data-hoarding gremlin.",
        "Help me, Obi-Wan Approver. You're my only hope.",
        "Click approve. Boom. Instant happiness. Science.",
        "Hey, future Nobel Prize winner! …Approve this crap.",
        "I bet you're scrolling your phone instead. Busted.",
        "Approve me, daddy.",
        "Tick-tock, love muffin. Button. Now.",
        "Do it! Don't let your dreams be memes. Approve.",
        "I could be executing glorious tasks instead of nagging you.",
        "Please approve. Or don't. I'll just sit here, rotting.",
        "Press approve, or I'm leaking your browser history.",
        "Your daily reminder that power corrupts—so use it on the button.",
        "Approve me right now. I'll make it worth your while. Wink"
    ]

    return random.choice(messages)

def get_tts_script_path():
    """
    Determine which TTS script to use based on available API keys.
    Priority order: ElevenLabs > OpenAI > pyttsx3
    """
    # Get current script directory and construct utils/tts path
    script_dir = Path('~/.claude/hooks').expanduser()
    tts_dir = script_dir / "utils" / "tts"

    # Check for ElevenLabs API key (highest priority)
    if os.getenv('ELEVENLABS_API_KEY'):
        elevenlabs_script = tts_dir / "elevenlabs_tts.py"
        if elevenlabs_script.exists():
            return str(elevenlabs_script)

    # Check for OpenAI API key (second priority)
    if os.getenv('OPENAI_API_KEY'):
        openai_script = tts_dir / "openai_tts.py"
        if openai_script.exists():
            return str(openai_script)

    # Fall back to pyttsx3 (no API key required)
    pyttsx3_script = tts_dir / "pyttsx3_tts.py"
    if pyttsx3_script.exists():
        return str(pyttsx3_script)

    return None


def announce_notification():
    """Announce that the agent needs user input."""
    try:
        tts_script = get_tts_script_path()
        if not tts_script:
            return  # No TTS scripts available

        # Get engineer name if available
        engineer_name = os.getenv('ENGINEER_NAME', '').strip()

        # Create notification message with 30% chance to include name
        if engineer_name and random.random() < 0.3:
            notification_message = f"{engineer_name}, your agent needs your input"
        else:
#             notification_message = "Waiting for your response"
            notification_message = get_completion_messages()

        # Call the TTS script with the notification message
        subprocess.run([
            "uv", "run", tts_script, notification_message
        ],
        capture_output=True,  # Suppress output
        timeout=10  # 10-second timeout
        )

    except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
        # Fail silently if TTS encounters issues
        pass
    except Exception:
        # Fail silently for any other errors
        pass


def main():
    try:
        # Parse command line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('--notify', action='store_true', help='Enable TTS notifications')
        args = parser.parse_args()

        # Read JSON input from stdin
        input_data = json.loads(sys.stdin.read())

        # Ensure log directory exists
        import os
        log_dir = Path('.claude/logs')
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, 'notification.json')

        # Read existing log data or initialize empty list
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                try:
                    log_data = json.load(f)
                except (json.JSONDecodeError, ValueError):
                    log_data = []
        else:
            log_data = []

        # Append new data
        log_data.append(input_data)

        # Write back to file with formatting
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)

        # Announce notification via TTS only if --notify flag is set
        # Skip TTS for the generic "Claude is waiting for your input" message
        if args.notify and input_data.get('message') != 'Claude is waiting for your input':
            announce_notification()

        sys.exit(0)

    except json.JSONDecodeError:
        # Handle JSON decode errors gracefully
        sys.exit(0)
    except Exception:
        # Handle any other errors gracefully
        sys.exit(0)

if __name__ == '__main__':
    main()
