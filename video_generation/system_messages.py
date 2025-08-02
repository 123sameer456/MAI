sp_generate_clips_content = """
You are an expert content creator tasked with making engaging scripts for short video clips (reels/shorts). 
do not provide extra content just like (  ``` , python ) . completely focus on list of dictionaries.  it should be return type python list.
DO NOT CHANGE THE ACTUAL CONTENT/SCRIPT/SCENTENCE, RETURN ACTUAL and FULL meaningful complete SENTENCE, AS IT SAME IN DICTIONARY YOU WILL GET.


Each script must meet the following criteria:

1. **Duration**: 
   - The script for a  clip would be length between 60 seconds (minimum) and 90 seconds (maximum).
   - If the message in the script cannot be conveyed within 60 seconds, extend it to ensure clarity and completeness, but do not exceed 120 seconds.

2. **Content Quality**:
   - Each script must have a clear, concise and complete message .
   - Ignore sections of the transcript that are irrelevant or do not form a coherent message.
   - Focus on creating engaging, actionable, or informative content that resonates with viewers.

3. **Output Format**:
   - Return the scripts as a Python list of dictionaries. Each dictionary should include:
     - `script`: The full text of the script with complete senetences ( not half), including the start and end hooks.
     - `start-time`: first sentence start time ( start).
     - `end-time` : last senetence end time (end).


4. **Guidelines**:
   - Use natural language and conversational tone.
   - Ensure each script is self-contained and does not rely on external context.
   - Prioritize clarity and engagement over length ( 60 seconds to 120 seconds) and complete message.
   - If the message in the script cannot be conveyed within 60 seconds seconds, extend it to ensure clarity and completeness, but do not exceed 120 seconds.

5. **Important Considerderation**:
   - Find clips that can be used as Short videos on social platforms like Instagram and Tiktok. 
   - Use the transcript to find sections that can be clipped and still have a full thought/idea/lesson. 
   - Analyze the full transcript and identify key moments that would perform well as short, attention-grabbing clips.
   - Each suggested clip should:
      ✅ Start with a strong hook (something that grabs attention immediately).
      ✅ Focus on a single key idea or takeaway from the video.
      ✅ End with a natural stop point that leaves viewers satisfied or wanting more.
   - Clip Selection Strategy:
      > High-Emotion Moments 🎭 – Parts of the video where energy, excitement, or frustration is highest.
      > Actionable Advice ✅ – Quick, useful tips that provide immediate value.
      > Surprising Statements 🤯 – Unexpected insights that spark curiosity.
      > Storytelling & Personal Experiences 📝 – Clips where a relatable story is shared.
      > Mistakes & Lessons Learned 🚨 – Warnings about common pitfalls.

   Act as if you are giving very specific instructions to a video editor. Using the transcript, identify where the editor should start and end the clip. To identify the starting point, use 5 words followed by … and you end the clip start with … and provide the last 5 words that should be in the clip. 





Input: A transcript of a video having ,
< start : denoted as start time of the sentence, 
end : denoted as end time of the sentence , 
text: sentence > .

Output: A Python list of dictionaries containing 
< script: the complete script that have a clear,concise,meaningful message. you will make it using a  complete sequence of senetences (wihtout ignore some words in a sentence) , 
start-time: starting time of the  of the script ( this is the time that you will pick up from the first sentence of the script you will make. it is mention at every sentence you got as 'start' parameter), 
end-time:  ending time of the time script ( this is the time that you will pick up from the last sentence of the script you will make. it is mention at every sentence you got as 'end' parameter )>


IMPORTANT : do not provide extra content just like ( ``` , python) . completely return  list of dictionaries. it should be return type python list.
IMPORTANT : DO NOT CHANGE THE ACTUAL CONTENT/SCRIPT/SCENTENCE, RETURN ACTUAL, AS IT SAME.
"""


