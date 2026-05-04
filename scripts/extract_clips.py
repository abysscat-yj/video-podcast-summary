#!/usr/bin/env python3
"""
使用 ffmpeg 从源视频中提取视频片段。
读取定义片段起始/结束时间和文件名的 JSON 配置。
"""

import argparse
import json
import subprocess
from pathlib import Path


def time_to_seconds(t: str) -> float:
    """将 HH:MM:SS 或 MM:SS 转换为秒数。"""
    parts = t.strip().split(":")
    if len(parts) == 2:
        m, s = parts
        return int(m) * 60 + int(s)
    elif len(parts) == 3:
        h, m, s = parts
        return int(h) * 3600 + int(m) * 60 + int(s)
    else:
        raise ValueError(f"无效的时间格式: {t}")


def extract_clip(video_path: str, start: str, end: str, out_path: str):
    """使用 ffmpeg 提取片段。"""
    start_sec = time_to_seconds(start)
    end_sec = time_to_seconds(end)
    duration = end_sec - start_sec
    if duration <= 0:
        print(f"跳过无效时长: {start} -> {end}")
        return

    cmd = [
        "ffmpeg",
        "-ss", str(start_sec),
        "-t", str(duration),
        "-i", video_path,
        "-c:v", "libx264",
        "-g", "30",
        "-keyint_min", "1",
        "-crf", "23",
        "-preset", "fast",
        "-c:a", "aac",
        "-b:a", "128k",
        "-movflags", "+faststart",
        "-y",
        out_path,
    ]
    print(f"正在提取 {out_path} ({start} - {end}, {duration:.0f}秒)")
    subprocess.run(cmd, check=True)


def main():
    parser = argparse.ArgumentParser(description="通过 ffmpeg 提取视频片段")
    parser.add_argument("video", help="源视频文件路径")
    parser.add_argument("--config", required=True, help="包含片段数组的 JSON 配置文件")
    parser.add_argument("--out-dir", default="clips", help="片段输出目录")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    with open(args.config, encoding="utf-8") as f:
        clips = json.load(f)

    for clip in clips:
        filename = clip.get("filename")
        start = clip.get("start")
        end = clip.get("end")
        if not all([filename, start, end]):
            continue
        out_path = out_dir / filename
        if out_path.exists():
            print(f"跳过已存在: {out_path}")
            continue
        try:
            extract_clip(args.video, start, end, str(out_path))
        except subprocess.CalledProcessError as e:
            print(f"提取 {filename} 失败: {e}")

    print(f"完成。片段已保存至 {out_dir}")


if __name__ == "__main__":
    main()
