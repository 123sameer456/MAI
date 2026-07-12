from moviepy.editor import VideoFileClip, CompositeVideoClip
import os
import openai
import moviepy.editor as mp
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from moviepy.video.fx.all import resize
import os
import shutil


client = openai.OpenAI(api_key="OPENAI_API_KEY")  # Replace with your actual OpenAI API key


def get_word_level_timestamps(video_path):
    """
    Extracts audio from video and transcribes it using OpenAI Whisper with word-level timestamps.
    """
    try:
        # Extract audio from video
        video = mp.VideoFileClip(video_path)
        audio_path = "static/uploads/temp_audio.mp3"
        os.makedirs("static/uploads", exist_ok=True)
        video.audio.write_audiofile(audio_path, verbose=False, logger=None)
        
        # Open the audio file and transcribe with word-level timestamps
        with open(audio_path, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="verbose_json",
                language="en",
                timestamp_granularities=["word"]
            )
        
        # Remove the temporary audio file
        os.remove(audio_path)
        video.close()
        
        # Extract word-level timestamps
        words = []
        if hasattr(response, 'words') and response.words:
            words = [{"start": word.start, "end": word.end, "word": word.word} for word in response.words]
        
        return response.text, words

    except Exception as e:
        print(f"Error extracting word-level timestamps: {e}")
        return "", []

# def create_subtitle_image(text, highlighted_word_index, width, height, fontsize=40):
#     """
#     Creates a subtitle image with highlighted word using PIL (no ImageMagick needed).
#     """
#     try:
#         # Create image with transparent background
#         img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
#         draw = ImageDraw.Draw(img)
        
#         # Try to use a better font, fall back to default if not available
#         try:
#             font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", fontsize)
#         except:
#             try:
#                 font = ImageFont.truetype("arial.ttf", fontsize)
#             except:
#                 font = ImageFont.load_default()
        
#         words = text.split()
        
#         # Calculate text positioning
#         total_text_width = draw.textlength(text, font=font)
#         start_x = (width - total_text_width) // 2
#         y = height - 80  # Position near bottom
        
#         current_x = start_x
        
#         # Draw each word
#         for i, word in enumerate(words):
#             word_width = draw.textlength(word + " ", font=font)
            
#             if i == highlighted_word_index:
#                 # Draw background rectangle for highlighted word
#                 padding = 5
#                 draw.rectangle([
#                     current_x - padding, 
#                     y - padding, 
#                     current_x + word_width - padding, 
#                     y + fontsize + padding
#                 ], fill=(255, 255, 0, 200))  # Yellow background
                
#                 # Draw highlighted word in black
#                 draw.text((current_x, y), word, fill=(0, 0, 0, 255), font=font)
#             else:
#                 # Draw normal word with background
#                 padding = 2
#                 draw.rectangle([
#                     current_x - padding, 
#                     y - padding, 
#                     current_x + word_width - padding, 
#                     y + fontsize + padding
#                 ], fill=(0, 0, 0, 180))  # Semi-transparent black background
                
#                 # Draw normal word in white
#                 draw.text((current_x, y), word, fill=(255, 255, 255, 255), font=font)
            
#             current_x += word_width
        
#         # Convert PIL image to numpy array for MoviePy
#         return np.array(img)
        
#     except Exception as e:
#         print(f"Error creating subtitle image: {e}")
#         return None

