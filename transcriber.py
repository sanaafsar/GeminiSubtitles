"""Audio transcription utility for Malay audio using Google Gemini."""

import os
import math
from typing import List, Optional

from dotenv import load_dotenv
from pydub import AudioSegment
import google.generativeai as genai

# 🔑 Load environment variables
load_dotenv()
api_key: Optional[str] = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=api_key)

# 🎯 Config
INPUT_FILE: str = "input.wav"
CHUNK_LENGTH_MS: int = 5 * 60 * 1000  # 5 minutes
OUTPUT_FILE: str = "transcript.txt"

model = genai.GenerativeModel("gemini-1.5-pro")


def split_audio(file_path: str, chunk_length_ms: int) -> List[str]:
    """Split a WAV audio file into smaller chunk files.

    Args:
        file_path: Path to the WAV input file.
        chunk_length_ms: Chunk duration in milliseconds.

    Returns:
        A list of chunk file paths created from the input audio.
    """
    audio = AudioSegment.from_wav(file_path)
    chunks: List[str] = []

    total_length = len(audio)
    num_chunks = math.ceil(total_length / chunk_length_ms)

    for i in range(num_chunks):
        start = i * chunk_length_ms
        end = min((i + 1) * chunk_length_ms, total_length)

        chunk = audio[start:end]
        chunk_name = f"chunk_{i}.wav"
        chunk.export(chunk_name, format="wav")
        chunks.append(chunk_name)

    return chunks


def transcribe_chunk(file_path: str, prev_context: str = "") -> str:
    """Transcribe a single audio chunk using Google Gemini.

    Args:
        file_path: Path to the audio chunk file.
        prev_context: Optional preceding transcript text for continuity.

    Returns:
        The transcribed text output.
    """
    uploaded_file = genai.upload_file(file_path)

    prompt = f"""
    Transcribe this audio into Malay (Malaysia).

    Rules:
    - Use natural conversational Malay
    - Remove filler words (uh, um)
    - Keep punctuation clean
    - Maintain continuity with previous context

    Previous context:
    {prev_context}

    Output: plain text
    """

    response = model.generate_content([prompt, uploaded_file])
    return response.text.strip()


def main() -> None:
    """Run the transcription pipeline and save the full transcript."""
    chunks = split_audio(INPUT_FILE, CHUNK_LENGTH_MS)

    full_transcript: List[str] = []
    prev_context: str = ""

    for chunk in chunks:
        print(f"Processing {chunk}...")

        text = transcribe_chunk(chunk, prev_context)
        full_transcript.append(text)

        # keep last ~200 chars for continuity
        prev_context = text[-200:]

    final_text = "\n".join(full_transcript)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(final_text)

    print("✅ Transcription complete!")


if __name__ == "__main__":
    main()