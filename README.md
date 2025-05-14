# personal-website
这是一个个人网站项目，旨在展示个人作品、博客文章和提供联系信息。该项目包含以下功能和文件结构：

## 项目结构
```
personal-website
├── _data
│   └── navigation.yml        # 定义网站的导航菜单
├── _posts
│   └── 2024-05-20-welcome.md # 博客文章
├── assets
│   ├── images                # 存放上传的图片内容
│   └── style.css             # 网站样式设置
├── pages
│   ├── about.html            # 关于页面
│   ├── categories.html       # 分类页面
│   ├── contact.html          # 联系页面
│   └── upload.html           # 上传页面
├── _config.yml               # 网站配置文件
├── index.html                # 网站首页
└── README.md                 # 项目文档和说明
```

## 功能说明
- **导航菜单**：通过 `_data/navigation.yml` 文件定义，提供首页、博客、关于和分类链接。
- **博客文章**：在 `_posts` 文件夹中创建 Markdown 文件，记录博客内容。
- **分类功能**：在 `pages/categories.html` 页面展示不同文章的分类。
- **留言功能**：在 `pages/contact.html` 页面提供联系方式和留言表单。
- **图片上传**：在 `pages/upload.html` 页面允许用户上传图片，存放在 `assets/images` 文件夹中。

## 使用说明
1. 克隆此项目到本地。
2. 使用 Jekyll 或其他静态网站生成器进行构建和预览。
3. 根据需要修改配置文件 `_config.yml` 和样式文件 `assets/style.css`。

欢迎贡献和反馈！