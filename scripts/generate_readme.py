#!/usr/bin/env python3
"""Regenerate the resource tables in README.md from data/*.json.

The README contains marker comment pairs like:

    <!-- BOTS:START --> ... <!-- BOTS:END -->

Everything between a pair is replaced with a markdown table built from the
corresponding data file. Run this after editing any file under data/.

Usage:
    python3 scripts/generate_readme.py [--readme README.md] [--data-dir data]
"""
import argparse
import json
from collections import defaultdict
from pathlib import Path

# Maps marker name -> (data filename, section is grouped by "category")
SECTIONS = {
    "BOTS": "bots.json",
    "CHANNELS": "channels.json",
    "GROUPS": "groups.json",
}


def load(data_dir: Path, filename: str):
    path = data_dir / filename
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def render_table(entries) -> str:
    if not entries:
        return "_暂无条目，欢迎提交 PR 补充。_\n"

    by_category = defaultdict(list)
    for entry in entries:
        by_category[entry.get("category", "未分类")].append(entry)

    lines = []
    for category in sorted(by_category):
        lines.append(f"#### {category}\n")
        lines.append("| 名称 | 链接 | 简介 |")
        lines.append("| --- | --- | --- |")
        for entry in by_category[category]:
            name = entry.get("name", "")
            url = entry.get("url", "")
            desc = entry.get("description", "")
            lines.append(f"| {name} | [{url}]({url}) | {desc} |")
        lines.append("")
    return "\n".join(lines)


def render_maintainer(data_dir: Path) -> str:
    path = data_dir / "maintainer.json"
    if not path.exists():
        return "_未配置维护者信息。_\n"
    info = json.loads(path.read_text(encoding="utf-8"))
    name = info.get("name", "")
    channel_name = info.get("channel_name", "")
    channel_url = info.get("channel_url", "")
    return f"本项目由 **{name}** 维护。项目相关讨论 / 联系方式：[{channel_name}]({channel_url})\n"


def replace_section(content: str, marker: str, replacement: str) -> str:
    start = f"<!-- {marker}:START -->"
    end = f"<!-- {marker}:END -->"
    start_idx = content.find(start)
    end_idx = content.find(end)
    if start_idx == -1 or end_idx == -1:
        raise ValueError(f"Markers for {marker} not found in README")
    return (
        content[: start_idx + len(start)]
        + "\n\n"
        + replacement
        + "\n"
        + content[end_idx:]
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--readme", default="README.md", type=Path)
    parser.add_argument("--data-dir", default="data", type=Path)
    args = parser.parse_args()

    content = args.readme.read_text(encoding="utf-8")

    for marker, filename in SECTIONS.items():
        entries = load(args.data_dir, filename)
        content = replace_section(content, marker, render_table(entries))

    content = replace_section(content, "MAINTAINER", render_maintainer(args.data_dir))

    args.readme.write_text(content, encoding="utf-8")
    print(f"Updated {args.readme}")


if __name__ == "__main__":
    main()
