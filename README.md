# video-podcast-summary-skill

> 丢给 Agent 一个视频链接，收获一份设计精美、可离线打开、带时间戳和精彩对谈的交互式 HTML 总结。

支持 **YouTube / B站 / X(Twitter) / 本地视频**。Agent 自动处理下载、转录、分析、设计，全程无需干预。

---

## 🎯 这能帮你解决什么

| 你的痛点 | 它的解决方式 |
|---------|------------|
| 看了 2 小时播客/访谈，笔记散落各处，回头找不到重点 | Agent 自动生成结构化 HTML 总结：章节、时间戳、要点、原话引述，一页纸看完 |
| 视频里某个精彩观点只记得大概，想回看却翻不到位置 | 交互式目录 + 片段索引网格，点击时间戳直接跳转到对应内容 |
| 外语音频/视频啃得慢，想快速 get 核心信息 | 自动转录 + AI 分析 + 中文字幕烧录，输出中文总结页面 |
| 想分享视频精华给朋友，只能发一堆截图或丢一个长链接 | 一个 `.html` 文件即可分享，手机/电脑/离线都能看，体验像原生网页 |
| 视频平台太多，YouTube、B站、X 各用各的工具 | 一个 Skill 全覆盖，链接丢过去就行 |

---

## 🎨 先看看效果

> **注意：** GitHub Pages 在线预览展示完整的 HTML 结构和样式。点击视频封面将跳转至原视频平台观看。

### Demo 1：Replit CEO 深度访谈（科技/AI 主题）

[**👉 在线预览**](https://abysscat-yj.github.io/video-podcast-summary/examples/replit_ceo_interview_summary.html) · [📥 本地下载完整体验](https://github.com/abysscat-yj/video-podcast-summary/raw/master/examples/replit_ceo_interview_summary.html)

- **YouTube 1.5 小时深度访谈**，13 个结构化章节
- **精彩对谈文字还原**，原汁原味呈现嘉宾对话
- **章节时间戳可跳转 YouTube**，想看完整段落一键直达
- 科技/AI 风格：青绿 + 天蓝配色，深色沉浸式主题
- 关键引述（中文翻译）、彩色高亮框、对比表格、章节索引网格
- 滚动进度条、章节进入动画、卡片悬浮、时间戳 hover 高亮
- 完全自包含（无 CDN），可本地离线打开

### Demo 2：蔡康永 × 罗永浩（文化/人文 主题）

[**👉 在线预览**](https://abysscat-yj.github.io/video-podcast-summary/examples/cai_kangyong_luo_yonghao_summary.html) · [📥 本地下载完整体验](https://github.com/abysscat-yj/video-podcast-summary/raw/master/examples/cai_kangyong_luo_yonghao_summary.html)

- **B站 3.5 小时深度访谈**，10 个结构化章节
- **精彩对谈文字还原**，原汁原味呈现嘉宾对话
- **章节时间戳可跳转 B站**，想看完整段落一键直达
- 文化/人文风格：玫瑰红 + 琥珀金配色，衬线体引述，杂志质感
- 对谈还原块：呈现原汁原味的嘉宾对话场景
- 暗色/亮色自适应主题，移动端完美适配

---

## 🚀 一句话使用

**第 1 步：把 GitHub 链接丢给你的 Agent**

> 帮我安装这个 skill：https://github.com/abysscat-yj/video-podcast-summary

Agent 会自动从 GitHub 拉取代码、放到正确的 skills 目录、检查并安装 ffmpeg / yt-dlp / Python 依赖。

**第 2 步：丢视频链接**

> "帮我把这个视频转成 HTML 总结：https://www.youtube.com/watch?v=..."
>
> "把这个 B站视频生成结构化笔记：https://www.bilibili.com/video/BV..."
>
> "整理这条 X 访谈的要点：https://x.com/..."

Agent 自动完成：识别平台 → 下载音频 → 转录 → AI 分析 → 生成主题自适应 HTML。你什么都不用管。

**兼容 Agent**：Claude Code · GitHub Copilot / Codex CLI · Cursor Agent · OpenClaw · 任何支持从 GitHub 安装 Skill 的 Agent

---

## 📺 支持平台

| 平台 | 链接格式 | 状态 |
|------|---------|------|
| **YouTube** | `youtube.com/watch?v=` `youtu.be/` | ✅ 完整支持 |
| **B站** | `bilibili.com/video/BV` `bilibili.com/video/av` | ✅ 完整支持 |
| **X / Twitter** | `x.com/...` `twitter.com/...` | ✅ 视频 & Spaces |
| **本地视频** | `.mp4` `.mkv` `.mov` 等 | ✅ 完整支持 |

---

## 🛠 功能一览

- **多平台通吃** — YouTube、B站、X/Twitter、本地视频文件，一个命令全支持
- **AI 结构化分析** — 自动生成带时间戳的章节、核心要点、原话引述、对比表格
- **精美 HTML 输出** — 4 套主题自适应（科技/商业/教育/文化，暗色+亮色），自包含无 CDN
- **丰富微交互** — 滚动进度条、视口进入动画、卡片悬浮、时间戳高亮、渐变流动背景
- **精彩对谈还原** — 关键章节附 2-4 轮对话文字片段（中文翻译），还原访谈现场感
- **首屏封面背景** — 视频封面作为 Hero 背景，深色遮罩 + 白色文字，视觉冲击力更强

---

## 📂 目录结构

```
video-podcast-summary/
├── SKILL.md                     # 技能主定义（Agent 读取）
├── README.md                    # 本文件
├── references/
│   └── html-template.md         # HTML 组件参考：4 套主题系统 + 交互组件库
├── scripts/
│   └── transcribe.py            # 音频/视频转录（Whisper API / 本地模型）
└── examples/
    ├── replit_ceo_interview_summary.html   # Demo 1：科技/AI 主题
    └── cai_kangyong_luo_yonghao_summary.html   # Demo 2：文化/人文 主题（B站 3.5h 访谈）
```

---

## 🧰 技术细节

### Agent 模式（推荐）

复制到 skills 目录即可，Agent 自动检测并安装 ffmpeg、yt-dlp、Python 依赖，无需手动配置。

### 手动模式

如果你偏好自己跑脚本：

```bash
# 1. 下载音频（任意平台）
yt-dlp -x --audio-format mp3 --audio-quality 0 -o "audio.%(ext)s" "URL"

# 2. 转录
python3 scripts/transcribe.py audio.mp3 --model base -o transcript.txt --json transcript.json --vtt transcript.vtt

# 3. 用 AI 分析 transcript.txt 生成结构化 JSON（提示词见 SKILL.md）

# 4. 根据 JSON 和 references/html-template.md 生成 HTML
```

### 依赖说明

Agent 会自动处理以下依赖。手动执行时需要：

```bash
# 系统工具
brew install yt-dlp               # macOS
sudo apt install yt-dlp           # Ubuntu/Debian

# Python 依赖
pip install openai-whisper
```

---

## ⚠️ 已知限制

- 本地 whisper 模型首次加载需下载（约 150MB-3GB，取决于模型大小）
- B站、X/Twitter 等平台可能因区域限制或反爬策略需要 `yt-dlp -U` 更新到最新版本

## License

MIT
