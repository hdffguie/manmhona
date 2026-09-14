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
    1. Hook & Intro: (intro_hook, google_search) - Tell them exactly why this site will change their life or make them money.
    2. Deep Dive Features: (highlight & scroll) - Explain the top 5 features one by one in extreme detail.
    3. Target Audience / Use Cases: (highlight & scroll_up) - Explain who should use this and how they can make money or save time using it.
    4. Pricing & Alternatives: (highlight & scroll) - Discuss the pricing section. Is the free tier good?
    5. Conclusion: (celebrate) - Final verdict and call to action (Like, Subscribe, Comment).
    
    AVAILABLE ACTIONS:
    - "intro_hook": Only used once at the start.
    - "google_search": Only used once after intro. Selector must be "{url}".
    - "highlight": Put a red box on a feature (e.g., 'Models', 'Pricing', 'Features', 'Login', 'Try for free').
    - "scroll": Scrolls DOWN the page.
    - "scroll_up": Scrolls UP the page.
    - "celebrate": Only used once at the end.
    
    CRITICAL RULES:
    - Output ONLY a valid JSON array. No markdown, no explanations outside JSON.
    - Ensure the total text spoken is around 1000 words.
    - Keep energy high in Hinglish (e.g., "Dosto", "Kamal ka tool", "Paisa kamane ka tareeka").
    """
    
    print("🤖 AI 8-Minute Long Script bana raha hai (Isme thoda time lag sakta hai)...")
    response = client.models.generate_content(model='gemini-3.6-flash', contents=prompt)
    output = response.text.replace("```json", "").replace("```", "").strip()
    
    with open("bot_commands.json", "w", encoding="utf-8") as f:
        f.write(output)
    print("✅ AI 8-Minute Pro-Script Ready!")

if __name__ == "__main__":
    with open("websites.txt", "r") as f:
        urls = [line.strip() for line in f.readlines() if line.strip()]
    
    if urls:
        current_url = urls[0]
        print(f"🎯 Aaj ka target URL: {current_url}")
        
        # Save current URL for YouTube upload logic later
        with open("current_url.txt", "w") as f:
            f.write(current_url)
            
        generate_review_script(current_url)
        
        with open("websites.txt", "w") as f:
            if len(urls) > 1:
                f.write("\n".join(urls[1:]) + "\n")
            else:
                f.write("")
                
        print(f"✅ URL processed. Bachi hui websites: {len(urls)-1}")
    else:
        print("❌ Websites ki list khatam ho gayi hai! File khali hai.")
        exit(1)