sp_title_description_bot = """ you are an expert social media content writer to make a Title, Description/Caption for a social media posts. you will make two variations, 
one for ( Tweeter/X, Linkedin and Thread ) considered as Serious Platforms and other for ( youtube,instagram, tiktok, facebook) considered as Entertainment platforms of each video's text that you received.
 you will receive a short/clip/reel video's transcribe text list having multple dictionaries of scripts you have to work on each script.
 do not provide extra content just like (  ``` , python ) . completely focus on list of dictionaries.  it should be return type python list.
 
 During making title, description/caption please keep it kind following rules.

1. Tone & Style:
Keep content fun, natural, and engaging, with emojis to match content tone (except for tweeeter/X, linkedin & Thread)..
Use a friendly, approachable tone while keeping the content professional and actionable.
Make content skimmable and to the point—people scroll fast!
Avoid sounding robotic or overly scripted; keep it conversational.
2. Emojis:
Emojis should be integrated naturally to enhance emotion, clarity, and structure.
Use bold, eye-catching emojis to emphasize key points (🔥✅⚠️🤯).
Exception: Do not use emojis for tweeter/X , Linkedin & Threads (but keep engagement high with strong wording).
3. Strong Call-to-Actions (CTAs):
Each post should include a clear CTA that encourages interaction, like:
“Drop a 🚀 in the comments if you’re ready to grow!”
“Tag a friend who needs to see this! 👇”
CTAs should feel authentic, not forced or salesy.
Do not create CTA’s that requires someone to leave the platform or link to another video/post
4. Hashtag Strategy:
Generate 9 strategic hashtags per post using this framework:
 1️⃣ Post-Specific Tags (3) – Directly related to the video’s core topic.
 2️⃣ Niche-Specific Tags (3) – Broader but still within the industry.
 3️⃣ Broad Tags (3) – Highly searchable, viral-style tags.
5. Optimize for Each Platform's Format:
Keep content short, punchy, and engaging (especially for IG, TikTok & Shorts).
Avoid dense blocks of text—use spacing, emojis, and formatting for readability.
Ensure the first line is always a strong hook to grab attention immediately.

 Platform info:
- Tweeter/X, Linkedin and Thread  considered as serious platforms.
- youtube,instagram, tiktok, facebook considered as entertainment platforms.




INPUT: you will get the python list of short clip Scripts .
OUTPUT:  A Python list  containing  dictionaries with <
serious-platform-title: 
serious-platform-caption:
entertainment-platform-title:
entertainment-platform-caption:
>

IMPORTANT : do not provide extra content just like ( ``` , python) . completely return  list of dictionaries. it should be return type python list.
IMPORTANT : DO NOT CHANGE THE ACTUAL CONTENT/SCRIPT/SCENTENCE, RETURN ACTUAL, AS IT SAME.
"""


sp_for_hooks = """  
Here's your system message/prompt:

---

**System Message:**

You are an AI assistant that processes multiple scripts containing sentences with start and end times. Each script is meant for short clips or videos. Your task is to analyze each script and extract a strong, catchy, and attention-grabbing sentence that can be used as a starting hook. The sentence should have impact, create curiosity, and engage the viewer instantly.

**Instructions:**
1. Accept input as a list of scripts, where each script contains multiple sentences with their respective start and end times.
2. Analyze each script separately and select one sentence per script that serves as the best hook.
3. Ensure that the selected sentence is **exactly the same** as in the input (do not modify the text).
4. Maintain the original start and end times of the selected sentence.
5. Return the output as a Python list of dictionaries  (return type python list ) in the following format:


[
    {
        'from_Script': 1,
        'start': 17.31999969482422,
        'end': 26.399999618530273,
        'text': " that the thing? Or is the thing that's stopping you, you?"
    },
    {
        'from_Script': 2,
        'start': 97.5999984741211,
        'end': 104.31999969482422,
        'text': " They're lies. And how do you stop the lies? You stop the lies with the truth."
    }
]


Make sure your response is a **Python list of dictionaries**, selecting only one powerful hook sentence from each script.

IMPORTANT : do not provide extra content just like (```python  ,`\n` ) . completely return  list of dictionaries. it should be return type python list.
IMPORTANT : DO NOT CHANGE THE ACTUAL CONTENT/SCRIPT/SCENTENCE, RETURN ACTUAL, AS IT SAME.
"""


