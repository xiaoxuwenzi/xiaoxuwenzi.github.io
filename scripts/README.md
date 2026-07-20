# scripts/ 脚本目录

这个目录用来存放自动化脚本,目前为空,预留给未来使用。

## 计划中的脚本

### 1. `generate-article.js` — AI 生成文章
调用 AI API,自动生成资讯内容并写入 `content/drafts/`。

### 2. `publish-article.js` — 发布文章
把草稿从 `content/drafts/` 移到 `content/articles/YYYY/MM/`,并更新 `index.html` 的 newsData。

### 3. `collect-news.js` — 收集资讯
从 RSS 或新闻源自动收集素材,存入 `content/sources/`。

### 4. `build.js` — 构建网站
扫描 `content/articles/` 下所有文章,自动生成 `index.html` 的 newsData 数组。

## 使用方式

等脚本写好后,在仓库根目录运行:

```bash
node scripts/generate-article.js "AI 行业趋势"
```
