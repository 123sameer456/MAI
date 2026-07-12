from flask import Flask, render_template, request, redirect, url_for
import os
import ast

from clip_info import script_details
from video_text_semgment import extract_video_text_segment
from short_clips import create_all_clips
from title_desciption_bot import title_description_bot
from hooks_bot import hooks_bots, extract_segments_times_from_script, process_video_hooks_creation
from system_messages import sp_generate_clips_content, sp_title_description_bot, sp_for_hooks ,save_caption_data_to_json , convert_to_json
import jsonify

from subtitles import create_clip_with_word_subtitles

from moviepy.editor import VideoFileClip, AudioFileClip
from moviepy.audio.fx.all import audio_loop  # Only needed if using looping
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '.'

from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from elevenlabs.client import ElevenLabs
from elevenlabs import save
import os
import uuid
import json
import os
from flask import render_template, request
from werkzeug.utils import secure_filename
import uuid
from mixture import combine_voice_and_music
import glob
from flask import request, jsonify, send_from_directory
import os
import uuid
from pydub import AudioSegment
import glob


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/voices'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
# ElevenLabs client
client = ElevenLabs(api_key="YOUR_ELEVENLABS_API_KEY")  # Replace with your actual API key


# Add these imports at the top of your app.py
import glob
import shutil

# Add this new route for video processing
@app.route("/process_video", methods=["POST"])
def process_video():
    try:
        data = request.json
        selected_video_path = data.get('video_path')
        
        if not selected_video_path:
            return jsonify({"success": False, "error": "No video selected"})
        
        # Get the latest combined audio file
        combined_dir = os.path.join(app.static_folder, 'combined')
        if not os.path.exists(combined_dir):
            return jsonify({"success": False, "error": "No combined audio found"})
        
        # Find the most recent combined audio file
        audio_files = glob.glob(os.path.join(combined_dir, "combined_*.mp3"))
        if not audio_files:
            return jsonify({"success": False, "error": "No combined audio files found"})
        
        latest_audio = max(audio_files, key=os.path.getctime)
        
        # Create output directory for custom audio videos
        output_dir = os.path.join(app.static_folder, 'custom_audio_video')
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate output filename
        video_name = os.path.splitext(os.path.basename(selected_video_path))[0]
        output_filename = f"{video_name}_custom_audio_{uuid.uuid4()}.mp4"
        output_path = os.path.join(output_dir, output_filename)
        
        # Construct full path for the input video
        if not selected_video_path.startswith('static/'):
            input_video_path = os.path.join(app.static_folder, selected_video_path.replace('static/', ''))
        else:
            input_video_path = selected_video_path
            
        # Process the video with new audio
        try:
            result_path = replace_video_audio(
                input_video_path=input_video_path,
                output_path=output_path,
                new_audio_path=latest_audio
            )
            
            return jsonify({
                "success": True,
                "message": "Video processed successfully!",
                "output_file": os.path.basename(result_path),
                "output_path": f"static/custom_audio_video/{os.path.basename(result_path)}"
            })
            
        except Exception as e:
            return jsonify({"success": False, "error": f"Video processing failed: {str(e)}"})
            
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({"success": False, "error": str(e)})

