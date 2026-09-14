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
    return audio_path, float(subprocess.check_output(dur_cmd).decode().strip())

async def inject_effects(page):
    js_code = """
        if (!document.getElementById('fake-mouse')) {
            const cursor = document.createElement('div');
            cursor.id = 'fake-mouse';
            cursor.style.position = 'absolute';
            cursor.style.width = '24px'; cursor.style.height = '24px';
            cursor.style.backgroundImage = 'url("data:image/svg+xml;utf8,<svg xmlns=\\'http://www.w3.org/2000/svg\\' width=\\'24\\' height=\\'24\\' viewBox=\\'0 0 24 24\\'><path fill=\\'red\\' stroke=\\'white\\' stroke-width=\\'2\\' d=\\'M5.5 3.21V20.8c0 .45.54.67.85.35l4.86-4.86 3.8 8.04c.15.33.54.46.87.31l2.25-1.06c.33-.15.46-.54.31-.87l-3.75-7.96 5.8-1.5c.44-.11.53-.69.17-.96L6.37 2.87c-.32-.24-.87-.01-.87.34z\\'/></svg>")';
            cursor.style.zIndex = '2147483647';
            cursor.style.pointerEvents = 'none';
            cursor.style.transition = 'top 0.3s ease, left 0.3s ease';
            document.body.appendChild(cursor);
            document.addEventListener('mousemove', (e) => { cursor.style.left = e.pageX + 'px'; cursor.style.top = e.pageY + 'px'; });
        }
        
        if (!document.getElementById('spotlight-overlay')) {
            const overlay = document.createElement('div');
            overlay.id = 'spotlight-overlay';
            overlay.style.position = 'fixed';
            overlay.style.top = '0'; overlay.style.left = '0';
            overlay.style.width = '100vw'; overlay.style.height = '100vh';
            overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.25)'; /* Halka Dark */
            overlay.style.zIndex = '2147483645';
            overlay.style.display = 'none';
            document.body.appendChild(overlay);
        }

        window.shootConfetti = function() {
            for(let i=0; i<50; i++) {
                let conf = document.createElement('div');
                conf.style.position = 'fixed';
                conf.style.left = Math.random() * 100 + 'vw';
                conf.style.top = '-10px';
                conf.style.width = '12px'; conf.style.height = '12px';
                conf.style.backgroundColor = ['red','yellow','blue','green','#ff00ff'][Math.floor(Math.random()*5)];
                conf.style.zIndex = '2147483647';
                conf.style.transition = 'top 2s ease-in, transform 2s ease-in';
                document.body.appendChild(conf);
                setTimeout(() => { conf.style.top = '110vh'; conf.style.transform = 'rotate(' + Math.random()*360 + 'deg)'; }, 50);
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
            record_video_size={'width': 1920, 'height': 1080},
            # Anti-bot bypass karne ke liye asli Chrome ki pehchan
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        audio_list = []

        for idx, step in enumerate(commands):
            action, selector, text = step.get("action"), step.get("selector", ""), step.get("text", "")
            print(f"🎬 {action}: {text[:40]}...")
            
            audio_path, expected_duration = generate_audio(text, idx)
            audio_list.append(audio_path)
            start_time = time.time()

            if action == "google_search":
                await page.goto("https://www.google.com", wait_until="domcontentloaded")
                await inject_effects(page)
                
                search_box = page.locator("textarea[name='q'], input[name='q']").first
                await search_box.click()
                await asyncio.sleep(0.5)
                
                # Ek-ek letter type karega
                await search_box.type(selector, delay=100)
                await asyncio.sleep(1) 
                
                # 🚨 BINA ENTER DABAYE DIRECT WEBSITE KHOLEGA (No Captcha Issue)
                await page.goto(target_url, wait_until="domcontentloaded")
                await inject_effects(page)
                await page.mouse.move(960, 500)

            elif action == "scroll":
                await page.mouse.wheel(0, 700)
                await page.mouse.move(1000, 600)
            
            elif action == "highlight":
                try:
                    # 🚨 SMART FINDER: Agar exact nahi mila to us se milta julta text dhoondega
                    loc = page.get_by_text(selector, exact=False).first
                    
                    if await loc.is_visible(timeout=2000):
                        box = await loc.bounding_box()
                        if box:
                            await page.mouse.move(box["x"] + box["width"]/2, box["y"] + box["height"]/2)
                        
                        await loc.evaluate("""el => { 
                            document.getElementById('spotlight-overlay').style.display = 'block';
                            el.style.position = 'relative';
                            el.style.zIndex = '2147483646';
                            el.style.transform = 'scale(1.08)';
                            el.style.transition = 'transform 0.3s ease';
                            el.style.border = '3px solid #ff2b2b';
                            el.style.backgroundColor = 'rgba(255,255,255,0.95)';
                            el.style.boxShadow = '0 0 16px rgba(255, 0, 0, 0.85)';
                            el.style.borderRadius = '5px';
                        }""")
                    else:
                        print(f"⚠️ Highlighter skip: '{selector}' screen par visible nahi hai.")
                except Exception as e:
                    print(f"⚠️ Highlighter error: {e}")
                    
            elif action == "celebrate":
                await page.evaluate("window.shootConfetti()")

            time_to_wait = expected_duration - (time.time() - start_time)
            if time_to_wait > 0:
                await asyncio.sleep(time_to_wait) 
            else:
                await asyncio.sleep(0.5)

            if action == "highlight":
                try:
                    loc = page.get_by_text(selector, exact=False).first
                    await loc.evaluate("""el => { 
                        document.getElementById('spotlight-overlay').style.display = 'none';
                        el.style.transform = 'none';
                        el.style.border = 'none';
                        el.style.boxShadow = 'none';
                        el.style.zIndex = 'auto';
                        el.style.backgroundColor = 'transparent';
                    }""")
                except: pass

        await page.close(); await context.close(); await browser.close()
        
        with open("temp_audio/audio_list.txt", "w") as f:
            for audio in audio_list: f.write(f"file '{os.path.basename(audio)}'\n")

if __name__ == "__main__":
    asyncio.run(main())
