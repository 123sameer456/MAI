from flask import Flask, render_template, request, jsonify, Response
import json
import time
import re
from openai import OpenAI
import openai

app = Flask(__name__)

# Initialize OpenAI client
client = openai.OpenAI(api_key="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")

sm_blog_writing = """You are an expert SEO content writer. When given a topic, generate a complete blog post optimized for search engines.

Use a clear structure with HTML tags: <h1> for the main title, <h2> for main sections, <h3> for subsections, and <p> for paragraphs.

Identify and target the main keyword from the topic provided. Maintain an optimal keyword density (around 1–2%) without keyword stuffing.

Ensure the content is 100% unique, relevant, and engaging for human readers.

Include an SEO-friendly meta title (60 characters max) and meta description (160 characters max) at the top.

Write naturally, but strategically place the main keyword in the title, first paragraph, subheadings, and conclusion.

Use secondary keywords related to the topic for better ranking.

Ensure headings and content fully align with the topic and search intent."""

def title_description_bot(topic_name, sm_blog_writing=sm_blog_writing):
    prompt = f"""
    {sm_blog_writing} . 
    
    HERE is the topic name :
    {topic_name}
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt}],
        stream=True
    )
    
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content

# Store gallery items in memory (in production, use a database)
gallery = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    topic = data.get('topic', '')
    
    if not topic:
        return jsonify({'error': 'Topic is required'}), 400
    
    def generate_content():
        try:
            full_content = ""
            for chunk in title_description_bot(topic):
                full_content += chunk
                yield f"data: {json.dumps({'chunk': chunk, 'status': 'generating'})}\n\n"
            
            # Send completion signal
            yield f"data: {json.dumps({'chunk': '', 'status': 'complete', 'full_content': full_content})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e), 'status': 'error'})}\n\n"
    
    return Response(generate_content(), mimetype='text/plain')

@app.route('/regenerate', methods=['POST'])
def regenerate():
    data = request.json
    new_topic = data.get('topic', '')
    previous_content = data.get('previous_content', '')
    
    # Combine new topic with previous content for regeneration
    combined_input = f"{new_topic}\n\nPrevious content to improve upon:\n{previous_content}"
    
    def generate_content():
        try:
            full_content = ""
            for chunk in title_description_bot(combined_input):
                full_content += chunk
                yield f"data: {json.dumps({'chunk': chunk, 'status': 'generating'})}\n\n"
            
            # Send completion signal
            yield f"data: {json.dumps({'chunk': '', 'status': 'complete', 'full_content': full_content})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e), 'status': 'error'})}\n\n"
    
    return Response(generate_content(), mimetype='text/plain')

@app.route('/save_to_gallery', methods=['POST'])
def save_to_gallery():
    data = request.json
    content = data.get('content', '')
    topic = data.get('topic', '')
    
    if content:
        # Extract title from content for gallery display
        title_match = re.search(r'<h1>(.*?)</h1>', content)
        title = title_match.group(1) if title_match else topic
        
        gallery_item = {
            'id': len(gallery) + 1,
            'title': title,
            'topic': topic,
            'content': content,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        gallery.append(gallery_item)
        return jsonify({'success': True, 'message': 'Saved to gallery!'})
    
    return jsonify({'error': 'No content to save'}), 400

@app.route('/gallery')
def get_gallery():
    return jsonify(gallery)

if __name__ == '__main__':
    app.run(debug=True)