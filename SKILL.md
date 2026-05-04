---
name: video-podcast-summary
description: 将播客或访谈视频转换为设计精美的独立 HTML 总结页面。当用户希望将 YouTube、B站、X/Twitter 视频、播客节目或访谈转换为结构化 HTML 文档、视频总结页面或摘要时触发此技能。也适用于用户提到"播客转 HTML"、"视频总结"、"访谈笔记"、"从视频生成总结页面"，或希望从长视频内容中提取关键洞察和片段的场景。支持 YouTube、B站、X/Twitter 链接和本地视频文件。
---

# 播客视频总结

将长视频内容（播客、访谈、演讲）转换为精美的主题自适应 HTML 总结页面，包含结构化章节、时间戳、关键引述、高亮框和可选的嵌入式视频片段。支持 YouTube、B站、X/Twitter 及本地视频文件。

## 输出示例

最终 HTML 页面包含：
- 首屏区域：标题、副标题、嘉宾/主持人元信息
- 交互式目录
- 带时间戳的编号内容章节
- 关键引述的引用块
- 洞察的彩色高亮框
- 对比表格
- 流程可视化的箭头流程图
- 嵌入式视频片段（可选，通过 ffmpeg 提取）
- 片段索引网格，便于快速导航
- 关键要点总结
- 完全响应式、多主题设计（暗色/亮色/品牌自适应，无外部依赖）
- 丰富微交互：滚动进度条、章节进入动画、卡片悬浮、时间戳 hover 高亮

## 工作流程

### 步骤 1：识别输入

确定用户提供的内容：
- **YouTube 链接**：`https://www.youtube.com/watch?v=...` 或 `https://youtu.be/...`
- **B站链接**：`https://www.bilibili.com/video/BV...` 或 `https://www.bilibili.com/video/av...`
- **X/Twitter 链接**：`https://twitter.com/...` 或 `https://x.com/...`（注：X 上的视频/Space 音频）
- **本地视频文件**：`.mp4`、`.mkv`、`.mov` 等文件的绝对或相对路径
- **仅音频/转录稿**：音频文件路径或转录文本

### 步骤 2：检查依赖

检查可用工具。静默运行以下命令：
```bash
which yt-dlp || echo "缺少 yt-dlp"
which ffmpeg || echo "缺少 ffmpeg"
python3 -c "import whisper" 2>/dev/null || echo "缺少 whisper"
```

**完整工作流程需要：**
- `yt-dlp`（用于 YouTube、B站、X 等平台下载）
- `ffmpeg`（用于视频片段提取）
- `openai-whisper` 或 API 访问（用于转录）

**Agent 行为：** 若检测到缺失依赖，Agent 应自动尝试安装（如 `brew install ffmpeg yt-dlp` / `apt install ffmpeg yt-dlp` / `pip install openai-whisper` 等），无需用户手动操作。仅在自动安装失败时，才向用户展示简洁的修复指引，或回退到仅转录模式（用户手动提供转录稿）。

### 步骤 3：提取元数据

**YouTube：**
```bash
curl -s "https://www.youtube.com/oembed?url=<YOUTUBE_URL>&format=json"
```
也可尝试通过 `yt-dlp --print-json --skip-download <URL>` 获取时长和描述。

**B站：**
```bash
# 通过 yt-dlp 获取（推荐，可获取标题、时长、封面等完整信息）
yt-dlp --print-json --skip-download <BILIBILI_URL>

# 或通过 bvid 调用 B站 API（备用）
# 从 URL 提取 BV 号后：curl -s "https://api.bilibili.com/x/web-interface/view?bvid=BV..."
```

**X/Twitter：**
```bash
# 通过 yt-dlp 获取元数据（支持 X 视频和 Spaces 音频）
yt-dlp --print-json --skip-download <X_URL>
```

**本地文件：**
```bash
ffprobe -v quiet -print_format json -show_format -show_streams <文件>
```

提取：标题、频道/作者、时长、缩略图 URL、描述。

### 步骤 4：获取转录稿

