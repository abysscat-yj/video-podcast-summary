# HTML 组件参考

本文档不是固定模板，而是**组件库参考**。实际生成 HTML 时，请根据视频内容主题自定义视觉风格，而非直接套用以下代码。

## 占位符约定

- `{{TITLE}}` — 页面标题（也用于 `<title>` 和首屏区域）
- `{{SUBTITLE}}` — 一句话节目描述
- `{{GUEST}}` — 嘉宾姓名及头衔
- `{{HOST}}` — 主持人姓名
- `{{DURATION}}` — 大致时长（例如"~85 分钟"）
- `{{CLIP_COUNT}}` — 提取的片段数量
- `{{TAG}}` — 播客/节目名称标签（例如"Y Combinator 深度访谈"）
- `{{SECTIONS_HTML}}` — 生成的章节区块
- `{{TOC_LINKS}}` — 生成的目录链接
- `{{CLIP_INDEX_CARDS}}` — 生成的片段索引卡片
- `{{KEY_TAKEAWAY_TITLE}}` — 要点总结区域标题
- `{{KEY_TAKEAWAY_CONTENT}}` — 要点段落
- `{{FOOTER_TEXT}}` — 页脚署名

## 主题系统

根据内容类型选择一套主题方案，每套均包含**暗色版**与**亮色版**完整 CSS 变量定义。

### 1. 科技/AI（青绿/天蓝）

| 模式 | 背景 | 卡片 | 文字 | 主强调色 | 辅助色 |
|-----|------|------|------|---------|--------|
| 暗色 | `#050810` 深空黑 | `#0d1321` | `#e8ecf1` | `#00e5a0` 青绿 | `#38bdf8` 天蓝 |
| 亮色 | `#fafafa` 极白 | `#ffffff` | `#111827` | `#059669` 深青绿 | `#0284c7` 深天蓝 |

```css
/* 暗色版 */
:root {
  --bg: #050810;
  --bg-elevated: #0a0f1e;
  --bg-card: #0d1321;
  --bg-glass: rgba(13, 19, 33, 0.7);
  --border: rgba(255, 255, 255, 0.06);
  --border-hover: rgba(0, 229, 160, 0.25);
  --text: #e8ecf1;
  --text-secondary: #8892a0;
  --text-muted: #4a5568;
  --accent: #00e5a0;
  --accent-dim: rgba(0, 229, 160, 0.12);
  --accent-glow: rgba(0, 229, 160, 0.3);
  --accent-blue: #38bdf8;
  --gradient-hero: linear-gradient(180deg, #0a1628 0%, #050810 100%);
}

/* 亮色版 */
@media (prefers-color-scheme: light) {
  :root {
    --bg: #fafafa;
    --bg-elevated: #f3f4f6;
    --bg-card: #ffffff;
    --bg-glass: rgba(255, 255, 255, 0.85);
    --border: rgba(0, 0, 0, 0.08);
    --border-hover: rgba(5, 150, 105, 0.35);
    --text: #111827;
    --text-secondary: #4b5563;
    --text-muted: #9ca3af;
    --accent: #059669;
    --accent-dim: rgba(5, 150, 105, 0.1);
    --accent-glow: rgba(5, 150, 105, 0.25);
    --accent-blue: #0284c7;
    --gradient-hero: linear-gradient(180deg, #eef2ff 0%, #fafafa 100%);
  }
}
```

### 2. 商业/创业（暖金/紫）

| 模式 | 背景 | 卡片 | 文字 | 主强调色 | 辅助色 |
|-----|------|------|------|---------|--------|
| 暗色 | `#0a0f1e` 深蓝黑 | `#111827` | `#f3f4f6` | `#f59e0b` 暖金 | `#a78bfa` 紫 |
| 亮色 | `#fdfbf7` 象牙白 | `#ffffff` | `#1f2937` | `#d97706` 深金 | `#7c3aed` 深紫 |

