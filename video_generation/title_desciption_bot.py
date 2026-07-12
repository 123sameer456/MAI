from openai import OpenAI
import openai

from system_messages  import sp_title_description_bot


client = openai.OpenAI(api_key="OPENAI_API_KEY")  # Replace with your actual OpenAI API key


def title_description_bot(short_clips_text , sp_title_description_bot):

   
    prompt = f"""
    {sp_title_description_bot} . 
    
    HERE is the list of short clips texts :
    {short_clips_text}
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt}]
                        )
        
        # Extract the raw response content
    response_content = response.choices[0].message.content
        
        # Debugging: Print raw response for inspection
        
    return response_content



# from openai import OpenAI
# import openai

# from system_messages  import sp_title_description_bot

# client = openai.OpenAI(api_key="OPENAI_API_KEY")  # Replace with your actual OpenAI API key


# short_clips = """[
#         {'from_Script': 1, 'start': 17.31999969482422, 'end': 26.399999618530273, 'text': " that the thing? Or is the thing that's stopping you, you?"}, 
#         {'from_Script': 2, 'start': 97.55999755859375, 'end': 104.31999969482422, 'text': " They're lies. And how do you stop the lies? You stop the lies with the truth."},
#         {'from_Script': 3, 'start': 141.83999633789062, 'end': 148.0, 'text': ' This is your shot. This is your moment. This is your time. This is your place. This is your opportunity.'}, 
#         {'from_Script': 4, 'start': 159.0, 'end': 165.55999755859375, 'text': ' it happen. If you wanted to have it, rise and grind. You still got work to do. Stay on that'}
#     ]"""

# sp_title_description_bot = """ you are an expert social media content writer to make a Title, Description/Caption for a social media posts. you will make two variations, 
# one for ( Tweeter/X, Linkedin and Thread ) considered as Serious Platforms and other for ( youtube,instagram, tiktok, facebook) considered as Entertainment platforms of each video's text that you received.
#  you will receive a short/clip/reel video's transcribe text list having multple dictionaries of scripts you have to work on each script.
#  do not provide extra content just like (  ``` , python ) . completely focus on list of dictionaries.  it should be return type python list.
 
#  During making title, description/caption please keep it kind following rules.

# 1. Tone & Style:
# Keep content fun, natural, and engaging, with emojis to match content tone (except for tweeeter/X, linkedin & Thread)..
# Use a friendly, approachable tone while keeping the content professional and actionable.
# Make content skimmable and to the point—people scroll fast!
# Avoid sounding robotic or overly scripted; keep it conversational.
# 2. Emojis:
# Emojis should be integrated naturally to enhance emotion, clarity, and structure.
# Use bold, eye-catching emojis to emphasize key points (🔥✅⚠️🤯).
# Exception: Do not use emojis for tweeter/X , Linkedin & Threads (but keep engagement high with strong wording).
# 3. Strong Call-to-Actions (CTAs):
# Each post should include a clear CTA that encourages interaction, like:
# “Drop a 🚀 in the comments if you’re ready to grow!”
# “Tag a friend who needs to see this! 👇”
# CTAs should feel authentic, not forced or salesy.
# Do not create CTA’s that requires someone to leave the platform or link to another video/post
# 4. Hashtag Strategy:
# Generate 9 strategic hashtags per post using this framework:
#  1️⃣ Post-Specific Tags (3) – Directly related to the video’s core topic.
#  2️⃣ Niche-Specific Tags (3) – Broader but still within the industry.
#  3️⃣ Broad Tags (3) – Highly searchable, viral-style tags.
# 5. Optimize for Each Platform's Format:
# Keep content short, punchy, and engaging (especially for IG, TikTok & Shorts).
# Avoid dense blocks of text—use spacing, emojis, and formatting for readability.
# Ensure the first line is always a strong hook to grab attention immediately.

#  Platform info:
# - Tweeter/X, Linkedin and Thread  considered as serious platforms.
# - youtube,instagram, tiktok, facebook considered as entertainment platforms.




# INPUT: you will get the python list of short clip Scripts .
# OUTPUT:  A Python list  containing  dictionaries with <
# serious-platform-title: 
# serious-platform-caption:
# entertainment-platform-title:
# entertainment-platform-caption:
# >

# IMPORTANT : do not provide extra content just like ( ``` , python) . completely return  list of dictionaries. it should be return type python list.
# IMPORTANT : DO NOT CHANGE THE ACTUAL CONTENT/SCRIPT/SCENTENCE, RETURN ACTUAL, AS IT SAME.
# """

# def title_description_bot(short_clips_text , sp_title_description_bot):

   
#     prompt = f"""
#     {sp_title_description_bot} . 
    
#     HERE is the list of short clips texts :
#     {short_clips_text}
#     """
    
#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[{"role": "system", "content": prompt}]
#                         )
        
#         # Extract the raw response content
#     response_content = response.choices[0].message.content
        
#         # Debugging: Print raw response for inspection
        
#     return response_content

# print(type(title_description_bot(short_clips , sp_title_description_bot)))
# print(title_description_bot(short_clips , sp_title_description_bot))