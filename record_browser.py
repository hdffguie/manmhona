import asyncio
import json
import os
import subprocess
from playwright.async_api import async_playwright

os.makedirs("temp_audio", exist_ok=True)
os.makedirs("final_output", exist_ok=True)

def generate_audio(text, index):
    """Text to Speech convert karega aur uski duration nikalega"""
    audio_path = f"temp_audio/speech_{index}.mp3"
    cmd = ["edge-tts", "--voice", "hi-IN-MadhurNeural", "--text", text, "--write-media", audio_path]
    subprocess.run(cmd, check=True)
    
    # Audio ki lambai (duration) pata karna
    dur_cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", audio_path]
    duration = float(subprocess.check_output(dur_cmd).decode().strip())
    return audio_path, duration

async def main():
    with open("bot_commands.json", "r", encoding="utf-8") as f:
        commands = json.load(f)

    print("🌐 Playwright Browser Open ho raha hai...")
    async with async_playwright() as p:
        # Video recording on kar di gayi hai
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            record_video_dir="temp_video/"
        )
        page = await context.new_page()

        audio_list = []

        for idx, step in enumerate(commands):
            action = step.get("action")
            selector = step.get("selector")
            text = step.get("text")

            print(f"🎬 Action: {action} | Text: {text[:30]}...")

            # 1. Pehle Audio Generate karo
            audio_path, duration = generate_audio(text, idx)
            audio_list.append(audio_path)

            # 2. Browser me Action karo
            if action == "goto":
                await page.goto(selector, wait_until="networkidle")
                await asyncio.sleep(1)
            
            elif action == "scroll":
                await page.mouse.wheel(0, 800)
            
            elif action == "highlight":
                # 🚨 YAHAN LAL BOX BANAYA JAYEGA
                try:
                    # Text ke hisaab se button dhoondho (jaise "Pricing", "Try")
                    loc = page.locator(f"text='{selector}'").first
                    if await loc.is_visible(timeout=3000):
                        # JavaScript se 5px ka Lal border banao
                        await loc.evaluate("el => el.style.border = '5px solid red'")
                        await loc.evaluate("el => el.style.boxShadow = '0 0 15px red'")
                    else:
                        print(f"⚠️ '{selector}' nahi mila screen par.")
                except Exception as e:
                    print("Highlight error:", e)

            # 3. Audio khatam hone tak wait karo
            await asyncio.sleep(duration + 0.5)

            # Wait ke baad agar highlight tha, to hata do taaki agla box ban sake
            if action == "highlight":
                try:
                    loc = page.locator(f"text='{selector}'").first
                    if await loc.is_visible():
                        await loc.evaluate("el => el.style.border = 'none'")
                        await loc.evaluate("el => el.style.boxShadow = 'none'")
                except: pass

        print("🛑 Recording bnd ki jaa rahi hai...")
        await page.close()
        await context.close()
        await browser.close()
        
        # Audio list ko ek file me save kar lo baad me merge karne ke liye
        with open("temp_audio/audio_list.txt", "w") as f:
            for audio in audio_list:
                f.write(f"file '{os.path.basename(audio)}'\n")

if __name__ == "__main__":
    asyncio.run(main())
