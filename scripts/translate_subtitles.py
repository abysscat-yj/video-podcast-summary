#!/usr/bin/env python3
"""
从完整 VTT 文件中提取每个视频片段的字幕段，
翻译为中文，并保存为 .zh.srt（主格式，兼容烧录脚本和 ffmpeg）和 .zh.vtt（备用）。

用法：
    python3 translate_subtitles.py \
        --vtt full_video.en.vtt \
        --clips clips.json \
        --out-dir clips/

clips.json 格式：
[
    {"filename": "01_opening_hook.mp4", "start": "00:00", "end": "00:55"},
    ...
]
"""

import argparse
import json
import os
import re
from pathlib import Path


def parse_vtt(path: str):
    """将 VTT 解析为 (起始秒, 结束秒, 文本) 元组列表。"""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    entries = []
    pattern = re.compile(
        r"(\d{2}:\d{2}:\d{2}\.\d{3})\s+-->\s+(\d{2}:\d{2}:\d{2}\.\d{3}).*?\n(.*?)(?=\n\n|\Z)",
        re.DOTALL,
    )
    for m in pattern.finditer(content):
        start_str, end_str, text = m.groups()
        start = time_to_seconds(start_str)
        end = time_to_seconds(end_str)
        text = re.sub(r"<[^>]+>", "", text).strip()
        text = re.sub(r"\s+", " ", text)
        if text:
            entries.append((start, end, text))
    return entries


def time_to_seconds(t: str) -> float:
    h, m, s = t.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


def seconds_to_vtt_time(s: float) -> str:
    hours = int(s // 3600)
    minutes = int((s % 3600) // 60)
    secs = s % 60
    return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"


def seconds_to_srt_time(s: float) -> str:
    hours = int(s // 3600)
    minutes = int((s % 3600) // 60)
    secs = int(s % 60)
    ms = int((s % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"


def translate_with_retry(translator, text, max_retries=3):
    """带重试的单条翻译。"""
    import time
    for attempt in range(max_retries):
        try:
            return translator.translate(text, src="en", dest="zh-cn")
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(0.5 * (attempt + 1))
            else:
                raise e
    return None


def translate_texts(texts: list[str], translator, chunk_size: int = 30) -> list[str]:
    """批量将文本翻译为中文。"""
    results = []
    for i in range(0, len(texts), chunk_size):
        chunk = texts[i : i + chunk_size]
        joined = "\n|||\n".join(chunk)
        try:
            translated = translate_with_retry(translator, joined)
            parts = translated.text.split("|||")
            if len(parts) != len(chunk):
                parts = []
                for t in chunk:
                    try:
                        r = translate_with_retry(translator, t)
                        parts.append(r.text)
                    except Exception:
                        parts.append(t)
            results.extend(parts)
        except Exception as e:
            print(f"  翻译错误: {e}，回退到原文")
            results.extend(chunk)
    return [r.strip() for r in results]


def main():
    parser = argparse.ArgumentParser(description="将片段字幕翻译为中文")
    parser.add_argument("--vtt", required=True, help="完整视频 VTT 字幕文件")
    parser.add_argument("--clips", required=True, help="包含片段时间范围的 JSON 配置")
    parser.add_argument("--out-dir", default="clips", help=".zh.srt 和 .zh.vtt 文件输出目录")
    args = parser.parse_args()

    try:
        from googletrans import Translator
    except ImportError:
        print("错误: 未安装 googletrans。运行: pip install googletrans-py")
        return

    print("正在解析 VTT...")
    entries = parse_vtt(args.vtt)
    print(f"总条目数: {len(entries)}")

    with open(args.clips, encoding="utf-8") as f:
        clips = json.load(f)

    translator = Translator()
    os.makedirs(args.out_dir, exist_ok=True)

    for clip in clips:
        filename = clip["filename"]
        base = Path(filename).stem
        start_sec = time_to_seconds(clip["start"])
        end_sec = time_to_seconds(clip["end"])
        srt_path = os.path.join(args.out_dir, f"{base}.zh.srt")

        if os.path.exists(srt_path):
            print(f"跳过（已存在）: {base}.zh.srt")
            continue

        clip_entries = [
            (s, e, t) for s, e, t in entries if e > start_sec and s < end_sec
        ]
        if not clip_entries:
            print(f"跳过（无字幕）: {base}")
            continue

        texts = []
        adjusted = []
        for s, e, t in clip_entries:
            adj_s = max(0, s - start_sec)
            adj_e = e - start_sec
            adjusted.append((adj_s, adj_e, t))
            texts.append(t)

        print(f"翻译中: {base} ({len(texts)} 条字幕)")
        translated = translate_texts(texts, translator)

        # 输出为 SRT（兼容 burn_subtitles.py 和 ffmpeg subtitles 滤镜）
        srt_lines = []
        idx = 1
        for (s, e, _), zh_text in zip(adjusted, translated):
            srt_lines.append(str(idx))
            srt_lines.append(f"{seconds_to_srt_time(s)} --> {seconds_to_srt_time(e)}")
            srt_lines.append(zh_text)
            srt_lines.append("")
            idx += 1

        srt_path = os.path.join(args.out_dir, f"{base}.zh.srt")
        with open(srt_path, "w", encoding="utf-8") as f:
            f.write("\n".join(srt_lines))
        print(f"  -> {srt_path}")

        # 同时输出 VTT 供备用
        vtt_path = os.path.join(args.out_dir, f"{base}.zh.vtt")
        lines = ["WEBVTT", "Kind: captions", "Language: zh-CN", ""]
        for (s, e, _), zh_text in zip(adjusted, translated):
            lines.append(f"{seconds_to_vtt_time(s)} --> {seconds_to_vtt_time(e)}")
            lines.append(zh_text)
            lines.append("")
        with open(vtt_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    print("完成。")


if __name__ == "__main__":
    main()
