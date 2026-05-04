# video-podcast-summary

将播客、访谈、演讲等长视频转换为精美的独立 HTML 总结页面，支持 YouTube、B站、X/Twitter 及本地视频，一键提取关键片段与中文字幕烧录。

## 功能

- **多平台视频支持** — YouTube、B站（bilibili.com）、X/Twitter（twitter.com / x.com）、本地视频文件，一键转录（Whisper API 或本地模型）
- **AI 结构化分析** 生成带时间戳的章节、要点、原话引述
- **精美 HTML 输出** 主题自适应设计，含亮色/暗色/品牌主题，自包含无依赖
- **精彩片段剪辑** 自动提取高价值片段为独立视频
- **中文字幕烧录** 将翻译后的字幕直接嵌入视频画面（无需 HTTP 服务）

## 目录结构

```
video-podcast-summary/
├── SKILL.md                     # 技能主定义（Agent 读取）
├── README.md                    # 本文件
├── references/
│   └── html-template.md         # HTML 组件参考（非固定模板）
├── scripts/
│   ├── transcribe.py            # 音频/视频转录
│   ├── extract_clips.py         # 视频片段提取
│   ├── translate_subtitles.py   # 字幕翻译（VTT → SRT + VTT）
│   └── burn_subtitles.py        # 字幕烧录到视频帧
└── examples/
    └── replit_ceo_interview_summary.html   # 完整 Demo（可通过 GitHub Pages 预览）
```

---

## 🚀 通过 AI Agent 一键使用

本 Skill 兼容市面主流通用 Agent 工具，安装后只需发一句话即可自动完成全部工作流。

**支持的 Agent 工具：**
- Claude Code
- GitHub Copilot / Codex CLI
- Cursor Agent
- OpenClaw / 其他遵循 Skill 协议的 Agent

### 安装方式

将本目录复制到你的 Agent skills 目录即可：

```bash
# Claude Code
cp -r video-podcast-summary ~/.claude/skills/

# 其他 Agent（路径可能不同，复制到对应 skills 目录即可）
```

Agent 会在首次使用时自动检测并安装缺失依赖（ffmpeg、yt-dlp、Python 包等），**无需你手动操作**。

### 一句话使用

安装后，直接在对话中发送：

> "帮我把这个视频转成 HTML 总结：https://www.youtube.com/watch?v=..."
>
> "把这个 B站视频生成结构化笔记：https://www.bilibili.com/video/BV..."
>
> "整理这条 X 访谈的要点：https://x.com/..."

Agent 会自动识别平台、下载/转录、分析内容、生成主题自适应的 HTML，全程无需干预。

---

## 依赖说明（Agent 自动处理）

> 以下依赖在 Agent 模式下会自动检测和安装，普通用户无需关注。手动执行时才需要自行安装。

### 系统工具

```bash
# macOS
brew install ffmpeg yt-dlp

# Ubuntu/Debian
sudo apt update
sudo apt install ffmpeg yt-dlp

# 若需 ffmpeg libass 支持（字幕烧录最快方案）
brew tap homebrew-ffmpeg/ffmpeg
brew install homebrew-ffmpeg/ffmpeg/ffmpeg
```

### Python 依赖

```bash
pip install openai-whisper googletrans-py opencv-python Pillow numpy
```

- `openai-whisper`：本地转录（可选，也可用 API）
- `googletrans-py`：字幕翻译
- `opencv-python Pillow numpy`：字幕烧录备用方案

### 环境变量（可选）

```bash
export OPENAI_API_KEY="sk-..."   # 使用 Whisper API 时设置
```

---

## 使用方式

### 方式一：AI Agent Skill 模式（推荐）

复制到 skills 目录后，直接对 Agent 描述需求即可。Agent 会自动：

1. 识别视频平台（YouTube / B站 / X / 本地文件）
2. 检查并安装缺失依赖
3. 提取视频元数据
4. 下载音频并转录
5. 使用大模型分析内容
6. 生成主题自适应的交互式 HTML
7. 按需提取视频片段并烧录字幕

### 方式二：手动分步执行

#### 1. 下载与转录