**选项 A：自动转录（推荐）**
1. 下载音频（YouTube / B站 / X）：
   ```bash
   yt-dlp -x --audio-format mp3 --audio-quality 0 -o "audio.%(ext)s" <URL>
   ```
   注：B站、X 等平台的音频下载同样通过 yt-dlp 处理。
2. 使用 `scripts/transcribe.py`（参见附带脚本）带时间戳转录。
   - 如果设置了 `OPENAI_API_KEY`，使用 OpenAI Whisper API
   - 如果本地 `whisper` 模块可用，则回退到本地
   - 输出格式：带时间戳的 VTT 或 JSON

**选项 B：已有转录稿**
- 接受用户提供的 `.vtt`、`.srt`、`.txt` 或原始转录文本
- 如有时间戳则解析

**选项 C：无可用转录稿**
- 告知用户转录稿是必需的
- 如果用户可以粘贴转录文本，则提供继续处理的选项

### 步骤 5：使用大模型分析内容

将转录稿（带时间戳）输入大模型，使用以下分析提示。要求输出结构化 JSON。

**分析提示：**
```
你是一位资深内容分析师。请分析以下播客/访谈转录稿，并生成结构化总结。

转录稿格式：[HH:MM:SS] 说话人：文本

生成如下结构的 JSON 对象：
{
  "title": "主标题，中文或原文",
  "subtitle": "一句话描述本期节目",
  "guest": "嘉宾姓名及头衔",
  "host": "主持人姓名",
  "duration_approx": "约85分钟",
  "total_clips": 13,
  "sections": [
    {
      "id": "s1",
      "num": "01",
      "title": "章节标题（中文）",
      "timestamp_start": "01:33",
      "timestamp_end": "03:19",
      "summary": "2-4段总结该片段",
      "bullet_points": ["要点1", "要点2"],
      "quote": "该片段中最具影响力的原话引述",
      "has_clip": true,
      "clip_filename": "01_section_title.mp4",
      "clip_label": "精彩片段：描述 (timestamp_start - timestamp_end)"
    }
  ],
  "key_takeaway": {
    "title": "一句话总结",
    "content": "一段有力的话，概括核心洞察"
  },
  "clip_index": [
    {
      "title": "01 - 章节标题",
      "time_range": "01:33 - 03:19",
      "duration": "1分46秒",
      "section_id": "s1"
    }
  ]
}

分章说明：
- 根据自然话题转换创建 10-25 个章节
- 每个章节应覆盖一个独特的主题或问题
- 标题应具体性强且吸引人
- 为大部分章节包含一句有力的直接引述
- 将包含特别视觉化/演示性时刻的章节标记为 has_clip=true
- 总结应捕捉洞察，而非仅仅重述事实
- 使用高亮框呈现对比概念（之前/之后、问题/解决方案等）
- 包含对比表格（产品、团队、方法）
```

### 步骤 6：生成 HTML

使用 JSON 输出生成单个独立的 HTML 文件。

**设计原则 —— 主题自适应系统：**

不要生硬套用固定模板。根据视频内容主题和受众偏好，从以下 4 套主题方案中选择最合适的，并进一步微调：

| 内容类型 | 配色方向 | 暗色版背景 | 亮色版背景 | 氛围关键词 |
|---------|---------|-----------|-----------|-----------|
| 科技/AI | 青绿 `#00e5a0` / 天蓝 `#38bdf8` | `#050810` 深空黑 | `#fafafa` 极白 | 未来、锐利、流动 |
| 商业/创业 | 暖金 `#f59e0b` / 紫 `#a78bfa` | `#0a0f1e` 深蓝黑 | `#fdfbf7` 象牙白 | 稳重、精致、温度 |
| 教育/知识 | 蓝 `#38bdf8` / 青 `#22d3ee` | `#0d1117` GitHub黑 | `#ffffff` 纸白 | 清晰、理性、可读 |
| 文化/人文 | 玫瑰 `#fb7185` / 琥珀 `#fbbf24` | `#1c1917` 暖石黑 | `#faf9f6` 米白 | 温暖、叙事、质感 |

