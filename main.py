import os
import glob
import toml
import openai

# Import module functions from Source
from Source import video2soundtrack, soundtrack2text, slide2text, text2note


def ensure_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def process_course(course_path):
    course_name = os.path.basename(course_path)
    work_course_dir = os.path.join("Workfolder", course_name)
    output_course_dir = os.path.join("Output")
    ensure_dir(work_course_dir)
    ensure_dir(output_course_dir)
    
    # Process video playbacks
    playback_dir = os.path.join(course_path, "Playback")
    audio_files = []
    if os.path.exists(playback_dir):
        video_files = sorted(glob.glob(os.path.join(playback_dir, "*")))
        for idx, video in enumerate(video_files):
            audio_output = os.path.join(work_course_dir, f"audio_{idx+1}.mp3")
            print(f"Extracting audio from {video} to {audio_output}")
            video2soundtrack.extract_soundtrack(video, audio_output)
            audio_files.append(audio_output)
    transcript = ""
    for audio in audio_files:
        print(f"Transcribing audio {audio}")
        transcript += soundtrack2text.transcribe_audio(audio) + "\n"
    
    # Process slide PDFs
    slide_dir = os.path.join(course_path, "Slide")
    slide_text = ""
    if os.path.exists(slide_dir):
        pdf_files = sorted(glob.glob(os.path.join(slide_dir, "*.pdf")))
        for pdf in pdf_files:
            print(f"Extracting text from slide {pdf}")
            slide_text += slide2text.extract_slides_text(pdf) + "\n"
    
    # Generate final note
    print("Generating final note")
    note = text2note.generate_note(transcript, slide_text)
    output_file = os.path.join(output_course_dir, f"{course_name}_note.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(note)
    print(f"Note saved to {output_file}")


def main():
    # Load config
    config = toml.load("config.toml")
    openai.api_key = config.get("OPENAI_API_KEY")
    
    input_dir = "Input"
    courses = [os.path.join(input_dir, d) for d in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, d))]
    for course in courses:
        process_course(course)
    

if __name__ == "__main__":
    main()
