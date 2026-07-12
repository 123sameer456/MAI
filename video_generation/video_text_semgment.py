

from openai import OpenAI
import moviepy.editor as mp
import openai
import os


client = openai.OpenAI(api_key="OPENAI_API_KEY")  # Replace with your actual OpenAI API key





#  this function will take a video and transcribe it in a sentences (segments)
def extract_video_text_segment(video_path):
    """Extracts audio from video and transcribes it using OpenAI Whisper with sentence-level timestamps."""
    try:
        # Extract audio from video
        video = mp.VideoFileClip(video_path)
        audio_path = "static/uploads/temp_audio.mp3"
        video.audio.write_audiofile(audio_path, verbose=False, logger=None)
        
        # Initialize OpenAI client
        # client = openai.OpenAI(api_key="OPENAI_API_KEY")  # Replace with your actual OpenAI API key
        # Open the audio file and transcribe with sentence-level timestamps
        with open(audio_path, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="verbose_json",
                language="en",
                timestamp_granularities=["segment"]
            )
        
        # Remove the temporary audio file
        os.remove(audio_path)
        
        # Extract transcribed text and segment-level timestamps
        text = response.text
        segments = [{"start": seg.start, "end": seg.end, "text": seg.text} for seg in response.segments]
        
        return text, segments

    except Exception as e:
        print(f"Error extracting captions: {e}")
        return "", []

# print(extract_video_text_segment("v.mp4"))