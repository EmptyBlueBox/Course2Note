# Course2Note

## Brief

This is a tool to help convert course playbacks and course slides into a comprehensive note.

## Features

1. Extract soundtracks from course playbacks.
2. Convert soundtracks into text.
3. Convert course slides into structured text.
4. Merge audio and text into a comprehensive note.

## Tech Stack

- Python
- OpenAI Whisper API (for audio transcription)
- Pytesseract (for slides OCR)
- OpenAI ChatGPT API (for note generation from transcripts and slides)

## Usage

1. Clone the repository.

```bash
git clone git@github.com:EmptyBlueBox/Course2Note.git
cd Course2Note
```

2. Install the dependencies.

```bash
pip install -r requirements.txt
```

3. Put your course playbacks and slides in the `Input` folder.

The project folder should have the following structure:

```bash
tree
.
├── Input
│   └── <Course Name>
│       ├── Playback
│       │   ├── 1.mp4
│       │   ├── 2.mp4
│       │   ├── 3.mp4
│       │   └── 4.mp4
│       └── Slide
│           ├── 0.pdf
│           ├── 1.pdf
│           └── 2.pdf
├── LICENSE
├── Output
├── README.md
└── Workfolder
```

The python script will automatically go through all courses in the `Input` folder and generate the `Workfolder` and `Output` folders, so you don't need to create them manually.

The `Workfolder` is a temporary folder for storing intermediate files:

- Sound track
- Video Transcript
- Slides OCR

The `Output` folder will store the final note.

4. Configure the OpenAI API key in the `config.toml` file.

```bash
OPENAI_API_KEY = "your_openai_api_key"
```

5. Run the script.

```bash
python main.py
```
