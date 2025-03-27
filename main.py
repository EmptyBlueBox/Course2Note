import os
from typing import Dict

import toml

from Source.soundtrack2text import process_course_audio
from Source.text2note import generate_course_notes
from Source.video2soundtrack import process_course_videos


def load_config() -> Dict:
    """Load configuration from config.toml file."""
    try:
        with open("config_private.toml", "r") as f:
            return toml.load(f)
    except Exception as e:
        print(
            f"Error loading config: {str(e)}, please don't forget to create a config_private.toml file"
        )
        return {}


def process_course(course_name: str, config: Dict) -> None:
    """
    Process a single course directory.

    Args:
        course_name (str): Name of the course
        config (dict): Configuration dictionary
    """
    try:
        print(f"Processing course: {course_name}")

        # Create course-specific directories
        course_dir = os.path.join("Course", course_name)
        playback_dir = os.path.join(course_dir, "Playback")
        soundtrack_dir = os.path.join(course_dir, "SoundTrack")
        transcript_dir = os.path.join(course_dir, "Transcript")
        note_dir = os.path.join(course_dir, "Note")

        # Create all required directories
        for directory in [
            course_dir,
            playback_dir,
            soundtrack_dir,
            transcript_dir,
            note_dir,
        ]:
            os.makedirs(directory, exist_ok=True)

        # Process video files
        if os.path.exists(playback_dir) and os.listdir(playback_dir):
            print("Extracting audio from videos...")
            process_course_videos(playback_dir, soundtrack_dir)

            print("Transcribing audio files...")
            process_course_audio(
                soundtrack_dir,
                transcript_dir,
                config.get("XUNFEI_APP_ID", ""),
                config.get("XUNFEI_SECRET_KEY", ""),
            )

            print("Generating course notes...")
            generate_course_notes(
                transcript_dir,
                note_dir,
                config.get("OPENAI_ENDPOINT", ""),
                config.get("OPENAI_API_KEY", ""),
                config.get("MODEL", "gpt-4o-mini"),
                course_name,
                config.get("STYLE", "cleaner"),
            )
        else:
            print("No video files found in Playback directory.")

    except Exception as e:
        print(f"Error processing course {course_name}: {str(e)}")


def main():
    """Main function to process all courses."""
    try:
        # Load configuration
        config = load_config()
        if not config:
            print("Failed to load configuration. Please check config.toml file.")
            return

        # Check required API keys
        required_keys = ["XUNFEI_APP_ID", "XUNFEI_SECRET_KEY", "OPENAI_API_KEY"]
        missing_keys = [key for key in required_keys if not config.get(key)]
        if missing_keys:
            print(f"Missing required API keys: {', '.join(missing_keys)}")
            return

        # Create main Course directory
        os.makedirs("Course", exist_ok=True)

        # Get course name from config
        course_name = config.get("COURSE_NAME")
        if not course_name:
            print("No course name specified in config file.")
            return

        process_course(course_name, config)

        print("Course processed successfully!")

    except Exception as e:
        print(f"Error in main process: {str(e)}")


if __name__ == "__main__":
    main()
