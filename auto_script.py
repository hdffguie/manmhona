import os
import json
from google import genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_review_script(url):
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    prompt = f"""You are an expert, high-energy Hindi Tech YouTuber. 
    Your goal is to make a VERY DETAILED, 8-MINUTE LONG deep-dive review video about this EXACT URL: {url}.
    
    To make an 8-minute video, you MUST generate a MASSIVE JSON array with at least 35 to 40 steps. 
    The 'text' for each step should be long (3-4 detailed sentences).
    
    VIDEO STRUCTURE & SCRIPT ROADMAP:
    1. Hook & Intro: (intro_hook, google_search) - Tell them exactly why this site will change their life.
    2. Deep Dive Features: (highlight & scroll) - Explain the top 5 features one by one in extreme detail. What does it do? How does it save time?
    3. Target Audience / Use Cases: (highlight & scroll_up) - Explain who should use this (Students? Coders? Video Editors?) and how they can make money or save time using it.
    4. Pricing & Alternatives: (highlight & scroll) - Discuss the pricing section. Is the free tier good? Should they upgrade?
    5. Conclusion: (celebrate) - Final verdict and call to action (Like, Subscribe, Comment).
    
    AVAILABLE ACTIONS:
    - "intro_hook": Only used once at the start.
    - "google_search": Only used once after intro. Selector must be "{url}".
    - "highlight": Put a red box on a feature (e.g., 'Models', 'Pricing', 'Features', 'Login', 'Try for free').
    - "scroll": Scrolls DOWN the page.
    - "scroll_up": Scrolls UP the page (Use this so you don't get stuck at the bottom).
    - "celebrate": Only used once at the end.
    
    CRITICAL RULES:
    - You MUST output ONLY a valid JSON array. No markdown, no explanations outside JSON.
    - Ensure the total text spoken is around 1000-1200 words to fill 8 minutes.
    - Keep the energy high and use professional Hindi/Hinglish (e.g., "Dosto", "Kamal ka tool", "Ghanto ka kaam seconds mein").
    """
    
    print("🤖 AI 8-Minute Long Script aur Deep-Dive Commands bana raha hai (Isme thoda time lag sakta hai)...")
    # Using a high token limit to ensure it doesn't cut off the long JSON
    response = client.models.generate_content(
        model='gemini-3.6-flash', 
        contents=prompt
    )
    
    output = response.text.replace("```json", "").replace("```", "").strip()
    
    with open("bot_commands.json", "w", encoding="utf-8") as f:
        f.write(output)
    print("✅ AI 8-Minute Pro-Script Ready!")

if __name__ == "__main__":
    with open("websites.txt", "r") as f:
        url = f.read().strip()
    generate_review_script(url)
