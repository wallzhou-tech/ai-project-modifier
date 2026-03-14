#!/usr/bin/env python3
"""
🤖 AI项目改造器 - 把热门开源项目改造成CLI工具

用法:
    python3 main.py --list              查看已支持项目
    python3 main.py --search <关键词>    搜索项目
    python3 main.py --clone <项目名>     克隆项目
    python3 main.py --trending          今日热门
    python3 main.py --install <项目名>   一键安装
    python3 main.py --interactive        交互模式
"""

import argparse
import json
import os
import subprocess
import sys
import requests
from typing import Dict, List, Optional

# ANSI颜色
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
HEADERS = {"Accept": "application/vnd.github.v3+json"}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"token {GITHUB_TOKEN}"

# 热门AI项目数据库
AI_PROJECTS = {
    # 浏览器自动化
    "browser-use": {
        "repo": "browser-use/browser-use",
        "desc": "让AI控制浏览器自动化",
        "stars": 80760,
        "category": "browser",
        "install": "pip install browser-use"
    },
    "agent-browser": {
        "repo": "vercel-labs/agent-browser",
        "desc": "AI Agent浏览器自动化CLI",
        "stars": 21925,
        "category": "browser",
        "install": "cargo install agent-browser"
    },
    "stagehand": {
        "repo": "browserbase/stagehand",
        "desc": "AI浏览器自动化框架",
        "stars": 21504,
        "category": "browser",
        "install": "npx @browserbase/stagehand"
    },
    "skyvern": {
        "repo": "Skyvern-AI/skyvern",
        "desc": "用AI自动化浏览器工作流",
        "stars": 20807,
        "category": "browser",
        "install": "pip install skyvern"
    },
    "crawlee": {
        "repo": "apify/crawlee",
        "desc": "网页爬取和浏览器自动化库",
        "stars": 22326,
        "category": "browser",
        "install": "npm install crawlee"
    },
    
    # AI记忆/知识
    "mem0": {
        "repo": "mem0ai/mem0",
        "desc": "AI的记忆层",
        "stars": 49793,
        "category": "memory",
        "install": "pip install mem0ai"
    },
    
    # Agent编排
    "crewai": {
        "repo": "crewAIInc/crewAI",
        "desc": "AI Agent编排框架",
        "stars": 46043,
        "category": "orchestration",
        "install": "pip install crewai"
    },
    "autogen": {
        "repo": "microsoft/autogen",
        "desc": "微软多Agent协作框架",
        "stars": 35000,
        "category": "orchestration",
        "install": "pip install pyautogen"
    },
    
    # CLI工具
    "cli-anything": {
        "repo": "HKUDS/CLI-Anything",
        "desc": "让所有软件变成CLI工具",
        "stars": 13127,
        "category": "cli",
        "install": "git clone"
    },
    "gemini-cli": {
        "repo": "google-gemini/gemini-cli",
        "desc": "在终端里运行Gemini AI",
        "stars": 97689,
        "category": "cli",
        "install": "npm install -g @gemini/cli"
    },
    
    # RAG/知识库
    "rag": {
        "repo": "Shubhamsaboo/awesome-llm-apps",
        "desc": "LLM应用集合(含RAG)",
        "stars": 102063,
        "category": "rag",
        "install": "git clone"
    },
    "flowise": {
        "repo": "FlowiseAI/Flowise",
        "desc": "可视化RAG工作流",
        "stars": 50737,
        "category": "rag",
        "install": "npm install flowise"
    },
    
    # 开发工具
    "opencode": {
        "repo": "anthropics/opencode",
        "desc": "AI代码编辑助手",
        "stars": 15000,
        "category": "dev",
        "install": "npm install -g opencode"
    },
}

CATEGORIES = {
    "browser": "🌐 浏览器自动化",
    "memory": "💾 AI记忆/知识",
    "orchestration": "🔧 Agent编排",
    "cli": "⌨️ CLI工具",
    "rag": "📚 RAG/知识库",
    "dev": "🛠️ 开发工具",
}


