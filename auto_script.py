import os
import re
import json
from google import genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_review_script(url):
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    # 🚨 AI ko strict instructions ki JSON format me hi answer de
    prompt = f"""You are an expert Hindi Tech YouTuber reviewing websites.
    Create a 1-minute engaging review for this URL: {url}.
    
    I am building an automated bot that records the screen. You need to provide the output strictly in a JSON array format.
    The bot will read this JSON, speak the 'text', and perform the 'action'.
    
    Actions can be:
    - "goto": Opens the URL (Must be the first action)
    - "scroll": Scrolls the page down
    - "highlight": Draws a red box around a specific element on the screen. (For 'selector', guess a common text that might be on this site, e.g., 'Pricing', 'Login', 'Models', 'Try', 'Get Started')
    
    Format Example:
    [
      {{"action": "goto", "selector": "{url}", "text": "Hey guys! Aaj main aapko ek aisi kamal ki website batane wala hu jiska naam hai..."}},
      {{"action": "highlight", "selector": "Models", "text": "Yahan models wale option par agar aap dekhenge..."}},
      {{"action": "scroll", "selector": "down", "text": "Neeche scroll karne par aapko iske aur bhi features dikhenge."}},
      {{"action": "highlight", "selector": "Pricing", "text": "Aur haan, yahan pricing par click karke aap inke plans dekh sakte hain. Ye bilkul genuine site hai."}}
    ]
    
    Write a 4-5 step script in Hinglish. Return ONLY valid JSON, no markdown.
    """
    
    print("🤖 AI se Website ka Review likhwa raha hu...")
    response = client.models.generate_content(model='gemini-3.6-flash', contents=prompt)
    
    # Clean output to get valid JSON
    output = response.text.replace("```json", "").replace("```", "").strip()
    
    with open("bot_commands.json", "w", encoding="utf-8") as f:
        f.write(output)
    
    print("✅ AI ne script aur commands bana diye!")

if __name__ == "__main__":
    with open("websites.txt", "r") as f:
        url = f.read().strip()
    generate_review_script(url)
