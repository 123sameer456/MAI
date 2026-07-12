
# =========================================================================
# # Python 3.13.1
# # Flask 3.1.0
# # Werkzeug 3.1.3

#  here is my code and this file name is step1.py
from clip_info import script_details
from video_text_semgment import extract_video_text_segment
import json
import ast
from system_messages import sp_generate_clips_content  , sp_title_description_bot , sp_for_hooks


# sm_generate_clips_content = <Clip Content> if <Clip Content is not empty> else sp_generate_clips_content
# sm_title_description_bot = <Title and Description> if <Title and Description is not empty> else sp_title_description_bot
# sm_for_hooks = <Hooks> if <Hooks is not empty> else sp_for_hooks


from short_clips import create_all_clips
from title_desciption_bot import title_description_bot
from hooks_bot import hooks_bots , extract_segments_times_from_script , process_hooks_videos ,process_hooks_with_voice

video_text, segments_var = extract_video_text_segment("v.mp4")
script_details_var = script_details(segments_var , sp_generate_clips_content)
scripts_for_title_caption_generation_var = [{f'script_{i+1}': item['script']} for i, item in enumerate(script_details_var)]

title_description__bot_var = title_description_bot(scripts_for_title_caption_generation_var, sp_title_description_bot )
# I want to see the output of below print statement on flask web app:
print("title_description_bot: ", title_description__bot_var)


created_clips = create_all_clips("v.mp4", script_details_var)
# I want to see the output of below print statement on flask web app:
print("created clips: " , created_clips)


script_times = [(item['start-time'], item['end-time']) for item in script_details_var]
script_sentences_with_times = [extract_segments_times_from_script(segments_var, start, end) for start, end in script_times]

hooks_bots_var = hooks_bots(script_sentences_with_times , sp_for_hooks )
hooks_bots_var = ast.literal_eval(hooks_bots_var)
    

    # Process all hooks and create clips
created_clips = process_hooks_videos(hooks_bots_var, "v.mp4")
    
print(f"\nCreated {len(created_clips)} hook video clips:")
for clip in created_clips:
# I want to see the output of below print statement on flask web app:
    print(f"- {clip}")

# ====================================================================================

# final_clips = process_hooks_with_voice(hooks_bots_var, "v.mp4", voice="Charlotte", api_key="ELEVENLABS_API_KEY")

# # I want to see the output of below print statement:
# print(f"\nCreated {len(final_clips)} hook video clips with voice:")
# for clip in final_clips:
#     print(f"- {clip}")


# from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
# import os
# import time
# from werkzeug.utils import secure_filename
# import json

# # Import your processing modules
# from clip_info import script_details
# from video_text_semgment import extract_video_text_segment
# from short_clips import create_all_clips
# from title_desciption_bot import title_description_bot
# from hooks_bot import hooks_bots, extract_segments_times_from_script, process_hooks_videos, process_hooks_with_voice
# import ast

# app = Flask(__name__)
# app.secret_key = "your_secret_key"  # Required for flashing messages

# # Configuration
# UPLOAD_FOLDER = 'uploads'
# ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # Limit file size to 500MB

# # Ensure upload directory exists
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs('static/clips', exist_ok=True)
# os.makedirs('hooks_videos', exist_ok=True)
# os.makedirs('hooks_with_voice', exist_ok=True)
# os.makedirs('eleven_voices', exist_ok=True)

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'video' not in request.files:
#         flash('No file part')
#         return redirect(request.url)
    
#     file = request.files['video']
#     if file.filename == '':
#         flash('No selected file')
#         return redirect(request.url)
    
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(file_path)
        
#         # Store the file path in session for processing
#         return redirect(url_for('process_video', video_path=file_path))
#     else:
#         flash('File type not allowed')
#         return redirect(request.url)

# @app.route('/process/<path:video_path>')
# def process_video(video_path):
#     return render_template('process.html', video_path=video_path)

# @app.route('/start_processing', methods=['POST'])
# def start_processing():
#     video_path = request.form.get('video_path')
#     voice = request.form.get('voice', 'Charlotte')
#     api_key = request.form.get('api_key', '')
    
#     try:
#         # Extract video text segment
#         video_text, segments = extract_video_text_segment(video_path)
        
#         # Get script details
#         script_details_var = script_details(segments)
        
#         # Format scripts for title/caption generation
#         scripts_for_title_caption = [{f'script_{i+1}': item['script']} for i, item in enumerate(script_details_var)]
        
#         # Generate titles and descriptions
#         title_descriptions = title_description_bot(scripts_for_title_caption)
        
#         # Create clips
#         clips = create_all_clips(video_path, script_details_var)
        
#         # Process hooks
#         script_times = [(item['start-time'], item['end-time']) for item in script_details_var]
#         script_sentences_with_times = [extract_segments_times_from_script(segments, start, end) for start, end in script_times]
        
#         # Generate hooks
#         hooks = hooks_bots(script_sentences_with_times)
#         hooks = ast.literal_eval(hooks)
        
#         # Create hook videos
#         hook_clips = process_hooks_videos(hooks, video_path)
        
#         # Create hook videos with voice
#         final_clips = process_hooks_with_voice(hooks, video_path, voice=voice, api_key=api_key)
        
#         # Prepare results
#         results = {
#             'segments': segments,
#             'script_details': script_details_var,
#             'title_descriptions': title_descriptions,
#             'clips': clips,
#             'hooks': hooks,
#             'hook_clips': hook_clips,
#             'final_clips': final_clips
#         }
        
#         return jsonify({
#             'status': 'success',
#             'results': results
#         })
        
#     except Exception as e:
#         return jsonify({
#             'status': 'error',
#             'message': str(e)
#         })

# @app.route('/results')
# def view_results():
#     # This would be used to display results after processing
#     # You could either pass data through query parameters or use a session/database
#     return render_template('results.html')

# if __name__ == '__main__':
#     app.run(debug=True , port=5002 )