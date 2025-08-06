from moviepy import VideoFileClip
from moviepy.audio.fx import audiofadein, audiofadeout, audioloop, audionormalize, multiplyvolume

clip = VideoFileClip("one.mp4")

# 1️⃣ Fade In
fadein_clip = clip.with_audio(audiofadein(clip.audio, duration=3))
fadein_clip.write_videofile("audio_fadein.mp4", fps=24, codec="libx264")

# 2️⃣ Fade Out
fadeout_clip = clip.with_audio(audiofadeout(clip.audio, duration=3))
fadeout_clip.write_videofile("audio_fadeout.mp4", fps=24, codec="libx264")

# 3️⃣ Loop audio
loop_clip = clip.with_audio(audioloop(clip.audio, duration=15))
loop_clip.write_videofile("audio_loop.mp4", fps=24, codec="libx264")

# 4️⃣ Normalize
normalize_clip = clip.with_audio(audionormalize(clip.audio))
normalize_clip.write_videofile("audio_normalize.mp4", fps=24, codec="libx264")

# 5️⃣ Change volume
volume_clip = clip.with_audio(multiplyvolume(clip.audio, factor=2.0))
volume_clip.write_videofile("volume_boost.mp4", fps=24, codec="libx264")
