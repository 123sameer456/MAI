

from system_messages import sp_generate_clips_content 
from openai import OpenAI
import openai
# client
# client = openai.OpenAI(api_key="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")

client = openai.OpenAI(api_key="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")


#  this function will a video transcribe or text segements and generate scripts, start and end time for a short clips
def generate_clips_info(segments , sp_generate_clips_content):
    """
    Generates scripts for short video clips based on timestamped segments.
    
    Args:
        segments (list): List of dictionaries containing 'start', 'end', and 'text' for each segment.
    
    Returns:
        list: List of dictionaries containing scripts with start and end times.
    """
   

    prompt = f"""
    {sp_generate_clips_content} . 
    
    HERE is the transcript of a longer video :
    {segments}

    strictly follow this rule:  respond ONLY in valid JSON format like this:
[
  {{
    "script": "Sample script here...",
    "start-time": 0.0,
    "end-time": 10.0
  }},
  ...
]
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt}]
                        )
        
        # Extract the raw response content
    response_content = response.choices[0].message.content
        
        # Debugging: Print raw response for inspection
        
    return response_content



import json

def script_details(segments , sp_generate_clips_content):
    """
    Processes the scripts information by generating clips info, validating, and parsing it as JSON.
    
    Args:
        segments: Input data required to generate clips info.
    
    Returns:
        dict or str: Parsed JSON data if successful, or an error message if processing fails.
    """
    try:
        # Generate the scripts information
        scripts = generate_clips_info(segments ,sp_generate_clips_content )
        print("generate clip info fn: ", scripts)
        # Check if scripts is empty or None
        if not scripts:
            return "Error: The scripts variable is empty or None"
        
        # Attempt to parse the scripts as JSON
        try:
            scripts_details = json.loads(scripts)
            return scripts_details  # Return the parsed JSON data
        except json.JSONDecodeError as e:
            return f"JSON Decode Error: {e}"
    
    except Exception as e:
        return f"Unexpected Error: {e}"