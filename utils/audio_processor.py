# import yt_dlp
# from pydub import AudioSegment
# import os
# from youtube_transcript_api import YouTubeTranscriptApi
# import re

# DOWNLOAD_DIR = 'downloades'
# os.makedirs(DOWNLOAD_DIR,exist_ok = True)

# def download_youtube_audio(url :str) ->str:
#     output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
#     ydl_opts = {
#         "format": "bestaudio/best",
#         "outtmpl": output_path,
#         "postprocessors": [
#             {
#                 "key": "FFmpegExtractAudio",
#                 "preferredcodec": "wav",
#                 "preferredquality": "192",
#             }
#         ],
#         "quiet": True,
#     } 
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         info = ydl.extract_info(url, download=True)
#         filename = ydl.prepare_filename(info).replace(".webm", ".wav").replace(".m4a", ".wav")
#     return filename


# def convert_to_wav(input_path : str) -> str:
#     """Convert any audio/video file to WAV format using pydub."""
#     output_path = os.path.splitext(input_path)[0] + "_converted.wav"
#     audio = AudioSegment.from_file(input_path)
#     audio = audio.set_channels(1).set_frame_rate(16000)
#     audio.export(output_path, format = "wav")
#     return output_path


# def chunk_audio(wav_path : str, chunk_minutes : int = 10) -> list:
#     audio = AudioSegment.from_wav(wav_path)
#     chunk_ms = chunk_minutes * 60 * 1000

#     chunks = []

#     for i, start in enumerate(range(0, len(audio),chunk_ms)):
#         chunk = audio[start : start + chunk_ms]
#         chunk_path = f"{wav_path}_chunk_{i}.wav"
#         chunk.export(chunk_path, format = "wav")

#         chunks.append(chunk_path)

#     return chunks


# def process_input(source_url):
#     ydl_opts = {
#         'format': 'm4a/bestaudio/best',
#         'outtmpl': '%(id)s.%(ext)s',
#         'quiet': True,
#         'no_warnings': True,
#         # Rotate extraction clients to bypass 403 Forbidden on cloud servers
#         'extractor_args': {
#             'youtube': {
#                 'player_client': ['android', 'web']
#             }
#         }
#     }
    
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         info = ydl.extract_info(source_url, download=True)
#         filename = ydl.prepare_filename(info)
#         return filename


# def get_youtube_transcript(video_url):
#     # Extract YouTube Video ID from URL
#     video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", video_url)
#     if not video_id_match:
#         raise ValueError("Invalid YouTube URL")
    
#     video_id = video_id_match.group(1)
    
#     # Fetch transcript captions directly
#     transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'hi'])
    
#     # Combine text items into a single transcript string
#     full_transcript = " ".join([item['text'] for item in transcript_list])
#     return full_transcript


# import os
# import re
# import yt_dlp
# from pydub import AudioSegment
# from youtube_transcript_api import YouTubeTranscriptApi

# DOWNLOAD_DIR = 'downloades'
# os.makedirs(DOWNLOAD_DIR, exist_ok=True)


# def download_youtube_audio(url: str) -> str:
#     """Download audio from YouTube bypassing 403 Forbidden errors."""
#     output_template = os.path.join(DOWNLOAD_DIR, "%(id)s.%(ext)s")
    
#     ydl_opts = {
#         "format": "m4a/bestaudio/best",
#         "outtmpl": output_template,
#         "postprocessors": [
#             {
#                 "key": "FFmpegExtractAudio",
#                 "preferredcodec": "wav",
#                 "preferredquality": "192",
#             }
#         ],
#         "quiet": True,
#         "no_warnings": True,
#         # Bypassing YouTube 403 Forbidden on Cloud Providers
#         "extractor_args": {
#             "youtube": {
#                 "player_client": ["android", "ios", "web"],
#                 "player_skip": ["webpage", "configs"],
#             }
#         },
#         "http_headers": {
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#             "Accept-Language": "en-us,en;q=0.5",
#         },
#     }

#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         info = ydl.extract_info(url, download=True)
#         filename = ydl.prepare_filename(info)
#         # Ensure path points to the converted WAV file
#         wav_path = os.path.splitext(filename)[0] + ".wav"
#         return wav_path


# def convert_to_wav(input_path: str) -> str:
#     """Convert any audio/video file to 16kHz mono WAV format using pydub."""
#     output_path = os.path.splitext(input_path)[0] + "_converted.wav"
#     audio = AudioSegment.from_file(input_path)
#     audio = audio.set_channels(1).set_frame_rate(16000)
#     audio.export(output_path, format="wav")
#     return output_path


# def chunk_audio(wav_path: str, chunk_minutes: int = 10) -> list:
#     """Split WAV audio into chunks for Whisper processing."""
#     audio = AudioSegment.from_wav(wav_path)
#     chunk_ms = chunk_minutes * 60 * 1000

