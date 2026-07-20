# AI 资讯站

用 AI 生成与整理的资讯展示网站。

🌐 **访问地址**:https://xiaoxuwenzi.github.io

## 仓库结构

```
xiaoxuwenzi.github.io/
├── index.html              # 主站(资讯展示页面)
├── content/                # 内容区
│   ├── articles/           # 已发布资讯(按年/月归档)
│   │   └── 2026/07/        # 示例:2026年7月的文章
│   ├── drafts/             # 草稿区(未发布)
│   ├── sources/            # 原始素材(按分类存放)
│   │   ├── 科技/ AI/ 商业/ 产品/ 观点/
│   └── assets/             # 文章配图
├── data/
│   └── news.json           # 资讯数据(备份/未来数据源)
├── templates/
│   └── article.md          # 新文章模板(复制即用)
├── scripts/                # 自动化脚本(预留)
└── README.md               # 本文件
```

## 怎么添加新资讯(三步)

### 第 1 步:写文章
复制 `templates/article.md` 到 `content/drafts/`,填写内容。

### 第 2 步:发布
写好后把文件移到 `content/articles/YYYY/MM/`,命名为 `YYYY-MM-DD-标题.md`。

### 第 3 步:更新网站
打开 `index.html`,找到 `newsData` 数组,按格式添加一条:

```javascript
{
  id: 9,
  category: "科技",
  title: "你的资讯标题",
  excerpt: "一句话摘要…",
  date: "2026-07-21",
  readTime: "3 分钟",
  source: "来源",
  content: [
    "第一段正文…",
    { quote: "可选的引用金句" },
    "第二段正文…"
  ]
}
```

保存后告诉我「帮我推送」,我会帮你提交到 GitHub。

## 内容分类

| 分类 | 说明 |
|------|------|
| 科技 | 编程语言、开发工具、技术趋势、AI |
| 财经 | 商业模式、市场分析、行业洞察、投资 |
| 时事 | 热点事件、社会动态、国际要闻 |
| 生活 | 生活方式、健康、文化、消费 |
| 观点 | 深度观点、评论、思考 |

## 技术说明

- **网站**:纯 HTML + CSS + JavaScript,无后端依赖
- **托管**:GitHub Pages,免费
- **字体**:系统字体栈,零依赖
- **内容**:AI 生成与整理

## 未来计划

- [ ] 脚本自动从 Markdown 生成 newsData
- [ ] RSS 自动收集素材到 sources/
- [ ] AI API 自动生成文章
- [ ] 全文搜索功能
- [ ] 标签系统

---

最后更新:2026-07-21
