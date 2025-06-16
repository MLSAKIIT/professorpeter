import subprocess
import os
from typing import Optional
import re
from pydub import AudioSegment

def overlay_image_on_video(template_path: str, image_path: str, output_path: str, position: str = "custom"):
    """
    Overlay an image (PNG) onto a video template using ffmpeg.
    The overlayed image will be 40% of video width, placed at the bottom and slightly left of center.
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
    # Place Peter at the bottom, slightly right of center
    overlay_filter = f"overlay=x=(W-w)/2-0.05*W:y=H-h-0.05*H"
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
    Subtitles are placed in the center (bottom center, Alignment=2).
    """
    import os
    import subprocess
    import json    # Validate and fix SRT before burning
    validate_and_fix_srt(subtitles_path)
    # Compute relative path from cwd (project root) to subtitles_path
    cwd = r"c:/professorpeter"
    rel_subtitles_path = os.path.relpath(subtitles_path, cwd)
    subtitles_path_ffmpeg = rel_subtitles_path.replace('\\', '/')    # Place subtitles at the center of video screen using simple, reliable styling
    # Using basic subtitle filter without complex force_style that might fail
    filter_arg = f"subtitles={subtitles_path_ffmpeg}:force_style='Fontsize=24,PrimaryColour=&Hffffff,OutlineColour=&H000000,Outline=2,Alignment=2,MarginV=200,MarginL=0'"
    video_path = os.path.abspath(video_path)
    output_path = os.path.abspath(output_path)
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

def transcript_txt_to_word_srt(txt_path: str, srt_path: str, duration_per_word: float = 0.5):
    """
    Convert a plain text transcript to a word-by-word SRT file (each word = one subtitle, fixed duration per word).
    Ensures correct SRT timestamp format (00:00:00,000), blank lines, and short lines for ffmpeg compatibility.
    """
    with open(txt_path, "r", encoding="utf-8") as f:
        text = f.read().strip()
    words = text.split()
    with open(srt_path, "w", encoding="utf-8") as f:
        for idx, word in enumerate(words):
            start = idx * duration_per_word
            end = (idx + 1) * duration_per_word
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
            f.write(f"{word}\n\n")

def transcript_txt_to_word_srt_synced(txt_path: str, srt_path: str, audio_path: str):
    """
    Convert a plain text transcript to a word-by-word SRT file synchronized with audio duration.
    Gets actual audio duration and distributes words evenly across that time.
    """
    import subprocess
    import json
    
    # Get audio duration using ffprobe
    probe_cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "json", audio_path
    ]
    probe_result = subprocess.run(probe_cmd, capture_output=True, text=True)
    audio_info = json.loads(probe_result.stdout)
    audio_duration = float(audio_info['format']['duration'])
    
    with open(txt_path, "r", encoding="utf-8") as f:
        text = f.read().strip()
    words = text.split()
    
    # Calculate duration per word based on actual audio length
    duration_per_word = audio_duration / len(words) if len(words) > 0 else 0.5
    
    with open(srt_path, "w", encoding="utf-8") as f:
        for idx, word in enumerate(words):
            start = idx * duration_per_word
            end = (idx + 1) * duration_per_word
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
            f.write(f"{word}\n\n")

