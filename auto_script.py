import os
import json
from google import genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_review_script(url):
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    prompt = f"""You are an expert, high-energy Hindi Tech YouTuber. Goal: 100% Audience Retention.
    You are reviewing this EXACT URL: {url}.
    
    Return EXACTLY a JSON array. Actions MUST be in this order:
    1. "intro_hook": (No selector). Text: "Agar tum tech me master banna chahte ho, toh ye website tumhare bahut kaam aane wali hai. Dhyan se dekhna!"
    2. "google_search": (Selector MUST be "{url}"). Text: "Sabse pehle Google par ye secret link type karke direct is website par chalte hain."
    3. "highlight": (Pick a very common button name on this site like 'Models', 'Spaces', 'Features', 'Docs'). Text: "Website khulte hi sabse pehle is option par nazar dalo. Iska kaam hai aapke ghanto ke kaam ko asaan banana. Ye bahut zaroori feature hai."
    4. "scroll": (No selector). Text: "Ab thoda neeche chal kar dekhte hain ki website ke andar asli khazana kahan hai."
    5. "highlight": (Pick another common button like 'Pricing', 'Login', 'Datasets'). Text: "Yahan par dekho, is section se aap bahut kuch naya explore kar sakte ho. Ye bilkul try karne laayak hai."
    6. "celebrate": (No selector). Text: "Agar ye review pasand aaya, toh turant video ko Like karo, Comment me batao kaisa laga, aur Channel ko Subscribe zaroor karna!"
    
    CRITICAL: 
    - Write energetic Hinglish. 
    - Output ONLY a valid JSON array. No markdown, no intro text.
    """
    
    print("🤖 AI Script bana raha hai...")
    response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
    output = response.text.replace("```json", "").replace("```", "").strip()
    
    with open("bot_commands.json", "w", encoding="utf-8") as f:
        f.write(output)
    print("✅ AI Pro-Script Ready!")

if __name__ == "__main__":
    with open("websites.txt", "r") as f:
        url = f.read().strip()
    generate_review_script(url)
