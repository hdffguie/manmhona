import os
import json
from google import genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_review_script(url):
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    prompt = f"""You are an expert, high-energy Hindi Tech YouTuber. Goal: 100% Audience Retention.
    You are reviewing this EXACT URL: {url}.
    
    THINKING PROCESS:
    1. Figure out what this website is for (e.g., Coding, AI, Hosting, Design, Tools).
    2. Identify the target audience (e.g., Coders, Students, Video Editors, Gamers).
    3. Create a 5-second Hook specifically for them. (e.g., "Agar tum ek coder ho aur free me bot host karna chahte ho, toh ye site tumhari zindagi badal degi!")
    
    Return EXACTLY a JSON array. Actions MUST be in this order:
    1. "intro_hook": (No selector). Text: [Your targeted 5-second hook here].
    2. "google_search": (Selector MUST be "{url}"). Text: "Sabse pehle Google par ye link type karke is site par chalte hain."
    3. "highlight": (Point to the top-left or main header feature, e.g., 'Features' or 'Explore'). Text: "Website khulte hi sabse pehle upar is option par nazar dalo. Iska kaam hai [Explain what it does]. Ye bahut zaroori hai."
    4. "highlight": (Point to the next feature down). Text: "Uske theek bagal me ye [Feature name] ka option hai. Isse aap [Explain its use case]. Ekdum kamaal ki cheez hai."
    5. "scroll": (No selector). Text: "Ab thoda neeche scroll karte hain, kyunki asli khazana toh yahan chhipa hai."
    6. "highlight": (Point to a mid-page feature like 'Pricing', 'Docs', 'Try'). Text: "Yahan par dekho, is section se aap [Explain what it does]. Ye aapke ghanto ka kaam second me kar dega."
    7. "celebrate": (No selector). Text: "Agar ye detailed review pasand aaya toh video ko turant like aur channel ko subscribe kar lo!"
    
    CRITICAL: 
    - Explain step-by-step from TOP to BOTTOM.
    - Explain 'What this does' for every highlighted point.
    - Write energetic Hinglish. 
    - Return ONLY valid JSON array. No markdown.
    """
    
    print("🤖 AI Target Audience dhundh raha hai aur detailed script bana raha hai...")
    response = client.models.generate_content(model='gemini-3.6-flash', contents=prompt)
    output = response.text.replace("```json", "").replace("```", "").strip()
    
    with open("bot_commands.json", "w", encoding="utf-8") as f:
        f.write(output)
    print("✅ AI Pro-Script Ready!")

if __name__ == "__main__":
    with open("websites.txt", "r") as f:
        url = f.read().strip()
    generate_review_script(url)
