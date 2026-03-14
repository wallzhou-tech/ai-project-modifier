#!/usr/bin/env python3
"""
AI项目改造器 - 把热门开源项目改造成CLI工具
"""

import argparse
import json
import os
import subprocess
import sys
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
HEADERS = {"Accept": "application/vnd.github.v3+json"}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"token {GITHUB_TOKEN}"

SUPPORTED_PROJECTS = {
    "browser-use": {
        "repo": "browser-use/browser-use",
        "desc": "让AI控制浏览器自动化",
        "stars": 80760
    },
    "mem0": {
        "repo": "mem0ai/mem0", 
        "desc": "AI的记忆层",
        "stars": 49793
    },
    "crewai": {
        "repo": "crewAIInc/crewAI",
        "desc": "AI Agent编排框架",
        "stars": 46043
    },
    "cli-anything": {
        "repo": "HKUDS/CLI-Anything",
        "desc": "让所有软件变成CLI工具",
        "stars": 13127
    }
}

def get_trending_projects(language="python", limit=10):
    """获取GitHub热门项目"""
    url = f"https://api.github.com/search/repositories?q=language:{language}+sort:stars&order=desc&per_page={limit}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        return resp.json().get("items", [])
    return []

def list_supported():
    """列出已支持的项目"""
    print("\n📦 已支持的项目:\n")
    for name, info in SUPPORTED_PROJECTS.items():
        print(f"  • {name}")
        print(f"    {info['desc']} ⭐ {info['stars']:,}")
        print()
    
def search_projects(query):
    """搜索项目"""
    url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page=10"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        items = resp.json().get("items", [])
        print(f"\n🔍 搜索 '{query}' 结果:\n")
        for i, item in enumerate(items, 1):
            print(f"  {i}. {item['full_name']}")
            print(f"     {item.get('description', 'No description')[:60]}...")
            print(f"     ⭐ {item['stargazers_count']:,} | {item.get('language', 'N/A')}")
            print()
    else:
        print(f"❌ 搜索失败: {resp.text}")

def clone_project(repo):
    """克隆项目到本地"""
    print(f"📥 正在克隆 {repo}...")
    result = subprocess.run(
        ["git", "clone", f"https://github.com/{repo}.git", f"/tmp/{repo.replace('/', '-')}"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"✅ 克隆成功! 保存到 /tmp/{repo.replace('/', '-')}")
    else:
        print(f"❌ 克隆失败: {result.stderr}")

def main():
    parser = argparse.ArgumentParser(description="AI项目改造器")
    parser.add_argument("--list", "-l", action="store_true", help="列出已支持的项目")
    parser.add_argument("--search", "-s", type=str, help="搜索GitHub项目")
    parser.add_argument("--clone", "-c", type=str, help="克隆项目")
    parser.add_argument("--trending", "-t", action="store_true", help="获取今日热门")
    
    args = parser.parse_args()
    
    if args.list:
        list_supported()
    elif args.search:
        search_projects(args.search)
    elif args.trending:
        projects = get_trending_projects()
        print("\n🔥 今日GitHub热门 (Python):\n")
        for i, p in enumerate(projects, 1):
            print(f"  {i}. {p['full_name']} ⭐ {p['stargazers_count']:,}")
    elif args.clone:
        clone_project(args.clone)
    else:
        print("""
🤖 AI项目改造器

用法:
  python main.py --list          查看已支持项目
  python main.py --search <关键词>  搜索项目
  python main.py --clone <repo>    克隆项目
  python main.py --trending        今日热门
        """)

if __name__ == "__main__":
    main()
