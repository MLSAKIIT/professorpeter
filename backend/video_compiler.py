import subprocess
import os
from typing import Optional

def overlay_image_on_video(template_path: str, image_path: str, output_path: str, position: str = "custom"):
    """
    Overlay an image (PNG) onto a video template using ffmpeg.
    The overlayed image will be 40% of video width, placed a little left of center and higher above the bottom.
    This step will NOT include any audio (video only).
    """
    # Get video dimensions using ffprobe
    import subprocess, json
    probe_cmd = [
        "ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
        "stream=width,height", "-of", "json", template_path
    ]
    probe_result = subprocess.run(probe_cmd, capture_output=True, text=True)
    dims = json.loads(probe_result.stdout)
    width = dims['streams'][0]['width']
    height = dims['streams'][0]['height']
    # Scale image to 40% of video width, keep aspect ratio
    scale_expr = f"w=iw*min(0.4*{width}/iw\\,0.4*{height}/ih):h=-1"
    # Move Peter Griffin higher: y = H-h-0.18*H (was 0.08*H)
    overlay_filter = f"overlay=x=(W-w)/2-0.05*W:y=H-h-0.18*H"
    filter_complex = f"[1:v]scale={scale_expr}[img];[0:v][img]{overlay_filter}[v]"
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-i", template_path,
        "-i", image_path,
        "-filter_complex", filter_complex,
        "-map", "[v]", "-an", "-c:v", "libx264", "-shortest", output_path
    ]
    subprocess.run(ffmpeg_cmd, check=True)


def merge_audio_with_video(video_path: str, audio_path: str, output_path: str):
    """
    Merge audio with video using ffmpeg (video from overlay, audio ONLY from TTS, trims to shortest).
    After merging, check if the output video has an audio stream. Print a warning if not.
    """
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", audio_path,
        "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-shortest",
        output_path
    ]
    subprocess.run(ffmpeg_cmd, check=True)

    # Check if output video has audio stream
    import json
    probe_cmd = [
        "ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
        "stream=index", "-of", "json", output_path
    ]
    probe_result = subprocess.run(probe_cmd, capture_output=True, text=True)
    try:
        info = json.loads(probe_result.stdout)
        if not info.get('streams'):
            print(f"⚠️ Warning: No audio stream found in {output_path} after merging!")
        else:
            print(f"✅ Audio stream present in {output_path} after merging.")
    except Exception as e:
        print(f"⚠️ Could not verify audio stream in {output_path}: {e}")


def burn_subtitles_on_video(video_path: str, subtitles_path: str, output_path: str, audio_path: Optional[str] = None):
    """
    Burn subtitles (SRT) onto a video using ffmpeg. Uses absolute paths and explicit stream mapping to preserve audio. If subtitles are missing or invalid, copy video and audio as-is. Converts backslashes to forward slashes for ffmpeg compatibility on Windows.
    After burning, check if the output video has an audio stream. If not, and audio_path is provided, re-merge the audio.
    """
    import os
    import subprocess
    import json
    subtitles_path = os.path.abspath(subtitles_path)
    video_path = os.path.abspath(video_path)
    output_path = os.path.abspath(output_path)
    # ffmpeg on Windows requires forward slashes in filter paths
    subtitles_path_ffmpeg = subtitles_path.replace(os.sep, '/')
    # If subtitles file does not exist or is empty, just copy video and audio
    if not os.path.exists(subtitles_path) or os.path.getsize(subtitles_path) == 0:
        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-c:v", "copy", "-c:a", "copy", "-shortest",
            output_path
        ]
        subprocess.run(ffmpeg_cmd, check=True)
        return
    # Otherwise, burn subtitles and preserve audio
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vf", f"subtitles={subtitles_path_ffmpeg}",
        "-map", "0:v:0",
        "-map", "0:a:0",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        output_path
    ]
    subprocess.run(ffmpeg_cmd, check=True)

    # Check if output video has audio stream
    probe_cmd = [
        "ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
        "stream=index", "-of", "json", output_path
    ]
    probe_result = subprocess.run(probe_cmd, capture_output=True, text=True)
    try:
        info = json.loads(probe_result.stdout)
        if not info.get('streams'):
            print(f"⚠️ Warning: No audio stream found in {output_path} after burning subtitles!")
            # If audio_path is provided, re-merge audio
            if audio_path:
                print(f"🔄 Re-merging audio from {audio_path} into {output_path}...")
                temp_path = output_path + ".tmp.mp4"
                ffmpeg_cmd = [
                    "ffmpeg", "-y",
                    "-i", output_path,
                    "-i", audio_path,
                    "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-shortest",
                    temp_path
                ]
                subprocess.run(ffmpeg_cmd, check=True)
                os.replace(temp_path, output_path)
                print(f"✅ Audio restored in {output_path}.")
        else:
            print(f"✅ Audio stream present in {output_path} after burning subtitles.")
    except Exception as e:
        print(f"⚠️ Could not verify audio stream in {output_path}: {e}")


def transcript_txt_to_srt(txt_path: str, srt_path: str, duration_per_line: float = 3.0):
    """
    Convert a plain text transcript to a proper SRT file (each chunk = one subtitle, fixed duration).
    Ensures correct SRT timestamp format (00:00:00,000), blank lines, and short lines for ffmpeg compatibility.
    """
    import textwrap
    with open(txt_path, "r", encoding="utf-8") as f:
        text = f.read().strip()
    # Split into chunks of ~8 words for each subtitle
    words = text.split()
    chunk_size = 8
    lines = [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    with open(srt_path, "w", encoding="utf-8") as f:
        for idx, line in enumerate(lines):
            start = idx * duration_per_line
            end = (idx + 1) * duration_per_line
            start_h = int(start // 3600)
            start_m = int((start % 3600) // 60)
            start_s = int(start % 60)
            start_ms = int((start - int(start)) * 1000)
            end_h = int(end // 3600)
            end_m = int((end % 3600) // 60)
            end_s = int(end % 60)
            end_ms = int((end - int(end)) * 1000)
            f.write(f"{idx+1}\n")
            f.write(f"{start_h:02}:{start_m:02}:{start_s:02},{start_ms:03} --> {end_h:02}:{end_m:02}:{end_s:02},{end_ms:03}\n")
            # Wrap line to max 40 chars per line for SRT
            for wrapped in textwrap.wrap(line, width=40):
                f.write(f"{wrapped}\n")
            f.write("\n")

if __name__ == "__main__":
    # Example usage
    template = "templates/template1.mp4"
    image = "peter.png"
    overlayed = "outputs/template1_with_peter.mp4"
    audio = "outputs/output.mp3"
    subtitles_txt = "outputs/subtitles.txt"
    subtitles_srt = "outputs/subtitles.srt"
    final_video = "outputs/final_video.mp4"
    final_video_with_subs = "outputs/final_video_with_subs.mp4"

    overlay_image_on_video(template, image, overlayed, position="middle")
    merge_audio_with_video(overlayed, audio, final_video)
    transcript_txt_to_srt(subtitles_txt, subtitles_srt)
    burn_subtitles_on_video(final_video, subtitles_srt, final_video_with_subs)
    print(f"✅ Final video with subtitles saved as {final_video_with_subs}")
