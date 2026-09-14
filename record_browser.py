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

async def inject_mouse_and_effects(page):
    """Real Mouse Cursor + Spotlight CSS + Confetti Logic"""
    js_code = """
        // 1. Fake Mouse Cursor (Real Arrow shape)
        if (!document.getElementById('fake-mouse')) {
            const cursor = document.createElement('div');
            cursor.id = 'fake-mouse';
            cursor.style.position = 'absolute';
            cursor.style.width = '24px';
            cursor.style.height = '24px';
            // Real cursor icon (SVG)
            cursor.style.backgroundImage = 'url("data:image/svg+xml;utf8,<svg xmlns=\\'http://www.w3.org/2000/svg\\' width=\\'24\\' height=\\'24\\' viewBox=\\'0 0 24 24\\'><path fill=\\'red\\' stroke=\\'white\\' stroke-width=\\'2\\' d=\\'M5.5 3.21V20.8c0 .45.54.67.85.35l4.86-4.86 3.8 8.04c.15.33.54.46.87.31l2.25-1.06c.33-.15.46-.54.31-.87l-3.75-7.96 5.8-1.5c.44-.11.53-.69.17-.96L6.37 2.87c-.32-.24-.87-.01-.87.34z\\'/></svg>")';
            cursor.style.zIndex = '1000000';
            cursor.style.pointerEvents = 'none';
            cursor.style.transition = 'top 0.25s ease, left 0.25s ease';
            document.body.appendChild(cursor);
            document.addEventListener('mousemove', (e) => {
                cursor.style.left = e.pageX + 'px';
                cursor.style.top = e.pageY + 'px';
            });
        }
        
        // 2. Spotlight Overlay (Background Andhera karne ke liye)
        if (!document.getElementById('spotlight-overlay')) {
            const overlay = document.createElement('div');
            overlay.id = 'spotlight-overlay';
            overlay.style.position = 'fixed';
            overlay.style.top = '0'; overlay.style.left = '0';
            overlay.style.width = '100vw'; overlay.style.height = '100vh';
            overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
            overlay.style.zIndex = '999998';
            overlay.style.display = 'none'; // Pehle chhupa rahega
            overlay.style.transition = 'opacity 0.3s ease';
            document.body.appendChild(overlay);
        }
        
        // 3. Simple Confetti Function (End ke liye)
        window.shootConfetti = function() {
            for(let i=0; i<50; i++) {
                let conf = document.createElement('div');
                conf.style.position = 'fixed';
                conf.style.left = Math.random() * 100 + 'vw';
                conf.style.top = '-10px';
                conf.style.width = '10px'; conf.style.height = '10px';
                conf.style.backgroundColor = ['red','yellow','blue','green','pink'][Math.floor(Math.random()*5)];
                conf.style.zIndex = '999999';
                conf.style.transition = 'top 2s ease-in, transform 2s ease-in';
                document.body.appendChild(conf);
                setTimeout(() => {
                    conf.style.top = '110vh';
                    conf.style.transform = 'rotate(' + Math.random()*360 + 'deg)';
                }, 50);
            }
        };
    """
    await page.evaluate(js_code)

async def main():
    with open("bot_commands.json", "r", encoding="utf-8") as f:
        commands = json.load(f)

    with open("websites.txt", "r") as f:
        target_url = f.read().strip()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
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
                await inject_mouse_and_effects(page)
                
                search_box = page.locator("textarea[name='q'], input[name='q']").first
                await search_box.click()
                await asyncio.sleep(0.5)
                
                # 🚨 HUMAN TYPING EFFECT (Ek-ek letter type karega)
                await search_box.type(selector, delay=120) 
                
                await asyncio.sleep(0.5)
                await page.keyboard.press("Enter")
                await page.wait_for_load_state("networkidle")
                await asyncio.sleep(1.5)
                
                # Site kholo
                await page.goto(target_url, wait_until="domcontentloaded")
                await inject_mouse_and_effects(page)
                await page.mouse.move(960, 500)

            elif action == "scroll":
                await page.mouse.wheel(0, 900)
                await page.mouse.move(1000, 600)
            
            elif action == "highlight":
                try:
                    loc = page.locator(f"text='{selector}'").first
                    if await loc.is_visible(timeout=2000):
                        box = await loc.bounding_box()
                        if box:
                            await page.mouse.move(box["x"] + box["width"]/2, box["y"] + box["height"]/2)
                        
                        # 🚨 SPOTLIGHT & POP-OUT ZOOM EFFECT
                        await loc.evaluate("""el => { 
                            document.getElementById('spotlight-overlay').style.display = 'block';
                            el.style.position = 'relative';
                            el.style.zIndex = '999999';
                            el.style.transform = 'scale(1.2)';
                            el.style.transition = 'transform 0.3s ease';
                            el.style.border = '4px solid red';
                            el.style.backgroundColor = 'white';
                            el.style.boxShadow = '0 0 40px red, 0 0 100px rgba(255,0,0,0.5)';
                            el.style.borderRadius = '8px';
                        }""")
                except:
                    print(f"⚠️ '{selector}' nahi mila.")
                    
            elif action == "celebrate":
                # 🚨 CONFETTI EFFECT
                await page.evaluate("window.shootConfetti()")

            # EXACT AUDIO SYNC
            time_taken = time.time() - start_time
            time_to_wait = expected_duration - time_taken
            
            if time_to_wait > 0:
                await asyncio.sleep(time_to_wait) 
            else:
                await asyncio.sleep(0.2)

            # RESET HIGHLIGHT
            if action == "highlight":
                try:
                    loc = page.locator(f"text='{selector}'").first
                    await loc.evaluate("""el => { 
                        document.getElementById('spotlight-overlay').style.display = 'none';
                        el.style.transform = 'scale(1)';
                        el.style.border = 'none';
                        el.style.boxShadow = 'none';
                        el.style.zIndex = 'auto';
                    }""")
                except: pass

        await page.close()
        await context.close()
        await browser.close()
        
        with open("temp_audio/audio_list.txt", "w") as f:
            for audio in audio_list:
                f.write(f"file '{os.path.basename(audio)}'\n")

if __name__ == "__main__":
    asyncio.run(main())
