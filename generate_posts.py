# -*- coding: utf-8 -*-
"""生成博客独立文章页（why.design 风格）"""
import os
import html as _html

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'posts')
os.makedirs(OUT_DIR, exist_ok=True)

# ========================================
# 文章数据（4 分类：文章/笔记/随笔/收藏；收藏类为外链不生成独立页）
# ========================================
POSTS = [
    {
        "slug": "2026-07-21-llm-cost-drop",
        "category": "文章",
        "title": "大模型推理成本一年下降 90%，应用层创业迎来黄金窗口",
        "subtitle": "AI 行业观察",
        "excerpt": "随着底层模型价格持续走低，AI 应用的试错成本大幅降低。对于独立开发者和初创团队来说，现在正是用小成本验证大想法的最好时机。",
        "date": "2026-07-21", "readTime": "4 分钟", "source": "AI 行业观察",
        "tags": ["AI", "创业", "成本"],
        "content": [
            "过去一年里，主流大模型的 API 调用价格下降了超过 90%。这不是营销噱头，而是真实的行业趋势：同样的智能水平，去年要花一块钱，今天只要一毛钱。",
            "这意味着什么？意味着过去只有大公司玩得起的 AI 应用，现在一个人也能做。一个独立开发者用几百块钱的 API 预算，就能跑通一个完整的 AI 产品原型，验证用户是否愿意为它买单。",
            "成本下降的连锁反应正在显现。首先是试错变便宜了——你不再需要融资百万才能开始，几百块就能验证一个想法。其次是迭代变快了——今天想到的功能，明天就能上线让用户用上。最后是竞争门槛变了——当大家都能调用同样的模型，真正的壁垒变成了对用户需求的理解和产品的打磨。",
            {"quote": "当算力像水电一样便宜，真正稀缺的就不再是技术本身，而是用技术解决问题的想象力。"},
            "当然，窗口期不会永远敞开。随着越来越多玩家涌入，流量成本会回升，用户也会变得更加挑剔。但至少在当下，这是过去十年里个人开发者最好的机会之一。如果你有一个想做的 AI 应用，现在就是开始的最好时机。"
        ]
    },
    {
        "slug": "2026-07-20-rust-five-years",
        "category": "笔记",
        "title": "Rust 语言连续五年成为开发者最想学习的语言",
        "subtitle": "技术前沿",
        "excerpt": "Stack Overflow 最新调查显示，Rust 连续第五年位居开发者最想学习的编程语言榜首，内存安全和高性能是两大核心吸引力。",
        "date": "2026-07-20", "readTime": "3 分钟", "source": "技术前沿",
        "tags": ["Rust", "编程语言", "内存安全"],
        "content": [
            "Stack Overflow 发布的年度开发者调查结果显示，Rust 语言连续第五年成为开发者最想学习的编程语言。这一趋势背后，是整个行业对内存安全的日益重视。",
            "Rust 的核心优势在于它能在编译期消除整类内存错误，同时不牺牲运行时性能。这与 C/C++ 形成鲜明对比——后者虽然性能强大，但内存安全问题导致的漏洞占到了所有安全漏洞的约 70%。",
            "越来越多的基础设施项目开始迁移到 Rust。从操作系统内核到浏览器引擎，从数据库到区块链，Rust 正在渗透到对性能和可靠性要求极高的领域。Linux 内核在几年前的版本中正式接受了 Rust 作为可用的开发语言，这是一个标志性事件。",
            "不过 Rust 的学习曲线依然陡峭，所有权和生命周期的概念对新手并不友好。但随着工具链的成熟和社区资源的丰富，入门门槛正在逐步降低。对于想要投资未来技能的开发者来说，Rust 值得认真考虑。"
        ]
    },
    {
        "slug": "2026-07-19-subscription-fatigue",
        "category": "文章",
        "title": "订阅疲劳正在蔓延，用户开始为「少即是多」买单",
        "subtitle": "商业洞察",
        "excerpt": "当每个人手机里有几十个订阅服务，一种新的消费趋势正在兴起：用户愿意为精简、无打扰的体验支付溢价，而非为更多功能付费。",
        "date": "2026-07-19", "readTime": "5 分钟", "source": "商业洞察",
        "tags": ["订阅经济", "消费趋势", "产品"],
        "content": [
            "你手机里有多少个正在付费的订阅服务？音乐、视频、云存储、笔记、健身、新闻……当订阅数量超过某个临界点，一种名为「订阅疲劳」的现象开始显现。",
            "市场研究显示，用户平均订阅的服务数量在过去三年翻了一倍，但每月愿意为所有订阅支付的总金额几乎没有增长。这意味着每个服务能分到的钱越来越少，竞争变成了零和博弈。",
            "有趣的是，一批主打「做减法」的产品开始跑出来。它们不堆功能，不打扰用户，甚至主动提醒你取消不常用的订阅。这种克制反而成了卖点——用户愿意为不被打扰的体验付费。",
            {"quote": "未来的赢家不是功能最多的那个，而是让用户感到最轻松的那个。"},
            "这对产品人的启示是：在订阅经济里，留住用户的关键可能不是持续加功能，而是让用户觉得「这个钱花得值、花得安心」。减少摩擦、提升单次体验的质量，比堆砌功能更能建立长期信任。"
        ]
    },
    {
        "slug": "2026-07-18-ai-coding-assistant",
        "category": "文章",
        "title": "AI 编程助手让初级开发者生产力提升 40%，但对资深开发者几乎无影响",
        "subtitle": "AI 研究",
        "excerpt": "一项针对 2000 名开发者的实验显示，AI 编程助手对经验不足的开发者帮助最大，资深开发者则几乎不受影响。这可能重塑团队结构。",
        "date": "2026-07-18", "readTime": "4 分钟", "source": "AI 研究",
        "tags": ["AI", "开发者", "生产力"],
        "content": [
            "一项覆盖 2000 名软件开发者的对照实验得出了一个有意思的结论：AI 编程助手对生产力的影响，和开发者的经验水平强相关。",
            "实验数据显示，工作经验不足 3 年的初级开发者，在使用 AI 编程助手后生产力提升了约 40%。他们完成任务更快、代码质量更好、需要向资深同事求助的次数明显减少。",
            "但对于经验超过 10 年的资深开发者，AI 助手几乎没有带来可测量的生产力提升。资深开发者早已形成自己的工作流和解决问题的框架，AI 提供的建议要么他们已经想到，要么不够贴合复杂的上下文。",
            "这个发现可能重塑技术团队的结构。如果 AI 助手能大幅提升初级开发者的产出，团队对初级人力的需求可能会改变——要么需要更少的初级开发者，要么初级开发者能承担更多原本需要资深者才能做的任务。",
            "但资深开发者的价值并未被削弱。架构设计、技术决策、跨团队协调这些需要深度经验的工作，AI 目前还无法替代。团队依然需要资深者来把关方向，只是执行层的分工可能会重新调整。"
        ]
    },
    {
        "slug": "2026-07-17-use-and-go",
        "category": "随笔",
        "title": "为什么「用完即走」的产品反而让人念念不忘？",
        "subtitle": "产品思考",
        "excerpt": "好的产品不一定追求用户停留时长。那些帮你快速完成任务然后让你离开的工具，往往拥有最高的留存和口碑。",
        "date": "2026-07-17", "readTime": "3 分钟", "source": "产品思考",
        "tags": ["产品设计", "工具", "留存"],
        "content": [
            "在流量经济时代，几乎所有产品都在想方设法让你多停留一秒。推送通知、无限滚动、自动播放……但有一类产品反其道而行——它们的目标是让你尽快完成任务，然后离开。",
            "计算器、翻译工具、汇率换算、单位转换……这些工具型产品的共同特点是：你打开它，用几秒钟完成一件事，然后关掉。没有沉浸式 feed，没有打卡签到，没有积分体系。",
            "但恰恰是这些「用完即走」的产品，拥有惊人的留存率。因为它们提供了确定性——每次打开都能快速解决问题，没有多余干扰。这种可预期的良好体验，会让人在下次需要时第一个想到它。",
            {"quote": "最好的工具不会偷走你的时间，而是把时间还给你。"},
            "这给产品设计的启示是：不是所有产品都该追求 DAU 和停留时长。对于工具型产品，衡量成功的指标应该是「单次任务完成效率」和「下次需求时的首选率」。有时候，让用户更快离开，反而是最好的留存策略。"
        ]
    },
    {
        "slug": "2026-07-16-webassembly-dev-env",
        "category": "笔记",
        "title": "WebAssembly 突破新里程碑：浏览器内运行完整开发环境",
        "subtitle": "技术前沿",
        "excerpt": "基于 WebAssembly 的云端开发环境日趋成熟，开发者现在可以在浏览器里运行完整的 IDE、数据库和后端服务，无需本地安装任何东西。",
        "date": "2026-07-16", "readTime": "4 分钟", "source": "技术前沿",
        "tags": ["WebAssembly", "开发环境", "云端"],
        "content": [
            "WebAssembly（WASM）正在从一个让浏览器跑 C++ 的实验性技术，演变成改变软件开发方式的基础设施。最新的进展是：完整的开发环境可以直接在浏览器里运行。",
            "这意味着什么？想象一下：你打开一个网页，里面是一个功能完整的 VS Code，背后连接着真实的数据库、后端服务和文件系统。你写代码、运行、调试、部署，全部在浏览器里完成，本地不需要装任何开发工具。",
            "这对开发体验的改变是根本性的。新成员加入团队不再需要花半天配环境，打开链接就能开始写代码。在不同的设备之间切换也变得无缝——公司电脑、个人笔记本、甚至平板，体验完全一致。",
            "更重要的是，这降低了编程的入门门槛。初学者不再需要先搞懂环境配置这层门槛，打开浏览器就能开始动手。更多的计算正在从本地迁移到云端，WebAssembly 是这场迁移的关键技术底座。",
            "当然，离线场景和网络依赖仍是挑战。但随着网络基础设施的完善和浏览器能力的增强，「开发环境即服务」正在从概念走向日常。"
        ]
    },
    {
        "slug": "2026-07-15-ai-overestimate",
        "category": "随笔",
        "title": "我们高估了 AI 一年内能做到的事，却低估了它十年能做到的事",
        "subtitle": "深度观点",
        "excerpt": "每隔一段时间就会出现「AI 要取代某某职业」的恐慌。但回顾过去，技术对就业的影响从来不是简单的替代，而是重塑。",
        "date": "2026-07-15", "readTime": "5 分钟", "source": "深度观点",
        "tags": ["AI", "就业", "长期主义"],
        "content": [
            "每当一项 AI 能力取得突破，就会出现一波「某某职业要消失了」的讨论。翻译要被取代了、画师要失业了、程序员要被淘汰了……这些预测大多基于一个假设：AI 会在短期内达到人类的完整水平。",
            "但现实往往是：AI 在某个具体任务上表现惊艳，但在完整的工作流里还差得远。AI 能写出一段不错的代码，但不能独立完成一个复杂系统的设计和调试。AI 能生成一张好看的图片，但不能理解品牌的整体视觉策略。",
            "这就是「高估一年」的部分。我们容易把演示里的惊艳表现，等同于生产环境的可靠能力。而真正落地时，边缘情况、上下文理解、跨领域判断这些「最后一公里」往往比想象中难走得多。",
            {"quote": "技术不会在一夜之间消灭一个职业，但会在十年里彻底重塑它。"},
            "但「低估十年」同样真实。回看十年前，没有人预料到短视频会重塑整个内容产业，移动支付会改变所有人的消费习惯。技术的长期影响往往以我们意想不到的方式展开——不是简单的替代，而是创造全新的可能。",
            "所以面对 AI，既不必为短期恐慌，也不该对长期掉以轻心。真正值得思考的不是「我的工作会不会消失」，而是「我的工作在 AI 时代会变成什么样，我该如何准备」。"
        ]
    },
    {
        "slug": "2026-07-14-open-source-ai",
        "category": "文章",
        "title": "开源商业模式的第三次浪潮：从服务到云到 AI",
        "subtitle": "商业洞察",
        "excerpt": "开源软件如何赚钱？过去靠服务支持，后来靠云托管，现在 AI 正在开启第三种可能：基于开源模型构建增值 AI 服务。",
        "date": "2026-07-14", "readTime": "4 分钟", "source": "商业洞察",
        "tags": ["开源", "商业模式", "AI"],
        "content": [
            "开源软件的商业模式经历了两次大浪潮。第一波以 Red Hat 为代表，靠提供企业级支持、培训和认证赚钱——软件免费，服务收费。第二波以 MongoDB、Elastic 为代表，把开源软件打包成云服务，用户按用量付费。",
            "现在，第三波浪潮正在兴起，它的驱动力是 AI。越来越多的开源大模型、开源 AI 工具链涌现，围绕它们正在形成新的商业生态。",
            "新模式的核心是：开源模型和工具降低了 AI 应用的门槛，但把模型部署好、调优好、运营好依然有门槛。一批公司开始基于开源 AI 项目提供托管、微调、行业定制等服务，这和过去云托管开源数据库的逻辑一脉相承。",
            "区别在于，AI 服务的附加值更高。一个微调过的行业模型，可能比通用模型效果好数倍，用户愿意为此付费。这让开源 AI 商业化的空间比过去更大。",
            "当然挑战也不小。开源模型迭代极快，今天领先的开源模型可能下个月就被超越，基于它构建的服务需要持续跟进。但总体而言，AI 正在为开源商业化打开一扇新的大门，这波浪潮才刚刚开始。"
        ]
    },
    {
        "slug": "2026-07-21-github-weekly",
        "category": "收藏",
        "title": "GitHub 周热门项目 | 2026-07-14~2026-07-21",
        "subtitle": "GitHub Trending",
        "excerpt": "本周 GitHub Trending 呈现鲜明的 AI Agent 生态化特征：从代码审查、命令防护到 Office 文档、交易决策，Agent 正向开发者工作流每个环节渗透，同时 Agent 安全成为新独立赛道。",
        "date": "2026-07-21", "readTime": "5 分钟", "source": "GitHub Trending",
        "tags": ["GitHub", "AI Agent", "开源"],
        "cover": "assets/github-weekly-cover.jpg",
        "content": [
            "本周 GitHub Trending 呈现出鲜明的「AI Agent 生态化」特征：从代码审查、命令防护到 Office 文档处理、交易决策，AI Agent 正在向开发者工作流的每一个环节渗透。与此同时，开源社区对「Agent 安全」的关注度显著上升，命令拦截、代码图谱等防护类项目集中上榜，反映出开发者在拥抱 Agent 效率的同时，开始系统性地构建护栏。",
            "以下是本周值得关注的几个方向和代表项目。",
            {"image": "assets/github-weekly-agent-ecosystem.jpg", "caption": "AI Agent 从单点工具走向生态平台，能力像 npm 包一样被模块化"},
            "趋势一：AI Agent 从「单点工具」走向「生态平台」。多个项目都在构建「Agent 即技能」的分发模式。awesome-llm-apps 收录 100+ 可直接运行的 Agent 与 RAG 应用模板，支持 npx 一键安装为编码 Agent 的新技能；DeepTutor 把辅导、解题、测验、研究整合在同一 Agent 循环上；Vibe-Trading 则将量化研究的完整链路封装为可被 Agent 调用的技能。Agent 能力正像 npm 包一样被模块化、可发现、可组合。",
            "趋势二：垂直领域 Agent 深入行业流程。OfficeCLI 作为首个专为 AI Agent 设计的 Office 套件，单二进制即可读写编辑 Word、Excel、PowerPoint，把过去 50 行 Python 才能做的事压缩为一条命令。Agent 不再停留在通用聊天，而是深入到行业 Know-How。",
            {"image": "assets/github-weekly-agent-security.jpg", "caption": "Agent 安全成为新独立赛道，命令拦截、代码图谱等防护类项目集中上榜"},
            "趋势三：Agent 安全成为新独立赛道。destructive_command_guard（5,201 Star，本周新增 1,410）是一个高性能钩子，在 AI 编码 Agent 执行危险命令前将其拦截，支持 10+ Agent，内置 50+ 安全包，亚毫秒级延迟。code-review-graph 则通过 Tree-sitter 解析构建代码图谱，让 AI 只读必要文件，Token 消耗降低约 82 倍。社区已意识到 Agent 自主性的风险，开始系统性构建护栏。",
            "趋势四：「反 AI 味」设计需求浮现。Hallmark（8.8k Star）是一款面向 Claude Code、Cursor、Codex 的反 AI 味设计技能，内置 57 道「slop-test」门控，主动拒绝 LLM 训练数据中的同质化默认样式。用户对 LLM 生成内容的同质化已产生审美疲劳，「让 AI 输出不那么像 AI」本身正在成为一种产品定位。",
            {"image": "assets/github-weekly-terminal-agents.jpg", "caption": "终端编码 Agent 竞争白热化，Rust/TypeScript 成为主流实现语言"},
            "趋势五：终端编码 Agent 竞争白热化。openai/codex（Rust 重写）、earendil-works/pi（55.6k Star）、archify 等同周上榜。Rust/TypeScript 成为终端 Agent 的主流实现语言，多供应商 LLM 抽象成为标配。openai/codex 本周单周合并 30+ PR，是 OpenAI 对终端编码 Agent 赛道的持续投入。",
            {"quote": "当 Agent 能力像 npm 包一样可安装、可组合，开发者工作流的每个环节都在被重新定义。"},
            "总体来看，本周 GitHub Trending 呈现出清晰的演进路径：Agent 从单点工具走向生态平台，从通用聊天走向垂直行业，从效率优先走向安全并重。对于开发者和创业者来说，Agent 生态的每一层——基础设施、安全护栏、垂直技能——都蕴藏着新的机会。"
        ]
    }
]