def print_banner():
    """打印Banner"""
    banner = f"""
{BOLD}{BLUE}
╔═══════════════════════════════════════════════════════╗
║          🤖 AI 项目改造器 v1.0                         ║
║     把热门开源项目改造成你的CLI工具箱！                 ║
╚═══════════════════════════════════════════════════════╝
{RESET}
    """
    print(banner)


def get_trending_projects(language="python", limit=10) -> List[Dict]:
    """获取GitHub热门项目"""
    url = f"https://api.github.com/search/repositories?q=language:{language}+sort:stars&order=desc&per_page={limit}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            return resp.json().get("items", [])
    except Exception as e:
        print(f"{RED}❌ 获取热门失败: {e}{RESET}")
    return []


def search_projects(query: str):
    """搜索项目"""
    url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page=10"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            items = resp.json().get("items", [])
            print(f"\n{BLUE}🔍 搜索 '{query}' 结果:{RESET}\n")
            for i, item in enumerate(items, 1):
                stars = item.get('stargazers_count', 0)
                lang = item.get('language', 'N/A')
                desc = item.get('description', 'No description')[:50]
                print(f"  {i}. {BOLD}{item['full_name']}{RESET}")
                print(f"     {desc}...")
                print(f"     ⭐ {stars:,} | {lang}")
                print()
        else:
            print(f"{RED}❌ 搜索失败{RESET}")
    except Exception as e:
        print(f"{RED}❌ 搜索出错: {e}{RESET}")


def list_supported(category: Optional[str] = None):
    """列出已支持的项目"""
    print(f"\n{BOLD}📦 已支持的项目:{RESET}\n")
    
    # 按分类显示
    if category:
        cats = {category: CATEGORIES.get(category, category)}
    else:
        cats = CATEGORIES
    
    for cat_id, cat_name in cats.items():
        projects_in_cat = {k: v for k, v in AI_PROJECTS.items() if v.get("category") == cat_id}
        if projects_in_cat:
            print(f"{BOLD}{cat_name}{RESET}")
            for name, info in projects_in_cat.items():
                print(f"  • {GREEN}{name}{RESET}")
                print(f"    {info['desc']}")
                print(f"    ⭐ {info['stars']:,} | 安装: {info['install']}")
                print()
    
    print(f"{YELLOW}提示: 使用 --install <项目名> 直接安装{RESET}\n")


def clone_project(project_name: str):
    """克隆项目到本地"""
    if project_name not in AI_PROJECTS:
        print(f"{RED}❌ 未知项目: {project_name}{RESET}")
        print(f"{YELLOW}可用项目: {', '.join(AI_PROJECTS.keys())}{RESET}")
        return
    
    info = AI_PROJECTS[project_name]
    repo = info["repo"]
    target_dir = f"/root/.openclaw/workspace/projects/{project_name}"
    
    print(f"{BLUE}📥 正在克隆 {repo}...{RESET}")
    
    # 创建目录
    os.makedirs(target_dir, exist_ok=True)
    
    # 克隆
    result = subprocess.run(
        ["git", "clone", f"https://github.com/{repo}.git", target_dir],
        capture_output=True, text=True
    )
    
    if result.returncode == 0:
        print(f"{GREEN}✅ 克隆成功!{RESET}")
        print(f"   保存到: {target_dir}")
        
        # 检查是否有requirements
        req_file = os.path.join(target_dir, "requirements.txt")
        if os.path.exists(req_file):
            print(f"\n{YELLOW}发现 requirements.txt，是否安装依赖? (y/n){RESET}")
            choice = input("> ").strip().lower()
            if choice == 'y':
                subprocess.run(["pip3", "install", "--break-system-packages", "-r", req_file])
                print(f"{GREEN}✅ 依赖安装完成{RESET}")
    else:
        print(f"{RED}❌ 克隆失败: {result.stderr}{RESET}")


