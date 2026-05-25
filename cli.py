#!/usr/bin/env python3
"""
ai-prompt-library CLI - 快速搜索和使用 AI 提示词

Usage:
    python cli.py list                          # 列出所有提示词
    python cli.py search "code review"          # 搜索提示词
    python cli.py view prompts/coding/debug-assistant  # 查看提示词
    python cli.py copy prompts/coding/debug-assistant  # 复制到剪贴板
"""

import argparse
import os
import sys
import json
from pathlib import Path
from fnmatch import fnmatch

PROMPTS_DIR = Path(__file__).parent / "prompts"


def list_prompts():
    """列出所有提示词."""
    print("\n📋 提示词列表\n")
    categories = {}
    for md in PROMPTS_DIR.rglob("*.md"):
        cat = md.parent.name
        categories.setdefault(cat, []).append(md.name)

    for cat, files in sorted(categories.items()):
        print(f"  📁 {cat}/")
        for f in sorted(files):
            # Extract title from first line
            title = ""
            try:
                with open(PROMPTS_DIR / cat / f) as fh:
                    first = fh.readline()
                    if first.startswith("# "):
                        title = first[2:].strip()
            except Exception:
                pass
            print(f"      {title or f.replace('.md', '')}")
        print()


def search_prompts(query):
    """搜索提示词."""
    results = []
    query_lower = query.lower()
    for md in PROMPTS_DIR.rglob("*.md"):
        rel = md.relative_to(PROMPTS_DIR)
        try:
            with open(md, encoding="utf-8") as f:
                content = f.read()
            if query_lower in content.lower():
                title = ""
                for line in content.split("\n"):
                    if line.startswith("# "):
                        title = line[2:].strip()
                        break
                results.append((rel, title or rel.name))
        except Exception:
            pass

    if not results:
        print(f"❌ 没有找到与 '{query}' 相关的提示词")
        return

    print(f"\n🔍 找到 {len(results)} 个匹配\n")
    for i, (rel, title) in enumerate(results, 1):
        print(f"  {i}. {rel}")
        print(f"     {title}")
        print()


def view_prompt(path):
    """查看提示词内容."""
    md = PROMPTS_DIR / path
    if not md.exists():
        # Try to find it
        for f in PROMPTS_DIR.rglob("*.md"):
            if f.name == path or str(f.relative_to(PROMPTS_DIR)) == path:
                md = f
                break
    if not md.exists():
        print(f"❌ 找不到: {path}")
        return

    with open(md, encoding="utf-8") as f:
        content = f.read()
    print("\n" + content)


def copy_prompt(path):
    """复制提示词到剪贴板."""
    md = PROMPTS_DIR / path
    if not md.exists():
        for f in PROMPTS_DIR.rglob("*.md"):
            if f.name == path or str(f.relative_to(PROMPTS_DIR)) == path:
                md = f
                break
    if not md.exists():
        print(f"❌ 找不到: {path}")
        return

    with open(md, encoding="utf-8") as f:
        content = f.read()

    # Try to copy to clipboard
    try:
        import subprocess
        subprocess.run(["pbcopy"], input=content, text=True, check=True)
        print("✅ 已复制到剪贴板")
    except (FileNotFoundError, subprocess.SubprocessError):
        # Fallback: print raw text for manual copy
        # Extract code block content
        in_block = False
        lines = []
        for line in content.split("\n"):
            if line.strip() == "```" and not in_block:
                in_block = True
                continue
            elif line.strip() == "```" and in_block:
                break
            elif in_block:
                lines.append(line)

        if lines:
            print("✅ 提示词内容 (手动复制):")
            print("\n".join(lines))
        else:
            print(content)


def main():
    parser = argparse.ArgumentParser(
        prog="ai-prompts",
        description="AI 提示词库 CLI 工具",
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list", help="列出所有提示词")
    s = sub.add_parser("search", help="搜索提示词")
    s.add_argument("query", help="搜索关键词")
    s = sub.add_parser("view", help="查看提示词")
    s.add_argument("path", help="提示词路径")
    s = sub.add_parser("copy", help="复制到剪贴板")
    s.add_argument("path", help="提示词路径")

    args = parser.parse_args()

    if args.command == "list":
        list_prompts()
    elif args.command == "search":
        search_prompts(args.query)
    elif args.command == "view":
        view_prompt(args.path)
    elif args.command == "copy":
        copy_prompt(args.path)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