# 按日期降序（最新在前）
POSTS_SORTED = sorted(POSTS, key=lambda x: x['date'], reverse=True)

# ========================================
# 文章页 HTML 模板（why.design 风格）
# ========================================
CSS = """
:root {
  --bg: #f9f9f2; --bg2: #f3f3ea; --bg3: #ffffff;
  --ink: #1a1b1f; --muted: #6b6b66; --rule: #e3e3d8;
  --accent: #ed3a38; --accent-soft: rgba(237, 58, 56, 0.10);
  --font-sans: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  --font-serif: 'Lyontext web', 'Source Han Serif SC', 'Noto Serif SC', 'Songti SC', 'SimSun', Georgia, serif;
  --font-mono: 'Graphik', 'SF Mono', Consolas, 'Courier New', monospace;
  --t: 0.22s ease;
}
[data-theme="dark"] {
  --bg: #1a1b1f; --bg2: #23242a; --bg3: #2a2b31;
  --ink: #f9f9f2; --muted: #9a9a93; --rule: #383940;
  --accent: #ff5454; --accent-soft: rgba(255, 84, 84, 0.14);
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { font-size: 16px; scroll-behavior: smooth; }
body { font-family: var(--font-sans); color: var(--ink); background: var(--bg); line-height: 1.75; -webkit-font-smoothing: antialiased; transition: background var(--t), color var(--t); overflow-x: hidden; }
a { color: var(--ink); text-decoration: none; transition: color var(--t); }
a:hover { color: var(--accent); }
::selection { background: var(--accent); color: #fff; }
::-webkit-scrollbar { width: 10px; }
::-webkit-scrollbar-track { background: var(--bg2); }
::-webkit-scrollbar-thumb { background: var(--rule); border-radius: 10px; border: 2px solid var(--bg2); }
.container { max-width: 760px; margin: 0 auto; padding: 0 1.5rem; }
.site-header { position: sticky; top: 0; z-index: 100; background: color-mix(in srgb, var(--bg) 88%, transparent); backdrop-filter: saturate(180%) blur(14px); -webkit-backdrop-filter: saturate(180%) blur(14px); border-bottom: 1px solid var(--rule); transition: background var(--t), border-color var(--t); }
.site-header .container { display: flex; align-items: center; justify-content: space-between; height: 68px; }
.logo { font-family: var(--font-serif); font-size: 1.5rem; font-weight: 400; color: var(--ink); letter-spacing: -0.01em; }
.logo .q { color: var(--accent); }
.back-link { font-family: var(--font-mono); font-size: 0.95rem; color: var(--muted); display: inline-flex; align-items: center; gap: 0.35rem; }
.back-link:hover { color: var(--accent); }
.back-link svg { width: 14px; height: 14px; }
.theme-toggle { width: 38px; height: 38px; border-radius: 50%; border: 1px solid var(--rule); background: transparent; color: var(--ink); cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all var(--t); }
.theme-toggle:hover { color: var(--accent); border-color: var(--accent); }
.theme-toggle svg { width: 17px; height: 17px; }
[data-theme="dark"] .theme-toggle .sun { display: block; }
[data-theme="dark"] .theme-toggle .moon { display: none; }
.theme-toggle .sun { display: none; }
.theme-toggle .moon { display: block; }
.header-actions { display: flex; align-items: center; gap: 0.85rem; }
.article-head { padding: 4rem 0 2.5rem; border-bottom: 1px solid var(--rule); }
.article-cat { display: inline-block; font-family: var(--font-mono); font-size: 0.82rem; color: var(--accent); margin-bottom: 1.25rem; letter-spacing: 0.04em; }
.article-title { font-family: var(--font-serif); font-size: clamp(2rem, 5vw, 3rem); font-weight: 400; line-height: 1.1; letter-spacing: -0.02em; color: var(--ink); margin-bottom: 1rem; }
.article-subtitle { font-family: var(--font-serif); font-style: italic; font-size: 1.35rem; color: var(--muted); margin-bottom: 1.75rem; font-weight: 400; }
.article-meta { display: flex; gap: 1.75rem; flex-wrap: wrap; font-family: var(--font-mono); font-size: 0.88rem; color: var(--muted); }
.article-meta .source { font-family: var(--font-serif); font-style: italic; color: var(--accent); }
.article-body { padding: 2.5rem 0 3rem; font-family: var(--font-mono); font-size: 1.05rem; line-height: 1.85; color: var(--ink); transition: font-size var(--t); }
.article-body.size-sm { font-size: 0.96rem; }
.article-body.size-lg { font-size: 1.15rem; line-height: 1.9; }
.article-body p { margin-bottom: 1.5rem; }
.article-body p:first-of-type:first-letter { font-family: var(--font-serif); font-size: 3.8rem; float: left; line-height: 0.82; padding-right: 0.65rem; padding-top: 0.4rem; color: var(--accent); font-weight: 400; }
.article-body blockquote { border-left: 3px solid var(--accent); padding: 0.25rem 0 0.25rem 1.5rem; margin: 2rem 0; font-family: var(--font-serif); font-style: italic; font-size: 1.35rem; color: var(--ink); line-height: 1.4; }
.article-cover { margin: 0 -1.5rem 2.5rem; overflow: hidden; }
.article-cover img { width: 100%; height: auto; display: block; max-height: 480px; object-fit: cover; }
.article-body figure { margin: 2.5rem -1.5rem; }
.article-body figure img { width: 100%; height: auto; display: block; border-radius: 2px; }
.article-body figcaption { font-family: var(--font-mono); font-size: 0.82rem; color: var(--muted); padding: 0.75rem 1.5rem 0; text-align: center; line-height: 1.5; }
.article-body figcaption::before { content: '— '; color: var(--accent); }
.article-tags { display: flex; flex-wrap: wrap; gap: 0.6rem; padding: 1.5rem 0; border-top: 1px solid var(--rule); }
.article-tag { font-family: var(--font-mono); font-size: 0.82rem; color: var(--muted); }
.article-tag::before { content: '— '; color: var(--rule); }
.article-footer-note { margin-top: 2rem; padding: 1.1rem 1.25rem; background: var(--accent-soft); border-left: 3px solid var(--accent); font-family: var(--font-mono); font-size: 0.85rem; color: var(--ink); line-height: 1.6; }
.post-nav { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; padding: 2.5rem 0; border-top: 1px solid var(--rule); }
.post-nav a { display: flex; flex-direction: column; gap: 0.35rem; padding: 1rem 1.1rem; border: 1px solid var(--rule); border-radius: 4px; transition: all var(--t); }
.post-nav a:hover { border-color: var(--accent); }
.post-nav .nav-label { font-family: var(--font-mono); font-size: 0.75rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.06em; }
.post-nav .nav-title { font-family: var(--font-serif); font-size: 1rem; color: var(--ink); line-height: 1.3; }
.post-nav a:hover .nav-title { color: var(--accent); }
.post-nav .next { text-align: right; }
.post-nav .prev { visibility: hidden; }
.post-nav .next:empty { visibility: hidden; }
.back-home { text-align: center; padding: 2rem 0 4rem; }
.back-home a { font-family: var(--font-mono); font-size: 0.95rem; color: var(--muted); display: inline-flex; align-items: center; gap: 0.4rem; padding: 0.6rem 1.4rem; border: 1px solid var(--rule); border-radius: 4px; transition: all var(--t); }
.back-home a:hover { color: var(--accent); border-color: var(--accent); }
.back-top { position: fixed; right: 1.5rem; bottom: 1.5rem; width: 44px; height: 44px; border-radius: 50%; background: var(--ink); color: var(--bg); border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; box-shadow: 0 8px 24px rgba(0,0,0,0.18); opacity: 0; visibility: hidden; transform: translateY(10px); transition: all var(--t); z-index: 90; }
.back-top.show { opacity: 1; visibility: visible; transform: translateY(0); }
.back-top:hover { background: var(--accent); }
.back-top svg { width: 18px; height: 18px; }
.toast { position: fixed; bottom: 2rem; left: 50%; transform: translateX(-50%) translateY(20px); background: var(--ink); color: var(--bg); padding: 0.75rem 1.4rem; border-radius: 4px; font-family: var(--font-mono); font-size: 0.88rem; opacity: 0; visibility: hidden; transition: all 0.3s ease; z-index: 300; }
.toast.show { opacity: 1; visibility: visible; transform: translateX(-50%) translateY(0); }
.read-progress { position: fixed; top: 0; left: 0; height: 3px; background: var(--accent); width: 0; z-index: 150; transition: width 0.1s linear; }
@media (max-width: 600px) { .post-nav { grid-template-columns: 1fr; } .article-meta { gap: 1rem; } }
@media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; } }
"""

