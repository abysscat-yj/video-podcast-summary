#!/usr/bin/env python3
"""
使用 OpenCV + Pillow 将翻译后的字幕烧录到视频片段中。

需要：
    pip install opencv-python Pillow numpy

用法：
    python3 burn_subtitles.py \
        --video /path/to/full_video.mp4 \
        --clips clips.json \
        --subtitles-dir clips/ \
        --out-dir clips/ \
        --font /path/to/font.ttf \
        --font-size 26

clips.json 格式（与其他脚本统一）：
[
    {"filename": "01_opening_hook.mp4", "start": "00:00", "end": "00:55"},
    ...
]

字幕文件应命名为 `{clip_base}.zh.srt`（或 .en.srt）放在 --subtitles-dir 中。
如果片段没有字幕文件，则保留原始重新剪辑的视频。
"""

import argparse
import json
import os
import re
import subprocess
import sys

try:
    import cv2
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont
except ImportError as e:
    print(f"错误: 缺少依赖: {e}")
    print("运行: pip install opencv-python Pillow numpy")
    sys.exit(1)


def parse_srt(path):
    """将 SRT 解析为 (起始秒, 结束秒, 文本) 元组。"""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    cues = []
    for block in re.split(r"\n\n+", content.strip()):
        lines = block.strip().split("\n")
        if len(lines) < 3:
            continue
        m = re.match(
            r"(\d{2}):(\d{2}):(\d{2}),(\d{3})\s+-->\s+(\d{2}):(\d{2}):(\d{2}),(\d{3})",
            lines[1],
        )
        if not m:
            continue
        sh, sm, ss, sms, eh, em, es, ems = m.groups()
        start = int(sh) * 3600 + int(sm) * 60 + int(ss) + int(sms) / 1000
        end = int(eh) * 3600 + int(em) * 60 + int(es) + int(ems) / 1000
        text = "\n".join(lines[2:])
        cues.append((start, end, text))
    return cues


def render_subtitle_on_frame(frame_bgr, text, font, bottom_margin=50):
    h, w = frame_bgr.shape[:2]
    img = Image.fromarray(cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    max_width = int(w * 0.85)
    lines = []
    current_line = ""
    for char in text:
        test = current_line + char
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] > max_width and current_line:
            lines.append(current_line)
            current_line = char
        else:
            current_line = test
    if current_line:
        lines.append(current_line)
    line_height = font.size + 6
    total_h = len(lines) * line_height
    start_y = h - total_h - bottom_margin
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        text_w = bbox[2] - bbox[0]
        x = (w - text_w) // 2
        y = start_y + i * line_height
        for dx, dy in [
            (-2, -2), (-2, 2), (2, -2), (2, 2),
            (-2, 0), (2, 0), (0, -2), (0, 2),
        ]:
            draw.text((x + dx, y + dy), line, font=font, fill=(0, 0, 0))
        draw.text((x, y), line, font=font, fill=(255, 255, 255))
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)


def time_to_seconds(t) -> float:
    """将 HH:MM:SS、MM:SS 或数字秒数转换为秒数。"""
    if isinstance(t, (int, float)):
        return float(t)
    parts = t.strip().split(":")
    if len(parts) == 2:
        m, s = parts
        return int(m) * 60 + int(s)
    elif len(parts) == 3:
        h, m, s = parts
        return int(h) * 3600 + int(m) * 60 + int(s)
    else:
        raise ValueError(f"无效的时间格式: {t}")