```css
/* 暗色版 */
:root {
  --bg: #0a0f1e;
  --bg-elevated: #111827;
  --bg-card: #1f2937;
  --bg-glass: rgba(17, 24, 39, 0.7);
  --border: rgba(255, 255, 255, 0.06);
  --border-hover: rgba(245, 158, 11, 0.25);
  --text: #f3f4f6;
  --text-secondary: #9ca3af;
  --text-muted: #6b7280;
  --accent: #f59e0b;
  --accent-dim: rgba(245, 158, 11, 0.12);
  --accent-glow: rgba(245, 158, 11, 0.3);
  --accent-purple: #a78bfa;
  --gradient-hero: linear-gradient(180deg, #1e1b4b 0%, #0a0f1e 100%);
}

/* 亮色版 */
@media (prefers-color-scheme: light) {
  :root {
    --bg: #fdfbf7;
    --bg-elevated: #f9f7f3;
    --bg-card: #ffffff;
    --bg-glass: rgba(255, 255, 255, 0.85);
    --border: rgba(0, 0, 0, 0.08);
    --border-hover: rgba(217, 119, 6, 0.35);
    --text: #1f2937;
    --text-secondary: #4b5563;
    --text-muted: #9ca3af;
    --accent: #d97706;
    --accent-dim: rgba(217, 119, 6, 0.1);
    --accent-glow: rgba(217, 119, 6, 0.25);
    --accent-purple: #7c3aed;
    --gradient-hero: linear-gradient(180deg, #fffbeb 0%, #fdfbf7 100%);
  }
}
```

### 3. 教育/知识（蓝/青）

| 模式 | 背景 | 卡片 | 文字 | 主强调色 | 辅助色 |
|-----|------|------|------|---------|--------|
| 暗色 | `#0d1117` GitHub黑 | `#161b22` | `#c9d1d9` | `#38bdf8` 蓝 | `#22d3ee` 青 |
| 亮色 | `#ffffff` 纸白 | `#f6f8fa` | `#24292f` | `#0969da` 深蓝 | `#0e7c86` 深青 |

```css
/* 暗色版 */
:root {
  --bg: #0d1117;
  --bg-elevated: #161b22;
  --bg-card: #21262d;
  --bg-glass: rgba(22, 27, 34, 0.7);
  --border: rgba(255, 255, 255, 0.06);
  --border-hover: rgba(56, 189, 248, 0.25);
  --text: #c9d1d9;
  --text-secondary: #8b949e;
  --text-muted: #6e7681;
  --accent: #38bdf8;
  --accent-dim: rgba(56, 189, 248, 0.12);
  --accent-glow: rgba(56, 189, 248, 0.3);
  --accent-cyan: #22d3ee;
  --gradient-hero: linear-gradient(180deg, #0f172a 0%, #0d1117 100%);
}

/* 亮色版 */
@media (prefers-color-scheme: light) {
  :root {
    --bg: #ffffff;
    --bg-elevated: #f6f8fa;
    --bg-card: #f6f8fa;
    --bg-glass: rgba(255, 255, 255, 0.9);
    --border: rgba(0, 0, 0, 0.08);
    --border-hover: rgba(9, 105, 218, 0.3);
    --text: #24292f;
    --text-secondary: #57606a;
    --text-muted: #8c959f;
    --accent: #0969da;
    --accent-dim: rgba(9, 105, 218, 0.1);
    --accent-glow: rgba(9, 105, 218, 0.25);
    --accent-cyan: #0e7c86;
    --gradient-hero: linear-gradient(180deg, #ddf4ff 0%, #ffffff 100%);
  }
}
```

### 4. 文化/人文（玫瑰/琥珀）

| 模式 | 背景 | 卡片 | 文字 | 主强调色 | 辅助色 |
|-----|------|------|------|---------|--------|
| 暗色 | `#1c1917` 暖石黑 | `#292524` | `#f5f5f4` | `#fb7185` 玫瑰 | `#fbbf24` 琥珀 |
| 亮色 | `#faf9f6` 米白 | `#ffffff` | `#44403c` | `#e11d48` 深玫瑰 | `#d97706` 深琥珀 |

