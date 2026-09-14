import os
import json
from google import genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_review_script(url):
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    prompt = f"""You are an expert Hindi Tech YouTuber. Your goal is to make a 60-second video.
    Create a highly engaging review for this URL: {url}.
    
    Return EXACTLY a JSON array. Actions MUST be in this order:
    1. "google_search": (Selector MUST be "{url}"). Text: "Dosto agar aap internet ke master banna chahte ho, toh Google par type karo ye secret link. Chalo direct chalte hain is website par..."
    2. "highlight": (Point to a common word like 'Models', 'Explore', or 'Features'). Text: "Website khulte hi aapko is option par aana hai. Yahan par aapko aisi kamal ki AI chizein milengi jo aapne kabhi sochi bhi nahi hogi. Ye option sabse best hai."
    3. "scroll": Text: "Ab thoda neeche scroll karke dekhte hain ki isme aur kya kya naye features chhype hain..."
    4. "highlight": (Point to 'Pricing', 'Docs', 'Login' or 'Try'). Text: "Aur sabse badi baat, agar aap is wale section me jayenge, toh aapko pata chalega ki ye bilkul try karne laayak hai. Log iska bahut use kar rahe hain."
    5. "scroll": Text: "Website ka interface bahut hi smooth hai aur use karne me maza aata hai."
    6. "celebrate": Text: "Agar aapko ye secret trick aur website pasand aayi, toh turant video ko like aur channel ko subscribe thok do!"
    
    CRITICAL: 
    - Ensure the text is long enough to make the video at least 50-60 seconds long.
    - Output ONLY a valid JSON array. No markdown, no extra text.
    """
    
    print("🤖 AI Script bana raha hai (1 minute lambi)...")
    response = client.models.generate_content(model='gemini-3.6-flash', contents=prompt)
    output = response.text.replace("```json", "").replace("```", "").strip()
    
    with open("bot_commands.json", "w", encoding="utf-8") as f:
        f.write(output)
    print("✅ AI Script Ready!")

if __name__ == "__main__":
    with open("websites.txt", "r") as f:
        url = f.read().strip()
    generate_review_script(url)
