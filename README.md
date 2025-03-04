# Course2Note

## Brief

This is a tool to help convert course playbacks and course slides into a comprehensive note or cleaned transcripts.

## Features

1. Extract soundtracks from course playbacks.
2. Convert soundtracks into text.
3. Create a comprehensive summary or clean transcript from the original text. (At times, the notes generated by language models may not seem reliable, so I use them to produce a cleaner version of the transcripts instead.)

## Usage

1. Clone the repository.

```bash
git clone git@github.com:EmptyBlueBox/Course2Note.git
cd Course2Note
```

2. Configure the API keys in the `config_private.toml` file.

Copy the `config.toml` file to `config_private.toml` and configure the API keys:

- [XunFei API](https://console.xfyun.cn/services/lfasr)
- [OpenAI ChatGPT API](https://platform.openai.com/docs/api-reference/chat)
- [DeepSeek API](https://platform.deepseek.com/api_keys)

Note: You can choose one of the LLM API keys.

Configure the `COURSE_NAME` and `STYLE` in the `config_private.toml` file.

- To generate a note, set `STYLE` to `note`.
- To generate a cleaned transcripts, set `STYLE` to `cleaner`.

1. Put your course playbacks and slides in the `Input` folder.

The project folder should have the following structure:

```bash
tree
.
├── Course
│   └── <Course Name>
│       └── Playback
│           ├── 1.mp4
│           ├── 2.mp4
│           ├── 3.mp4
│           └── 4.mp4
├── LICENSE
├── README.md
└── Workfolder
```

4. Install the dependencies.

Create a conda environment and install the python dependencies using the following command:

```bash
conda create -n course2note python=3.10
conda activate course2note
pip install -r requirements.txt
```

5. Run the script.

```bash
python main.py
```

## Tech Support

- [XunFei API](https://console.xfyun.cn/services/lfasr) (for audio transcription)
- [OpenAI ChatGPT API](https://platform.openai.com/docs/api-reference/chat) (for note generation from transcripts and slides)
- [DeepSeek API](https://platform.deepseek.com/api_keys) (for note generation from transcripts and slides)

## Reason Why I Drop the Info in Slides

1. The context length of OpenAI API is limited.
2. The info in slides is complicated and not structured.
3. The OCR results are messy, but if use copy and paste, there will be a lot of information loss.

So I drop the info in slides and only keep the info in the audio, and wish you can read the slides for better understanding.
