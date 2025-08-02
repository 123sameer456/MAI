from elevenlabs.client import ElevenLabs
from elevenlabs import play, save
import os

# ElevenLabs client
client = ElevenLabs(api_key="sk_ba17a4a161f1a8379a2c613267f62c166e04ada6552be809")

# Create folder for outputs if it doesn't exist
output_dir = "eleven_voices"
os.makedirs(output_dir, exist_ok=True)

# List of text items
a = [

    {'from_Script': 2, 'start': 97.56, 'end': 104.32, 'text': " They're lies. And how do you stop the lies? You stop the lies with the truth."},
   
]

# Function to generate voice for each line
def generate_voice_lines(script_data, voice="Adam"):
    for i, item in enumerate(script_data):
        text = item["text"].strip()
        if not text:
            continue  # skip if empty

        print(f"Generating audio for line {i+1}: {text}")
        audio = client.generate(
            text=text,
            voice=voice
        )

        filename = f"{output_dir}/line_{i+1}.mp3"
        save(audio, filename)
        print(f"Saved to {filename}\n")

# Call the function
# generate_voice_lines(a, voice="Grace")


