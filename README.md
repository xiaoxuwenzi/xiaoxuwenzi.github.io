# AI 资讯?

用 AI 生成与整理的资讯展示博客网站。视觉设计参考 [why.design](https://www.why.design/) 的编辑式排版语言。

🌐 **访问地址**:https://xiaoxuwenzi.github.io

> **🤖 AI 助手请先阅读 [`AI-GUIDE.md`](./AI-GUIDE.md)** — 包含完整的数据结构、操作流程、代码示例,读完即可独立管理本网站。

## 仓库结构

```
xiaoxuwenzi.github.io/
├── index.html              # ⭐ 博客首页(postsData 元数据+样式+交互)
├── generate_posts.py       # ⭐ 文章页生成脚本(POSTS 正文数据+模板)
├── content/                # 内容区
│   ├── articles/           # 已发布文章(按年/月归档)
│   │   └── 2026/07/        # 示例:2026年7月的文章
│   ├── drafts/             # 草稿区(未发布)
│   └── sources/            # 原始素材(按分类存放)
├── posts/                  # 独立 HTML 文章页(脚本生成)
│   ├── assets/             # 文章配图(封面、正文插图)
│   └── YYYY-MM-DD-slug.html
├── data/
│   └── news.json           # 资讯数据(备份)
├── templates/
│   └── article.md          # 新文章模板(复制即用)
└── README.md               # 本文件
```

## 怎么添加新文章

1. 在 `generate_posts.py` 的 `POSTS` 数组中添加文章数据(含正文)
2. 在 `index.html` 的 `postsData` 数组中添加文章元数据
3. 运行 `python generate_posts.py` 生成独立文章页
4. 存档 Markdown 到 `content/articles/YYYY/MM/`
5. 推送到 GitHub

详见 [`AI-GUIDE.md`](./AI-GUIDE.md)。

## 内容分类

| 分类 | 说明 |
|------|------|
| 文章 | 深度分析、行业观察、长文论述 |
| 笔记 | 技术要点、学习记录、资讯速记 |
| 随笔 | 个人思考、产品感悟、观点短文 |
| 收藏 | 外部优质内容收藏(外链) |

## 技术说明

- **网站**:纯 HTML + CSS + JavaScript,无后端依赖
- **托管**:GitHub Pages,免费
- **设计**:why.design 风格(米白底/黑字/红色点缀/衬线标题)
- **内容**:AI 生成与整理

---

最后更新:2026-07-21