def process_clip(video_path, out_path, start_sec, end_sec, srt_path, font, bottom_margin):
    duration = end_sec - start_sec
    raw_path = out_path.replace(".mp4", "_raw.mp4")

    # 步骤 1：用 ffmpeg 重新剪辑（强制关键帧以获得可拖动的进度条）
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start_sec), "-t", str(duration),
        "-i", video_path,
        "-c:v", "libx264", "-g", "30", "-keyint_min", "1",
        "-crf", "23", "-preset", "fast",
        "-c:a", "aac", "-b:a", "128k",
        "-movflags", "+faststart",
        raw_path,
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"  ffmpeg 剪辑失败: {e}")
        return False

    if not os.path.exists(srt_path):
        print(f"  无字幕文件，保留原始视频")
        os.replace(raw_path, out_path)
        return True

    cues = parse_srt(srt_path)
    if not cues:
        print(f"  字幕文件为空，保留原始视频")
        os.replace(raw_path, out_path)
        return True

    # 步骤 2：用 OpenCV 烧录字幕
    cap = cv2.VideoCapture(raw_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video_out = out_path.replace(".mp4", "_v.mp4")
    writer = cv2.VideoWriter(video_out, fourcc, fps, (w, h))

    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        t = frame_idx / fps
        active = None
        for start, end, text in cues:
            if start <= t < end:
                active = text
                break
        if active:
            frame = render_subtitle_on_frame(frame, active, font, bottom_margin)
        writer.write(frame)
        frame_idx += 1

    cap.release()
    writer.release()

    # 步骤 3：合并回音频（再次强制关键帧）
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", video_out,
            "-i", raw_path,
            "-c:v", "libx264", "-g", "30", "-keyint_min", "1",
            "-crf", "23", "-preset", "fast",
            "-c:a", "aac", "-b:a", "128k",
            "-movflags", "+faststart",
            "-shortest", out_path,
        ],
        check=True,
        capture_output=True,
    )

    os.remove(raw_path)
    os.remove(video_out)
    print(f"  -> 完成 ({len(cues)} 条字幕已烧录)")
    return True


def main():
    parser = argparse.ArgumentParser(description="将字幕烧录到视频片段中")
    parser.add_argument("--video", required=True, help="完整视频文件路径")
    parser.add_argument("--clips", required=True, help="片段定义的 JSON 文件")
    parser.add_argument("--subtitles-dir", default="clips", help="包含 .srt 文件的目录")
    parser.add_argument("--out-dir", default="clips", help="最终片段输出目录")
    parser.add_argument(
        "--font",
        default=None,
        help="TrueType 字体路径（默认自动查找系统字体）",
    )
    parser.add_argument("--font-size", type=int, default=26, help="字幕字号")
    parser.add_argument("--bottom-margin", type=int, default=50, help="底部边距（像素）")
    args = parser.parse_args()

    with open(args.clips, encoding="utf-8") as f:
        clips = json.load(f)

    os.makedirs(args.out_dir, exist_ok=True)

    # 自动查找可用中文字体
    font_path = args.font
    if not font_path:
        candidates = [
            "/System/Library/Fonts/STHeiti Medium.ttc",          # macOS
            "/System/Library/Fonts/PingFang.ttc",                # macOS 备选
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",      # Linux
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",    # Linux 备选
            "C:/Windows/Fonts/simhei.ttf",                       # Windows
            "C:/Windows/Fonts/msyh.ttc",                         # Windows 备选
        ]
        for c in candidates:
            if os.path.exists(c):
                font_path = c
                print(f"使用字体: {c}")
                break
        if not font_path:
            print("错误: 未找到系统中文字体。请通过 --font 手动指定。")
            sys.exit(1)

    font = ImageFont.truetype(font_path, args.font_size)

    for clip in clips:
        filename = clip["filename"]
        base = os.path.splitext(filename)[0]
        start_sec = time_to_seconds(clip["start"])
        end_sec = time_to_seconds(clip["end"])
        srt_path = os.path.join(args.subtitles_dir, f"{base}.zh.srt")
        out_path = os.path.join(args.out_dir, filename)

        print(f"片段: {base} ({start_sec}秒-{end_sec}秒)")
        process_clip(args.video, out_path, start_sec, end_sec, srt_path, font, args.bottom_margin)

    print("\n全部完成。")


if __name__ == "__main__":
    main()
