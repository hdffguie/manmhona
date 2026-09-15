import os
import json
import time
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
    
    # 🚨 BULLETPROOF FIX: Server busy hone par retry karega
    models_to_try = ['gemini-3.6-flash', 'gemini-1.5-flash']
    max_retries = 5
    success = False
    output = ""

    for attempt in range(max_retries):
        for model_name in models_to_try:
            try:
                print(f"🔄 Trying model: {model_name} (Attempt {attempt+1}/{max_retries})")
                response = client.models.generate_content(model=model_name, contents=prompt)
                output = response.text.replace("```json", "").replace("```", "").strip()
                
                # Check if output is actually JSON
                if output.startswith("[") and output.endswith("]"):
                    success = True
                    break
            except Exception as e:
                print(f"⚠️ Error with {model_name}: API overload. Waiting 5 seconds...")
                time.sleep(5) # 5 second ruko fir try karo
                
        if success:
            break

    if not success:
        print("❌ AI API completely overloaded. Baad me try karein.")
        exit(1)
    
    with open("bot_commands.json", "w", encoding="utf-8") as f:
        f.write(output)
    print("✅ AI 8-Minute Pro-Script Ready!")

if __name__ == "__main__":
    with open("websites.txt", "r", encoding="utf-8") as f:
        raw_content = f.read()
    
    raw_content = raw_content.replace("https://", " \nhttps://").replace("http://", " \nhttp://")
    urls = [u.strip() for u in raw_content.split() if u.strip().startswith("http")]
    
    if urls:
        current_url = urls[0]
        print(f"🎯 Aaj ka target URL: {current_url}")
        
        with open("current_url.txt", "w", encoding="utf-8") as f:
            f.write(current_url)
            
        generate_review_script(current_url)
        
        with open("websites.txt", "w", encoding="utf-8") as f:
            if len(urls) > 1:
                f.write("\n".join(urls[1:]) + "\n")
            else:
                f.write("")
                
        print(f"✅ URL processed. Bachi hui websites: {len(urls)-1}")
    else:
        print("❌ Websites ki list khatam ho gayi hai! File khali hai.")
        exit(1)
