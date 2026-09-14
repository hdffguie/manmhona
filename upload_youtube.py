import os
import datetime
import base64
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google import genai

TOKEN_B64 = os.getenv("YOUTUBE_TOKEN_BASE64", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
VIDEO_FILE = "final_output/Final_Review_Test.mp4"

def generate_youtube_metadata():
    """AI se automatic Viral Title, Description aur Tags banwayega"""
    try:
        with open("websites.txt", "r") as f:
            url = f.read().strip()
            
        client = genai.Client(api_key=GEMINI_API_KEY)
        prompt = f"""Write a viral YouTube metadata for a review video of {url}.
        Format EXACTLY like this:
        TITLE: [Clickbait Hindi title with emojis]
        DESC: [Short description]
        TAGS: [comma separated 10 tags]
        """
        response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
        text = response.text
        
        title = text.split("TITLE:")[1].split("DESC:")[0].strip()
        desc = text.split("DESC:")[1].split("TAGS:")[0].strip()
        tags = [t.strip() for t in text.split("TAGS:")[1].strip().split(",")]
        return title[:100], desc, tags
    except Exception as e:
        print("⚠️ AI Metadata fail hua, default use kar raha hu.")
        return "Secret Website Review! 🔥", "Watch till the end!", ["tech", "review", "website"]

def get_schedule_time():
    """Smart Scheduling: 5:27 AM ya 8:26 PM (IST) khud set karega"""
    utc_now = datetime.datetime.utcnow()
    ist_now = utc_now + datetime.timedelta(hours=5, minutes=30)
    
    if ist_now.hour < 12:
        # Agar bot subha/raat me chal raha hai -> Aaj subha 5:27 AM ka time
        target_ist = ist_now.replace(hour=5, minute=27, second=0, microsecond=0)
        # Agar 5:27 nikal chuka hai, toh agle din subha 5:27
        if ist_now > target_ist:
            target_ist += datetime.timedelta(days=1)
        print("🌅 Morning Schedule: Video 5:27 AM par aayegi.")
    else:
        # Agar bot dopahar/shaam ko chal raha hai -> Aaj shaam 8:26 PM ka time
        target_ist = ist_now.replace(hour=20, minute=26, second=0, microsecond=0)
        # Agar 8:26 nikal chuka hai, toh agle din shaam 8:26
        if ist_now > target_ist:
            target_ist += datetime.timedelta(days=1)
        print("🌃 Evening Schedule: Video 8:26 PM par aayegi.")

    # YouTube API ko time UTC me chahiye hota hai
    target_utc = target_ist - datetime.timedelta(hours=5, minutes=30)
    return target_utc.strftime("%Y-%m-%dT%H:%M:%S.0Z")

def upload_to_youtube():
    if not TOKEN_B64:
        print("❌ YOUTUBE_TOKEN_BASE64 secret nahi mila. Upload cancel.")
        return

    if not os.path.exists(VIDEO_FILE):
        print("❌ Video file nahi mili. Upload cancel.")
        return

    try:
        # Token decode karna
        token_json = base64.b64decode(TOKEN_B64).decode('utf-8')
        creds_data = json.loads(token_json)
        creds = Credentials.from_authorized_user_info(creds_data)
        youtube = build('youtube', 'v3', credentials=creds)
        
        # AI Title & Description
        title, description, tags = generate_youtube_metadata()
        schedule_time = get_schedule_time()

        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': '28'  # Science & Technology Category
            },
            'status': {
                'privacyStatus': 'private',      
                'publishAt': schedule_time,      
                'selfDeclaredMadeForKids': False
            }
        }

        print(f"🚀 Video Upload ho rahi hai...\nTitle: {title}\nTime: {schedule_time}")
        media = MediaFileUpload(VIDEO_FILE, chunksize=-1, resumable=True, mimetype='video/mp4')
        request = youtube.videos().insert(part=','.join(body.keys()), body=body, media_body=media)
        response = request.execute()
        
        print(f"🎉 SUCCESS! Video YouTube par Scheduled ho gayi hai!")
        print(f"🔗 Link: https://youtu.be/{response.get('id')}")

    except Exception as e:
        print(f"❌ YouTube Upload Failed: {e}")

if __name__ == "__main__":
    upload_to_youtube()