```bash
# YouTube / B站 / X：下载音频
yt-dlp -x --audio-format mp3 --audio-quality 0 -o "audio.%(ext)s" "URL"

# 转录（本地），同时输出 txt、json、vtt
python3 scripts/transcribe.py audio.mp3 --model base -o transcript.txt --json transcript.json --vtt transcript.vtt

# 或转录（API，更快）
python3 scripts/transcribe.py audio.mp3 --api -o transcript.txt --json transcript.json --vtt transcript.vtt
```

#### 2. 字幕翻译准备

`transcribe.py` 默认同时输出 `transcript.vtt`，可直接用于 `translate_subtitles.py`。

> 注：Agent skill 模式下，转录脚本会自动处理此步骤。

#### 3. AI 分析生成 JSON

将 `transcript.txt` 提供给大模型（如 Claude/GPT），使用 `SKILL.md` 步骤 5 的分析提示，获得结构化 JSON。

#### 4. 生成 HTML

根据 JSON 和 `references/html-template.md` 组件参考，自定义设计并生成 HTML。

#### 5. 提取视频片段

```bash
# 先下载完整视频（YouTube / B站 / X）
yt-dlp -f "best[height<=1080]" -o "video.%(ext)s" "URL"

# 提取片段
python3 scripts/extract_clips.py video.mp4 --config clips.json --out-dir clips/
```

`clips.json` 格式：

```json
[
  {"filename": "01_opening.mp4", "start": "00:00", "end": "02:07"},
  {"filename": "02_strategy.mp4", "start": "02:07", "end": "06:28"}
]
```

#### 6. 翻译并烧录字幕（非中文视频）

```bash
# 从完整 VTT 提取片段字幕并翻译
python3 scripts/translate_subtitles.py \
    --vtt full_video.en.vtt \
    --clips clips.json \
    --out-dir clips/

# 烧录字幕到视频（ffmpeg libass，最快）
# 见 SKILL.md 步骤 8 的 ffmpeg 命令

# 或烧录字幕（OpenCV 备用，无需 libass）
python3 scripts/burn_subtitles.py \
    --video video.mp4 \
    --clips clips.json \
    --subtitles-dir clips/ \
    --out-dir clips/
```

---

## 各脚本说明

| 脚本 | 功能 | 输入 | 输出 |
|------|------|------|------|
| `transcribe.py` | 音频/视频转录 | `.mp3`, `.mp4` 等 | `transcript.txt`, `transcript.json`, `transcript.vtt` |
| `extract_clips.py` | 按时间码提取片段 | 视频 + `clips.json` | `clips/*.mp4` |
| `translate_subtitles.py` | 提取并翻译字幕 | `full_video.en.vtt` + `clips.json` | `clips/*.zh.srt`, `clips/*.zh.vtt` |
| `burn_subtitles.py` | 将 SRT 烧录到视频 | 视频 + SRT | 带字幕的 `clips/*.mp4` |

---

## 🎨 在线预览

我们提供了一个完整的 Replit CEO 访谈 Demo，展示最终 HTML 输出的效果：

- **主题**：科技/AI 暗色主题（青绿/天蓝配色）
- **内容**：13 个结构化章节，含时间戳、关键引述、高亮框、视频片段嵌入与片段索引
- **交互**：滚动进度条、章节 fade-in、卡片悬浮、时间戳 hover 高亮

**在线预览地址**：
👉 [https://yuanjie05.github.io/video-podcast-summary/examples/replit_ceo_interview_summary.html](https://yuanjie05.github.io/video-podcast-summary/examples/replit_ceo_interview_summary.html)

> 提示：将本仓库开启 GitHub Pages（Source 设为 `/root` 或 `/docs`），`examples/` 目录下的 HTML 即可自动成为可访问的在线 Demo。

---

## 已知限制

- `googletrans-py` 偶尔会因 Google 反爬机制超时，已内置 3 次重试
- 字幕烧录的 ffmpeg `subtitles` 滤镜需要 libass 支持，否则需回退到 OpenCV（慢 10-20 倍）
- 本地 whisper 模型首次加载需下载（约 150MB-3GB，取决于模型大小）
- B站、X/Twitter 等平台可能因区域限制或反爬策略需要 yt-dlp 更新到最新版本

## License

MIT
