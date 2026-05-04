#!/usr/bin/env python3
"""
使用 OpenAI Whisper API 或本地 whisper 转录音频/视频文件。
输出带时间戳的文本、JSON 和可选的 VTT 字幕。
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def transcribe_api(audio_path: str, api_key: str | None = None) -> dict:
    """使用 OpenAI Whisper API 转录。"""
    import urllib.request
    import urllib.error

    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("未设置 OPENAI_API_KEY")

    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    data = []
    data.append(f"--{boundary}".encode())
    data.append(b'Content-Disposition: form-data; name="model"')
    data.append(b"")
    data.append(b"whisper-1")
    data.append(f"--{boundary}".encode())
    data.append(b'Content-Disposition: form-data; name="response_format"')
    data.append(b"")
    data.append(b"verbose_json")
    data.append(f"--{boundary}".encode())
    data.append(f'Content-Disposition: form-data; name="file"; filename="{Path(audio_path).name}"'.encode())
    data.append(b"Content-Type: audio/mpeg")
    data.append(b"")
    with open(audio_path, "rb") as f:
        data.append(f.read())
    data.append(f"--{boundary}--".encode())

    body = b"\r\n".join(data)
    req = urllib.request.Request(
        "https://api.openai.com/v1/audio/transcriptions",
        data=body,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"API 错误: {e.code} {e.reason}")
        print(e.read().decode())
        raise


def transcribe_local(audio_path: str, model: str = "base") -> dict:
    """使用本地 openai-whisper 转录。"""
    import whisper

    print(f"加载本地 whisper 模型: {model}")
    m = whisper.load_model(model)
    print(f"正在转录 {audio_path} ...")
    result = m.transcribe(audio_path, verbose=True)
    return result


def format_timestamp(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def format_vtt_time(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"


def save_vtt(result: dict, out_path: str):
    """保存为 WebVTT 字幕文件。"""
    segments = result.get("segments", [])
    if not segments and "text" in result:
        segments = [{"start": 0, "end": 0, "text": result["text"]}]

    lines = ["WEBVTT", ""]
    for seg in segments:
        start = seg.get("start", 0)
        end = seg.get("end", 0)
        text = seg.get("text", "").strip()
        if text:
            lines.append(f"{format_vtt_time(start)} --> {format_vtt_time(end)}")
            lines.append(text)
            lines.append("")

    Path(out_path).write_text("\n".join(lines), encoding="utf-8")
    print(f"VTT 字幕已保存至 {out_path}")


def save_transcript(result: dict, out_path: str):
    """保存为 [HH:MM:SS] 说话人: 文本 格式的干净文本文件。"""
    segments = result.get("segments", [])
    if not segments and "text" in result:
        # API verbose_json 不总是有 segments；创建一个
        segments = [{"start": 0, "end": 0, "text": result["text"]}]

    lines = []
    for seg in segments:
        start = seg.get("start", 0)
        text = seg.get("text", "").strip()
        speaker = seg.get("speaker", "")
        prefix = f"[{format_timestamp(start)}]"
        if speaker:
            prefix += f" {speaker}:"
        lines.append(f"{prefix} {text}")

    Path(out_path).write_text("\n".join(lines), encoding="utf-8")
    print(f"转录稿已保存至 {out_path}")


def main():
    parser = argparse.ArgumentParser(description="将音频转录为带时间戳的文本")
    parser.add_argument("input", help="音频或视频文件路径")
    parser.add_argument("-o", "--output", default="transcript.txt", help="输出文本文件")
    parser.add_argument("--api", action="store_true", help="使用 OpenAI API")
    parser.add_argument("--model", default="base", help="本地 whisper 模型大小 (tiny/base/small/medium/large)")
    parser.add_argument("--json", default="transcript.json", help="输出原始 JSON 文件")
    parser.add_argument("--vtt", default="transcript.vtt", help="输出 VTT 字幕文件")
    args = parser.parse_args()

    audio_path = args.input

    # 如果是视频，先提取音频
    ext = Path(audio_path).suffix.lower()
    if ext in (".mp4", ".mkv", ".mov", ".avi", ".webm"):
        audio_tmp = Path(audio_path).with_suffix(".mp3")
        if not audio_tmp.exists():
            print(f"正在提取音频到 {audio_tmp} ...")
            subprocess.run(
                ["ffmpeg", "-i", audio_path, "-q:a", "0", "-map", "a", str(audio_tmp), "-y"],
                check=True,
            )
        audio_path = str(audio_tmp)

    if args.api:
        result = transcribe_api(audio_path)
    else:
        result = transcribe_local(audio_path, model=args.model)

    # 保存原始 JSON
    Path(args.json).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"原始 JSON 已保存至 {args.json}")

    # 保存格式化文本
    save_transcript(result, args.output)

    # 保存 VTT 字幕
    save_vtt(result, args.vtt)


if __name__ == "__main__":
    main()
