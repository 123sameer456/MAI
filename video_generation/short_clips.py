# #   it will take a orignal video, start and end time then make a short clip ( mp4)

# import os
# import random
# from moviepy.video.io.VideoFileClip import VideoFileClip
# def create_clip(video_path, start_time, end_time, cleanup_existing=False):
#     """
#     Creates a single clip from the specified start and end times of the input video.
#     Optionally removes old clips first to prevent folder size growth.
    
#     Args:
#         video_path (str): Path to the input video file.
#         start_time (float): Start time of the clip in seconds.
#         end_time (float): End time of the clip in seconds.
#         cleanup_existing (bool): Whether to clean up existing files in the folder.
    
#     Returns:
#         str: Path to the created clip if successful, or None if an error occurs.
#     """
#     # Define the output directory for clips
#     output_dir = "static/clips"
#     os.makedirs(output_dir, exist_ok=True)  # Ensure the output directory exists
    
#     # Clean up old video files from the folder if requested
#     if cleanup_existing:
#         for file in os.listdir(output_dir):
#             if file.endswith(('.mp4', '.avi', '.mov', '.mkv')):
#                 file_path = os.path.join(output_dir, file)
#                 try:
#                     os.remove(file_path)
#                 except Exception as e:
#                     print(f"Error removing file {file}: {e}")
    
#     try:
#         # Load the video with audio explicitly enabled
#         video = VideoFileClip(video_path, audio=True)
#         video_duration = video.duration
        
#         # Check if audio is present in the video
#         if video.audio is None:
#             print("Warning: Source video doesn't have an audio track!")
#         else:
#             print("Source video has audio track")
        
#         # Validate the start and end times
#         if start_time < 0 or end_time > video_duration or start_time >= end_time:
#             print("Invalid start or end time. Please ensure 0 <= start_time < end_time <= video_duration.")
#             return None
        
#         # Generate the clip name
#         clip_name = f"clip_from_{format_time(start_time)}_to_{format_time(end_time)}.mp4"
#         clip_path = os.path.join(output_dir, clip_name)
        
#         # Create the subclip and save it with explicit audio settings
#         subclip = video.subclip(start_time, end_time)
        
#         # Write the video file with explicit audio settings
#         subclip.write_videofile(
#             clip_path, 
#             codec='libx264', 
#             audio_codec='aac',
#             temp_audiofile="temp-audio.m4a",
#             remove_temp=True,
#             verbose=True,  # Set to True to see more output for debugging
#             logger=None
#         )
        
#         # Clean up
#         video.close()
#         print(f"Successfully created clip with audio at: {clip_path}")
#         return clip_path
#     except Exception as e:
#         print(f"Error creating clip: {e}")
#         return None

# def format_time(seconds):
#     """
#     Formats time in seconds into HHMMSS format for naming clips.
    
#     Args:
#         seconds (float): Time in seconds.
    
#     Returns:
#         str: Formatted time string in HHMMSS format.
#     """
#     hours = int(seconds // 3600)
#     minutes = int((seconds % 3600) // 60)
#     seconds = int(seconds % 60)
#     return f"{hours:02d}{minutes:02d}{seconds:02d}"
# def create_all_clips(video_path, script_de):
#     created_clips = []

#     if not script_de:
#         print("Error: The script details are empty or None.")
#         return created_clips
    
#     clips_dir = "static/clips"
#     os.makedirs(clips_dir, exist_ok=True)

#     print("Cleaning up old clips...")
#     for file in os.listdir(clips_dir):
#         if file.endswith(('.mp4', '.avi', '.mov', '.mkv')):
#             clip_path = os.path.join(clips_dir, file)
#             try:
#                 os.remove(clip_path)  # Fixed variable name
#                 print(f"Removed old clip: {file}")
#             except Exception as e:
#                 print(f"Error removing file {file}: {e}")

#     for segment in script_de:
#         try:
#             start_time = segment.get('start-time')
#             end_time = segment.get('end-time')

#             if start_time is None or end_time is None:
#                 print(f"Skipping segment due to missing start-time or end-time: {segment}")
#                 continue

#             clip_path = create_clip(video_path, start_time, end_time, cleanup_existing=False)

#             if clip_path:
#                 print(f"Clip successfully created at: {clip_path}")
#                 # Only append the filename, not the full path
#                 created_clips.append(os.path.basename(clip_path))
#             else:
#                 print(f"Failed to create clip for segment: {segment}")
#         except Exception as e:
#             print(f"Error processing segment {segment}: {e}")

#     return created_clips
    
# # print("done: " , create_clip("v.mp4" , 10.0 , 30.0))


# =======================================================


#   it will take a orignal video, start and end time then make a short clip ( mp4) with fade effects

import os
import random
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import concatenate_videoclips

