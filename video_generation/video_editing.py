

# ------------------------------- fade in and fade out ----------------------

# from moviepy.editor import VideoFileClip, concatenate_videoclips

# clip = VideoFileClip("Two AI agents on a phone call realize they’re both AI shorts.mp4")

# # Split clip at timestamp where you want the fade
# start = clip.subclip(0, 5).fadein(3) # First 5 seconds
# middle = clip.subclip(5, clip.duration).fadeout(2)   # Apply fade in/out in 5s–10s

# final = concatenate_videoclips([start, middle]) 
# final.write_videofile("output_fade.mp4")


# ------------------------------  silence detection and apply fade in and fade out


# from moviepy.editor import VideoFileClip, concatenate_videoclips
# from pydub import AudioSegment, silence
# import os

# def process_video_with_silence_fades(video_path, output_path, silence_len=3000, silence_thresh=-40, fade_duration=1):
#     # 1. Load video and extract audio
#     clip = VideoFileClip(video_path)
#     audio_path = "temp_audio.wav"
#     clip.audio.write_audiofile(audio_path, verbose=False, logger=None)

#     # 2. Load audio with pydub
#     audio = AudioSegment.from_wav(audio_path)

#     # 3. Detect silence (returns list of (start_ms, end_ms))
#     silence_ranges = silence.detect_silence(audio, min_silence_len=silence_len, silence_thresh=silence_thresh)
#     silence_ranges = [(start/1000.0, end/1000.0) for start, end in silence_ranges]

#     if not silence_ranges:
#         print("No silence longer than threshold found.")
#         clip.write_videofile(output_path)
#         return

#     # 4. Split and apply fades
#     final_clips = []
#     last_end = 0

#     for start_silence, end_silence in silence_ranges:
#         silence_center = (start_silence + end_silence) / 2
#         fade_clip_start = max(silence_center - 2.5, 0)
#         fade_clip_end = min(silence_center + 2.5, clip.duration)

#         # Add non-silent section before
#         if last_end < fade_clip_start:
#             final_clips.append(clip.subclip(last_end, fade_clip_start))

#         # Apply fade to the 5s segment
#         faded_clip = clip.subclip(fade_clip_start, fade_clip_end) \
#                          .fadein(fade_duration) \
#                          .fadeout(fade_duration)
#         final_clips.append(faded_clip)
#         last_end = fade_clip_end

#     # Add the remaining clip after last fade
#     if last_end < clip.duration:
#         final_clips.append(clip.subclip(last_end, clip.duration))

#     # 5. Concatenate and export
#     final = concatenate_videoclips(final_clips)
#     final.write_videofile(output_path)

#     # 6. Clean up
#     os.remove(audio_path)

# process_video_with_silence_fades(
#     video_path="Two AI agents on a phone call realize they’re both AI shorts.mp4",
#     output_path="output_silence.mp4",
#     silence_len=2000,     # minimum 3 seconds silence
#     silence_thresh=-40,   # volume threshold in dBFS
#     fade_duration=2       # 1 sec fade in/out
# )