def create_subtitle_image(text, highlighted_word_index, width, height, fontsize=40):
    """
    Creates a subtitle image with highlighted word using PIL (no ImageMagick needed).
    """
    try:
        # Create image with transparent background
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Try to use a better font, fall back to default if not available
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", fontsize)
        except:
            try:
                font = ImageFont.truetype("arial.ttf", fontsize)
            except:
                font = ImageFont.load_default()
        
        words = text.split()
        
        # Calculate text positioning
        total_text_width = draw.textlength(text, font=font)
        start_x = (width - total_text_width) // 2
        y = height - 80  # Position near bottom
        
        current_x = start_x
        
        # Helper function to create gradient background
        def create_gradient_background(x1, y1, x2, y2):
            # Create a small image for the gradient
            grad_width = int(x2 - x1)
            grad_height = int(y2 - y1)
            
            if grad_width <= 0 or grad_height <= 0:
                return
            
            gradient_img = Image.new('RGBA', (grad_width, grad_height))
            grad_pixels = gradient_img.load()
            
            # Colors from the gradient: #667eea to #764ba2
            start_color = (102, 126, 234)  # #667eea
            end_color = (118, 75, 162)     # #764ba2
            
            # Create diagonal gradient (135 degrees)
            for i in range(grad_width):
                for j in range(grad_height):
                    # Calculate position along diagonal (135 degrees)
                    diagonal_pos = (i + j) / (grad_width + grad_height - 2)
                    diagonal_pos = max(0, min(1, diagonal_pos))
                    
                    # Interpolate colors
                    r = int(start_color[0] + (end_color[0] - start_color[0]) * diagonal_pos)
                    g = int(start_color[1] + (end_color[1] - start_color[1]) * diagonal_pos)
                    b = int(start_color[2] + (end_color[2] - start_color[2]) * diagonal_pos)
                    
                    grad_pixels[i, j] = (r, g, b, 200)  # 200 for some transparency
            
            # Paste gradient onto main image
            img.paste(gradient_img, (int(x1), int(y1)), gradient_img)
        
        # Draw each word
        for i, word in enumerate(words):
            word_width = draw.textlength(word + " ", font=font)
            
            if i == highlighted_word_index:
                # Draw gradient background for highlighted word
                padding = 5
                create_gradient_background(
                    current_x - padding, 
                    y - padding, 
                    current_x + word_width - padding, 
                    y + fontsize + padding
                )
                
                # Draw highlighted word in black
                draw.text((current_x, y), word, fill=(0, 0, 0, 255), font=font)
            else:
                # Draw normal word with background
                padding = 2
                draw.rectangle([
                    current_x - padding, 
                    y - padding, 
                    current_x + word_width - padding, 
                    y + fontsize + padding
                ], fill=(0, 0, 0, 180))  # Semi-transparent black background
                
                # Draw normal word in white
                draw.text((current_x, y), word, fill=(255, 255, 255, 255), font=font)
            
            current_x += word_width
        
        # Convert PIL image to numpy array for MoviePy
        return np.array(img)
        
    except Exception as e:
        print(f"Error creating subtitle image: {e}")
        return None

        
import os
import shutil
from moviepy.editor import VideoFileClip, CompositeVideoClip
from moviepy.video.VideoClip import ImageClip

