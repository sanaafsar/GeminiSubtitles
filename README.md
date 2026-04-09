# GeminiSubtitles

A simple Python audio transcription tool that splits a WAV file into chunks and uses Google Gemini to transcribe spoken Malay (Malaysia) into clean text.

## Features

- Splits long WAV audio files into 5-minute chunks
- Uploads each chunk to the Google Gemini API
- Transcribes audio into conversational Malay
- Writes the full transcription to `transcript.txt`

## Requirements

- Python 3.10+ recommended
- `requirements.txt` contains the required packages:
  - `google-generativeai`
  - `pydub`
  - `python-dotenv`

## Setup

1. Create a virtual environment:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with your Google API key:

   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```

4. Place your WAV file as `input.wav` in the project folder.

## Usage

Run the transcription script:

```bash
python transcriber.py
```

The output will be saved as `transcript.txt`.

## Notes

- The current configuration uses `gemini-1.5-pro`.
- The transcription prompt is set to remove filler words and keep punctuation clean.
- If your input audio is longer than 5 minutes, the script automatically splits it into chunks.

## Customization

- Change `INPUT_FILE`, `OUTPUT_FILE`, or `CHUNK_LENGTH_MS` in `transcriber.py`.
- Adjust the transcription prompt inside `transcribe_chunk()` if you want a different output style.

## License

This project is provided as-is without warranty.
