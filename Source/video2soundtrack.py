import os
from moviepy.editor import VideoFileClip


def extract_audio(video_path: str, output_path: str) -> str:
    """
    Extract audio from a video file and save it as an MP3 file.

    Args:
        video_path (str): Path to the input video file
        output_path (str): Path to save the output audio file

    Returns:
        str: Path to the saved audio file
    """
    try:
        # Load the video file
        video = VideoFileClip(video_path)

        # Extract the audio
        audio = video.audio

        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Save the audio as MP3
        audio.write_audiofile(output_path)

        # Close the video to free up resources
        video.close()

        return output_path
    except Exception as e:
        print(f"Error extracting audio from {video_path}: {str(e)}")
        return None


def process_course_videos(playback_folder: str, soundtrack_folder: str) -> list:
    """
    Process all video files in a course folder and extract their audio.

    Args:
        input_folder (str): Path to the input folder containing course videos e.g. Course2Note/Input/OS/Playback
        soundtrack_folder (str): Path to the soundtrack folder for storing audio files e.g. Course2Note/OS

    Returns:
        list: List of paths to the extracted audio files e.g. [Course2Note/OS/SoundTrack/1.mp3, Course2Note/OS/SoundTrack/2.mp3, ...]
    """
    audio_files = []
    # Process each video file
    for filename in sorted(os.listdir(playback_folder)):
        if filename.endswith((".mp4", ".avi", ".mkv")):
            video_path = os.path.join(playback_folder, filename)
            audio_path = os.path.join(
                soundtrack_folder, f"{os.path.splitext(filename)[0]}.mp3"
            )

            # Skip if audio file already exists
            if os.path.exists(audio_path):
                print(f"Audio file [{audio_path}]: already exists, skipping")
                audio_files.append(audio_path)
            else:
                print(
                    f"Audio file [{audio_path}]: does not exist, processing video file"
                )
                result = extract_audio(video_path, audio_path)
                if result:
                    audio_files.append(result)

    return audio_files