def create_clip(video_path, start_time, end_time, cleanup_existing=False, fadein_duration=3, fadeout_duration=2):
    """
    Creates a single clip from the specified start and end times of the input video with fade effects.
    Optionally removes old clips first to prevent folder size growth.
    
    Args:
        video_path (str): Path to the input video file.
        start_time (float): Start time of the clip in seconds.
        end_time (float): End time of the clip in seconds.
        cleanup_existing (bool): Whether to clean up existing files in the folder.
        fadein_duration (float): Duration of fade-in effect in seconds (default: 3).
        fadeout_duration (float): Duration of fade-out effect in seconds (default: 2).
    
    Returns:
        str: Path to the created clip if successful, or None if an error occurs.
    """
    # Define the output directory for clips
    output_dir = "static/clips"
    os.makedirs(output_dir, exist_ok=True)  # Ensure the output directory exists
    
    # Clean up old video files from the folder if requested
    if cleanup_existing:
        for file in os.listdir(output_dir):
            if file.endswith(('.mp4', '.avi', '.mov', '.mkv')):
                file_path = os.path.join(output_dir, file)
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Error removing file {file}: {e}")
    
    try:
        # Load the video with audio explicitly enabled
        video = VideoFileClip(video_path, audio=True)
        video_duration = video.duration
        
        # Check if audio is present in the video
        if video.audio is None:
            print("Warning: Source video doesn't have an audio track!")
        else:
            print("Source video has audio track")
        
        # Validate the start and end times
        if start_time < 0 or end_time > video_duration or start_time >= end_time:
            print("Invalid start or end time. Please ensure 0 <= start_time < end_time <= video_duration.")
            return None
        
        # Create the subclip
        subclip = video.subclip(start_time, end_time)
        clip_duration = subclip.duration
        
        # Check if the clip is long enough for the fade effects
        total_fade_duration = fadein_duration + fadeout_duration
        if clip_duration <= total_fade_duration:
            print(f"Warning: Clip duration ({clip_duration}s) is too short for fade effects ({total_fade_duration}s total).")
            print("Applying fade effects to the entire clip duration.")
            # Adjust fade durations proportionally
            fadein_duration = min(fadein_duration, clip_duration / 2)
            fadeout_duration = min(fadeout_duration, clip_duration / 2)
        
        # Apply fade effects
        if clip_duration > fadein_duration + fadeout_duration:
            # Split the clip into three parts: fade-in, middle, fade-out
            fade_in_part = subclip.subclip(0, fadein_duration).fadein(fadein_duration)
            middle_part = subclip.subclip(fadein_duration, clip_duration - fadeout_duration)
            fade_out_part = subclip.subclip(clip_duration - fadeout_duration, clip_duration).fadeout(fadeout_duration)
            
            # Concatenate all parts
            final_clip = concatenate_videoclips([fade_in_part, middle_part, fade_out_part])
            
        else:
            # For very short clips, apply both fade effects to the entire clip
            final_clip = subclip.fadein(fadein_duration).fadeout(fadeout_duration)
        
        # Generate the clip name
        clip_name = f"clip_from_{format_time(start_time)}_to_{format_time(end_time)}_fade.mp4"
        clip_path = os.path.join(output_dir, clip_name)
        
        # Write the video file with explicit audio settings
        final_clip.write_videofile(
            clip_path, 
            codec='libx264', 
            audio_codec='aac',
            temp_audiofile="temp-audio.m4a",
            remove_temp=True,
            verbose=True,  # Set to True to see more output for debugging
            logger=None
        )
        
        # Clean up
        video.close()
        final_clip.close()
        print(f"Successfully created clip with fade effects at: {clip_path}")
        return clip_path
        
    except Exception as e:
        print(f"Error creating clip: {e}")
        return None

def format_time(seconds):
    """
    Formats time in seconds into HHMMSS format for naming clips.
    
    Args:
        seconds (float): Time in seconds.
    
    Returns:
        str: Formatted time string in HHMMSS format.
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02d}{minutes:02d}{seconds:02d}"

def create_all_clips(video_path, script_de, fadein_duration=3, fadeout_duration=2):
    """
    Creates multiple clips with fade effects from a video based on script details.
    
    Args:
        video_path (str): Path to the input video file.
        script_de (list): List of dictionaries containing start-time and end-time for each clip.
        fadein_duration (float): Duration of fade-in effect in seconds (default: 3).
        fadeout_duration (float): Duration of fade-out effect in seconds (default: 2).
    
    Returns:
        list: List of created clip filenames.
    """
    created_clips = []

    if not script_de:
        print("Error: The script details are empty or None.")
        return created_clips
    
    clips_dir = "static/clips"
    os.makedirs(clips_dir, exist_ok=True)

    print("Cleaning up old clips...")
    for file in os.listdir(clips_dir):
        if file.endswith(('.mp4', '.avi', '.mov', '.mkv')):
            clip_path = os.path.join(clips_dir, file)
            try:
                os.remove(clip_path)
                print(f"Removed old clip: {file}")
            except Exception as e:
                print(f"Error removing file {file}: {e}")

    for segment in script_de:
        try:
            start_time = segment.get('start-time')
            end_time = segment.get('end-time')

            if start_time is None or end_time is None:
                print(f"Skipping segment due to missing start-time or end-time: {segment}")
                continue

            # Create clip with fade effects
            clip_path = create_clip(
                video_path, 
                start_time, 
                end_time, 
                cleanup_existing=False,
                fadein_duration=fadein_duration,
                fadeout_duration=fadeout_duration
            )

            if clip_path:
                print(f"Clip with fade effects successfully created at: {clip_path}")
                # Only append the filename, not the full path
                created_clips.append(os.path.basename(clip_path))
            else:
                print(f"Failed to create clip for segment: {segment}")
        except Exception as e:
            print(f"Error processing segment {segment}: {e}")

    return created_clips

# Example usage:
# print("done: ", create_clip("Two AI agents on a phone call realize they’re both AI shorts.mp4", 10.0, 29.0, fadein_duration=3, fadeout_duration=2))