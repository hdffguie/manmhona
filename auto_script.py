import os
import json
from google import genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_review_script(url):
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    # URL ko saaf karke site ka naam nikalna (e.g., https://www.huggingface.co -> Huggingface)
    clean_url = url.split("://")[-1].replace("www.", "")
    site_name = clean_url.split(".")[0].capitalize()
    
    prompt = f"""You are an expert Hindi Tech YouTuber reviewing websites.
    Create a 1-minute engaging review for this URL: {url} (Name: {site_name}).
    
    Return EXACTLY a JSON array. Actions must be in this order:
    1. "google_search": (Selector should be "{site_name}"). Text: "Dosto aaj main aapko ek aisi kamal ki website dikhata hu, sabse pehle google par likhte hain {site_name} aur is pehli link par click karte hain."
    2. "highlight": Point to a specific feature (e.g., 'Models', 'Pricing', 'Login'). Text MUST start explaining it immediately.
    3. "scroll": "Agar hum thoda neeche scroll karein toh..."
    4. "highlight": Another feature.
    5. "highlight": One last feature. "Ye site bilkul genuine hai, try zaroor karna!"
    
    Format Example:
    [
      {{"action": "google_search", "selector": "{site_name}", "text": "Dosto aaj main aapko ek gazab ki website dikhata hu..."}},
      {{"action": "highlight", "selector": "Models", "text": "Yahan models wale option par click karke aap inke tools dekh sakte hain."}},
      {{"action": "scroll", "selector": "down", "text": "Is site ko thoda neeche scroll karein toh aur bhi details milengi."}},
      {{"action": "highlight", "selector": "Pricing", "text": "Aur haan, yahan inke pricing plans bhi hain. Try zaroor karna!"}}
    ]
    
    Write 4-5 steps max in Hinglish. Return ONLY valid JSON array without any markdown formatting.
    """
    
    print("🤖 AI Script aur Actions bana raha hai...")
    response = client.models.generate_content(model='gemini-3.6-flash', contents=prompt)
    output = response.text.replace("```json", "").replace("```", "").strip()
    
    with open("bot_commands.json", "w", encoding="utf-8") as f:
        f.write(output)
    print("✅ AI Script Ready!")

if __name__ == "__main__":
    with open("websites.txt", "r") as f:
        url = f.read().strip()
    generate_review_script(url)
