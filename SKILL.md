---
name: video-podcast-summary
description: 将播客或访谈视频转换为设计精美的独立 HTML 总结页面。当用户希望将 YouTube、B站、X/Twitter 视频、播客节目或访谈转换为结构化 HTML 文档、视频总结页面或摘要时触发此技能。也适用于用户提到"播客转 HTML"、"视频总结"、"访谈笔记"、"从视频生成总结页面"，或希望从长视频内容中提取关键洞察和片段的场景。支持 YouTube、B站、X/Twitter 链接和本地视频文件。
---

# 播客视频总结

将长视频内容（播客、访谈、演讲）转换为精美的主题自适应 HTML 总结页面，包含结构化章节、时间戳、关键引述、高亮框和可选的嵌入式视频片段。支持 YouTube、B站、X/Twitter 及本地视频文件。

## 输出示例

最终 HTML 页面包含：
- 首屏区域：视频封面背景、标题、副标题、嘉宾/主持人元信息
- 核心洞察前置
- 交互式目录
- 带时间戳的编号内容章节（含精彩对谈还原 + 关键引述）
- 关键引述的引用块（中文翻译）
- 精彩对话片段的文字还原
- 洞察的彩色高亮框
- 对比表格
- 流程可视化的箭头流程图
- 章节索引网格，便于快速导航
- 关键要点总结
- 完全响应式、多主题设计（暗色/亮色/品牌自适应，无外部依赖）
- 丰富微交互：滚动进度条、章节进入动画、卡片悬浮、时间戳 hover 高亮

## 工作流程

### 步骤 0：项目隔离（重要）

**每个视频必须创建独立工作目录**，防止 clips/、transcript.* 等文件被之前项目污染。

```bash
# 示例：在当前工作目录下创建子目录
mkdir -p "<视频标题>_summary" && cd "<视频标题>_summary"
```

**进入独立目录后再执行所有后续操作。** 若用户未指定路径，默认在当前目录下创建以视频标题命名的子目录。

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
# yt-dlp 可能通过 brew/pip 安装，需检测多种调用方式
(which yt-dlp && echo "yt-dlp: $(yt-dlp --version)") || \
  (python3 -m yt_dlp --version 2>/dev/null && echo "yt-dlp: via python module") || \
  echo "缺少 yt-dlp"

(which ffmpeg && echo "ffmpeg: $(ffmpeg -version 2>/dev/null | head -1)") || echo "缺少 ffmpeg"
python3 -c "import whisper" 2>/dev/null || echo "缺少 whisper"
```

**完整工作流程需要：**
- `yt-dlp`（用于 YouTube、B站、X 等平台下载）
- `openai-whisper` 或 API 访问（用于转录）
- `ffmpeg`（可选，仅在需要下载完整视频时用到）

**Agent 行为：** 若检测到缺失依赖，Agent 应自动尝试安装（如 `brew install ffmpeg yt-dlp` / `apt install ffmpeg yt-dlp` / `pip install --user yt-dlp openai-whisper` 等），无需用户手动操作。仅在自动安装失败时，才向用户展示简洁的修复指引，或回退到仅转录模式（用户手动提供转录稿）。

**yt-dlp 调用优先级：** 优先尝试 `yt-dlp` 命令；若不存在，回退到 `python3 -m yt_dlp`。

### 步骤 3：提取元数据

**YouTube：**
```bash
# 通过 yt-dlp 获取完整元数据（标题、时长、描述、封面等）
yt-dlp --print-json --skip-download <YOUTUBE_URL>
```

**B站：**
```bash
# 通过 yt-dlp 获取（推荐，可获取标题、时长、封面等完整信息）
# B站视频通常为音视频分离流，--list-formats 查看可用格式
yt-dlp --list-formats <BILIBILI_URL>

# 示例：下载 720p + 最高音质（组合格式 ID）
# 先用 --list-formats 找到视频和音频格式 ID，如 30064(video) + 30280(audio)
yt-dlp -f "30064+30280" -o "video_raw.%(ext)s" <BILIBILI_URL>