```css
/* 暗色版 */
:root {
  --bg: #1c1917;
  --bg-elevated: #292524;
  --bg-card: #44403c;
  --bg-glass: rgba(41, 37, 36, 0.7);
  --border: rgba(255, 255, 255, 0.06);
  --border-hover: rgba(251, 113, 133, 0.25);
  --text: #f5f5f4;
  --text-secondary: #a8a29e;
  --text-muted: #78716c;
  --accent: #fb7185;
  --accent-dim: rgba(251, 113, 133, 0.12);
  --accent-glow: rgba(251, 113, 133, 0.3);
  --accent-amber: #fbbf24;
  --gradient-hero: linear-gradient(180deg, #312e81 0%, #1c1917 100%);
}

/* 亮色版 */
@media (prefers-color-scheme: light) {
  :root {
    --bg: #faf9f6;
    --bg-elevated: #f5f5f0;
    --bg-card: #ffffff;
    --bg-glass: rgba(255, 255, 255, 0.85);
    --border: rgba(0, 0, 0, 0.08);
    --border-hover: rgba(225, 29, 72, 0.3);
    --text: #44403c;
    --text-secondary: #57534e;
    --text-muted: #a8a29e;
    --accent: #e11d48;
    --accent-dim: rgba(225, 29, 72, 0.1);
    --accent-glow: rgba(225, 29, 72, 0.25);
    --accent-amber: #d97706;
    --gradient-hero: linear-gradient(180deg, #fef3c7 0%, #faf9f6 100%);
  }
}
```

## 交互设计组件

以下交互效果均使用纯 CSS `@keyframes` 实现，不依赖外部库。

### Hover 卡片抬升

片段索引卡片在 hover 时轻微上浮并加深阴影：

```css
.clip-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.clip-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
  border-color: var(--border-hover);
}
```

### 按钮/链接微动效

时间戳、目录项 hover 时微缩放+颜色过渡：

```css
.toc-item, .timestamp {
  transition: transform 0.2s ease, color 0.2s ease, background 0.2s ease;
}
.toc-item:hover, .timestamp:hover {
  transform: scale(1.02);
  color: var(--accent);
}
```

### 滚动进度条

固定在页面顶部的细条，随滚动百分比改变宽度：

```html
<div class="progress-bar"><div class="progress-fill"></div></div>
```

```css
.progress-bar {
  position: fixed;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: var(--bg-elevated);
  z-index: 9999;
}
.progress-fill {
  height: 100%;
  width: 0%;
  background: linear-gradient(90deg, var(--accent), var(--accent-blue));
  transition: width 0.1s linear;
}
```

```javascript
window.addEventListener('scroll', () => {
  const scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
  const scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
  const pct = (scrollTop / scrollHeight) * 100;
  document.querySelector('.progress-fill').style.width = pct + '%';
});
```

### 章节进入视口 fade-in 动画

各章节在进入视口时触发淡入+上移：

```css
.section {
  opacity: 0;
  transform: translateY(24px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}
.section.visible {
  opacity: 1;
  transform: translateY(0);
}
```

```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) entry.target.classList.add('visible');
  });
}, { threshold: 0.1 });
document.querySelectorAll('.section').forEach(s => observer.observe(s));
```

### 渐变背景流动

首屏 hero 区域缓慢流动的渐变背景：

```css
.hero {
  background: linear-gradient(-45deg, #0a1628, #1e1b4b, #0f172a, #050810);
  background-size: 400% 400%;
  animation: gradientFlow 15s ease infinite;
}
@keyframes gradientFlow {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
```

### 时间戳 hover 高亮

```css
.timestamp {
  font-family: 'SF Mono', monospace;
  color: var(--text-secondary);
  cursor: pointer;
  transition: color 0.2s ease, text-shadow 0.2s ease;
}
.timestamp:hover {
  color: var(--accent);
  text-shadow: 0 0 12px var(--accent-glow);
}
```

### 视频卡片 play 按钮脉冲

未播放时中心 play 图标带柔和脉冲：

