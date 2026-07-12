
from openai import OpenAI
import openai

from system_messages  import sp_title_description_bot

client = openai.OpenAI(api_key="OPENAI_API_KEY")  # Replace with your actual OpenAI API key

sm_blog_writing = """You are an expert SEO content writer. When given a topic, generate a complete blog post optimized for search engines.

Use a clear structure with HTML tags: <h1> for the main title, <h2> for main sections, <h3> for subsections, and <p> for paragraphs.

Identify and target the main keyword from the topic provided. Maintain an optimal keyword density (around 1–2%) without keyword stuffing.

Ensure the content is 100% unique, relevant, and engaging for human readers.

Include an SEO-friendly meta title (60 characters max) and meta description (160 characters max) at the top.

Write naturally, but strategically place the main keyword in the title, first paragraph, subheadings, and conclusion.

Use secondary keywords related to the topic for better ranking.

Ensure headings and content fully align with the topic and search intent."""

def title_description_bot(topic_name , sm_blog_writing= sm_blog_writing):

   
    prompt = f"""
    {sm_blog_writing} . 
    
    HERE is the topic name :
    {topic_name}
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt}]
                        )
        
        # Extract the raw response content
    response_content = response.choices[0].message.content
        
        # Debugging: Print raw response for inspection
        
    return response_content


print(title_description_bot(topic_name="Newtons laws of motion"))