# Updated combine_audio function with cleanup
@app.route("/combine_audio", methods=["POST"])
def combine_audio():
    try:
        data = request.json
        
        # Debug: Log incoming data
        print("Received combine request:", data)
        
        # Extract data from request
        voice_filename = data.get('voice_filename')
        background_sounds = data.get('background_sounds', [])
        start_time = float(data.get('start_time', 0))
        end_time = float(data.get('end_time', 0))
        voice_volume = int(data.get('voice_volume', 9))
        music_volume = int(data.get('music_volume', -9))
        
        # Validate input
        if not voice_filename or not background_sounds:
            return jsonify({"success": False, "error": "Missing voice or background sound"})
        
        # Strip any URL parts from the filename
        voice_filename = voice_filename.split('/')[-1]
        print(f"Processing voice file: {voice_filename}")
        
        # Create combined directory if it doesn't exist
        combined_dir = os.path.join(app.static_folder, 'combined')
        os.makedirs(combined_dir, exist_ok=True)
        
        # 🧹 Clean up old combined audio files BEFORE creating new ones
        print("Cleaning up old combined audio files...")
        for old_file in glob.glob(os.path.join(combined_dir, "combined_*.mp3")):
            try:
                os.remove(old_file)
                print(f"Removed old file: {old_file}")
            except Exception as e:
                print(f"Error removing {old_file}: {e}")
        
        # Define paths
        voice_path = os.path.join(app.static_folder, 'voices', voice_filename)
        
        # Debug: Check if voice file exists
        if not os.path.exists(voice_path):
            print(f"Voice file not found at {voice_path}")
            # Try to find the file in UPLOAD_FOLDER as fallback
            voice_path = os.path.join(app.config['UPLOAD_FOLDER'], voice_filename)
            if not os.path.exists(voice_path):
                print(f"Voice file not found in UPLOAD_FOLDER either")
                return jsonify({"success": False, "error": f"Voice file not found: {voice_filename}"})
            
        output_filename = f"combined_{uuid.uuid4()}.mp3"
        output_path = os.path.join(combined_dir, output_filename)
        
        # Process each selected background sound
        for i, sound_filename in enumerate(background_sounds):
            bg_music_path = os.path.join(app.static_folder, 'background_sound_effects', sound_filename)
            
            # Debug: Check if background file exists
            if not os.path.exists(bg_music_path):
                print(f"Background sound not found: {bg_music_path}")
                return jsonify({"success": False, "error": f"Background sound not found: {sound_filename}"})
            
            # Use our combine function
            if i == 0:
                # First background track - combine with voice
                success = combine_voice_and_music(
                    voice_path=voice_path,
                    music_path=bg_music_path,
                    output_path=output_path,
                    start_time=start_time * 1000,  # Convert to milliseconds
                    end_time=end_time * 1000,      # Convert to milliseconds
                    voice_volume=voice_volume,
                    music_volume=music_volume
                )
            else:
                # Additional background tracks - mix with existing output
                temp_output = output_path
                output_path = os.path.join(combined_dir, f"combined_{uuid.uuid4()}.mp3")
                success = mix_additional_background(
                    combined_path=temp_output,
                    music_path=bg_music_path,
                    output_path=output_path,
                    music_volume=music_volume
                )
        
        if not success:
            return jsonify({"success": False, "error": "Failed to combine audio"})
        
        print(f"Successfully combined audio to: {output_path}")
        return jsonify({
            "success": True, 
            "output_file": os.path.basename(output_path)
        })
        
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({"success": False, "error": str(e)})

# Updated replace_video_audio function with better error handling
def replace_video_audio(input_video_path, output_path=None, new_audio_path=None):
    """
    Replace a video's audio with a new audio file or remove audio if none is provided.
    
    Args:
        input_video_path (str): Path to the input video file.
        output_path (str, optional): Output video file path. Defaults to input_with_modified suffix.
        new_audio_path (str, optional): Path to new audio file. If None, audio will be removed.
    
    Returns:
        str: Path to the saved video.
    """
    if not os.path.exists(input_video_path):
        raise FileNotFoundError(f"Video file not found: {input_video_path}")

    if new_audio_path and not os.path.exists(new_audio_path):
        raise FileNotFoundError(f"Audio file not found: {new_audio_path}")

    # Generate default output path
    if output_path is None:
        base, ext = os.path.splitext(input_video_path)
        output_path = f"{base}_modified{ext}"

    try:
        video = VideoFileClip(input_video_path).without_audio()

        if new_audio_path:
            new_audio = AudioFileClip(new_audio_path)

            # 🔥 Trim or loop the audio to exactly match the video length
            if new_audio.duration >= video.duration:
                new_audio = new_audio.subclip(0, video.duration)
            else:
                # Loop audio if shorter
                from moviepy.audio.fx.all import audio_loop
                new_audio = audio_loop(new_audio, duration=video.duration)

            video = video.set_audio(new_audio)

        # Write final video
        video.write_videofile(output_path, codec="libx264", audio=new_audio_path is not None)
        
        # Clean up resources
        video.close()
        if new_audio_path:
            new_audio.close()

        return output_path
        
    except Exception as e:
        print(f"Error in replace_video_audio: {e}")
        raise e


