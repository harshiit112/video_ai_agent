import yt_dlp
from pydub import AudioSegment
import os
from youtube_transcript_api import YouTubeTranscriptApi
import re

DOWNLOAD_DIR = 'downloades'
os.makedirs(DOWNLOAD_DIR,exist_ok = True)

def download_youtube_audio(url :str) ->str:
    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
    } 
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).replace(".webm", ".wav").replace(".m4a", ".wav")
    return filename


def convert_to_wav(input_path : str) -> str:
    """Convert any audio/video file to WAV format using pydub."""
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio.export(output_path, format = "wav")
    return output_path


def chunk_audio(wav_path : str, chunk_minutes : int = 10) -> list:
    audio = AudioSegment.from_wav(wav_path)
    chunk_ms = chunk_minutes * 60 * 1000

    chunks = []

    for i, start in enumerate(range(0, len(audio),chunk_ms)):
        chunk = audio[start : start + chunk_ms]
        chunk_path = f"{wav_path}_chunk_{i}.wav"
        chunk.export(chunk_path, format = "wav")

        chunks.append(chunk_path)

    return chunks


def process_input(source_url):
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': '%(id)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        # Rotate extraction clients to bypass 403 Forbidden on cloud servers
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web']
            }
        }
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(source_url, download=True)
        filename = ydl.prepare_filename(info)
        return filename


def get_youtube_transcript(video_url):
    # Extract YouTube Video ID from URL
    video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", video_url)
    if not video_id_match:
        raise ValueError("Invalid YouTube URL")
    
    video_id = video_id_match.group(1)
    
    # Fetch transcript captions directly
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'hi'])
    
    # Combine text items into a single transcript string
    full_transcript = " ".join([item['text'] for item in transcript_list])
    return full_transcript