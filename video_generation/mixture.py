from pydub import AudioSegment

def combine_voice_and_music(
    voice_path: str,
    music_path: str,
    output_path: str = "combined_output.mp3",
    voice_volume: float = 0.0,
    music_volume: float = 0.0
):
    """
    Combines a voice track and background music into one audio file with volume adjustments.

    Parameters:
        voice_path (str): Path to the voice audio file.
        music_path (str): Path to the background music audio file.
        output_path (str): Path to save the combined output file.
        voice_volume (float): dB adjustment for voice audio (e.g., +6 to boost).
        music_volume (float): dB adjustment for music audio (e.g., -6 to lower).
    """

    # Load both audio files
    voice = AudioSegment.from_file(voice_path)
    music = AudioSegment.from_file(music_path)

    # Adjust volumes
    voice += voice_volume
    music += music_volume

    # Trim or loop music to match voice length
    music = music[:len(voice)]  # or use music * n for repeating

    # Overlay background music under voice
    combined = voice.overlay(music)

    # Export the result
    combined.export(output_path, format="mp3")
    print(f"Combined audio exported to {output_path}")


# combine_voice_and_music(
#     voice_path="generated_b61fe3fa-4f11-4687-b236-2116e4c19340.mp3",
#     music_path="Beau Walker - Dreaming.mp3",
#     output_path="final_mix.mp3",
#     voice_volume=6,
#     music_volume=-6
# )