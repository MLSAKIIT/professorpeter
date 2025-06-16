import subprocess
import os
from typing import Optional

def overlay_image_on_video(template_path: str, image_path: str, output_path: str, position: str = "bottomright"):
    """
    Overlay an image (PNG) onto a video template using ffmpeg.
    position: 'bottomright', 'topleft', etc.
    """
    # Position mapping for ffmpeg overlay
    positions = {
        "bottomright": "overlay=W-w-10:H-h-10",
        "topleft": "overlay=10:10",
        "topright": "overlay=W-w-10:10",
        "bottomleft": "overlay=10:H-h-10"
    }
    overlay_filter = positions.get(position, positions["bottomright"])
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-i", template_path,
        "-i", image_path,
        "-filter_complex", overlay_filter,
        "-codec:a", "copy",
        output_path
    ]
    subprocess.run(ffmpeg_cmd, check=True)


def merge_audio_with_video(video_path: str, audio_path: str, output_path: str):
    """
    Merge audio with video using ffmpeg (keeps video, replaces audio, trims to shortest).
    """
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "copy", "-c:a", "aac", "-shortest",
        output_path
    ]
    subprocess.run(ffmpeg_cmd, check=True)


def burn_subtitles_on_video(video_path: str, subtitles_path: str, output_path: str):
    """
    Burn subtitles (SRT) onto a video using ffmpeg.
    """
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vf", f"subtitles={subtitles_path}",
        "-c:a", "copy",
        output_path
    ]
    subprocess.run(ffmpeg_cmd, check=True)


def transcript_txt_to_srt(txt_path: str, srt_path: str, duration_per_line: float = 3.0):
    """
    Convert a plain text transcript to a simple SRT file (each line = one subtitle, fixed duration).
    """
    with open(txt_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    with open(srt_path, "w", encoding="utf-8") as f:
        for idx, line in enumerate(lines):
            start = idx * duration_per_line
            end = (idx + 1) * duration_per_line
            f.write(f"{idx+1}\n")
            f.write(f"{int(start//60):02}:{int(start%60):02},000 --> {int(end//60):02}:{int(end%60):02},000\n")
            f.write(f"{line}\n\n")

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

    overlay_image_on_video(template, image, overlayed, position="bottomright")
    merge_audio_with_video(overlayed, audio, final_video)
    transcript_txt_to_srt(subtitles_txt, subtitles_srt)
    burn_subtitles_on_video(final_video, subtitles_srt, final_video_with_subs)
    print(f"✅ Final video with subtitles saved as {final_video_with_subs}")
