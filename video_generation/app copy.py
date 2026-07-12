from flask import Flask, render_template, request, redirect, url_for
import os
import ast

from clip_info import script_details
from video_text_semgment import extract_video_text_segment
from short_clips import create_all_clips
from title_desciption_bot import title_description_bot
from hooks_bot import hooks_bots, extract_segments_times_from_script, process_hooks_videos
from system_messages import sp_generate_clips_content, sp_title_description_bot, sp_for_hooks ,save_caption_data_to_json , convert_to_json
import jsonify

from system_messages import sp_generate_clips_content  , sp_title_description_bot , sp_for_hooks
from subtitles import create_clip_with_word_subtitles



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '.'

from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from elevenlabs.client import ElevenLabs
from elevenlabs import save
import os
import uuid
import json
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/voices'

# Create folder if not exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ElevenLabs client
client = ElevenLabs(api_key="YOUR_ELEVENLABS_API_KEY")  # Replace with your actual API key


import os
from flask import render_template, request
from werkzeug.utils import secure_filename
import uuid
from mixture import combine_voice_and_music

import glob

# combine_voice_and_music(
#     voice_path="<voice path, it would be the audio that is in between markers>",
#     music_path="<that is music, select by the dropdown ( with checkbox) w>",
#     output_path="final_mix.mp3",
#     voice_volume=6,
#     music_volume=-6
# )

from flask import request, jsonify, send_from_directory
import os
import uuid
from pydub import AudioSegment
import glob

# Add these routes to your Flask application

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
        music_volume = int(data.get('music_volume', -6))
        
        # Validate input
        if not voice_filename or not background_sounds:
            return jsonify({"success": False, "error": "Missing voice or background sound"})
        
        # Strip any URL parts from the filename
        voice_filename = voice_filename.split('/')[-1]
        print(f"Processing voice file: {voice_filename}")
        
        # Create combined directory if it doesn't exist
        combined_dir = os.path.join(app.static_folder, 'combined')
        os.makedirs(combined_dir, exist_ok=True)
        
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
    return render_template(
        "hooks.html",
        result_audio=result_audio,
        result_audio_filename=result_audio_filename,
        background_sounds=background_sounds
    )




@app.route("/preview/", methods=["GET", "POST"])
def preview():
    
    with open("static/title_caption_data.json", "r", encoding="utf-8") as f:
        raw = f.read()
        caption_json = convert_to_json(raw)
        # caption_data = json.dumps(caption_json)
        caption_data = caption_json

    return render_template("preview.html" ,caption_data=caption_data)

# Add this route to your Flask application


# Add this route to your Flask application
# Add this route to your Flask application

import os
from flask import jsonify, url_for

@app.route('/api/videos/<video_type>')
def get_videos(video_type):
    """
    Fetch video files from the specified folders
    video_type: 'hooks' or 'clips'
    """
    base_path = '/home/master/applications/pffdwzzskr/public_html/smcg-data/static'
    
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

    
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video = request.files["video"]
        # Get message box inputs
        msg_clip_content = request.form.get("clip_content_msg")
        msg_title_description = request.form.get("title_description_msg")
        msg_hooks = request.form.get("hooks_msg")

        sm_generate_clips_content = sp_generate_clips_content 

        # Fallback to defaults if empty
        sm_title_description_bot =  sp_title_description_bot 
        sm_for_hooks =  sp_for_hooks 

        if video:
            video_path = os.path.join(app.config['UPLOAD_FOLDER'], "v.mp4")
            video.save(video_path)

            video_text, segments_var = extract_video_text_segment(video_path)  # video ka pora text or segments bhi nikal kr dega with time stamp
            script_details_var = script_details(segments_var, sm_generate_clips_content)   # isy dekhna ha error dera ha script_details_var :  JSON Decode Error: Expecting property name enclosed in double quotes: line 1 column 3 (char 2)
            print("script_details_var : " ,script_details_var )
            scripts_for_title_caption_generation_var = [{f'script_{i+1}': item['script']} for i, item in enumerate(script_details_var)]


            # Title & Description Output
            title_description__bot_var = title_description_bot(
            scripts_for_title_caption_generation_var, sm_title_description_bot)
            # print("title_description_bot: ", title_description__bot_var)
            print(f"Type of title_caption_data: {type(title_description__bot_var)}")
            print(f"Content of title_caption_data: {title_description__bot_var}")  # title caption generate krta ha
            save_caption_data_to_json(title_description__bot_var, filename='static/title_caption_data.json')
        # Convert string to Python list/dict if it's a string
            if isinstance(title_description__bot_var, str):
                try:
                    title_description__bot_var = ast.literal_eval(title_description__bot_var)
                except (ValueError, SyntaxError) as e:
                    print(f"Error parsing title_description_bot output: {e}")
                    title_description__bot_var = []

            # Created Clips Output
            created_clips = create_all_clips(video_path, script_details_var)
            print ("creat clips: " , created_clips)   # clips bnata ha
            # Hook Clips Output
            script_times = [(item['start-time'], item['end-time']) for item in script_details_var]
            print("script times: ", script_times)  # scripts times for short clips
            script_sentences_with_times = [
                extract_segments_times_from_script(segments_var, start, end)
                for start, end in script_times
            ]
            print("script_sentences_with_times: " , script_sentences_with_times)

            hooks_bots_var = hooks_bots(script_sentences_with_times, sm_for_hooks)
            hooks_bots_var = ast.literal_eval(hooks_bots_var)
            hook_clips = process_hooks_videos(hooks_bots_var, video_path)
            # print("hooks  clips: " , hook_clips)  # hook clips bnanta hai

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

            for idx, (start_time, end_time) in enumerate(script_times):
                print(f"Processing clip {idx + 1}: {start_time} to {end_time}")
                clip_path = create_clip_with_word_subtitles(
                    video_path=video_path,
                    start_time=start_time,
                    end_time=end_time
                )
                
                # subtitle_clip_paths.append(clip_path)
                relative_clip_path = clip_path.split("static/")[-1]
                subtitle_clip_paths.append(relative_clip_path)



            print("Generated clips:")
            for path in subtitle_clip_paths:
                print(path)

            with open("static/title_caption_data.json", "r", encoding="utf-8") as f:
                raw = f.read()
                caption_json = convert_to_json(raw)
                # caption_data = json.dumps(caption_json)
                caption_data = caption_json

            return render_template(
                "preview.html" , title_caption_data=title_description__bot_var,
    created_clips=created_clips,
    hook_clips=hook_clips,
    subtitle_clips=subtitle_clip_paths,
    caption_data=caption_data

               

            )
    return render_template("sixth.html")

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0' ,  port=8000 , debug=False)


# ps aux | grep gunicorn
# kill PID_NUMBER
# kill -9 PID_NUMBER