def create_clip_with_word_subtitles(video_path, start_time, end_time, words=None, output_path=None, fontsize=40):
    """
    Creates a clip with word-level highlighted subtitles using PIL instead of ImageMagick.
    """
    try:
        # Get word timestamps if not provided
        if words is None:
            print("Getting word-level timestamps...")
            _, words = get_word_level_timestamps(video_path)
        
        # Load the original video
        video = VideoFileClip(video_path)
        
        # Create clip
        clip = video.subclip(start_time, end_time)
        clip_duration = end_time - start_time
        
        # Filter words that fall within the clip time range
        clip_words = []
        for word in words:
            if word['start'] >= start_time and word['end'] <= end_time:
                # Adjust timestamps to be relative to clip start
                clip_words.append({
                    'start': word['start'] - start_time,
                    'end': word['end'] - start_time,
                    'word': word['word'].strip()
                })
        
        if not clip_words:
            print("No words found in the specified time range")
            return None
        
        print(f"Found {len(clip_words)} words in clip")
        
        # Group words into subtitle groups
        subtitle_groups = group_words_into_sentences(clip_words, max_words_per_line=5)
        
        # Create subtitle clips using custom image generation
        subtitle_clips = []
        
        for group in subtitle_groups:
            group_words = group['words']
            group_text = ' '.join([w['word'] for w in group_words])
            
            # Create subtitle for each word in the group
            for i, word_data in enumerate(group_words):
                word_start = word_data['start']
                word_end = word_data['end']
                
                # Create subtitle image with current word highlighted
                subtitle_img = create_subtitle_image(
                    text=group_text,
                    highlighted_word_index=i,
                    width=clip.w,
                    height=clip.h,
                    fontsize=fontsize
                )
                
                if subtitle_img is not None:
                    subtitle_clip = ImageClip(subtitle_img, duration=word_end - word_start)
                    subtitle_clip = subtitle_clip.set_start(word_start).set_position(('center', 'center'))
                    subtitle_clips.append(subtitle_clip)

        # Combine video with subtitles
        if subtitle_clips:
            final_video = CompositeVideoClip([clip] + subtitle_clips)
        else:
            print("No subtitle clips created, returning original clip")
            final_video = clip

        # Generate output path if not provided
        output_dir = "static/clips_with_subtitles"
        
        
        
        if output_path is None:
            output_path = os.path.join(output_dir, f"clip_{format_time(start_time)}_to_{format_time(end_time)}_subtitled.mp4")

        # Write the final video
        final_video.write_videofile(
            output_path, 
            codec='libx264', 
            audio_codec='aac',
            temp_audiofile="temp-audio.m4a",
            remove_temp=True,
            logger=None
        )
        
        # Clean up
        video.close()
        final_video.close()
        
        print(f"Successfully created subtitled clip at: {output_path}")
        return output_path

    except Exception as e:
        print(f"Error creating clip with subtitles: {e}")
        return None

def group_words_into_sentences(words, max_words_per_line=5, max_duration=4.0):
    """
    Groups words into subtitle groups for better readability.
    """
    if not words:
        return []
    
    groups = []
    current_group = []
    current_start = words[0]['start']
    
    for word in words:
        # Start new group if we hit limits
        if (len(current_group) >= max_words_per_line or 
            (current_group and word['start'] - current_start > max_duration)):
            
            if current_group:
                groups.append({
                    'start': current_start,
                    'end': current_group[-1]['end'],
                    'words': current_group.copy()
                })
                current_group = []
                current_start = word['start']
        
        current_group.append(word)
    
    # Add the last group
    if current_group:
        groups.append({
            'start': current_start,
            'end': current_group[-1]['end'],
            'words': current_group
        })
    
    return groups


def format_time(seconds):
    """
    Formats time in seconds into HHMMSS format for naming clips.
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02d}{minutes:02d}{seconds:02d}"


# Example usage
if __name__ == "__main__":
    video_path = "Two AI agents on a phone call realize they’re both AI shorts.mp4"
    
    

    # Test word-level version
    print("\nTesting word-level subtitled clip...")
    word_clip = create_clip_with_word_subtitles(
        video_path=video_path,
        start_time=0.1199951171875,
        end_time=25.3599853515625
    )
    
    time_intervals = [
    (0.0, 25.239999771118164), 
    
    
    
]

    output_dir = "static/clips_with_subtitles"

    # 🔥 Clear the directory ONCE before the loop starts
    if os.path.exists(output_dir):
        for f in os.listdir(output_dir):
            file_path = os.path.join(output_dir, f)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")
    else:
        os.makedirs(output_dir, exist_ok=True)

    subtitle_clip_paths = []

    for idx, (start_time, end_time) in enumerate(time_intervals):
        print(f"Processing clip {idx + 1}: {start_time} to {end_time}")
        clip_path = create_clip_with_word_subtitles(
                    video_path=video_path,
                    start_time=start_time,
                    end_time=end_time
                )
        if subtitle_clip_paths:
            clip_paths.append(subtitle_clip_paths)

    print("Generated clips:")
    for path in subtitle_clip_paths:
        print(path)



