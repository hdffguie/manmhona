import os
import subprocess
import glob
import urllib.request

def download_bgm():
    bgm_file = "temp_audio/bgm.mp3"
    print("🎵 Background Music Download kar raha hu...")
    try:
        req = urllib.request.Request(
            "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=lofi-study-112191.mp3",
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req) as response, open(bgm_file, 'wb') as out_file:
            out_file.write(response.read())
        return bgm_file
    except Exception as e:
        print(f"⚠️ BGM download fail hua: {e}. Bina music ke proceed kar rahe hain.")
        return None

def merge():
    # 🚨 FIX: Yahan folder automatically ban jayega taaki error na aaye!
    os.makedirs("final_output", exist_ok=True)
    os.makedirs("temp_audio", exist_ok=True)
    
    print("✂️ Audio files ko combine kar raha hu...")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "temp_audio/audio_list.txt", "-c", "copy", "temp_audio/final_voice.mp3"])
    
    video_files = glob.glob("temp_video/*.webm")
    if not video_files:
        print("❌ Video file (webm) nahi mili. Playwright ne record nahi kiya.")
        return
        
    raw_video = video_files[0]
    final_output = "final_output/Final_Review_Test.mp4"
    bgm_file = download_bgm()
    
    print("🎬 Video Export ho rahi hai, kripya pratiksha karein...")
    
    if bgm_file:
        cmd = [
            "ffmpeg", "-y", 
            "-i", raw_video, 
            "-i", "temp_audio/final_voice.mp3", 
            "-stream_loop", "-1", "-i", bgm_file,
            "-filter_complex", "[1:a]volume=1.5[voice]; [2:a]volume=0.08[bgm]; [voice][bgm]amix=inputs=2:duration=first:dropout_transition=0[a_out]",
            "-map", "0:v", "-map", "[a_out]",
            "-c:v", "libx264", "-preset", "fast", 
            "-c:a", "aac", 
            "-shortest", final_output
        ]
    else:
        cmd = [
            "ffmpeg", "-y", 
            "-i", raw_video, 
            "-i", "temp_audio/final_voice.mp3", 
            "-filter_complex", "[1:a]volume=1.5[a_out]",
            "-map", "0:v", "-map", "[a_out]",
            "-c:v", "libx264", "-preset", "fast", 
            "-c:a", "aac", 
            "-shortest", final_output
        ]
        
    subprocess.run(cmd, check=True)
    
    print(f"🎉 MASTERPIECE READY! Aapki video yaha save hai: {final_output}")

if __name__ == "__main__":
    merge()