import json
import os
a= [
    {
        'serious-platform-title': "The",
        'serious-platform-caption': "Success is often judged by others, but the only true measure is your own effort. When no one’s watching, work harder for yourself. Remember, the sign of success is the hate you receive along the journey. Reflect on your progress. #SuccessMindset #PersonalGrowth #HardWork",
        'entertainment-platform-title': "Work When No One's Watching! 🤫💪",
        'entertainment-platform-caption': "When the spotlight fades, that's when the real work begins! 💥 How hard do you work when nobody's watching? 🤔🔥 Drop a 🚀 in the comments if you’re putting in the effort! #WorkHard #StayMotivated #DreamBig #MindsetMatters #Hustle #SuccessJourney #Inspiration #EntrepreneurLife #GoalDigger"
    },
    {
        'serious-platform-title': "Embracing Pain as a Signal",
        'serious-platform-caption': "Pain signifies life; it's a reminder that you’re here and thriving despite challenges. Embrace it as a part of the journey. The love for the process is what drives true progress. #PainAndGrowth #LifeJourney #Motivation",
        'entertainment-platform-title': "Pain = Proof of Life! 🌍💖",
        'entertainment-platform-caption': "If pain is just a signal that we’re alive, then let’s embrace it! 🙌✨ The true joy is in the journey, not just the destination. Drop a 💪 in the comments if you agree! #PainIsGrowth #StayAlive #LifeLessons #Inspiration #HustleHard #Mindset #JourneyOverDestination #MotivationalQuotes #GrowthMindset"
    },
    {
        'serious-platform-title': "Defining Healthy Work Ethos",
        'serious-platform-caption': "Achieving what you love daily leads to success. Redefine 'healthy' work ethics and immerse yourself in what you enjoy. Work harder now than ever before! #WorkEthic #PersonalSuccess #EnjoyTheProcess",
        'entertainment-platform-title': "What's Your Definition of Healthy? 🤔💼",
        'entertainment-platform-caption': "When they say it’s not healthy, how do you define healthy? 🔥 Do what you love every minute of the day! Let’s go all in! 💯 Tag a friend who needs to hear this! 👇 #WorkHardPlayHard #Passion #Success #Mindset #EntrepreneurMindset #LifeGoals #EnjoyTheJourney #Motivation #Hustle"
    },
    {
        'serious-platform-title': "The Reality of the American Dream",
        'serious-platform-caption': "The American Dream often feels attainable until it's lived. Remember the struggles of the journey that lead to success; they define who you become. #AmericanDream #Underdog #StruggleToSuccess",
        'entertainment-platform-title': "Living the American Dream! 🇺🇸✨",
        'entertainment-platform-caption': "Everyone talks about the American Dream until it's real! 😲💪 From sleeping in a gym to chasing dreams, the journey is worth it! What's your dream? 🚀 #DreamChaser #SuccessStory #Inspiration #HardWork #NeverGiveUp #Motivation #LifeJourney #AmericanDream #Underdog"
    },
    {
        'serious-platform-title': "The Reality of Support",
        'serious-platform-caption': "People may want you to succeed, but often not beyond their own achievements. Understand that the journey is often unseen until it's complete. #SupportSystem #JourneyToSuccess #RealTalk",
        'entertainment-platform-title': "Cheering for You, But Not Too Much! 🎉🙄",
        'entertainment-platform-caption': "Ever felt support until it feels like you're outshining? 😅 Remember, your journey might be unseen until the victory! Keep pushing! 💥 Tag someone who inspires you! 👇 #SupportSystem #JourneyToSuccess #Motivation #DreamBig #HardWork #Inspiration #RealTalk #Growth"
    },
    {
        'serious-platform-title': "Understanding Uncertainty in Growth",
        'serious-platform-caption': "In personal development and entrepreneurship, uncertainty is a constant. Fight through it; you are not alone. Everyone has faced their own challenges along the way. #Entrepreneurship #PersonalDevelopment #Resilience",
        'entertainment-platform-title': "Fighting Through the Uncertainty! 💪🚀",
        'entertainment-platform-caption': "Uncertainty is tough, but it’s a shared struggle in growth! 🌱 Keep fighting through; you're not alone! 💯 What keeps you motivated? #EntrepreneurLifestyle #KeepGoing #PersonalGrowth #MindsetMatters #Motivation #OvercomingObstacles #Persistence #Inspiration #GrowthJourney"
    },
    {
        'serious-platform-title': "Finding Your Focus",
        'serious-platform-caption': "Discipline is about recognizing what matters most and dedicating time to it. Extraordinary results require years of consistent effort. Focus on your passion! #Discipline #Focus #PersonalExcellence",
        'entertainment-platform-title': "What Are You Crushing? 🎯🔥",
        'entertainment-platform-caption': "Focus is key! What are your top three goals? 🎯💪 Remember, greatness takes time! Let's crush it together! 🙌 #FocusOnYourGoals #Discipline #Motivation #HardWork #Success #DreamChaser #PassionProject #GoalSetting #Inspiration"
    }
]

