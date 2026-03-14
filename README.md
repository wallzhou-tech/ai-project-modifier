# 🤖 AI 项目改造器

> 把热门开源项目改造成CLI工具，打造你自己的AI工具箱！

## ✨ 特性

- 🎯 支持 **20+** 热门AI项目一键安装
- 🌐 按分类浏览（浏览器自动化、Agent编排、RAG等）
- 🔍 GitHub项目搜索
- 📥 项目克隆到本地
- ⚡ 交互式CLI菜单

## 📦 已支持项目

### 🌐 浏览器自动化
| 项目 | 描述 | Stars |
|------|------|-------|
| browser-use | AI控制浏览器自动化 | 80,760 |
| agent-browser | AI Agent浏览器CLI | 21,925 |
| stagehand | AI浏览器自动化框架 | 21,504 |
| skyvern | AI自动化浏览器工作流 | 20,807 |
| crawlee | 网页爬取+自动化 | 22,326 |

### 💾 AI记忆/知识
| 项目 | 描述 | Stars |
|------|------|-------|
| mem0 | AI的记忆层 | 49,793 |

### 🔧 Agent编排
| 项目 | 描述 | Stars |
|------|------|-------|
| crewai | AI Agent编排框架 | 46,043 |
| autogen | 微软多Agent协作 | 35,000 |

### ⌨️ CLI工具
| 项目 | 描述 | Stars |
|------|------|-------|
| gemini-cli | 终端运行Gemini AI | 97,689 |
| cli-anything | 让所有软件变CLI | 13,127 |

### 📚 RAG/知识库
| 项目 | 描述 | Stars |
|------|------|-------|
| awesome-llm-apps | LLM应用集合 | 102,063 |
| flowise | 可视化RAG工作流 | 50,737 |

## 🚀 快速开始

### 安装

```bash
git clone https://github.com/wallzhou-tech/ai-project-modifier.git
cd ai-project-modifier
pip3 install --break-system-packages -r requirements.txt
```

### 使用方法

```bash
# 查看支持的项目
python3 main.py --list

# 按分类查看
python3 main.py --list --category browser

# 搜索GitHub项目
python3 main.py --search "AI agent"

# 克隆项目到本地
python3 main.py --clone browser-use

# 一键安装
python3 main.py --install mem0

# 今日热门
python3 main.py --trending

# 交互模式
python3 main.py --interactive
```

## 📖 交互模式

```
╔═══════════════════════════════════════════════════════╗
║          🤖 AI 项目改造器 v1.0                         ║
║     把热门开源项目改造成你的CLI工具箱！                 ║
╚═══════════════════════════════════════════════════════╝

请选择操作:

  1. 🌐 浏览分类项目
  2. 🔍 搜索GitHub项目
  3. 📥 克隆项目到本地
  4. ⚡ 一键安装项目
  5. 🔥 今日热门项目
  6. 🚪 退出
```

## 🛠️ 技术栈

- Python 3
- GitHub API
- 请求库

## 📝 更新日志

### v1.0 (2026-03-14)
- 初始版本
- 支持20+热门AI项目
- 交互式CLI
- 项目搜索和克隆

## 🤝 贡献

欢迎提交Issue和PR！

## �License

MIT License

---

**让每个好项目都能被轻松调用！** 🚀
