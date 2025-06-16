import subprocess
import os
from typing import Optional
import re

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
    Burn subtitles (SRT) onto a video using ffmpeg. Uses relative path for subtitles (with forward slashes) to match working PowerShell command. If subtitles are missing or invalid, copy video and audio as-is. Automatically validates and fixes the SRT file before burning.
    After burning, check if the output video has an audio stream. If not, and audio_path is provided, re-merge the audio.
    """
    import os
    import subprocess
    import json
    # Validate and fix SRT before burning
    validate_and_fix_srt(subtitles_path)
    # Compute relative path from cwd (project root) to subtitles_path
    cwd = r"c:/professorpeter"
    rel_subtitles_path = os.path.relpath(subtitles_path, cwd)
    subtitles_path_ffmpeg = rel_subtitles_path.replace('\\', '/')
    # Use absolute paths for video and output, but relative for subtitles
    video_path = os.path.abspath(video_path)
    output_path = os.path.abspath(output_path)
    filter_arg = f'subtitles={subtitles_path_ffmpeg}:charenc=UTF-8'
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vf", filter_arg,
        "-map", "0:v:0",
        "-map", "0:a:0",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        output_path
    ]
    subprocess.run(ffmpeg_cmd, check=True, cwd=cwd)

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

def validate_and_fix_srt(srt_path: str):
    """
    Validates and fixes an SRT file for ffmpeg compatibility:
    - Ensures correct numbering
    - Ensures timestamps are in 00:00:00,000 format with commas
    - Ensures blank lines between blocks
    - Removes empty or malformed blocks
    - Wraps lines to max 40 chars
    """
    import textwrap
    with open(srt_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Split into blocks by double newlines
    blocks = re.split(r'\n{2,}', content.strip())
    fixed_blocks = []
    idx = 1
    for block in blocks:
        lines = block.strip().splitlines()
        if len(lines) < 2:
            continue
        # Fix numbering
        number = str(idx)
        # Fix timestamp line
        ts_line = lines[1] if len(lines) > 1 else ''
        ts_line = re.sub(r'(\d{2}:\d{2}:\d{2})[.,](\d{3})', r'\1,\2', ts_line)
        # Validate timestamp
        if not re.match(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', ts_line):
            continue
        # Wrap text lines
        text_lines = []
        for l in lines[2:]:
            text_lines.extend(textwrap.wrap(l, width=40))
        if not text_lines:
            continue
        fixed_block = f"{number}\n{ts_line}\n" + "\n".join(text_lines)
        fixed_blocks.append(fixed_block)
        idx += 1
    # Write back as UTF-8 without BOM
    with open(srt_path, 'w', encoding='utf-8') as f:
        # Remove BOM if present
        content_to_write = "\n\n".join(fixed_blocks) + "\n"
        if content_to_write.startswith('\ufeff'):
            content_to_write = content_to_write.lstrip('\ufeff')
        f.write(content_to_write)

def generate_video_with_subtitles(template_path: str, image_path: str, audio_path: str, subtitles_txt_path: str, output_path: str):
    """
    Full pipeline: overlay Peter Griffin, merge audio, generate SRT, burn subtitles, output to final_video.mp4.
    """
    import os
    from .video_compiler import overlay_image_on_video, merge_audio_with_video, transcript_txt_to_srt, burn_subtitles_on_video
    temp_overlay = output_path.replace('.mp4', '_overlay.mp4')
    temp_audio = output_path.replace('.mp4', '_audio.mp4')
    temp_srt = subtitles_txt_path.replace('.txt', '.srt')

    overlay_image_on_video(template_path, image_path, temp_overlay)
    merge_audio_with_video(temp_overlay, audio_path, temp_audio)
    transcript_txt_to_srt(subtitles_txt_path, temp_srt)
    # Burn subtitles directly into final_video.mp4
    burn_subtitles_on_video(temp_audio, temp_srt, output_path, audio_path=audio_path)
    # Clean up temp files if desired
    # for f in [temp_overlay, temp_audio, temp_srt]:
    #     if os.path.exists(f):
    #         os.remove(f)

if __name__ == "__main__":
    # Use correct paths relative to the backend directory
    template = "backend/templates/template1.mp4"
    image = "backend/templates/peter.png"
    overlayed = "backend/outputs/template1_with_peter.mp4"
    audio = "backend/outputs/output.mp3"
    subtitles_txt = "backend/outputs/subtitles.txt"
    subtitles_srt = "backend/outputs/subtitles.srt"
    final_video = "backend/outputs/final_video.mp4"
    final_video_with_subs = "backend/outputs/final_video_with_subs.mp4"

    overlay_image_on_video(template, image, overlayed, position="middle")
    merge_audio_with_video(overlayed, audio, final_video)
    transcript_txt_to_srt(subtitles_txt, subtitles_srt)
    burn_subtitles_on_video(final_video, subtitles_srt, final_video_with_subs)
    print(f"✅ Final video with subtitles saved as {final_video_with_subs}")

    # Remove all other files in outputs except final_video_with_subs.mp4
    import os
    outputs_dir = os.path.dirname(final_video_with_subs)
    for fname in os.listdir(outputs_dir):
        fpath = os.path.join(outputs_dir, fname)
        if fpath != final_video_with_subs and os.path.isfile(fpath):
            try:
                os.remove(fpath)
            except Exception as e:
                print(f"Warning: Could not delete {fpath}: {e}")
