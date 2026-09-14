import os
import json
from google import genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_review_script(url):
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    prompt = f"""You are an expert Hindi Tech YouTuber reviewing websites. Your goal is 100% audience retention.
    Create a highly engaging 1-minute review for this EXACT URL: {url}.
    
    Return EXACTLY a JSON array. Actions must be in this order:
    1. "google_search": (Selector MUST be exactly "{url}"). Text: "Dosto agar aap bhi internet ke master banna chahte ho, toh Google par type karo ye secret link, aur magic dekho..."
    2. "highlight": Point to a main feature (e.g., 'Models', 'Explore', 'Features'). Text: "Website khulte hi aapko is option par aana hai. Yahan aapko aisi chizein milengi jo aapne sochi nahi hogi."
    3. "scroll": "Thoda neeche scroll karte hain taaki asli khazana mil sake..."
    4. "highlight": Point to another feature (e.g., 'Pricing', 'Login'). Text: "Aur sabse badi baat, ye feature bilkul try karne laayak hai."
    5. "celebrate": (No selector needed). Text: "Agar ye secret trick pasand aayi, toh turant like aur subscribe thok do!"
    
    Write max 5 steps in energetic Hinglish. Return ONLY valid JSON array.
    """
    
    print("🤖 AI Script aur Actions bana raha hai (with new suspense logic)...")
    response = client.models.generate_content(model='gemini-3.6-flash', contents=prompt)
    output = response.text.replace("```json", "").replace("```", "").strip()
    
    with open("bot_commands.json", "w", encoding="utf-8") as f:
        f.write(output)
    print("✅ AI Script Ready!")

if __name__ == "__main__":
    with open("websites.txt", "r") as f:
        url = f.read().strip()
    generate_review_script(url)
