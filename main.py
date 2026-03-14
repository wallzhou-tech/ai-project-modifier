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
    "firecrawl": {
        "repo": "mendableai/firecrawl",
        "desc": "AI网页数据抓取API",
        "stars": 92879,
        "category": "browser",
        "install": "pip install firecrawl"
    },
    
    # AI记忆/知识
    "mem0": {
        "repo": "mem0ai/mem0",
        "desc": "AI的记忆层",
        "stars": 49793,
        "category": "memory",
        "install": "pip install mem0ai"
    },
    "ragflow": {
        "repo": "infiniflow/ragflow",
        "desc": "深度RAG引擎",
        "stars": 74987,
        "category": "memory",
        "install": "git clone"
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
    "langgraph": {
        "repo": "langchain-ai/langgraph",
        "desc": "构建有状态的多Actor应用",
        "stars": 28000,
        "category": "orchestration",
        "install": "pip install langgraph"
    },
    "dify": {
        "repo": "langgenius/dify",
        "desc": "Agent工作流开发平台",
        "stars": 132790,
        "category": "orchestration",
        "install": "git clone"
    },
    "langflow": {
        "repo": "langflow-ai/langflow",
        "desc": "可视化AI工作流",
        "stars": 145651,
        "category": "orchestration",
        "install": "pip install langflow"
    },
    
    # LLM/Transformer模型
    "transformers": {
        "repo": "huggingface/transformers",
        "desc": "🤗 Transformers模型库",
        "stars": 157802,
        "category": "llm",
        "install": "pip install transformers"
    },
    "vllm": {
        "repo": "vllm-project/vllm",
        "desc": "高效LLM推理服务",
        "stars": 73075,
        "category": "llm",
        "install": "pip install vllm"
    },
    "ollama": {
        "repo": "ollama/ollama",
        "desc": "本地运行大模型",
        "stars": 120000,
        "category": "llm",
        "install": "curl -fsSL https://ollama.com/install.sh | sh"
    },
    "litgpt": {
        "repo": "Lightning-AI/litgpt",
        "desc": "高性能开源大模型",
        "stars": 28000,
        "category": "llm",
        "install": "pip install litgpt"
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
    "opencode": {
        "repo": "anomalyco/opencode",
        "desc": "AI代码编辑助手",
        "stars": 122021,
        "category": "cli",
        "install": "npm install -g opencode"
    },
    "cline": {
        "repo": "cline/cline",
        "desc": "IDE中的自主编程Agent",
        "stars": 58964,
        "category": "cli",
        "install": "npm install -g cline"
    },
    "daytona": {
        "repo": "daytonaio/daytona",
        "desc": "AI开发基础设施",
        "stars": 64958,
        "category": "cli",
        "install": "brew install daytona"
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
    "llamaindex": {
        "repo": "run-llama/llama_index",
        "desc": "LLM数据框架",
        "stars": 45000,
        "category": "rag",
        "install": "pip install llama-index"
    },
    "qdrant": {
        "repo": "qdrant/qdrant",
        "desc": "向量搜索引擎",
        "stars": 32000,
        "category": "rag",
        "install": "docker pull qdrant/qdrant"
    },
    
    # 开发工具
    "open-webui": {
        "repo": "open-webui/open-webui",
        "desc": "AI聊天界面",
        "stars": 127154,
        "category": "dev",
        "install": "git clone"
    },
    "comfyui": {
        "repo": "Comfy-Org/ComfyUI",
        "desc": "模块化扩散模型GUI",
        "stars": 105827,
        "category": "dev",
        "install": "git clone"
    },
    "autogpt": {
        "repo": "Significant-Gravitas/AutoGPT",
        "desc": "自主AI Agent",
        "stars": 182449,
        "category": "dev",
        "install": "git clone"
    },
    "lobehub": {
        "repo": "lobehub/lobe-chat",
        "desc": "现代化AI聊天框架",
        "stars": 73641,
        "category": "dev",
        "install": "npx create-lobe-chat"
    },
    "nextchat": {
        "repo": "ChatGPTNextWeb/ChatGPT-Next-Web",
        "desc": "轻量级AI助手",
        "stars": 87494,
        "category": "dev",
        "install": "npx create-next-chat"
    },
    "one-api": {
        "repo": "justsong/one-api",
        "desc": "OpenAI接口管理",
        "stars": 28000,
        "category": "dev",
        "install": "docker run -d --name one-api -p 3000:3000 -v /root/.openclaw/workspace/ai-project-modifier/data:/data justsong/one-api"
    },
    
    # MCP服务器
    "mcp": {
        "repo": "modelcontextprotocol/spec",
        "desc": "MCP协议规范",
        "stars": 33000,
        "category": "mcp",
        "install": "npm install @modelcontextprotocol/sdk"
    },
    "mcp-servers": {
        "repo": "anthropics/mcp",
        "desc": "官方MCP服务器集合",
        "stars": 93317,
        "category": "mcp",
        "install": "git clone"
    },
    "n8n": {
        "repo": "n8n-io/n8n",
        "desc": "工作流自动化",
        "stars": 98000,
        "category": "mcp",
        "install": "docker run -d --name n8n -p 5678:5678 n8nio/n8n"
    },
    "claude-code": {
        "repo": "anthropics/claude-code",
        "desc": "Claude代码编写工具",
        "stars": 45000,
        "category": "mcp",
        "install": "npm install -g @anthropic-ai/claude-code"
    },
}

CATEGORIES = {
    "browser": "🌐 浏览器自动化",
    "memory": "💾 AI记忆/知识",
    "orchestration": "🔧 Agent编排",
    "llm": "🧠 LLM/模型",
    "cli": "⌨️ CLI工具",
    "rag": "📚 RAG/知识库",
    "dev": "🛠️ 开发工具",
    "mcp": "🔌 MCP/自动化",
}


def print_banner():
    """打印Banner"""
    banner = f"""
{BOLD}{BLUE}
╔═══════════════════════════════════════════════════════╗
║          🤖 AI 项目改造器 v2.0                         ║
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


def search_projects(query: str, language: Optional[str] = None, min_stars: int = 0, sort_by: str = "stars"):
    """搜索项目 - 支持过滤和排序"""
    params = [query]
    if language:
        params.append(f"language:{language}")
    if min_stars > 0:
        params.append(f"stars:>={min_stars}")
    
    search_query = "+".join(params)
    url = f"https://api.github.com/search/repositories?q={search_query}&sort={sort_by}&order=desc&per_page=15"
    
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            items = resp.json().get("items", [])
            print(f"\n{BLUE}🔍 搜索 '{query}' 结果 ({len(items)}个):{RESET}\n")
            if language:
                print(f"   {YELLOW}语言过滤: {language}{RESET}")
            if min_stars > 0:
                print(f"   {YELLOW}最低stars: {min_stars}{RESET}")
            print()
            
            for i, item in enumerate(items, 1):
                stars = item.get('stargazers_count', 0)
                lang = item.get('language', 'N/A')
                desc = item.get('description', 'No description')[:60]
                topics = item.get('topics', [])[:3]
                
                print(f"  {i}. {BOLD}{item['full_name']}{RESET}")
                print(f"     📝 {desc}")
                print(f"     ⭐ {stars:,} | {lang} | 🕐 {item.get('updated_at', '')[:10]}")
                if topics:
                    print(f"     🏷️ {', '.join(topics)}")
                print()
        elif resp.status_code == 422:
            print(f"{RED}❌ 搜索语法错误{RESET}")
        else:
            print(f"{RED}❌ 搜索失败: {resp.status_code}{RESET}")
    except Exception as e:
        print(f"{RED}❌ 搜索出错: {e}{RESET}")


def compare_projects(project_names: List[str]):
    """项目对比功能"""
    projects = []
    for name in project_names:
        if name in AI_PROJECTS:
            projects.append((name, AI_PROJECTS[name]))
        else:
            print(f"{YELLOW}⚠️ 未知项目: {name}{RESET}")
    
    if not projects:
        print(f"{RED}没有可对比的项目{RESET}")
        return
    
    print(f"\n{BOLD}{BLUE}📊 项目对比{RESET}\n")
    print("=" * 80)
    
    header = f"{'项目名':<20} {'描述':<30} {'Stars':<10} {'分类':<15}"
    print(header)
    print("-" * 80)
    
    for name, info in projects:
        desc = info['desc'][:28] + ".." if len(info['desc']) > 30 else info['desc']
        cat = CATEGORIES.get(info['category'], info['category'])
        print(f"{name:<20} {desc:<30} {info['stars']:>8,} {cat:<15}")
    
    print("-" * 80)
    
    if len(projects) >= 2:
        max_stars = max(p[1]['stars'] for p in projects)
        print(f"\n{GREEN}🏆 最受欢迎: {[p[0] for p in projects if p[1]['stars'] == max_stars][0]}{RESET}")
    
    print()


def deploy_project(project_name: str, method: str = "docker"):
    """自动部署项目"""
    if project_name not in AI_PROJECTS:
        print(f"{RED}❌ 未知项目: {project_name}{RESET}")
        return
    
    info = AI_PROJECTS[project_name]
    repo = info["repo"]
    
    print(f"\n{BLUE}🚀 自动部署: {project_name}{RESET}\n")
    print(f"   仓库: {repo}")
    print(f"   方式: {method}")
    
    if method == "docker":
        port = input(f"{YELLOW}请输入端口 (默认8080): {RESET}").strip() or "8080"
        container_name = f"ai-{project_name}"
        
        print(f"\n{GREEN}📦 拉取Docker镜像...{RESET}")
        
        result = subprocess.run(
            ["docker", "run", "-d", f"--name={container_name}", f"-p={port}:8080", 
             "--restart=unless-stopped", f"ghcr.io/{repo.lower()}/latest"],
            capture_output=True, text=True
        )
        
        if result.returncode == 0:
            print(f"{GREEN}✅ 部署成功!{RESET}")
            print(f"   访问地址: http://localhost:{port}")
            print(f"   容器名: {container_name}")
        else:
            print(f"{YELLOW}⚠️ 自动部署失败，尝试克隆部署...{RESET}")
            deploy_from_source(project_name, port)
    
    elif method == "source":
        port = input(f"{YELLOW}请输入端口 (默认8080): {RESET}").strip() or "8080"
        deploy_from_source(project_name, port)
    
    else:
        print(f"{RED}❌ 未知部署方式: {method}{RESET}")
        print(f"可用方式: docker, source")


def deploy_from_source(project_name: str, port: str):
    """从源码部署"""
    info = AI_PROJECTS[project_name]
    repo = info["repo"]
    target_dir = f"/root/.openclaw/workspace/deployed/{project_name}"
    
    print(f"\n{BLUE}📥 克隆项目...{RESET}")
    os.makedirs(target_dir, exist_ok=True)
    
    result = subprocess.run(
        ["git", "clone", f"https://github.com/{repo}.git", target_dir],
        capture_output=True, text=True
    )
    
    if result.returncode == 0:
        print(f"{GREEN}✅ 克隆成功!{RESET}")
        
        if os.path.exists(os.path.join(target_dir, "Dockerfile")):
            print(f"{BLUE}🐳 构建Docker镜像...{RESET}")
            img_name = f"ai-{project_name}:latest"
            build_result = subprocess.run(
                ["docker", "build", "-t", img_name, target_dir],
                capture_output=True, text=True
            )
            if build_result.returncode == 0:
                container_name = f"ai-{project_name}"
                subprocess.run(["docker", "rm", "-f", container_name], capture_output=True)
                run_result = subprocess.run(
                    ["docker", "run", "-d", f"--name={container_name}", f"-p={port}:8080",
                     "--restart=unless-stopped", img_name],
                    capture_output=True, text=True
                )
                if run_result.returncode == 0:
                    print(f"{GREEN}✅ 部署成功!{RESET}")
                    print(f"   访问地址: http://localhost:{port}")
                else:
                    print(f"{RED}❌ 启动失败: {run_result.stderr}{RESET}")
            else:
                print(f"{RED}❌ 构建失败: {build_result.stderr}{RESET}")
        else:
            print(f"{YELLOW}⚠️ 未找到Dockerfile，请手动配置运行{RESET}")
    else:
        print(f"{RED}❌ 克隆失败: {result.stderr}{RESET}")


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
  5. 🚀 自动部署项目
  6. 📊 项目对比
  7. 🔥 今日热门项目
  8. 🚪 退出

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
            lang = input("语言过滤 (python/typescript/go/java, 回车跳过): ").strip()
            min_stars = input("最低stars (回车跳过): ").strip()
            min_stars = int(min_stars) if min_stars.isdigit() else 0
            search_projects(query, language=lang if lang else None, min_stars=min_stars)
    
    elif choice == "3":
        project = input("输入项目名称: ").strip()
        if project:
            clone_project(project)
    
    elif choice == "4":
        project = input("输入项目名称: ").strip()
        if project:
            install_project(project)
    
    elif choice == "5":
        project = input("输入项目名称: ").strip()
        if project:
            method = input("部署方式 (docker/source, 默认docker): ").strip() or "docker"
            deploy_project(project, method)
    
    elif choice == "6":
        print(f"\n{BOLD}输入要对比的项目名 (空格分隔, 最多5个):{RESET}")
        projects = input(f"{BLUE}> {RESET}").strip().split()[:5]
        if projects:
            compare_projects(projects)
    
    elif choice == "7":
        lang_choice = input("语言 (python/typescript/go, 回车默认python): ").strip() or "python"
        projects = get_trending_projects(language=lang_choice)
        print(f"\n{BOLD}🔥 今日GitHub热门 ({lang_choice}):{RESET}\n")
        for i, p in enumerate(projects, 1):
            print(f"  {i}. {p['full_name']} ⭐ {p['stargazers_count']:,} | {p.get('language', 'N/A')}")


def main():
    parser = argparse.ArgumentParser(
        description="🤖 AI项目改造器 - 把热门开源项目改造成CLI工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 main.py --list              查看支持的项目
  python3 main.py --search AI agent    搜索项目
  python3 main.py --search ai --lang python --min-stars 1000
  python3 main.py --clone browser-use  克隆项目
  python3 main.py --install mem0       一键安装
  python3 main.py --deploy flowise     自动部署
  python3 main.py --compare mem0 crewai autogen
  python3 main.py --interactive        交互模式
        """
    )
    parser.add_argument("--list", "-l", action="store_true", help="列出已支持的项目")
    parser.add_argument("--search", "-s", type=str, help="搜索GitHub项目")
    parser.add_argument("--lang", type=str, help="搜索语言过滤 (python/typescript/go/java)")
    parser.add_argument("--min-stars", type=int, default=0, help="最低stars数")
    parser.add_argument("--clone", "-c", type=str, help="克隆项目到本地")
    parser.add_argument("--install", "-i", type=str, help="一键安装项目")
    parser.add_argument("--deploy", "-d", type=str, help="自动部署项目")
    parser.add_argument("--deploy-method", type=str, default="docker", choices=["docker", "source"], help="部署方式")
    parser.add_argument("--compare", nargs="+", help="对比多个项目")
    parser.add_argument("--trending", "-t", action="store_true", help="获取今日热门")
    parser.add_argument("--trending-lang", type=str, default="python", help="热门项目语言")
    parser.add_argument("--interactive", "-int", action="store_true", help="交互模式")
    parser.add_argument("--category", type=str, help="按分类查看项目")
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_mode()
    elif args.list:
        list_supported(args.category)
    elif args.search:
        search_projects(args.search, language=args.lang, min_stars=args.min_stars)
    elif args.trending:
        projects = get_trending_projects(language=args.trending_lang)
        print(f"\n{BOLD}🔥 今日GitHub热门 ({args.trending_lang}):{RESET}\n")
        for i, p in enumerate(projects, 1):
            print(f"  {i}. {p['full_name']} ⭐ {p['stargazers_count']:,} | {p.get('language', 'N/A')}")
    elif args.clone:
        clone_project(args.clone)
    elif args.install:
        install_project(args.install)
    elif args.deploy:
        deploy_project(args.deploy, args.deploy_method)
    elif args.compare:
        compare_projects(args.compare)
    else:
        print_banner()
        print(parser.format_help())


if __name__ == "__main__":
    main()