@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(os.path.join(app.static_folder, 'combined'), filename, as_attachment=True)

def combine_voice_and_music(voice_path, music_path, output_path, start_time, end_time, voice_volume, music_volume):
    """
    Combine voice and background music with proper timing and volume adjustments
    
    Parameters:
    - voice_path: Path to the voice audio file
    - music_path: Path to the background music file
    - output_path: Path for the output mixed file
    - start_time: Start time in milliseconds for the voice clip
    - end_time: End time in milliseconds for the voice clip
    - voice_volume: Volume adjustment for voice in dB
    - music_volume: Volume adjustment for music in dB
    
    Returns:
    - True if successful, False otherwise
    """
    try:
        print(f"Processing voice from {voice_path}")
        print(f"Using background music from {music_path}")
        print(f"Markers: Start={start_time}ms, End={end_time}ms")
        
        # Load the voice audio
        voice = AudioSegment.from_file(voice_path)
        print(f"Voice duration: {len(voice)}ms")
        
        # Extract the portion between markers
        if end_time <= 0:  # If end time is not properly set
            end_time = len(voice)
        
        # Safety checks
        if start_time < 0:
            start_time = 0
        if start_time >= len(voice):
            start_time = 0
        if end_time > len(voice):
            end_time = len(voice)
        if start_time >= end_time:
            print("Warning: Start time >= end time. Using full audio.")
            start_time = 0
            end_time = len(voice)
            
        voice_clip = voice[start_time:end_time]
        print(f"Extracted voice clip duration: {len(voice_clip)}ms")
        
        # Adjust voice volume
        voice_clip = voice_clip + voice_volume  # Increase by X dB
        
        # Load and adjust background music
        background = AudioSegment.from_file(music_path)
        print(f"Background music duration: {len(background)}ms")
        
        # Adjust music volume
        background = background + music_volume  # Adjust by X dB
        
        # Loop the background music if it's shorter than the voice clip
        if len(background) < len(voice_clip):
            print(f"Background music is shorter ({len(background)}ms) than voice clip ({len(voice_clip)}ms). Looping...")
            while len(background) < len(voice_clip):
                background = background + background
        
        # Trim background to match voice clip length
        background = background[:len(voice_clip)]
        
        # Mix voice and background
        output = voice_clip.overlay(background)
        
        # Export the final mix
        print(f"Exporting to {output_path}")
        output.export(output_path, format="mp3")
        
        print("Audio combination completed successfully")
        return True
    except Exception as e:
        import traceback
        print(f"Error combining audio: {e}")
        print(traceback.format_exc())
        return False

def mix_additional_background(combined_path, music_path, output_path, music_volume):
    """
    Mix additional background track with already combined audio
    
    Parameters:
    - combined_path: Path to the already combined audio
    - music_path: Path to the additional background music
    - output_path: Path for the new output file
    - music_volume: Volume adjustment for the additional music
    
    Returns:
    - True if successful, False otherwise
    """
    try:
        # Load the combined audio
        combined = AudioSegment.from_file(combined_path)
        
        # Load and adjust additional background
        additional_bg = AudioSegment.from_file(music_path)
        additional_bg = additional_bg + music_volume
        
        # Loop if needed
        while len(additional_bg) < len(combined):
            additional_bg = additional_bg + additional_bg
        
        # Trim to match combined audio length
        additional_bg = additional_bg[:len(combined)]
        
        # Mix with lower volume
        output = combined.overlay(additional_bg)
        
        # Export
        output.export(output_path, format="mp3")
        
        return True
    except Exception as e:
        print(f"Error mixing additional background: {e}")
        return False



