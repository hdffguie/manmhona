import asyncio
import json
import os
import subprocess
import time
from playwright.async_api import async_playwright

os.makedirs("temp_audio", exist_ok=True)
os.makedirs("temp_video", exist_ok=True)

def generate_audio(text, index):
    audio_path = f"temp_audio/speech_{index}.mp3"
    cmd = ["edge-tts", "--voice", "hi-IN-MadhurNeural", "--text", text, "--write-media", audio_path]
    subprocess.run(cmd, check=True)
    
    dur_cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", audio_path]
    duration = float(subprocess.check_output(dur_cmd).decode().strip())
    return audio_path, duration

async def inject_mouse(page):
    mouse_code = """
        if (!document.getElementById('fake-mouse')) {
            const box = document.createElement('div');
            box.id = 'fake-mouse';
            box.style.position = 'absolute';
            box.style.width = '25px';
            box.style.height = '25px';
            box.style.backgroundColor = 'rgba(255, 50, 50, 0.8)';
            box.style.borderRadius = '50%';
            box.style.zIndex = '999999';
            box.style.pointerEvents = 'none';
            box.style.transition = 'top 0.3s, left 0.3s ease-out';
            box.style.boxShadow = '0 0 10px red';
            document.body.appendChild(box);
            document.addEventListener('mousemove', (e) => {
                box.style.left = e.pageX + 'px';
                box.style.top = e.pageY + 'px';
            });
        }
    """
    await page.evaluate(mouse_code)

async def main():
    with open("bot_commands.json", "r", encoding="utf-8") as f:
        commands = json.load(f)

    with open("websites.txt", "r") as f:
        target_url = f.read().strip()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # 🚨 FIX: Yaha explicitly record_video_size define kar diya, ab video 1080p HD aayegi!
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080}, 
            record_video_dir="temp_video/",
            record_video_size={'width': 1920, 'height': 1080}
        )
        page = await context.new_page()
        
        audio_list = []

        for idx, step in enumerate(commands):
            action = step.get("action")
            selector = step.get("selector")
            text = step.get("text")

            print(f"🎬 {action}: {text[:40]}...")
            
            audio_path, expected_duration = generate_audio(text, idx)
            audio_list.append(audio_path)
            
            start_time = time.time()

            if action == "google_search":
                await page.goto("https://www.google.com", wait_until="domcontentloaded")
                await inject_mouse(page)
                search_box = page.locator("textarea[name='q'], input[name='q']").first
                await search_box.fill(selector)
                await asyncio.sleep(0.5)
                await page.keyboard.press("Enter")
                await page.wait_for_load_state("networkidle")
                await asyncio.sleep(1)
                
                await page.goto(target_url, wait_until="domcontentloaded")
                await inject_mouse(page)
                await page.mouse.move(500, 500)

            elif action == "scroll":
                await page.mouse.wheel(0, 800)
                await page.mouse.move(960, 540)
            
            elif action == "highlight":
                try:
                    loc = page.locator(f"text='{selector}'").first
                    if await loc.is_visible(timeout=2000):
                        box = await loc.bounding_box()
                        if box:
                            await page.mouse.move(box["x"] + box["width"]/2, box["y"] + box["height"]/2)
                        
                        await loc.evaluate("el => { el.style.border = '5px solid red'; el.style.backgroundColor = 'rgba(255, 0, 0, 0.15)'; el.style.boxShadow = '0 0 25px red'; el.style.borderRadius = '5px'; }")
                except:
                    print(f"⚠️ '{selector}' text screen par nahi mila, skip kar raha hu.")

            time_taken = time.time() - start_time
            time_to_wait = expected_duration - time_taken
            
            if time_to_wait > 0:
                await asyncio.sleep(time_to_wait) 
            else:
                await asyncio.sleep(0.2)

            if action == "highlight":
                try:
                    loc = page.locator(f"text='{selector}'").first
                    await loc.evaluate("el => { el.style.border = 'none'; el.style.backgroundColor = 'transparent'; el.style.boxShadow = 'none'; }")
                except: pass

        await page.close()
        await context.close()
        await browser.close()
        
        with open("temp_audio/audio_list.txt", "w") as f:
            for audio in audio_list:
                f.write(f"file '{os.path.basename(audio)}'\n")

if __name__ == "__main__":
    asyncio.run(main())