def transcript_txt_to_natural_srt_synced(txt_path: str, srt_path: str, audio_path: str):
    """
    Convert a plain text transcript to an SRT file synchronized with audio duration.
    Creates natural phrase timing that matches the actual audio.
    """
    import subprocess
    import json
    import re
    
    # Get audio duration using ffprobe
    probe_cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "json", audio_path
    ]
    probe_result = subprocess.run(probe_cmd, capture_output=True, text=True)
    audio_info = json.loads(probe_result.stdout)
    audio_duration = float(audio_info['format']['duration'])
    
    with open(txt_path, "r", encoding="utf-8") as f:
        text = f.read().strip()
    
    # Split text into sentences first
    sentences = re.split(r'[.!?]+', text)
    clean_sentences = [s.strip() for s in sentences if s.strip()]
    
    # Create subtitle chunks - group sentences into 2-3 word chunks for better reading
    chunks = []
    for sentence in clean_sentences:
        words = sentence.split()
        # Group words into chunks of 2-4 words for natural reading
        for i in range(0, len(words), 3):
            chunk = ' '.join(words[i:i+3])
            if chunk:
                chunks.append(chunk)
    
    if not chunks:
        return
    
    # Calculate timing - distribute evenly across audio duration
    time_per_chunk = audio_duration / len(chunks)
    
    with open(srt_path, "w", encoding="utf-8") as f:
        for idx, chunk in enumerate(chunks):
            start_time = idx * time_per_chunk
            end_time = min((idx + 1) * time_per_chunk, audio_duration)
            
            # Format timestamps
            start_h = int(start_time // 3600)
            start_m = int((start_time % 3600) // 60)
            start_s = int(start_time % 60)
            start_ms = int((start_time - int(start_time)) * 1000)
            
            end_h = int(end_time // 3600)
            end_m = int((end_time % 3600) // 60)
            end_s = int(end_time % 60)
            end_ms = int((end_time - int(end_time)) * 1000)
            
            f.write(f"{idx+1}\n")
            f.write(f"{start_h:02}:{start_m:02}:{start_s:02},{start_ms:03} --> {end_h:02}:{end_m:02}:{end_s:02},{end_ms:03}\n")
            f.write(f"{chunk}\n\n")

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
    transcript_txt_to_word_srt(subtitles_txt_path, temp_srt)
    # Burn subtitles directly into final_video.mp4
    burn_subtitles_on_video(temp_audio, temp_srt, output_path, audio_path=audio_path)
    # Clean up temp files if desired
    # for f in [temp_overlay, temp_audio, temp_srt]:
    #     if os.path.exists(f):
    #         os.remove(f)

def generate_subtitles(audio_path, output_path):
    """Generate subtitles from audio with word-by-word timing"""
    try:
        # Load audio file
        audio = AudioSegment.from_file(audio_path)
        duration = len(audio) / 1000.0  # Convert to seconds
        
        # Example text - replace this with your actual text
        text = "This is a test subtitle that will appear word by word."
        words = text.split()
        
        # Calculate timing for each word
        words_with_timing = []
        current_time = 0
        
        for i, word in enumerate(words):
            # Calculate word duration based on length
            word_duration = len(word) * 0.1  # 100ms per character
            word_duration = max(0.3, min(word_duration, 0.8))  # Keep between 300ms and 800ms
            
            # Add extra pause after full stops
            if word.endswith('.'):
                word_duration += 0.5  # Add 500ms pause after full stop
            
            words_with_timing.append({
                "start": current_time,
                "end": current_time + word_duration,
                "text": word
            })
            current_time += word_duration
        
        # Write subtitles in SRT format with improved positioning
        with open(output_path, 'w', encoding='utf-8') as f:
            for i, word in enumerate(words_with_timing, 1):
                start_time = format_time(word["start"])
                end_time = format_time(word["end"])
                
                f.write(f"{i}\n")
                f.write(f"{start_time} --> {end_time}\n")
                # Add ASS styling for better positioning
                f.write(f"{{\\an8\\pos(960,540)\\fs24}}{word['text']}\n\n")
        
        return True
    except Exception as e:
        print(f"Error generating subtitles: {str(e)}")
        return False

def format_time(seconds):
    """Convert seconds to SRT time format (HH:MM:SS,mmm)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{int(seconds):02d},{milliseconds:03d}"

if __name__ == "__main__":    
    # Use correct paths relative to the backend directory
    template = "templates/template1.mp4"
    image = "templates/peter.png"
    overlayed = "outputs/template1_with_peter.mp4"
    audio = "outputs/output.mp3"
    subtitles_txt = "outputs/subtitles.txt"
    subtitles_srt = "outputs/subtitles.srt"
    final_video = "outputs/final_video.mp4"
    final_video_with_subs = "outputs/final_video_with_subs.mp4"

    overlay_image_on_video(template, image, overlayed, position="middle")
    merge_audio_with_video(overlayed, audio, final_video)
    transcript_txt_to_natural_srt_synced(subtitles_txt, subtitles_srt, audio)
    burn_subtitles_on_video(final_video, subtitles_srt, final_video_with_subs)
    print(f"✅ Final video with subtitles saved as {final_video_with_subs}")