def render_content_blocks(blocks):
    parts = []
    for b in blocks:
        if isinstance(b, str):
            parts.append(f"<p>{_html.escape(b)}</p>")
        elif isinstance(b, dict) and 'quote' in b:
            parts.append(f"<blockquote>{_html.escape(b['quote'])}</blockquote>")
        elif isinstance(b, dict) and 'image' in b:
            cap = _html.escape(b.get('caption', ''))
            cap_html = f"<figcaption>{cap}</figcaption>" if cap else ""
            parts.append(f'<figure><img src="{_html.escape(b["image"])}" alt="{cap}">{cap_html}</figure>')
    return "\n      ".join(parts)

def render_tags(tags):
    return "".join(f'<span class="article-tag">{_html.escape(t)}</span>' for t in tags)

def build_post_html(post, prev_post, next_post):
    prev_html = ""
    if prev_post:
        prev_html = f'<a class="prev" href="{prev_post["slug"]}.html"><span class="nav-label">← 上一篇</span><span class="nav-title">{_html.escape(prev_post["title"])}</span></a>'
    else:
        prev_html = '<a class="prev" style="visibility:hidden"></a>'
    next_html = ""
    if next_post:
        next_html = f'<a class="next" href="{next_post["slug"]}.html"><span class="nav-label">下一篇 →</span><span class="nav-title">{_html.escape(next_post["title"])}</span></a>'
    else:
        next_html = '<a class="next" style="visibility:hidden"></a>'

    return f"""<!-- Generated by Trae Work -->
<!DOCTYPE html>
<html lang="zh-CN" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{_html.escape(post['title'])} — AI 资讯?</title>
  <meta name="description" content="{_html.escape(post['excerpt'])}">
  <style>{CSS}</style>
</head>
<body>
  <div class="read-progress" id="progress"></div>
  <header class="site-header">
    <div class="container">
      <a href="../index.html" class="back-link"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m15 18-6-6 6-6"/></svg>返回首页</a>
      <div class="header-actions">
        <a href="../index.html" class="logo">AI 资讯<span class="q">?</span></a>
        <button class="theme-toggle" id="theme-toggle" aria-label="切换主题" title="切换深浅色 (Shift+L)">
          <svg class="moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
          <svg class="sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>
        </button>
      </div>
    </div>
  </header>

  <article>
    <div class="container">
      <header class="article-head">
        <span class="article-cat">{_html.escape(post['category'])}</span>
        <h1 class="article-title">{_html.escape(post['title'])}</h1>
        <div class="article-subtitle">{_html.escape(post['subtitle'])}</div>
        <div class="article-meta">
          <span>{post['date']}</span>
          <span>{_html.escape(post['readTime'])}阅读</span>
          <span class="source">{_html.escape(post['source'])}</span>
        </div>
      </header>""" + (f'<div class="article-cover"><img src="{post["cover"]}" alt="{_html.escape(post["title"])}"></div>' if post.get('cover') else '') + f"""
      <div class="article-body" id="body">
        {render_content_blocks(post['content'])}
        <div class="article-footer-note">本文由 AI 生成与整理，内容仅供参考。如需引用请核实原始来源。</div>
      </div>
      <div class="article-tags">{render_tags(post['tags'])}</div>
      <nav class="post-nav">
        {prev_html}
        {next_html}
      </nav>
    </div>
    <div class="back-home"><a href="../index.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px"><path d="m18 15-6-6-6 6"/></svg>返回首页</a></div>
  </article>

  <button class="back-top" id="back-top" aria-label="返回顶部"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m18 15-6-6-6 6"/></svg></button>
  <div class="toast" id="toast"></div>

  <script>
    const themeToggle = document.getElementById('theme-toggle');
    function applyTheme(t) {{ document.documentElement.setAttribute('data-theme', t); localStorage.setItem('ai-news-theme', t); }}
    (function(){{ const s=localStorage.getItem('ai-news-theme'); if(s)applyTheme(s); else if(window.matchMedia&&window.matchMedia('(prefers-color-scheme: dark)').matches)applyTheme('dark'); }})();
    themeToggle.addEventListener('click', () => applyTheme(document.documentElement.getAttribute('data-theme')==='dark'?'light':'dark'));
    document.addEventListener('keydown', e => {{ if(e.shiftKey && (e.key==='L'||e.key==='l')) themeToggle.click(); }});

    const backTop = document.getElementById('back-top');
    const progress = document.getElementById('progress');
    window.addEventListener('scroll', () => {{
      backTop.classList.toggle('show', window.scrollY > 300);
      const max = document.documentElement.scrollHeight - window.innerHeight;
      progress.style.width = (max > 0 ? (window.scrollY / max) * 100 : 0) + '%';
    }});
    backTop.addEventListener('click', () => window.scrollTo({{ top: 0, behavior: 'smooth' }}));

    const toastEl = document.getElementById('toast');
    let toastTimer;
    function showToast(msg) {{ toastEl.textContent = msg; toastEl.classList.add('show'); clearTimeout(toastTimer); toastTimer = setTimeout(() => toastEl.classList.remove('show'), 2000); }}
  </script>
</body>
</html>"""

# ========================================
# 生成所有文章页
# ========================================
n = len(POSTS_SORTED)
for i, post in enumerate(POSTS_SORTED):
    prev_post = POSTS_SORTED[i + 1] if i + 1 < n else None  # 更旧的一篇
    next_post = POSTS_SORTED[i - 1] if i - 1 >= 0 else None  # 更新的一篇
    html = build_post_html(post, prev_post, next_post)
    path = os.path.join(OUT_DIR, post['slug'] + '.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"生成: {post['slug']}.html")

print(f"\n共生成 {n} 篇文章页到 {OUT_DIR}")