- **默认暗色**：适合沉浸式长文阅读、夜晚场景、科技/商业内容
- **亮色模式**：适合白天阅读、教育/知识类内容、需要打印或分享的场景
- **品牌自适应**：若内容来自特定品牌（如 B站粉 `#FB7299`、X 黑 `#000000`），可提取品牌主色作为 accent

**交互感设计指引（必须包含至少 3 项）：**
- **Hover 卡片抬升**：片段索引卡片在 hover 时 `transform: translateY(-4px)` + `box-shadow` 加深过渡
- **按钮/链接微动效**：时间戳、目录项 hover 时 `scale(1.02)` + 颜色过渡
- **滚动进度条**：页面顶部固定细条，随滚动百分比改变宽度
- **章节进入视口动画**：各章节使用 `IntersectionObserver` 或 CSS `@keyframes fadeInUp`，在进入视口时触发淡入+上移
- **渐变背景流动**：首屏 hero 区域使用缓慢流动的线性渐变背景（`background-size: 200% 200%` + `animation`）
- **时间戳 hover 高亮**：时间戳文本 hover 时发光或变色，暗示可点击跳转
- **视频卡片 play 按钮脉冲**：未播放时中心 play 图标带柔和脉冲动画

**基础结构（必须包含）：**
- 首屏区域：标题、副标题、嘉宾/主持人元信息
- 核心洞察前置（放在目录上方，降低阅读决策成本）
- 交互式目录
- 编号章节区块：时间戳、总结、要点、原话引述
- 视频片段嵌入（`clips/` 相对路径）
- 片段索引导航
- 关键要点总结
- 页脚

**技术约束：**
- 完全自包含（无 CDN、无外部 CSS/JS）
- 响应式布局（移动端 < 640px 适配）
- 内联 CSS 变量便于主题切换（`:root` 定义暗色/亮色变量集）
- 中文优先字体栈：`SF Pro Display`, `Noto Sans SC`, `-apple-system`
- CSS 动画使用 `@keyframes` 内联实现，不引用外部动画库

**输出文件命名：**
```
<视频标题>_summary.html
```
保存到当前工作目录或用户指定的路径。

参考 `references/html-template.md` 获取占位符命名约定、主题配色方案、交互组件片段和常用组件片段。

### 步骤 7：提取视频片段（可选）

如果用户需要嵌入式片段且 `ffmpeg` 可用：

1. 在 HTML 文件旁边创建 `clips/` 目录
2. 对每个标记为 `has_clip=true` 的章节，提取片段并强制关键帧，使进度条可拖动：
   ```bash
   ffmpeg -ss <起始秒数> -t <持续秒数> -i <视频文件> \
     -c:v libx264 -g 30 -keyint_min 1 -crf 23 -preset fast \
     -c:a aac -b:a 128k -movflags +faststart -y clips/<片段文件名>
   ```
3. 更新 HTML `<video>` 标签指向 `clips/<文件名>`

对于 YouTube / B站 / X 视频，先下载完整视频：
```bash
yt-dlp -f "best[height<=1080]" -o "video.%(ext)s" <URL>
```

如果下载完整视频过大，跳过片段提取并告知用户。

### 步骤 8：将中文字幕烧录到片段中（可选）

如果原视频不是中文，且用户希望字幕直接嵌入视频画面（无需外部文件或 HTTP 服务）：

**为什么选择烧录而非 `<track>` 标签：**
- `<track>` 需要通过 HTTP 提供 VTT 文件；`file://` 协议在大多数浏览器中会阻止它们
- 烧录字幕在任何地方都能工作，包括本地文件打开

**首选方法：ffmpeg `subtitles` 滤镜（最快）**

需要 ffmpeg 编译时启用 `--enable-libass`。通过以下方式安装：
```bash
brew tap homebrew-ffmpeg/ffmpeg
brew install homebrew-ffmpeg/ffmpeg/ffmpeg
```

