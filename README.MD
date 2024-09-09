# Record & Video Summarization
- This project demonstrates a workflow for converting audio recordings or videos into text using 
  OpenAI's Whisper model and then summarizing the transcribed text using a fine-tuned GPT-2 model.

![Recod-Summarize](media/recordsummarize.png)
![Video-Summarize](media/VideoSummarization.png)

## Project 
![Project](media/project.png)
## Overview

1. **Speech-to-Text (S2T)**: Convert spoken language from audio recordings or video files into text using OpenAI's Whisper model.
2. **Text Summarization**: Generate concise summaries of the transcribed text using a fine-tuned GPT-2 model.

## Requirements

- Python 3.7 or higher
- Transformers library
- PyTorch
- FASTAPI
- jinja2
- Additional dependencies (as listed in `requirements.txt`)

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/Shymaa2611/SpeechSummarization_API.git
   cd SpeechSummarization_API
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

## Usage 
 http://127.0.0.1:8000/