# 仅获取元数据
yt-dlp --print-json --skip-download <BILIBILI_URL>
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

提取：标题、频道/作者、时长、缩略图 URL、描述、BV号/视频ID。

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
   - **注意：** Whisper 本地模型对中文视频可能输出繁体中文转录稿，不影响分析，但需知悉

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
  "bvid": "BVxxxxxxxxx",
  "tag": "节目名 · 分类标签",
  "sections": [
    {
      "id": "s1",
      "num": "01",
      "title": "章节标题（中文）",
      "timestamp_start": "01:33",
      "timestamp_end": "03:19",
      "timestamp_sec": 93,
      "summary": "2-4段总结该片段的核心内容",
      "details": "（可选）补充细节、背景信息或延伸解读，让内容更丰满",
      "bullet_points": ["要点1", "要点2"],
      "quote": "该片段中最具影响力的原话引述（翻译成中文）",
      "dialogue": [
        ("说话人A", "精彩对谈内容1（翻译成中文）"),
        ("说话人B", "精彩对谈内容2（翻译成中文）")
      ]
    }
  ],
  "key_takeaway": {
    "title": "一句话总结",
    "content": "一段有力的话，概括核心洞察"
  }
}

分章说明：
- 根据自然话题转换创建 10-25 个章节
- 每个章节应覆盖一个独特的主题或问题
- 标题应具体性强且吸引人
- **所有 quote（原话引述）必须翻译成中文**，保留原文感染力
- **所有 dialogue（对谈还原）必须翻译成中文**，选取 2-4 轮最精彩的对话，呈现访谈现场感
- 为关键章节补充 details 段落，补充背景信息和延伸解读
- summary 捕捉洞察而非仅仅重述事实；details 补充背景和细节
- 使用高亮框呈现对比概念（之前/之后、问题/解决方案等）
- 包含对比表格（产品、团队、方法）
```

### 步骤 6：生成 HTML

使用 JSON 输出生成单个独立的 HTML 文件。

**HTML 生成脚本的健壮性要求：**
- **严禁在 Python 字符串字面量中直接使用中文引号 `「` `」` `『` `』`**。这些字符会被 Python 解释器误判为非法 token 导致 SyntaxError。如果 JSON 数据中包含这些字符，使用 `json.dumps()` 自动转义后再插入 HTML。
- **f-string 表达式部分不能包含反斜杠**。如需在 f-string 中拼接含换行符的多行字符串，先将拼接结果赋值给变量，再在 f-string 中引用该变量。
- **内容数据与生成逻辑分离**：推荐将结构化数据保存在独立 JSON 文件中，生成脚本只负责读取 JSON + 渲染模板，避免大段中文内容硬编码在 Python 源码中产生引号/编码问题。
- **中文引号在 HTML/CSS 中完全安全**，只在 Python 字符串字面量中有问题。

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
- **Hover 卡片抬升**：章节索引卡片在 hover 时 `transform: translateY(-4px)` + `box-shadow` 加深过渡
- **按钮/链接微动效**：时间戳、目录项 hover 时 `scale(1.02)` + 颜色过渡
- **滚动进度条**：页面顶部固定细条，随滚动百分比改变宽度
- **章节进入视口动画**：各章节使用 `IntersectionObserver` 或 CSS `@keyframes fadeInUp`，在进入视口时触发淡入+上移
- **时间戳 hover 高亮**：时间戳文本 hover 时发光或变色，暗示可点击跳转

**基础结构（必须包含）：**
- **首屏区域（Hero）**：使用视频封面缩略图作为全屏背景，叠加深色渐变遮罩（确保文字可读），标题、副标题、嘉宾/主持人元信息以白色文字 + `text-shadow` 呈现，避免使用 iframe 或渐变背景色
- **视频入口区**：使用封面图 + 播放按钮 + 外部链接（`<a>` 指向原视频平台），替代 iframe（`file://` 协议下 YouTube iframe 会报错）
- 核心洞察前置（放在目录上方，降低阅读决策成本）
- 交互式目录
- 编号章节区块：时间戳（可跳转原视频平台）、总结、details 补充、要点、对谈还原（中文翻译）、原话引述（中文翻译）
- 章节索引导航
- 关键要点总结
- 页脚