#     chunks = []
#     base_name = os.path.splitext(wav_path)[0]

#     for i, start in enumerate(range(0, len(audio), chunk_ms)):
#         chunk = audio[start : start + chunk_ms]
#         chunk_path = f"{base_name}_chunk_{i}.wav"
#         chunk.export(chunk_path, format="wav")
#         chunks.append(chunk_path)

#     return chunks


# def process_input(source: str) -> list:
#     """
#     Main processing function. Accepts YouTube URL or local file path
#     and returns a list of chunked WAV files ready for transcription.
#     """
#     # Check if input is a YouTube URL
#     if "youtube.com" in source or "youtu.be" in source:
#         raw_audio_path = download_youtube_audio(source)
#     else:
#         raw_audio_path = source

#     # Convert to standard format & chunk
#     converted_wav = convert_to_wav(raw_audio_path)
#     audio_chunks = chunk_audio(converted_wav, chunk_minutes=10)
    
#     return audio_chunks


# def get_youtube_transcript(video_url: str) -> str:
#     """Extract YouTube Video ID and fetch transcript directly via API."""
#     video_id_match = re.search(r"(?:v=|\/|embed\/|shorts\/)([0-9A-Za-z_-]{11})", video_url)
#     if not video_id_match:
#         raise ValueError("Invalid YouTube URL")
    
#     video_id = video_id_match.group(1)
    
#     # Fetch transcript captions directly
#     transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'hi'])
    
#     # Combine text items into a single transcript string
#     full_transcript = " ".join([item['text'] for item in transcript_list])
#     return full_transcript

import os
import re
import yt_dlp
from pydub import AudioSegment
from youtube_transcript_api import YouTubeTranscriptApi

DOWNLOAD_DIR = 'downloades'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def extract_video_id(url: str) -> str:
    """Extract YouTube Video ID from various URL formats."""
    video_id_match = re.search(r"(?:v=|\/|embed\/|shorts\/)([0-9A-Za-z_-]{11})", url)
    if video_id_match:
        return video_id_match.group(1)
    raise ValueError("Invalid YouTube URL")


def get_youtube_transcript(video_url: str) -> str:
    """Fetch captions directly from YouTube API without downloading media files."""
    video_id = extract_video_id(video_url)
    
    # Instantiate API client
    api = YouTubeTranscriptApi()
    
    # Try fetching transcript in English, Hindi, or auto-generated languages
    transcript_list = api.get_transcript(video_id, languages=['en', 'hi', 'en-US', 'en-GB'])
    
    # Join text into a single string
    full_transcript = " ".join([item['text'] for item in transcript_list])
    return full_transcript


def download_youtube_audio(url: str) -> str:
    """Fallback audio downloader using Web/Android player spoofing."""
    output_template = os.path.join(DOWNLOAD_DIR, "%(id)s.%(ext)s")
    
    ydl_opts = {
        "format": "m4a/bestaudio/best",
        "outtmpl": output_template,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
        "no_warnings": True,
        "extractor_args": {
            "youtube": {
                "player_client": ["android", "ios", "web_creator"],
                "player_skip": ["webpage", "configs"],
            }
        },
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        },
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        return os.path.splitext(filename)[0] + ".wav"


def convert_to_wav(input_path: str) -> str:
    """Convert local audio/video file to 16kHz mono WAV."""
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio.export(output_path, format="wav")
    return output_path


def chunk_audio(wav_path: str, chunk_minutes: int = 10) -> list:
    """Split WAV audio into chunks for Whisper processing."""
    audio = AudioSegment.from_wav(wav_path)
    chunk_ms = chunk_minutes * 60 * 1000
    chunks = []
    base_name = os.path.splitext(wav_path)[0]

    for i, start in enumerate(range(0, len(audio), chunk_ms)):
        chunk = audio[start : start + chunk_ms]
        chunk_path = f"{base_name}_chunk_{i}.wav"
        chunk.export(chunk_path, format="wav")
        chunks.append(chunk_path)

    return chunks


def process_input(source: str):
    """
    Main entry point.
    - If YouTube URL: Attempts direct transcript API download (bypasses 403 entirely).
      If direct transcript fails, falls back to audio download.
    - If Local File Path: Converts and chunks audio for Whisper.
    """
    if "youtube.com" in source or "youtu.be" in source:
        try:
            # 1. Direct transcript fetch (Fast & immune to 403)
            return get_youtube_transcript(source)
        except Exception as e:
            print(f"Direct transcript API unavailable, attempting audio download fallback... Error: {e}")
            # 2. Fallback to audio download
            raw_audio_path = download_youtube_audio(source)
            converted_wav = convert_to_wav(raw_audio_path)
            return chunk_audio(converted_wav, chunk_minutes=10)
    else:
        # Local file processing
        converted_wav = convert_to_wav(source)
        return chunk_audio(converted_wav, chunk_minutes=10)