def install_project(project_name: str):
    """一键安装项目"""
    if project_name not in AI_PROJECTS:
        print(f"{RED}❌ 未知项目: {project_name}{RESET}")
        return
    
    info = AI_PROJECTS[project_name]
    install_cmd = info["install"]
    
    print(f"{BLUE}🔧 正在安装 {project_name}...{RESET}")
    print(f"   命令: {install_cmd}")
    
    # 根据安装类型选择不同方式
    if install_cmd.startswith("pip"):
        subprocess.run(["pip3", "install", "--break-system-packages"] + install_cmd.split()[1:])
    elif install_cmd.startswith("npm"):
        subprocess.run(install_cmd.split())
    elif install_cmd.startswith("cargo"):
        subprocess.run(install_cmd.split())
    elif install_cmd == "git clone":
        clone_project(project_name)
        return
    else:
        print(f"{YELLOW}⚠️ 无法自动安装，请手动执行: {install_cmd}{RESET}")
        return
    
    print(f"{GREEN}✅ 安装完成!{RESET}")


def interactive_mode():
    """交互模式"""
    print_banner()
    print(f"""
{BOLD}请选择操作:{RESET}

  1. 🌐 浏览分类项目
  2. 🔍 搜索GitHub项目
  3. 📥 克隆项目到本地
  4. ⚡ 一键安装项目
  5. 🔥 今日热门项目
  6. 🚪 退出

""")
    
    choice = input(f"{BLUE}> {RESET}").strip()
    
    if choice == "1":
        print(f"\n{BOLD}选择分类:{RESET}\n")
        for i, (cat_id, cat_name) in enumerate(CATEGORIES.items(), 1):
            print(f"  {i}. {cat_name}")
        cat_choice = input(f"\n{BLUE}> {RESET}").strip()
        cat_ids = list(CATEGORIES.keys())
        if cat_choice.isdigit() and 1 <= int(cat_choice) <= len(cat_ids):
            list_supported(cat_ids[int(cat_choice)-1])
    
    elif choice == "2":
        query = input("输入搜索关键词: ").strip()
        if query:
            search_projects(query)
    
    elif choice == "3":
        project = input("输入项目名称: ").strip()
        if project:
            clone_project(project)
    
    elif choice == "4":
        project = input("输入项目名称: ").strip()
        if project:
            install_project(project)
    
    elif choice == "5":
        projects = get_trending_projects()
        print(f"\n{BOLD}🔥 今日GitHub热门 (Python):{RESET}\n")
        for i, p in enumerate(projects, 1):
            print(f"  {i}. {p['full_name']} ⭐ {p['stargazers_count']:,}")


def main():
    parser = argparse.ArgumentParser(
        description="🤖 AI项目改造器 - 把热门开源项目改造成CLI工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 main.py --list              查看支持的项目
  python3 main.py --search AI agent    搜索项目
  python3 main.py --clone browser-use  克隆项目
  python3 main.py --install mem0       一键安装
  python3 main.py --interactive        交互模式
        """
    )
    parser.add_argument("--list", "-l", action="store_true", help="列出已支持的项目")
    parser.add_argument("--search", "-s", type=str, help="搜索GitHub项目")
    parser.add_argument("--clone", "-c", type=str, help="克隆项目到本地")
    parser.add_argument("--install", "-i", type=str, help="一键安装项目")
    parser.add_argument("--trending", "-t", action="store_true", help="获取今日热门")
    parser.add_argument("--interactive", "-int", action="store_true", help="交互模式")
    parser.add_argument("--category", type=str, help="按分类查看项目")
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_mode()
    elif args.list:
        list_supported(args.category)
    elif args.search:
        search_projects(args.search)
    elif args.trending:
        projects = get_trending_projects()
        print(f"\n{BOLD}🔥 今日GitHub热门 (Python):{RESET}\n")
        for i, p in enumerate(projects, 1):
            print(f"  {i}. {p['full_name']} ⭐ {p['stargazers_count']:,} | {p.get('language', 'N/A')}")
    elif args.clone:
        clone_project(args.clone)
    elif args.install:
        install_project(args.install)
    else:
        print_banner()
        print(parser.format_help())


if __name__ == "__main__":
    main()