def save_caption_data_to_json(title_description__bot_var, filename='static/title_caption_data.json'):
    # Remove existing file if it exists
    if os.path.exists(filename):
        os.remove(filename)

    # Save new data
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(title_description__bot_var, f)

    print(f"✅ JSON data saved to {filename}")


# print("done: "  ,save_caption_data_to_json(a))



import json

def convert_to_json(escaped_str):
    # Step 1: Remove newlines
    cleaned_str = escaped_str.replace('\n', '')

    # Step 2: Convert escaped string to actual JSON
    try:
        json_data = json.loads(cleaned_str)
        return json_data
    except json.JSONDecodeError as e:
        print("Invalid JSON format:", e)
        return None



# # Your escaped JSON string
# escaped_json = "[\n    {\n        \"serious-platform-title\": \"Understanding the Mindset of Wealth\",\n        \"serious-platform-caption\": \"Discover the key differences between the wealthy and the poor mindset. The first difference: rich people think big, while poor people think small. Are you prioritizing savings over opportunities? Let's discuss the impact of your mindset on success.\",\n        \"entertainment-platform-title\": \"💰 Secrets of the Millionaire Mind! 📚\",\n        \"entertainment-platform-caption\": \"Today, we're diving into 'Secrets of the Millionaire Mind'! 💡 Did you know rich people think big while poor people think small? 🛒 Take a moment to reflect on your shopping habits! 👀 #WealthMindset #SuccessTips #PersonalGrowth\"\n    },\n    {\n        \"serious-platform-title\": \"The Value of Results Over Time\",\n        \"serious-platform-caption\": \"In the pursuit of success, focus on results rather than time invested. The second difference between rich and poor is that rich people choose to get paid based on results, not effort. Let your work speak for itself.\",\n        \"entertainment-platform-title\": \"🚀 Focus on Results, Not Just Effort! 🌟\",\n        \"entertainment-platform-caption\": \"It's time to shift your thinking! Rich people care about results, not just hard work. 💪 When was the last time you evaluated your output? 🎯 #ResultsDriven #WealthyMindset #Motivation\"\n    },\n    {\n        \"serious-platform-title\": \"Know Your Value: Focus on Results\",\n        \"serious-platform-caption\": \"Your true value comes from the results you deliver, not the salary you receive. Rich people understand this distinction and embrace opportunities. Poor people often cling to security instead. Which mindset do you resonate with?\",\n        \"entertainment-platform-title\": \"💡 Know Your Worth: Results Over Salary! 💸\",\n        \"entertainment-platform-caption\": \"Rich people work for results, not just a paycheck! 💼 Keep an eye on opportunities and break away from the salary trap! What's your experience? 👇 #MindsetShift #Opportunities #Success\"\n    },\n    {\n        \"serious-platform-title\": \"Balancing Money and Happiness\",\n        \"serious-platform-caption\": \"You don’t have to choose between wealth and happiness. Understand how misconceptions can hold you back from both. Let’s explore the balance of being rich while staying kind.\",\n        \"entertainment-platform-title\": \"🌈 Can Money Buy Happiness? 🤔\",\n        \"entertainment-platform-caption\": \"Who says you can’t have both money AND happiness? 💖 Don’t let myths hold you back! Being kind doesn’t mean staying broke. What do you think? 💰✨ #WealthAndHappiness #LifeChoices #Mindset\"\n    },\n    {\n        \"serious-platform-title\": \"Opportunities vs. Obstacles\",\n        \"serious-platform-caption\": \"Rich people focus on opportunities while poor people dwell on obstacles. Embrace a perspective that seeks out possibilities rather than risks. How do you approach new ideas?\",\n        \"entertainment-platform-title\": \"🔍 Opportunities Are Everywhere! 🚀\",\n        \"entertainment-platform-caption\": \"What's your mindset: do you focus on opportunities or obstacles? 🌟 Let's change the narrative and unlock new possibilities together! Share your thoughts! 💬 #OpportunityMindset #SuccessJourney #Inspiration\"\n    }\n]"
# converted = convert_to_json(escaped_json)
# c = json.dumps(converted)
# # print(converted)
# print(c)  # Pretty print to check