@app.route("/hooks/", methods=["GET", "POST"])
def hooks():
    result_audio = None
    result_audio_filename = None
    background_sounds = []

    # 🧹 Step 1: Clear all old files from the voices folder
    voices_folder = app.config['UPLOAD_FOLDER']
    for f in glob.glob(os.path.join(voices_folder, '*')):
        try:
            os.remove(f)
        except Exception as e:
            print(f"Error deleting file {f}: {e}")
    
    # 🎵 Step 2: Get list of background sounds
    bg_dir = os.path.join(app.static_folder, 'background_sound_effects')
    if os.path.exists(bg_dir):
        background_sounds = [f for f in os.listdir(bg_dir) if f.endswith('.mp3')]

    # 🧠 Step 3: Handle POST logic
    if request.method == "POST":
        action = request.form.get("action")
        selected_bg = request.form.get("background_sound")

        if action == "upload":
            file = request.files["uploaded_audio"]
            if file.filename:
                filename = secure_filename(file.filename)
                file_path = os.path.join(voices_folder, filename)
                file.save(file_path)
                result_audio = file_path
                result_audio_filename = filename

        elif action == "record":
            audio_blob = request.files["recorded_audio"]
            filename = f"recorded_{uuid.uuid4()}.webm"
            file_path = os.path.join(voices_folder, filename)
            audio_blob.save(file_path)
            result_audio = file_path
            result_audio_filename = filename

        elif action == "text_to_voice":
            text = request.form.get("text")
            voice = request.form.get("voice")
            selected_bg = request.form.get("background_sound")

            if text and voice:
                audio = client.generate(text=text.strip(), voice=voice)
                filename = f"generated_{uuid.uuid4()}.mp3"
                file_path = os.path.join(voices_folder, filename)
                save(audio, file_path)
                result_audio = file_path
                result_audio_filename = filename

    if result_audio and not result_audio_filename:
        result_audio_filename = os.path.basename(result_audio)

    print("result_audio: " , result_audio)
    print("result_audio_filename: " , result_audio_filename)
    print("background_sounds: " , background_sounds)


    # 📂 Step 4: Load videos from each folder
    clips_path = os.path.join(app.static_folder, "clips")
    clips_with_subtitles_path = os.path.join(app.static_folder, "clips_with_subtitles")
    hooks_path = os.path.join(app.static_folder, "hooks")

    clips = [f"static/clips/{f}" for f in os.listdir(clips_path) if f.endswith(('.mp4', '.webm'))]
    clips_with_subtitles = [f"static/clips_with_subtitles/{f}" for f in os.listdir(clips_with_subtitles_path) if f.endswith(('.mp4', '.webm'))]
    hooks_videos = [f"static/hooks/{f}" for f in os.listdir(hooks_path) if f.endswith(('.mp4', '.webm'))]
    return render_template(
        "hooks.html",
        result_audio=result_audio,
        result_audio_filename=result_audio_filename,
        background_sounds=background_sounds,
        clips=clips,
        clips_with_subtitles=clips_with_subtitles,
        hooks_videos=hooks_videos
    )
    # return render_template(
    #     "hooks.html",
    #     result_audio=result_audio,
    #     result_audio_filename=result_audio_filename,
    #     background_sounds=background_sounds
    # )


# ================================================================================================================================================================
# ================================================================================================================================================================
# ================================================================================================================================================================
# ================================================================================================================================================================

@app.route("/preview/", methods=["GET", "POST"])
def preview():
    
    with open("static/title_caption_data.json", "r", encoding="utf-8") as f:
        raw = f.read()
        caption_json = convert_to_json(raw)
        caption_data = caption_json

    return render_template("preview.html" ,caption_data=caption_data)


import os
from flask import jsonify, url_for