```css
.play-button {
  width: 64px; height: 64px;
  border-radius: 50%;
  background: var(--accent);
  position: relative;
}
.play-button::after {
  content: '';
  position: absolute;
  inset: -8px;
  border-radius: 50%;
  border: 2px solid var(--accent);
  opacity: 0;
  animation: pulseRing 2s ease-out infinite;
}
@keyframes pulseRing {
  0% { transform: scale(0.8); opacity: 0.6; }
  100% { transform: scale(1.4); opacity: 0; }
}
```

## 章节 HTML 片段

```html
<div class="section" id="s1">
    <span class="section-anchor"></span>
    <div class="section-header">
        <div class="section-num-box">01</div>
        <div class="section-title-group">
            <h2>章节标题</h2>
            <span class="timestamp">01:33 - 03:19</span>
        </div>
    </div>
    <div class="section-body">
        <p>总结段落...</p>
        <ul class="bullet-list">
            <li><strong>要点：</strong>描述</li>
        </ul>
        <blockquote>"来自转录稿的直接引述"</blockquote>

        <div class="video-wrap">
            <video controls preload="metadata">
                <source src="clips/01_title.mp4" type="video/mp4">
            </video>
            <div class="video-label"><span class="play-dot"></span> 精彩片段：描述 (起始 - 结束)</div>
        </div>
    </div>
</div>
```

## 目录链接片段

```html
<a class="toc-item" href="#s1">
    <span class="toc-num">01</span>
    <span class="toc-title">章节标题</span>
    <span class="toc-time">01:33</span>
</a>
```

## 片段索引卡片片段

```html
<div class="clip-card" onclick="document.querySelector('#s1 video').scrollIntoView({behavior:'smooth'})">
    <div class="clip-card-title">01 - 章节标题</div>
    <div class="clip-card-time">01:33 - 03:19 <span class="clip-card-duration">1分46秒</span></div>
</div>
```

## 关键要点总结（前置）

建议放在目录上方，让用户在进入长文前先获得核心洞察：

```html
<div class="takeaway-lead">
    <h2>核心洞察</h2>
    <p>一段有力的话，概括本期最核心的 1-3 个洞察...</p>
</div>
```

## 高亮框变体

对不同语义目的使用不同颜色：
- **默认（蓝色）**：一般洞察、流程描述
- **`.green`**：积极结果、解决方案、"之后"状态
- **`.purple`**：团队/人员洞察、文化观察
- **`.orange`**：警告、权衡、问题、"之前"状态

```html
<div class="insight-box green">
    <h4>关键收获</h4>
    <p>这里是高亮内容...</p>
</div>
```

## 表格片段

```html
<table>
    <thead>
        <tr><th>列 A</th><th>列 B</th><th>列 C</th></tr>
    </thead>
    <tbody>
        <tr><td><strong>项目 1</strong></td><td>值</td><td>描述</td></tr>
    </tbody>
</table>
```

## 箭头流程片段

```html
<div class="arrow-flow">
    <span class="step">步骤 1</span>
    <span class="arrow">→</span>
    <span class="step">步骤 2</span>
</div>
```

## 技术约束清单

- **完全自包含**：所有 CSS 内联，无 CDN、无外部字体链接
- **响应式**：移动端 `< 640px` 自动单列、缩减间距
- **视频路径**：使用相对路径 `clips/01_title.mp4`，与 HTML 同目录
- **字幕烧录**：非中文视频必须将字幕烧录到视频帧中，不使用 `<track>` 标签（`file://` 协议下浏览器会阻止它们）
- **中文支持**：字体栈中保留 `Noto Sans SC` 或 `PingFang SC` 回退
- **滚动优化**：`section-anchor` 配合 `scroll-margin-top` 实现锚点偏移
- **CSS 动画**：所有动画使用 `@keyframes` 内联实现，不引用外部动画库（如 animate.css、GSAP）
- **主题切换**：通过 `prefers-color-scheme` 媒体查询或 JS 切换 body class 实现暗色/亮色切换