工作流程：
1. **提取 + 翻译** 片段字幕为 `.srt` 文件（参见 `scripts/translate_subtitles.py`）
2. **用 ffmpeg 一次烧录：**
   ```bash
   ffmpeg -y -i clip_raw.mp4 \
     -vf "subtitles=clip.zh.srt:force_style='FontName=STHeiti Medium,FontSize=26,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=2,Shadow=0,MarginV=50,Alignment=2'" \
     -c:v libx264 -g 30 -keyint_min 1 -crf 23 -preset fast \
     -c:a copy -movflags +faststart clip_final.mp4
   ```
- 速度：约 80 倍实时（90 秒片段约 1 秒完成）
- `-c:a copy` 避免重新编码音频

**备用方法：OpenCV + Pillow（无需 libass）**

如果 ffmpeg 缺少 libass 支持，使用 `scripts/burn_subtitles.py`：
- 逐帧 Python 处理
- 速度：约 1-5 倍实时（慢得多）
- 相同的视觉效果（白字 + 黑边）

**要求：**
- ffmpeg 方法：只需支持 libass 的 ffmpeg
- OpenCV 备用：`pip install opencv-python Pillow numpy googletrans-py`

### 步骤 9：交付结果

向用户呈现：
- 生成的 HTML 文件路径
- 生成的章节数量
- 是否提取了片段
- 是否添加了中文字幕
- 建议在浏览器中打开 HTML

## 边界情况

- **转录稿过长超出上下文窗口**：分块处理，依次分析，然后综合
- **非英语内容**：按原文分析，或根据用户偏好翻译
- **转录稿无时间戳**：从音频时长和字数估算章节时间，或省略时间戳
- **缺少 ffmpeg/yt-dlp**：Agent 自动尝试安装；若失败则生成不含视频片段的 HTML，告知用户后续如何添加
- **B站/X 下载失败**：尝试更新 yt-dlp（`yt-dlp -U`），或提示用户检查区域限制/登录状态
- **视频很短（<10 分钟）**：减少章节数量到 3-5 个，简化布局
- **多个说话人未识别**：在输出中注明说话人标签为近似值

## 常见踩坑与修复

### 转录稿清理
Whisper 生成的 VTT 常包含 `>>>` 说话人标记和 `&gt;&gt;&gt;` HTML 实体，分析前必须清理：
```python
text = text.replace(">>>", "").replace("&gt;&gt;&gt;", "").replace("&amp;", "&")
```

### VTT 解析必须同时提取起止时间
早期实现只提取了起始时间，导致字幕烧录时长短出错。正则必须捕获两侧：
```
(\d{2}:\d{2}:\d{2}\.\d{3})\s+-->\s+(\d{2}:\d{2}:\d{2}\.\d{3})
```

### 谷歌翻译超时
`googletrans-py` 容易触发 `httpx.ConnectTimeout`。translate_subtitles.py 已内置指数退避重试（3 次，间隔 0.5/1.0/1.5 秒）。

### 进度条不可拖动
ffmpeg 输入定位（`-ss` before `-i`）生成的片段缺少关键帧索引。修复：剪辑时强制 `-g 30 -keyint_min 1`。

### SSL 证书问题（Whisper 模型下载）
若本地 whisper 模型下载报 SSL 错误：
```python
import os
import certifi
os.environ["SSL_CERT_FILE"] = certifi.where()
```

### 字幕烧录的格式链
`translate_subtitles.py` 输出 `.zh.srt`（主格式，兼容 burn_subtitles.py 和 ffmpeg `subtitles` 滤镜），同时保留 `.zh.vtt` 备用。工作流中不要混用格式。

## 质量准则

- 章节标题应具体，而非泛泛（例如"极速发货的三个秘诀"而非"讨论发货"）
- 引述必须是原话或明确标注为改写
- 高亮框应将相关洞察分组（对不同观点使用不同颜色）
- 时间戳应精确到约 10 秒内
- HTML 必须完全独立（无 CDN 依赖）
- 中文内容应在字体栈中使用 Noto Sans SC 回退
- 设计应服务于内容，而非模板支配内容
- **交互体验优先**：至少包含滚动进度条、章节进入动画、卡片悬浮效果三项微交互，避免"静态海报"感
- **主题一致性**：同一页面的配色、圆角、阴影风格应统一，暗色/亮色切换时保持对比度合规（WCAG AA）