@app.route('/api/videos/<video_type>')
def get_videos(video_type):
    """
    Fetch video files from the specified folders
    video_type: 'hooks' or 'clips'
    """
    base_path = '/home/sameer/Desktop/MAI/MAI/video_generation/static'
    
    if video_type == 'hooks':
        folder_path = os.path.join(base_path, 'hooks')
        static_folder = 'hooks'
    elif video_type == 'clips':
        folder_path = os.path.join(base_path, 'clips')
        static_folder = 'clips'
    elif video_type == 'clips_with_subtitles':
        folder_path = os.path.join(base_path, 'clips_with_subtitles')
        static_folder = 'clips_with_subtitles'
    else:
        return jsonify({'error': 'Invalid video type'}), 400
    
    videos = []
    
    # Check if folder exists
    if not os.path.exists(folder_path):
        return jsonify({'videos': videos, 'message': 'Folder not found'})
    
    # Get all video files from the folder
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.webm', '.m4v']
    
    try:
        files = os.listdir(folder_path)
        video_files = [f for f in files if any(f.lower().endswith(ext) for ext in video_extensions)]
        
        for i, filename in enumerate(video_files):
            # Generate proper static URL using Flask's url_for
            try:
                video_url = url_for('static', filename=f'{static_folder}/{filename}')
            except:
                # Fallback to manual URL construction
                video_url = f'/static/{static_folder}/{filename}'
                
            videos.append({
                'id': i + 1,
                'title': os.path.splitext(filename)[0].replace('_', ' ').title(),
                'description': f"{video_type.title()} video",
                'filename': filename,
                'url': video_url
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    return jsonify({'videos': videos})




@app.route('/static/<path:filename>')
def custom_static(filename):
    """Serve static files from your custom static directory"""
    static_dir = '/home/master/applications/pffdwzzskr/public_html/smcg-data/static'
    return send_from_directory(static_dir, filename)

# app.py - Updated Flask routes
import uuid
import threading
import json
import time
import os
import ast
from flask import jsonify, request, render_template

# Global dictionary to store task progress
task_progress = {}

# Create a directory to store task data persistently
TASK_DATA_DIR = "task_data"
if not os.path.exists(TASK_DATA_DIR):
    os.makedirs(TASK_DATA_DIR)

def save_task_progress(task_id, progress_data):
    """Save task progress to file"""
    try:
        with open(os.path.join(TASK_DATA_DIR, f"{task_id}.json"), 'w') as f:
            json.dump(progress_data, f, indent=2)
        task_progress[task_id] = progress_data
        print(f"Saved task progress for {task_id}: {progress_data}")  # Debug log
    except Exception as e:
        print(f"Error saving task progress: {e}")

def load_task_progress(task_id):
    """Load task progress from file"""
    try:
        file_path = os.path.join(TASK_DATA_DIR, f"{task_id}.json")
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                progress_data = json.load(f)
                task_progress[task_id] = progress_data
                print(f"Loaded task progress for {task_id}: {progress_data}")  # Debug log
                return progress_data
    except Exception as e:
        print(f"Error loading task progress: {e}")
    return None

def update_progress(task_id, progress, step):
    """Update task progress - only allow forward progress"""
    # Get current progress to prevent going backwards
    current_data = task_progress.get(task_id, {'progress': 0})
    current_progress = current_data.get('progress', 0)
    
    # Only update if new progress is higher than current
    if progress > current_progress:
        progress_data = {
            'progress': progress,
            'step': step,
            'status': 'processing'
        }
        save_task_progress(task_id, progress_data)
        print(f"Progress updated for {task_id}: {progress}% - {step}")  # Debug log
    else:
        print(f"Progress not updated for {task_id}: {progress}% <= {current_progress}% - {step}")  # Debug log

def mark_task_completed(task_id, results):
    """Mark task as completed with final results"""
    final_results = {
        'progress': 100,
        'step': 'Complete!',
        'status': 'completed',
        'results': results
    }
    save_task_progress(task_id, final_results)
    print(f"Task {task_id} marked as completed")  # Debug log

def process_video_background(task_id, video_path, msg_clip_content, msg_title_description, msg_hooks):
    """Background video processing function with better progress tracking"""
    try:
        print(f"Starting background processing for task: {task_id}")  # Debug log
        
        # Step 1: Extract video text and segments
        update_progress(task_id, 10, 'Analyzing video content...')
        video_text, segments_var = extract_video_text_segment(video_path)
        print("video: " , video_text )
        print("segments_var: " , segments_var)
        # Step 2: Get script details
        update_progress(task_id, 25, 'Extracting key segments...')
        script_details_var = script_details(segments_var, sp_generate_clips_content)
        print("script_details_var: ", script_details_var)
        scripts_for_title_caption_generation_var = [{f'script_{i+1}': item['script']} for i, item in enumerate(script_details_var)]
        print("scripts_for_title_caption_generation_var: ", scripts_for_title_caption_generation_var)
        # Step 3: Generate titles and descriptions
        update_progress(task_id, 40, 'Generating titles and captions...')
        title_description__bot_var = title_description_bot(scripts_for_title_caption_generation_var, sp_title_description_bot )
        print("title_description__bot_var: " ,title_description__bot_var)
        print("save to file json: " , save_caption_data_to_json(title_description__bot_var, filename='static/title_caption_data.json'))
        
        if isinstance(title_description__bot_var, str):
            print("type: " , type(title_description__bot_var) )
            print("title_description_bot_var: " , title_description__bot_var)
            try:
                title_description__bot_var = convert_to_json(title_description__bot_var)
                # title_description__bot_var = ast.literal_eval(title_description__bot_var)
            except (ValueError, SyntaxError) as e:
                print(f"Error parsing title_description_bot output: {e}")
                title_description__bot_var = []
        
        # Step 4: Create clips
        update_progress(task_id, 55, 'Creating content clips...')
        created_clips = create_all_clips(video_path, script_details_var)
        
        # Step 5: Generate hooks
        update_progress(task_id, 70, 'Building hook videos...')
        script_times = [(item['start-time'], item['end-time']) for item in script_details_var]
        script_sentences_with_times = [
            extract_segments_times_from_script(segments_var, start, end)
            for start, end in script_times
        ]
        hooks_bots_var = hooks_bots(script_sentences_with_times, sp_for_hooks)
        hooks_bots_var = ast.literal_eval(hooks_bots_var)
        # hook_clips = process_hooks_videos(hooks_bots_var, video_path)
        hook_clips = process_video_hooks_creation(video_path, num_clips=4, clip_duration=5, speed_factor=1.25)
        
        # Step 6: Create subtitle clips
        update_progress(task_id, 85, 'Creating subtitled clips...')
        output_dir = "static/clips_with_subtitles"
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
        for idx, (start_time, end_time) in enumerate(script_times):
            clip_path = create_clip_with_word_subtitles(
                video_path=video_path,
                start_time=start_time,
                end_time=end_time
            )
            print("Generated clip_path:", clip_path)
            relative_clip_path = clip_path.split("static/")[-1]
            subtitle_clip_paths.append(relative_clip_path)

        # Step 7: Finalizing
        update_progress(task_id, 95, 'Finalizing your content...')
        
        # Read caption data
        with open("static/title_caption_data.json", "r", encoding="utf-8") as f:
            raw = f.read()
            caption_json = convert_to_json(raw)
            caption_data = caption_json

        # Store final results - Use the new function
        final_results = {
            'title_caption_data': title_description__bot_var,
            'created_clips': created_clips,
            'hook_clips': hook_clips,
            'subtitle_clips': subtitle_clip_paths,
            'caption_data': caption_data
        }
        
        # Mark as completed
        mark_task_completed(task_id, final_results)
        print(f"Task {task_id} completed successfully with final results" )  # Debug log
        
    except Exception as e:
        error_data = {
            'progress': 0,
            'step': f'Error: {str(e)}',
            'status': 'error',
            'error': str(e)
        }
        save_task_progress(task_id, error_data)
        print(f"Task {task_id} failed with error: {str(e)}" )  # Debug log

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        print("Form submitted")  # Debug log
        video = request.files.get("video")
        msg_clip_content = request.form.get("clip_content_msg")
        msg_title_description = request.form.get("title_description_msg")
        msg_hooks = request.form.get("hooks_msg")

        if video and video.filename: 
            # Generate unique task ID
            task_id = str(uuid.uuid4())
            print(f"Generated task ID: {task_id}")  # Debug log
            
            # Save video
            video_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{task_id}_v.mp4")
            video.save(video_path)
            print(f"Video saved to: {video_path}")  # Debug log
            
            # Initialize progress
            initial_progress = {
                'progress': 0,
                'step': 'Starting processing...',
                'status': 'processing'
            }
            save_task_progress(task_id, initial_progress)
            
            # Start background processing
            thread = threading.Thread(
                target=process_video_background,
                args=(task_id, video_path, msg_clip_content, msg_title_description, msg_hooks)
            )
            thread.daemon = True
            thread.start()
            print(f"Background thread started for task: {task_id}")  # Debug log
            
            # Return task ID to client
            return jsonify({'task_id': task_id})
        else:
            return jsonify({'error': 'No video file uploaded'}), 400
    
    return render_template("sixth.html")

@app.route("/progress/<task_id>")
def get_progress(task_id):
    """Get progress for a specific task"""
    print(f"Progress requested for task: {task_id}")  # Debug log
    
    # First check in memory
    if task_id in task_progress:
        progress_data = task_progress[task_id]
        print(f"Found task in memory: {json.dumps(progress_data, indent=2)}")  # Debug log
        return jsonify(progress_data)
    
    # Then check in file system
    progress_data = load_task_progress(task_id)
    if progress_data:
        print(f"Found task in file: {json.dumps(progress_data, indent=2)}")  # Debug log
        return jsonify(progress_data)
    
    print(f"Task not found: {task_id}")  # Debug log
    return jsonify({'error': 'Task not found'}), 404

@app.route("/results/<task_id>")
def get_results(task_id):
    """Get final results when processing is complete"""
    print(f"=== RESULTS ROUTE CALLED FOR TASK: {task_id} ===")
    
    # Check in memory first
    task_data = task_progress.get(task_id)
    print(f"Task data in memory: {task_data is not None}")
    
    # If not in memory, load from file
    if not task_data:
        print("Loading from file...")
        task_data = load_task_progress(task_id)
        print(f"Task data loaded from file: {task_data is not None}")
    
    if task_data:
        print(f"=== FULL TASK DATA ===")
        print(json.dumps(task_data, indent=2))
        print(f"=== END TASK DATA ===")
        
        status = task_data.get('status')
        progress = task_data.get('progress')
        
        print(f"Status: '{status}' (type: {type(status)})")
        print(f"Progress: {progress} (type: {type(progress)})")
        print(f"Status == 'completed': {status == 'completed'}")
        print(f"Progress == 100: {progress == 100}")
        print(f"Both conditions: {status == 'completed' and progress == 100}")
        
        if status == 'completed' and progress == 100:
            print("✅ CONDITIONS MET - RENDERING PREVIEW")
            results = task_data.get('results', {})
            
            if not results:
                print("❌ NO RESULTS DATA FOUND")
                return "Results data not available", 500
            
            print(f"Results keys: {list(results.keys())}")
            return render_template(
                "preview.html",
                title_caption_data=results.get('title_caption_data', []),
                created_clips=results.get('created_clips', []),
                hook_clips=results.get('hook_clips', []),
                subtitle_clips=results.get('subtitle_clips', []),
                caption_data=results.get('caption_data', [])
            )
        elif status == 'error':
            print("❌ TASK HAS ERROR STATUS")
            return f"Error processing video: {task_data.get('error', 'Unknown error')}", 500
        else:
            print("⏳ TASK NOT COMPLETED YET")
            return f"""
            <html>
            <head>
                <title>Processing...</title>
                <meta http-equiv="refresh" content="3;url=/results/{task_id}">
            </head>
            <body style="font-family: Arial, sans-serif; padding: 50px; text-align: center;">
                <h2>🔄 Processing still in progress...</h2>
                <div style="background: #f5f5f5; padding: 20px; border-radius: 10px; margin: 20px 0;">
                    <p><strong>Status:</strong> {status}</p>
                    <p><strong>Progress:</strong> {progress}%</p>
                    <p><strong>Current Step:</strong> {task_data.get('step', 'Unknown')}</p>
                </div>
                <p>This page will refresh automatically in 3 seconds...</p>
                <p><a href="/results/{task_id}">Click here to refresh manually</a></p>
            </body>
            </html>
            """, 202
    else:
        print("❌ TASK NOT FOUND")
        return "Task not found", 404
        

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0' ,  port=8000 , debug=False)


# ps aux | grep gunicorn
# kill PID_NUMBER
# kill -9 PID_NUMBER

