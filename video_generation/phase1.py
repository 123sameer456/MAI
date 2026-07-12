# -----------------------------------------  v2 flask code =================

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
import random
import openai
import moviepy.editor as mp
import cv2
import uuid
from werkzeug.utils import secure_filename
import requests
import time

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with your actual secret key for session management

# Set OpenAI API Key
client = openai.OpenAI(api_key="")

# Facebook configuration
FB_PAGE_ACCESS_TOKEN = "YOUR_FACEBOOK_PAGE_ACCESS_TOKEN"  # Replace with your actual Facebook Page Access Token

FB_PAGE_ID = "YOUR_FACEBOOK_PAGE_ID"  # Replace with your actual Facebook Page ID

# Configure upload folder
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max upload

# Create necessary directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('static/thumbnails', exist_ok=True)
os.makedirs('static/clips', exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_captions(video_path):
    """Extracts audio from video and transcribes it using OpenAI Whisper."""
    try:
        video = mp.VideoFileClip(video_path)
        audio_path = f"static/uploads/temp_audio_{uuid.uuid4()}.mp3"
        video.audio.write_audiofile(audio_path, verbose=False, logger=None)
        
        with open(audio_path, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="json",
                language="en"
            )
        os.remove(audio_path)
        return response.text
    except Exception as e:
        print(f"Error extracting captions: {e}")
        return ""

def generate_title(caption_text):
    """Generates a short, catchy video title."""
    if not caption_text:
        return "No title generated (Caption Missing)"
    
    prompt = f"Generate a short, catchy video title based on the transcript: {caption_text[:500]}"
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating title: {e}")
        return "No Title Generated"

def suggest_thumbnails(video_path, session_id):
    """Extracts three key frames for potential thumbnails."""
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    if frame_count < 3:
        return "Insufficient frames for thumbnails", []
    
    timestamps = [frame_count // 4, frame_count // 2, 3 * frame_count // 4]
    thumbnail_paths = []
    
    for i, ts in enumerate(timestamps):
        cap.set(cv2.CAP_PROP_POS_FRAMES, ts)
        ret, frame = cap.read()
        if ret:
            path = f"static/thumbnails/thumbnail_{session_id}_{i+1}.jpg"
            cv2.imwrite(path, frame)
            thumbnail_paths.append(path)
    
    cap.release()
    return "Suggested Thumbnails", thumbnail_paths

def generate_thumbnail_instructions(caption_text):
    """Generates a set of design instructions for thumbnails based on the transcript."""
    if not caption_text:
        return "No Thumbnail Instructions Generated (Caption Missing)"
    
    prompt = f"""
    Based on the following video transcript, suggest a thumbnail design:
    
    Transcript: {caption_text[:1000]}
    
    Instructions should include:
    - Background color
    - Text to display (Title, Call-to-Action)
    - Font style (Bold, Italic, etc.)
    - Any images/icons to include
    - Color scheme (Bright, Dark, etc.)
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating thumbnail instructions: {e}")
        return "No Thumbnail Instructions Generated"

def create_random_clips(video_path, session_id, num_clips=3, clip_duration=(20, 30)):
    """Creates a specified number of random clips with duration between min and max seconds."""
    output_dir = "static/clips"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    clip_paths = []
    
    try:
        # Load the video
        video = mp.VideoFileClip(video_path)
        video_duration = video.duration
        
        # Ensure we have enough video length for the clips
        max_start_time = video_duration - max(clip_duration)
        if max_start_time <= 0:
            print(f"Video duration ({video_duration}s) is too short for clips of {max(clip_duration)}s")
            return []
        
        # Generate random start times for clips
        used_segments = []
        for i in range(num_clips):
            attempts = 0
            clip_length = random.uniform(clip_duration[0], clip_duration[1])
            
            # Try to find a non-overlapping segment (maximum 10 attempts)
            while attempts < 10:
                start_time = random.uniform(0, max_start_time)
                end_time = start_time + clip_length
                
                # Check if this segment overlaps with any existing ones
                overlaps = False
                for segment in used_segments:
                    if (start_time <= segment[1] and end_time >= segment[0]):
                        overlaps = True
                        break
                
                if not overlaps:
                    used_segments.append((start_time, end_time))
                    break
                
                attempts += 1
            
            # Create clip name
            clip_name = f"clip_{session_id}_{i+1}_from_{format_time(start_time)}_to_{format_time(end_time)}.mp4"
            clip_path = os.path.join(output_dir, clip_name)
            
            # Create subclip and save
            subclip = video.subclip(start_time, end_time)
            subclip.write_videofile(clip_path, codec='libx264', audio_codec='aac', verbose=False, logger=None)
            clip_paths.append(clip_path)
        
        video.close()
        return clip_paths
    except Exception as e:
        print(f"Error creating clips: {e}")
        return []

def format_time(seconds):
    """Format time in seconds to HH_MM_SS format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02d}_{minutes:02d}_{seconds:02d}"

def process_video(video_path, session_id):
    """Processes the video and extracts relevant data."""
    result = {
        "video_path": video_path,
        "captions": "",
        "title": "",
        "thumbnail_info": "",
        "thumbnail_paths": [],
        "thumbnail_instructions": "",
        "clip_paths": []
    }
    
    # Extract captions
    captions = extract_captions(video_path)
    result["captions"] = captions
    
    # Generate title
    title = generate_title(captions)
    result["title"] = title
    
    # Generate thumbnails
    thumbnail_info, thumbnail_paths = suggest_thumbnails(video_path, session_id)
    result["thumbnail_info"] = thumbnail_info
    result["thumbnail_paths"] = thumbnail_paths
    
    # Generate thumbnail instructions
    thumbnail_instructions = generate_thumbnail_instructions(captions)
    result["thumbnail_instructions"] = thumbnail_instructions
    
    # Create 3 random clips of 20-30 seconds each
    clip_paths = create_random_clips(video_path, session_id, num_clips=3, clip_duration=(20, 30))
    result["clip_paths"] = clip_paths
    
    return result

def upload_facebook_video_with_thumbnail(page_access_token, page_id, video_path, title, description, thumbnail_path, delay_minutes=10):
    """
    Upload video to Facebook page with a custom thumbnail.
    
    :param page_access_token: (str) Facebook Page Access Token
    :param page_id: (str) Facebook Page ID
    :param video_path: (str) Path to video file
    :param title: (str) Video title
    :param description: (str) Video description
    :param thumbnail_path: (str) Path to thumbnail image
    :param delay_minutes: (int) Minutes to delay before posting (default: 10 minutes)
    :return: API response as JSON
    """
    scheduled_time = int(time.time()) + (delay_minutes * 60)

    # Step 1: Upload Video
    url = f"https://graph.facebook.com/v18.0/{page_id}/videos"
    data = {
        "access_token": page_access_token,
        "title": title,
        "description": description,
        "published": "false",
        "scheduled_publish_time": scheduled_time
    }
    
    try:
        files = {"source": open(video_path, "rb")}
        response = requests.post(url, data=data, files=files)
        video_response = response.json()
        
        if "id" not in video_response:
            print("Error uploading video:", video_response)
            return video_response, False

        video_id = video_response["id"]
        print(f"✅ Video Uploaded! Video ID: {video_id}")

        # Step 2: Upload Thumbnail
        thumbnail_url = f"https://graph.facebook.com/v18.0/{video_id}/thumbnails"
        thumb_files = {"source": open(thumbnail_path, "rb")}
        thumb_data = {"access_token": page_access_token}

        thumb_response = requests.post(thumbnail_url, data=thumb_data, files=thumb_files)
        print("✅ Thumbnail Uploaded:", thumb_response.json())

        return video_response, True
    except Exception as e:
        print(f"Error uploading to Facebook: {str(e)}")
        return {"error": str(e)}, False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'video' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['video']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        # Generate a unique session ID
        session_id = str(uuid.uuid4())
        
        # Save the uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{session_id}_{filename}")
        file.save(file_path)
        
        # Process the video (this will be async in production)
        return redirect(url_for('process', video_path=file_path, session_id=session_id))
    
    flash('Invalid file type. Please upload an MP4, AVI, MOV, or MKV file.')
    return redirect(request.url)

@app.route('/process')
def process():
    video_path = request.args.get('video_path')
    session_id = request.args.get('session_id')
    
    if not video_path or not os.path.exists(video_path):
        flash('Video file not found')
        return redirect(url_for('index'))
    
    # Process the video
    result = process_video(video_path, session_id)
    
    # Render results page
    return render_template('results.html', 
                          title=result["title"],
                          captions=result["captions"],
                          thumbnail_info=result["thumbnail_info"],
                          thumbnail_paths=result["thumbnail_paths"],
                          thumbnail_instructions=result["thumbnail_instructions"],
                          clip_paths=result["clip_paths"])

@app.route('/post_to_facebook', methods=['POST'])
def post_to_facebook():
    # Get form data
    video_path = request.form.get('selected_clip')
    thumbnail_path = request.form.get('selected_thumbnail')
    post_title = request.form.get('post_title')
    post_description = request.form.get('post_description')
    delay_minutes = int(request.form.get('delay_minutes', 10))
    
    # Validate data
    if not all([video_path, thumbnail_path, post_title, post_description]):
        flash('Missing required information for Facebook post')
        return redirect(url_for('index'))
    
    # Check if files exist
    if not (os.path.exists(video_path) and os.path.exists(thumbnail_path)):
        flash('Selected video or thumbnail file not found')
        return redirect(url_for('index'))
    
    # Upload to Facebook
    response, success = upload_facebook_video_with_thumbnail(
        FB_PAGE_ACCESS_TOKEN,
        FB_PAGE_ID,
        video_path,
        post_title,
        post_description,
        thumbnail_path,
        delay_minutes
    )
    
    if success:
        flash(f'Successfully scheduled post on Facebook! It will be published in {delay_minutes} minutes.')
    else:
        flash(f'Error posting to Facebook: {response.get("error", "Unknown error")}')
    
    # Redirect back to the results page with the same video path and session ID
    session_id = request.form.get('session_id')
    original_video_path = request.form.get('video_path')
    return redirect(url_for('process', video_path=original_video_path, session_id=session_id))

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0' ,  port=5000 , debug=True)