**技术约束：**
- 完全自包含（无 CDN、无外部 CSS/JS）
- 响应式布局（移动端 < 640px 适配）
- 内联 CSS 变量便于主题切换（`:root` 定义暗色/亮色变量集）
- 中文优先字体栈：`SF Pro Display`, `Noto Sans SC`, `-apple-system`
- CSS 动画使用 `@keyframes` 内联实现，不引用外部动画库
- 章节时间戳应链接到视频平台对应时间点（如 B站 `?t=秒数`），方便用户跳转看完整段落

**输出文件命名：**
```
<视频标题>_summary.html
```
保存到当前工作目录或用户指定的路径。

参考 `references/html-template.md` 获取占位符命名约定、主题配色方案、交互组件片段和常用组件片段。

### 步骤 7：交付结果

向用户呈现：
- 生成的 HTML 文件路径
- 生成的章节数量
- 关键引述和对话片段数量
- 建议在浏览器中打开 HTML

## 边界情况

- **转录稿过长超出上下文窗口**：分块处理，依次分析，然后综合
- **非英语内容**：按原文分析，或根据用户偏好翻译
- **转录稿无时间戳**：从音频时长和字数估算章节时间，或省略时间戳
- **缺少 yt-dlp**：Agent 自动尝试安装；若失败则请用户手动提供转录稿
- **B站/X 下载失败**：尝试更新 yt-dlp（`python3 -m yt_dlp -U` 或 `yt-dlp -U`），或提示用户检查区域限制/登录状态
- **B站需要登录/大会员才能下载高清**：回退到可用的最高免费清晰度（通常 720p 或 480p）
- **视频很短（<10 分钟）**：减少章节数量到 3-5 个，简化布局
- **多个说话人未识别**：在输出中注明说话人标签为近似值

## 常见踩坑与修复

### 项目隔离
**症状：** 工作目录里残留旧项目的 transcript.* 等文件，导致新视频分析出错。
**修复：** 每个视频创建独立工作目录，所有操作在子目录内进行。执行前清理旧文件：
```bash
rm -rf *.part *_summary.html
```

### Python SyntaxError：中文引号
**症状：** `SyntaxError: invalid character '「' (U+300C)`
**原因：** 中文左引号 `「` 被 Python 解释器误判为非法 token。
**修复：**
- 不在 Python 字符串字面量中直接写 `「」『』`
- 使用 `json.dumps(data, ensure_ascii=False)` 输出后再写入文件
- 或将内容数据保存为独立 JSON 文件，Python 脚本只负责读取和渲染

### f-string 反斜杠错误
**症状：** `SyntaxError: f-string expression part cannot include a backslash`
**原因：** f-string 的花括号内不能包含反斜杠（如 `\n`）。
**修复：** 先将拼接结果存到变量，再在 f-string 中引用：
```python
joined = '\n'.join(items)
html = f'<div>{joined}</div>'  # 正确
# html = f'<div>{"\n".join(items)}</div>'  # 错误！
```

### yt-dlp 调用方式
**症状：** `which yt-dlp` 返回空，但 `pip install yt-dlp` 已执行。
**修复：** 优先尝试 `yt-dlp` 命令；不存在时回退到 `python3 -m yt_dlp`。B站下载时如果为音视频分离流，需显式组合格式 ID。

### 转录稿清理
Whisper 生成的 VTT 常包含 `>>>` 说话人标记和 `&gt;&gt;&gt;` HTML 实体，分析前必须清理：
```python
text = text.replace(">>>", "").replace("&gt;&gt;&gt;", "").replace("&amp;", "&")
```

### SSL 证书问题（Whisper 模型下载）
若本地 whisper 模型下载报 SSL 错误：
```python
import os
import certifi
os.environ["SSL_CERT_FILE"] = certifi.where()
```

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
- **内容丰满度**：每个章节除 summary 外，尽可能补充 details 背景段和 dialogue 对谈还原，让 3+ 小时的内容在 HTML 中有足够的信息密度
