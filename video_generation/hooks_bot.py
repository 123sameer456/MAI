

from system_messages import sp_for_hooks
from openai import OpenAI
import openai

import os
from moviepy.editor import VideoFileClip


client = openai.OpenAI(api_key="OPENAI_API_KEY")  # Replace with your actual OpenAI API key


def extract_segments_times_from_script(segments, start_time, end_time):
    extracted_segments = []
    temp_text = []
    
    for segment in segments:
        if segment['start'] >= start_time and segment['end'] <= end_time:
            temp_text.append({
                'start': segment['start'],
                'end': segment['end'],
                'text': segment['text']
            })
    
    if temp_text:
        extracted_segments.append({
            'content' : 'script',
            'sentences': temp_text
        })
       
    
    return extracted_segments


def hooks_bots(scripts, sp_for_hooks):
   

    prompt = f"""
    {sp_for_hooks} . 
    
    HERE is the here is the scripts for the short videos :
    {scripts}
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt}]
                        )
        
        # Extract the raw response content
    response_content = response.choices[0].message.content
        
        # Debugging: Print raw response for inspection
        
    return response_content




def hooks_format_time(seconds):
    """
    Formats seconds into a string representation (MM_SS).
    
    Args:
        seconds (float): Time in seconds.
    
    Returns:
        str: Formatted time string.
    """
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    return f"{minutes:02d}_{remaining_seconds:02d}"
def process_video_hooks_creation(hooks_data, source_video_path):
    hooks_dir = "static/hooks"
    os.makedirs(hooks_dir, exist_ok=True)
    
    # Clean up old video files from the folder
    for file in os.listdir(hooks_dir):
        if file.endswith(('.mp4', '.avi', '.mov', '.mkv')):
            file_path = os.path.join(hooks_dir, file)
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error removing file {file}: {e}")
    
    created_clips = []
    
    # Process each hook entry
    for i, hook in enumerate(hooks_data):
        print("===========:")
        print("i:" ,  i)
        print("" , hook)
        start_time = hook['start']
        end_time = hook['end']
        
        # Create a descriptive filename - Using simple formatting instead of missing function
        hook_number = hook.get('from_Script', i+1)
        hook_filename = f"hook_{hook_number}_{start_time:.2f}_to_{end_time:.2f}.mp4"
        hook_path = os.path.join(hooks_dir, hook_filename)
        
        try:
            # Load the video
            video = VideoFileClip(source_video_path)
            
            # Create the subclip (keeping the audio)
            subclip = video.subclip(start_time, end_time)
            
            # Write the video file with audio
            subclip.write_videofile(hook_path, codec='libx264')
            
            # Clean up
            video.close()
            subclip.close()
            
            # Return just the filename, not the full path
            created_clips.append(os.path.basename(hook_path))
            
        except Exception as e:
            print(f"Error creating hook clip {hook_number}: {e}")
    
    return created_clips



    
# a= [{'from_Script': 1, 'start': 17.31999969482422, 'end': 26.399999618530273, 'text': " that the thing? Or is the thing that's stopping you, you?"}, {'from_Script': 2, 'start': 97.55999755859375, 'end': 104.31999969482422, 'text': " They're lies. And how do you stop the lies? You stop the lies with the truth."}, {'from_Script': 3, 'start': 141.83999633789062, 'end': 148.0, 'text': ' is your shot. This is your moment. This is your time. This is your place. This is your opportunity.'}]
# print(process_hooks_videos(a , "v.mp4"))
# Example usage
# if __name__ == "__main__":
#     The hooks data from your variable
    # hooks_bots_var = [
    #     {'from_Script': 1, 'start': 17.31999969482422, 'end': 26.399999618530273, 'text': " that the thing? Or is the thing that's stopping you, you?"}, 
    #     {'from_Script': 2, 'start': 97.55999755859375, 'end': 104.31999969482422, 'text': " They're lies. And how do you stop the lies? You stop the lies with the truth."},
    #     {'from_Script': 3, 'start': 141.83999633789062, 'end': 148.0, 'text': ' This is your shot. This is your moment. This is your time. This is your place. This is your opportunity.'}, 
    #     {'from_Script': 4, 'start': 159.0, 'end': 165.55999755859375, 'text': ' it happen. If you wanted to have it, rise and grind. You still got work to do. Stay on that'}
    # ]
    
#     # Path to your source video file
#     source_video = "v.mp4"
    
#     # Process all hooks and create clips
#     created_clips = process_hooks_videos(hooks_bots_var, source_video)
    
#     print(f"\nCreated {len(created_clips)} hook video clips (no audio):")
#     for clip in created_clips:
#         print(f"- {clip}")


# -------------------

import random
import os
import shutil
import urllib.request
import moviepy.editor as mp
from moviepy.video.fx import fadein, fadeout
import subprocess

def process_video_hooks_creation(input_path_or_url, output_path="final_output.mp4", num_clips=2, clip_duration=3, speed_factor=1.5):
    # --- DOWNLOAD VIDEO IF URL ---
    if input_path_or_url.startswith("http://") or input_path_or_url.startswith("https://"):
        tmp_video = "temp_downloaded.mp4"
        urllib.request.urlretrieve(input_path_or_url, tmp_video)
        input_path = tmp_video
    else:
        input_path = input_path_or_url

    # --- CLEAN OUTPUT FOLDER IF FIRST CALL ---
    if not hasattr(process_video_hooks_creation, "_cleaned_hooks_folder"):
        hooks_folder = "static/hooks"
        if os.path.exists(hooks_folder):
            shutil.rmtree(hooks_folder)
        os.makedirs(hooks_folder, exist_ok=True)
        process_video_hooks_creation._cleaned_hooks_folder = True

    video = mp.VideoFileClip(input_path)
    total_duration = video.duration

    segment_length = 300  # 5 minutes in seconds
    num_segments = int(total_duration // segment_length) + (1 if total_duration % segment_length > 0 else 0)

    for i in range(num_segments):
        start_time = i * segment_length
        end_time = min((i + 1) * segment_length, total_duration)
        segment = video.subclip(start_time, end_time)

        segment_duration = segment.duration
        total_needed = num_clips * clip_duration
        if segment_duration < total_needed + (num_clips - 1):
            print(f"Segment {i+1} is too short for the requested number of clips.")
            continue

        used = []
        clips = []
        while len(clips) < num_clips:
            start = random.uniform(0, segment_duration - clip_duration)
            if all(abs(start - u) > clip_duration for u in used):
                used.append(start)
                subclip = segment.subclip(start, start + clip_duration)
                faded = subclip.fx(fadein.fadein, 0.5).fx(fadeout.fadeout, 0.5)
                clips.append(faded)

        final_clip = mp.concatenate_videoclips(clips)
        temp_video = f"temp_segment_{i+1}.mp4"
        final_clip.write_videofile(temp_video, codec="libx264", audio_codec="aac", verbose=False, logger=None)

        # Speed audio/video
        audio_filters = []
        temp_speed = speed_factor
        while temp_speed > 2.0:
            audio_filters.append("atempo=2.0")
            temp_speed /= 2
        audio_filters.append(f"atempo={temp_speed:.2f}")
        atempo_filter = ",".join(audio_filters)

        output_segment_path = f"static/hooks/segment_{i+1}.mp4"
        cmd = [
            "ffmpeg", "-y",
            "-i", temp_video,
            "-filter_complex",
            f"[0:v]setpts=PTS/{speed_factor}[v];[0:a]{atempo_filter}[a]",
            "-map", "[v]", "-map", "[a]",
            "-preset", "fast",
            output_segment_path
        ]
        subprocess.run(cmd)

        # Cleanup
        os.remove(temp_video)

    video.reader.close()
    if video.audio:
        video.audio.reader.close_proc()

    if 'tmp_video' in locals():
        os.remove(tmp_video)

    print("✅ All processed segments saved in: static/hooks/")


# process_video_hooks_creation("v.mp4", num_clips=4, clip_duration=5, speed_factor=1.25)


# -----------------

from elevenlabs.client import ElevenLabs
from elevenlabs import save
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
import os

def hooks_format_time(seconds):
    """Format time in seconds to a string format for filenames."""
    return f"{int(seconds):03d}s"

def process_hooks_with_voice(hooks_data, source_video_path, voice="Charlotte", api_key=None):
    """
    Process hook entries by creating video clips and adding AI-generated voice.
    
    Args:
        hooks_data (list): List of dictionaries containing hook data with start/end times and text.
        source_video_path (str): Path to the source video file.
        voice (str): Name of the ElevenLabs voice to use.
        api_key (str): ElevenLabs API key.
        
    Returns:
        list: List of paths to created final video clips.
    """
    # Initialize ElevenLabs client
    if not api_key:
        print("Warning: No API key provided. Please provide your ElevenLabs API key.")
        return []
    
    client = ElevenLabs(api_key=api_key)
    
    # Create output directories
    hooks_dir = "hooks_videos"
    audio_dir = "eleven_voices"
    final_dir = "hooks_with_voice"
    
    for directory in [hooks_dir, audio_dir, final_dir]:
        os.makedirs(directory, exist_ok=True)
    
    final_clips = []
    
    # Process each hook entry
    for i, hook in enumerate(hooks_data):
        hook_number = hook.get('from_Script', i+1)
        start_time = hook['start']
        end_time = hook['end']
        text = hook.get('text', '').strip()
        
        if not text:
            print(f"Skipping hook {hook_number}: No text provided")
            continue
            
        print(f"\nProcessing hook {hook_number}: {start_time:.2f}s to {end_time:.2f}s")
        print(f"Text: {text}")
        
        # Create filenames for intermediate and final files
        video_filename = f"hook_{hook_number}_{hooks_format_time(start_time)}_to_{hooks_format_time(end_time)}.mp4"
        audio_filename = f"hook_{hook_number}_voice.mp3"
        final_filename = f"hook_{hook_number}_with_voice.mp4"
        
        video_path = os.path.join(hooks_dir, video_filename)
        audio_path = os.path.join(audio_dir, audio_filename)
        final_path = os.path.join(final_dir, final_filename)
        
        try:
            # Step 1: Create the video subclip without audio
            print(f"Creating video subclip...")
            video = VideoFileClip(source_video_path)
            subclip = video.subclip(start_time, end_time)
            subclip = subclip.without_audio()  # Remove original audio
            
            # Write the intermediate video file
            subclip.write_videofile(video_path, codec='libx264')
            print(f"Created video clip: {video_path}")
            
            # Step 2: Generate voice audio
            print(f"Generating ElevenLabs voice audio...")
            audio = client.generate(
                text=text,
                voice=voice
            )
            save(audio, audio_path)
            print(f"Saved voice audio to: {audio_path}")
            
            # Step 3: Combine video with voice audio
            print(f"Combining video with voice audio...")
            voice_audio = AudioFileClip(audio_path)
            
            # Create final video with voice audio
            final_clip = subclip.set_audio(voice_audio)
            final_clip.write_videofile(final_path, codec='libx264')
            print(f"Created final clip with voice: {final_path}")
            
            # Add to results list
            final_clips.append(final_path)
            
            # Clean up
            video.close()
            subclip.close()
            final_clip.close()
            voice_audio.close()
            
        except Exception as e:
            print(f"Error processing hook {hook_number}: {e}")
    
    return final_clips

# if __name__ == "__main__":
#     # Sample hooks data
#     hooks_data = [
#         {'from_Script': 1, 'start': 17.31999969482422, 'end': 26.399999618530273, 'text': "that the thing? Or is the thing that's stopping you, you?"}, 
#         {'from_Script': 2, 'start': 97.55999755859375, 'end': 104.31999969482422, 'text': "They're lies. And how do you stop the lies? You stop the lies with the truth."},
#         {'from_Script': 3, 'start': 141.83999633789062, 'end': 148.0, 'text': 'This is your shot. This is your moment. This is your time. This is your place. This is your opportunity.'}, 
#         {'from_Script': 4, 'start': 159.0, 'end': 165.55999755859375, 'text': 'it happen. If you wanted to have it, rise and grind. You still got work to do. Stay on that'}
#     ]
    
#     # Path to your source video file
#     source_video = "v.mp4"
    
#     # Your ElevenLabs API key
#     api_key = "YOUR_ELEVENLABS_API_KEY"  # Replace with your actual API key
    
#     # Process all hooks and create clips with voice
#     final_clips = process_hooks_with_voice(hooks_data, source_video, voice="Charlotte", api_key=api_key)
    
#     print(f"\nCreated {len(final_clips)} hook video clips with voice:")
#     for clip in final_clips:
#         print(f"- {clip}")