import os
import subprocess
import glob

def merge():
    print("✂️ Audio aur Video ko combine kiya jaa raha hai...")
    
    # 1. Saari audio files ko ek file me jodo
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "temp_audio/audio_list.txt", "-c", "copy", "temp_audio/final_audio.mp3"])
    
    # 2. Playwright ne jo video banayi hai use dhoondho (random name hota hai .webm)
    video_files = glob.glob("temp_video/*.webm")
    if not video_files:
        print("❌ Video file nahi mili!")
        return
    
    raw_video = video_files[0]
    final_output = "final_output/Final_Review_Test.mp4"
    
    # 3. Video aur Final Audio ko mux (merge) karo
    cmd = [
        "ffmpeg", "-y", 
        "-i", raw_video, 
        "-i", "temp_audio/final_audio.mp3", 
        "-c:v", "libx264", "-preset", "fast", 
        "-c:a", "aac", 
        "-shortest", final_output
    ]
    subprocess.run(cmd, check=True)
    
    print(f"🎉 TEST SUCCESSFUL! Aapki video yaha save hai: {final_output}")

if __name__ == "__main__":
    merge()
