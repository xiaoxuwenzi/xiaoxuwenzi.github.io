# AI 操作指南 (AI-GUIDE)

> 本文档供 AI 助手阅读。读完本文档,你应该能独立完成:生成文章、更新网站、修改配置、推送部署。
>
> **最后更新**:2026-07-21
> **网站地址**:https://xiaoxuwenzi.github.io

---

## 一、项目概况

这是一个**纯静态博客网站**,部署在 GitHub Pages 上,视觉设计参考 [why.design](https://www.why.design/) 的编辑式排版语言。

- **技术栈**:HTML + CSS + JavaScript(无后端、无框架、无构建步骤)
- **内容来源**:AI 生成与整理的资讯文章
- **数据存储**:文章元数据内嵌在 `index.html` 的 `postsData` 数组;正文内容存于 `generate_posts.py` 的 `POSTS` 数组
- **文章页**:每篇文章一个独立 HTML 文件,由 `generate_posts.py` 脚本生成
- **部署方式**:推送到 GitHub main 分支即自动部署,1-2 分钟生效

### 核心文件

| 文件 | 作用 | AI 是否需要修改 |
|------|------|----------------|
| `index.html` | 博客首页(元数据+样式+交互) | ✅ 新增/修改文章元数据时改这里 |
| `generate_posts.py` | 独立文章页生成脚本(含正文数据) | ✅ 新增/修改正文时改这里,然后运行 |
| `posts/` | 独立 HTML 文章页(脚本生成,勿手改) | ❌ 由脚本生成 |
| `posts/assets/` | 文章配图(封面、正文插图) | ✅ 新增配图存这里 |
| `content/articles/` | 已发布文章的 Markdown 归档 | ✅ 新文章存这里 |
| `content/drafts/` | 草稿区 | ✅ 草稿存这里 |
| `content/sources/` | 原始素材,按分类存放 | ✅ 素材存这里 |
| `data/news.json` | 数据备份(当前未被网站读取) | ⚠️ 可选,建议同步 |
| `templates/article.md` | 新文章模板 | ❌ 一般不改 |
| `README.md` | 仓库说明 | ❌ 一般不改 |
| `AI-GUIDE.md` | 本文件 | ❌ 一般不改 |

---

## 二、目录结构

```
xiaoxuwenzi.github.io/
├── index.html                          # ⭐ 博客首页(postsData 元数据+样式+交互)
├── generate_posts.py                   # ⭐ 文章页生成脚本(POSTS 正文数据+模板)
├── AI-GUIDE.md                         # 本文件(AI 操作指南)
├── README.md                           # 仓库说明
├── content/
│   ├── articles/                       # 已发布文章(按年月归档)
│   │   └── 2026/07/                    # 格式: YYYY/MM/YYYY-MM-DD-标题.md
│   ├── drafts/                         # 草稿区
│   ├── sources/                        # 原始素材(按分类)
│   └── assets/                         # 文章配图(预留)
├── posts/                              # ⭐ 独立 HTML 文章页(脚本生成)
│   ├── assets/                         # 文章配图(封面、正文插图)
│   │   └── github-weekly-cover.jpg
│   └── YYYY-MM-DD-slug.html            # 格式: YYYY-MM-DD-英文slug.html
├── data/
│   └── news.json                       # 数据备份
├── templates/
│   └── article.md                      # 新文章模板
└── scripts/                            # 自动化脚本(预留)
```

---

## 三、分类体系

网站使用 **4 个固定分类 + 标签系统**,文章只能归入其中一个分类:

| 分类 | 适用内容 | 示例 |
|------|----------|------|
| `文章` | 深度分析、行业观察、长文论述 | 大模型成本、订阅经济、AI 编程助手 |
| `笔记` | 技术要点、学习记录、资讯速记 | Rust 语言、WebAssembly |
| `随笔` | 个人思考、产品感悟、观点短文 | 用完即走、AI 长期影响 |
| `收藏` | 外部优质内容收藏(外链,不生成独立页) | GitHub Trending 周报 |

**规则**:
- 分类值必须**完全匹配**上述四个字符串
- `收藏`类文章使用 `link` 字段指向外部 URL,不生成独立文章页
- 其他三类文章使用 `slug` 字段,生成独立文章页
- 标签(tags)用于细分,每篇文章 2-4 个标签

---

## 四、postsData 数据结构 ⭐

首页的数据源是 `index.html` 中的 `postsData` 数组。**这是首页文章列表的元数据。**

### 位置

在 `index.html` 中搜索 `const postsData = [` 即可定位(约第 310 行)。

### 字段说明

```javascript
{
  id: 1,                    // 数字,唯一 ID,新文章取现有最大 id + 1
  category: "文章",          // 字符串,必须是 4 个分类之一
  slug: "2026-07-21-llm-cost-drop",  // 字符串,独立文章页文件名(不含 .html),收藏类可省略
  title: "文章标题",          // 字符串,显示在列表和文章页
  subtitle: "副标题",        // 字符串,斜体显示在标题下方(如分类说明)
  excerpt: "一句话摘要",      // 字符串,列表摘要(建议 50-100 字)
  date: "2026-07-21",        // 字符串,格式 YYYY-MM-DD
  readTime: "4 分钟",         // 字符串,预估阅读时间
  source: "来源名称",         // 字符串,资讯来源
  tags: ["AI", "创业"],      // 数组,2-4 个标签
  cover: "posts/assets/xxx.jpg",  // 可选,封面图路径(有则列表显示缩略图)
  link: "https://..."        // 可选,外链(收藏类用,有则点击跳转外部)
}
```

### 完整示例

```javascript
// 普通文章(有独立文章页)
{
  id: 1, category: "文章", slug: "2026-07-21-llm-cost-drop",
  title: "大模型推理成本一年下降 90%，应用层创业迎来黄金窗口", subtitle: "AI 行业观察",
  excerpt: "随着底层模型价格持续走低，AI 应用的试错成本大幅降低。",
  date: "2026-07-21", readTime: "4 分钟", source: "AI 行业观察", tags: ["AI", "创业", "成本"]
}

// 带封面图的文章
{
  id: 9, category: "收藏",
  title: "GitHub 周热门项目 | 2026-07-14~2026-07-21", subtitle: "GitHub Trending",
  excerpt: "本周 GitHub Trending 呈现鲜明的 AI Agent 生态化特征...",
  date: "2026-07-21", readTime: "5 分钟", source: "GitHub Trending", tags: ["GitHub", "AI Agent", "开源"],
  slug: "2026-07-21-github-weekly",
  cover: "posts/assets/github-weekly-cover.jpg"
}
```

### link vs slug

- `slug`:文章有独立 HTML 页面,文件位于 `posts/{slug}.html`,点击列表项跳转到该页面
- `link`:文章是外部链接,点击直接跳转到外部 URL(收藏类用)
- 两者都没有:不会生成可点击的文章页(应避免)

---

## 五、POSTS 数据结构(generate_posts.py)⭐

文章正文内容存储在 `generate_posts.py` 的 `POSTS` 数组中。**运行脚本即可生成所有文章页。**

### 位置

在 `generate_posts.py` 中搜索 `POSTS = [` 即可定位(约第 12 行)。

### 字段说明

```python
{
    "slug": "2026-07-21-llm-cost-drop",      # 必须与 postsData 中的 slug 一致
    "category": "文章",                        # 4 个分类之一
    "title": "文章标题",
    "subtitle": "副标题",
    "excerpt": "摘要",
    "date": "2026-07-21", "readTime": "4 分钟", "source": "AI 行业观察",
    "tags": ["AI", "创业", "成本"],
    "cover": "assets/xxx.jpg",                 # 可选,封面图(相对于 posts/ 目录)
    "content": [                                # ⭐ 正文内容数组
        "普通段落文本",                          # 字符串 = <p> 段落
        {"quote": "引用金句"},                   # 对象 = <blockquote> 引用块
        {"image": "assets/xxx.jpg", "caption": "图注"},  # 对象 = <figure> 配图
        "继续段落文本"
    ]
}
```

### content 数组支持三种元素

1. **字符串** → 渲染为 `<p>` 段落
2. **对象** `{ quote: "..." }` → 渲染为 `<blockquote>` 引用块
3. **对象** `{ image: "path", caption: "text" }` → 渲染为 `<figure><img><figcaption>` 配图块

### 运行脚本

```bash
cd <仓库本地路径>
python generate_posts.py
```

脚本会在 `posts/` 目录下生成所有文章的 HTML 文件。修改 `POSTS` 数组后重新运行即可更新文章页。

**注意**:`generate_posts.py` 中的 `OUT_DIR` 路径需指向仓库的 `posts/` 目录。

---

## 六、配图支持

### 封面图(cover)

- 在 `postsData` 和 `POSTS` 中添加 `cover` 字段
- 路径格式:
  - `postsData`(index.html):`posts/assets/文件名.jpg`
  - `POSTS`(generate_posts.py):`assets/文件名.jpg`(相对于 posts/ 目录)
- 首页列表:有封面的文章显示 180×120 缩略图(右侧)
- 文章页:封面显示在标题下方,全宽,最高 480px

### 正文插图(image 块)

- 在 `POSTS` 的 `content` 数组中添加 `{"image": "assets/xxx.jpg", "caption": "图注"}`
- 渲染为 `<figure>`,全宽显示,带 `<figcaption>` 图注
- 图注前自动添加「— 」引导符,使用 mono 字体

### 配图存放

- 统一存放在 `posts/assets/` 目录
- 命名规范:`{slug}-{描述}.jpg`(如 `github-weekly-cover.jpg`)
- 推荐使用 AI 生成配图,尺寸 2560×1440

---

## 七、操作场景

### 场景 A:新增一篇文章(完整流程)

1. **确定新 id**:查看 `postsData` 中最大的 id,新 id = 最大值 + 1

2. **生成文章内容**:按以下要求生成
   - 标题:15-30 字,有信息量
   - 副标题:简短分类说明(如「AI 行业观察」)
   - 摘录:50-100 字
   - 正文:3-6 个段落,每段 80-200 字,可穿插引用块和配图
   - 标签:2-4 个
   - 阅读时间:按 300 字/分钟估算
   - 日期:当天日期(YYYY-MM-DD)
   - slug:格式 `YYYY-MM-DD-英文简写`

3. **写入 generate_posts.py**:在 `POSTS` 数组末尾添加新对象(含 content 正文)

4. **写入 index.html**:在 `postsData` 数组末尾添加元数据对象(不含 content)

5. **运行脚本**:`python generate_posts.py` 生成独立文章页

6. **存档 Markdown**:在 `content/articles/YYYY/MM/` 下创建 `YYYY-MM-DD-标题简写.md`

7. **推送**:git add → commit → push

### 场景 B:修改已有文章

1. 在 `generate_posts.py` 的 `POSTS` 中按 `slug` 找到文章,修改正文
2. 在 `index.html` 的 `postsData` 中按 `slug` 找到文章,修改元数据
3. 运行 `python generate_posts.py` 重新生成文章页
4. 同步修改 `content/articles/` 下的 Markdown 文件
5. 推送

### 场景 C:删除文章

1. 从 `generate_posts.py` 的 `POSTS` 中删除对象
2. 从 `index.html` 的 `postsData` 中删除对象
3. 删除 `posts/` 下对应的 HTML 文件
4. 删除 `content/articles/` 下对应的 Markdown 文件
5. 推送

### 场景 D:添加配图

1. 生成或准备图片,存放到 `posts/assets/` 目录
2. 在 `POSTS` 中添加 `cover` 字段(封面)或 `{"image": "...", "caption": "..."}` 块(正文插图)
3. 在 `postsData` 中添加 `cover` 字段(仅封面需要,正文插图不需要)
4. 运行 `python generate_posts.py`
5. 推送

### 场景 E:调整网站样式

样式定义在 `index.html` 的 `<style>` 标签内,通过 CSS 变量控制:

```css
:root {
  --bg: #f9f9f2;          /* 主背景色(米白) */
  --bg2: #f3f3ea;         /* 次背景色 */
  --bg3: #ffffff;         /* 卡片背景 */
  --ink: #1a1b1f;         /* 主文字色(近黑) */
  --muted: #6b6b66;       /* 次文字色(灰) */
  --rule: #e3e3d8;        /* 边框色 */
  --accent: #ed3a38;      /* 主强调色(红,仅作点缀) */
  --accent-soft: rgba(237, 58, 56, 0.10);
  --font-sans: 'Montserrat', -apple-system, ...;  /* 无衬线正文 */
  --font-serif: 'Lyontext web', 'Source Han Serif SC', ...;  /* 衬线标题 */
  --font-mono: 'Graphik', 'SF Mono', ...;  /* 等宽字体(元信息) */
}
```

### 场景 F:调整文章页样式

文章页模板在 `generate_posts.py` 的 `build_post_html()` 函数中。修改模板的 CSS 或 HTML 结构后,重新运行脚本即可更新所有文章页。

---

## 八、设计系统(why.design 风格)

### 配色

- **背景**:米白 `#f9f9f2`(非纯白,带暖色调)
- **文字**:近黑 `#1a1b1f`
- **强调**:红色 `#ed3a38`,**仅作点缀**(标签、hover、关键数字),不作大面积底色
- **暗色模式**:深灰底 `#1a1b1f` + 米白文字 `#f9f9f2`

### 字体

- **标题**:Lyontext / Source Han Serif SC(衬线,weight 400,不用 bold)
- **正文**:Montserrat / 系统无衬线
- **元信息**:Graphik / SF Mono(等宽,用于日期、标签、分类标记)

### 排版原则

- 大量留白,呼吸感强
- 标题用衬线体,不用加粗(weight 400)
- 红色克制使用,只点睛不铺陈
- 列表项 hover 时左移 + 标题变红

---

## 九、Markdown 文件格式

`content/articles/` 下的文章用 Markdown 存储,包含 frontmatter:

```markdown
---
title: "文章标题"
category: "文章"
date: "2026-07-21"
source: "来源名称"
readTime: "4 分钟"
tags: ["AI", "创业"]
status: "published"
---

正文第一段。

正文第二段。

> 引用金句。

正文第三段。
```

**命名规范**:`YYYY-MM-DD-标题简写.md`
**存放路径**:`content/articles/YYYY/MM/`

---

## 十、Git 操作

### 推送流程

```bash
cd <仓库本地路径>
git add -A
git commit -m "描述本次改动"
git push origin
```

### 提交信息规范(Conventional Commits)

- 新增文章:`feat: 新增文章 <标题>`
- 修改文章:`docs: 更新文章 <标题>`
- 删除文章:`chore: 删除文章 <标题>`
- 样式调整:`style: <改了什么>`
- 功能改进:`feat: <新功能描述>`
- 修复问题:`fix: <修复了什么>`
- 文档更新:`docs: 更新 AI-GUIDE`

### 部署

- 推送到 main 分支后,GitHub Pages 自动构建
- **1-2 分钟**后访问 `https://xiaoxuwenzi.github.io` 查看效果

---

## 十一、内容生成规范

当用户要求生成新文章时,AI 应遵循:

### 标题
- 15-30 字,有信息量,不要标题党
- 可用数字、对比、疑问增加吸引力

### 副标题(subtitle)
- 简短的分类说明或视角标签
- 如「AI 行业观察」「技术前沿」「商业洞察」

### 摘录(excerpt)
- 50-100 字,概括核心观点
- 用句号结尾,不要省略号

### 正文
- 3-6 个段落,每段 80-200 字
- 逻辑清晰:问题→分析→观点→结论
- 可穿插 1-2 个引用块(`{"quote": "..."}`)突出金句
- 可穿插配图(`{"image": "...", "caption": "..."}`)辅助说明
- 语言风格:专业但不晦涩,有观点但不偏激

### 标签(tags)
- 2-4 个标签
- 简短(1-4 字),如「AI」「创业」「成本」

### 阅读时间
- 按 300 字/分钟估算,向上取整

### slug
- 格式:`YYYY-MM-DD-英文简写`(如 `2026-07-21-llm-cost-drop`)

### 日期
- 当天日期,格式 YYYY-MM-DD

---

## 十二、常见错误避免

| 错误 | 后果 | 正确做法 |
|------|------|----------|
| 分类名拼错 | 文章不显示在筛选中 | 严格用:文章/笔记/随笔/收藏 |
| postsData 末尾多逗号 | JS 报错,网站白屏 | 最后一个对象不加逗号 |
| POSTS 与 postsData 的 slug 不一致 | 文章页链接 404 | 两处 slug 必须完全一致 |
| content 元素格式错误 | 渲染异常 | 只用字符串、`{quote}` 或 `{image}` |
| id 重复 | 文章互相覆盖 | 新 id = 最大 id + 1 |
| 修改 POSTS 后忘记运行脚本 | 文章页未更新 | 每次改 POSTS 都要运行 generate_posts.py |
| 图片路径写错 | 图片不显示 | postsData 用 `posts/assets/xxx`,POSTS 用 `assets/xxx` |
| 忘记同步 Markdown | 归档不完整 | 每篇都存 Markdown 副本 |

---

## 十三、快速自检清单

操作完成后,AI 应确认:

- [ ] `postsData` 语法正确(无多余逗号,括号匹配)
- [ ] `POSTS` 语法正确(Python 语法,无多余逗号)
- [ ] 新文章的 id 唯一且递增
- [ ] 分类值是 4 个之一(文章/笔记/随笔/收藏)
- [ ] `POSTS` 和 `postsData` 中的 slug 一致
- [ ] date 格式为 YYYY-MM-DD
- [ ] 已运行 `python generate_posts.py` 生成文章页
- [ ] 如有 cover 字段,图片已存到 `posts/assets/`
- [ ] Markdown 文件已存到 `content/articles/YYYY/MM/`
- [ ] 提交信息符合规范
- [ ] 已推送到 GitHub

---

## 附:关键代码位置速查

| 内容 | 文件 | 搜索关键词 | 约第几行 |
|------|------|-----------|----------|
| 首页元数据 | index.html | `const postsData = [` | 310 |
| CSS 变量 | index.html | `:root {` | 11 |
| 渲染逻辑 | index.html | `function renderList()` | 470 |
| 分类筛选 | index.html | `currentCat` | 359 |
| 正文数据 | generate_posts.py | `POSTS = [` | 12 |
| 文章页模板 | generate_posts.py | `def build_post_html(` | — |
| 内容渲染 | generate_posts.py | `def render_content_blocks(` | — |
| 输出目录 | generate_posts.py | `OUT_DIR` | 6 |
