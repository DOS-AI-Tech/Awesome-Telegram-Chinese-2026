#!/usr/bin/env python3
"""Generate the static GitHub Pages site (docs/index.html + robots.txt +
sitemap.xml) from data/*.json — the same source of truth used by
generate_readme.py. Run this after editing any file under data/.

Usage:
    python3 scripts/generate_site.py [--data-dir data] [--out-dir docs]
"""
import argparse
import html
import json
from collections import defaultdict
from datetime import date
from pathlib import Path

SITE_URL = "https://dos-ai-tech.github.io/Awesome-Telegram-Chinese-2026/"
SITE_NAME = "Awesome Telegram Chinese 2026"
SITE_TITLE = "Awesome Telegram Chinese 2026 | 中文 Telegram 优质资源导航（机器人·频道·群组）"
SITE_DESCRIPTION = (
    "精心分类整理 2026 年最新、真实可用的中文 Telegram 机器人、频道与交流群组，"
    "所有条目均经过维护者或提交者亲自核实，持续更新，欢迎提交 PR 补充。"
)
REPO_URL = "https://github.com/DOS-AI-Tech/Awesome-Telegram-Chinese-2026"

SECTIONS = [
    ("bots", "🤖 实用机器人", "AI 助理、格式转换、下载工具等。", "bots.json"),
    ("channels", "📢 资讯与技术频道", "科技新闻、开发者社区、行业动态等。", "channels.json"),
    ("groups", "💬 优质交流群组", "以禁止发广告、纯技术 / 内容交流为特色的群组。", "groups.json"),
]


def load_json(path: Path):
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def render_cards(entries) -> str:
    if not entries:
        return '<p class="empty">暂无条目，欢迎提交 PR 补充。</p>'

    by_category = defaultdict(list)
    for entry in entries:
        by_category[entry.get("category", "未分类")].append(entry)

    parts = []
    for category in sorted(by_category):
        parts.append(f'<h3 class="category">{esc(category)}</h3>')
        parts.append('<div class="grid">')
        for entry in by_category[category]:
            name = esc(entry.get("name", ""))
            url = esc(entry.get("url", ""))
            desc = esc(entry.get("description", ""))
            search_blob = esc(f"{entry.get('name', '')} {entry.get('description', '')}".lower())
            parts.append(
                f'<article class="card" data-search="{search_blob}">'
                f'<h4>{name}</h4>'
                f'<p>{desc}</p>'
                f'<a class="btn" href="{url}" target="_blank" rel="noopener noreferrer ugc">'
                f'在 Telegram 中打开 →</a>'
                f'</article>'
            )
        parts.append('</div>')
    return "\n".join(parts)


def build_json_ld(all_entries) -> str:
    items = []
    for i, entry in enumerate(all_entries, start=1):
        items.append({
            "@type": "ListItem",
            "position": i,
            "url": entry.get("url", ""),
            "name": entry.get("name", ""),
        })
    data = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": SITE_NAME,
        "description": SITE_DESCRIPTION,
        "url": SITE_URL,
        "inLanguage": "zh-CN",
        "mainEntity": {
            "@type": "ItemList",
            "itemListElement": items,
        },
    }
    return json.dumps(data, ensure_ascii=False, indent=2)


def render_maintainer_footer(data_dir: Path) -> str:
    path = data_dir / "maintainer.json"
    if not path.exists():
        return ""
    info = json.loads(path.read_text(encoding="utf-8"))
    name = esc(info.get("name", ""))
    channel_name = esc(info.get("channel_name", ""))
    channel_url = esc(info.get("channel_url", ""))
    return (
        f'<p>本项目由 <strong>{name}</strong> 维护。'
        f'项目相关讨论 / 联系方式：<a href="{channel_url}" target="_blank" rel="noopener noreferrer">{channel_name}</a></p>'
    )


PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{site_title}</title>
<meta name="description" content="{site_description}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{site_url}">
<link rel="icon" type="image/png" href="assets/favicon-64.png">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">

<meta property="og:type" content="website">
<meta property="og:site_name" content="{site_name}">
<meta property="og:title" content="{site_title}">
<meta property="og:description" content="{site_description}">
<meta property="og:url" content="{site_url}">
<meta property="og:image" content="{site_url}assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="zh_CN">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{site_title}">
<meta name="twitter:description" content="{site_description}">
<meta name="twitter:image" content="{site_url}assets/og-image.png">

<script type="application/ld+json">
{json_ld}
</script>

<style>
  :root {{
    --accent-cyan: #22D3EE;
    --accent-teal: #2DD4A7;
    --accent-green: #86EFAC;
    --ink: #083344;
    --ink-soft: #0F3B33;
    --bg: #F7FBFA;
    --card-bg: #FFFFFF;
    --card-border: #E1EEEA;
    --muted: #5B6C68;
    --radius: 16px;
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{
      --bg: #0B1615;
      --card-bg: #12201E;
      --card-border: #1E332F;
      --ink: #EAF7F4;
      --ink-soft: #D6ECE6;
      --muted: #9DB3AE;
    }}
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    font-family: -apple-system, "PingFang SC", "Microsoft YaHei", "Segoe UI", sans-serif;
    background: var(--bg);
    color: var(--ink);
    line-height: 1.6;
  }}
  a {{ color: inherit; }}
  .skip-link {{
    position: absolute; left: -999px; top: 0;
    background: #fff; color: #000; padding: 8px 16px; z-index: 100;
  }}
  .skip-link:focus {{ left: 8px; top: 8px; }}
  header.hero {{
    background: linear-gradient(135deg, var(--accent-cyan) 0%, var(--accent-teal) 55%, var(--accent-green) 100%);
    padding: 48px 20px 40px;
    color: var(--ink);
  }}
  .hero-inner {{ max-width: 960px; margin: 0 auto; display: flex; gap: 28px; align-items: center; flex-wrap: wrap; }}
  .hero-logo {{ width: 120px; height: 120px; border-radius: 50%; background: #fff; padding: 4px; flex-shrink: 0; }}
  .hero-logo img {{ width: 100%; height: 100%; border-radius: 50%; object-fit: cover; display: block; }}
  .hero-text h1 {{ margin: 0 0 8px; font-size: clamp(28px, 4vw, 42px); }}
  .hero-text p.tagline {{ margin: 0 0 16px; font-size: 18px; color: var(--ink-soft); }}
  .badges {{ display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 16px; }}
  .badges img {{ height: 20px; display: block; }}
  .search-box {{ max-width: 420px; }}
  .search-box input {{
    width: 100%; padding: 12px 16px; border-radius: 999px; border: none;
    font-size: 16px; background: rgba(255,255,255,0.92); color: #0F3B33;
  }}
  nav.toc {{ max-width: 960px; margin: 0 auto; padding: 16px 20px 0; display: flex; gap: 16px; flex-wrap: wrap; font-size: 14px; }}
  nav.toc a {{ text-decoration: none; color: var(--muted); }}
  main {{ max-width: 960px; margin: 0 auto; padding: 24px 20px 60px; }}
  section {{ margin-bottom: 40px; }}
  section > p.section-desc {{ color: var(--muted); margin-top: -8px; }}
  h2 {{ font-size: 26px; border-bottom: 2px solid var(--card-border); padding-bottom: 8px; }}
  h3.category {{ font-size: 18px; color: var(--muted); margin: 24px 0 12px; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 14px; }}
  .card {{
    background: var(--card-bg); border: 1px solid var(--card-border); border-radius: var(--radius);
    padding: 16px; display: flex; flex-direction: column; gap: 8px;
  }}
  .card h4 {{ margin: 0; font-size: 16px; }}
  .card p {{ margin: 0; color: var(--muted); font-size: 14px; flex-grow: 1; }}
  .card .btn {{
    align-self: flex-start; text-decoration: none; font-size: 14px; font-weight: 600;
    color: #0EA5A0; margin-top: 4px;
  }}
  .card.hidden {{ display: none; }}
  .empty {{ color: var(--muted); }}
  footer {{
    max-width: 960px; margin: 0 auto; padding: 24px 20px 60px; color: var(--muted); font-size: 14px;
  }}
  footer a {{ color: #0EA5A0; }}
  footer p {{ margin: 4px 0; }}
</style>
</head>
<body>
<a class="skip-link" href="#main">跳到主要内容</a>
<header class="hero">
  <div class="hero-inner">
    <div class="hero-logo"><img src="assets/apple-touch-icon.png" alt="{site_name} logo" width="120" height="120"></div>
    <div class="hero-text">
      <h1>{site_name}</h1>
      <p class="tagline">中文 Telegram 优质资源导航：机器人、频道、群组分类整理</p>
      <div class="badges">
        <a href="https://awesome.re" target="_blank" rel="noopener noreferrer"><img src="https://awesome.re/badge.svg" alt="Awesome"></a>
        <a href="{repo_url}" target="_blank" rel="noopener noreferrer"><img src="https://img.shields.io/badge/GitHub-源码-181717?logo=github&logoColor=white" alt="GitHub"></a>
        <a href="{repo_url}/blob/main/LICENSE" target="_blank" rel="noopener noreferrer"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
      </div>
      <div class="search-box">
        <label for="search" class="sr-only" style="position:absolute;left:-9999px;">搜索资源</label>
        <input type="search" id="search" placeholder="搜索机器人 / 频道 / 群组名称或简介…" autocomplete="off">
      </div>
    </div>
  </div>
</header>

<nav class="toc" aria-label="分类导航">
  <a href="#about">关于本项目</a>
  <a href="#bots">实用机器人</a>
  <a href="#channels">资讯与技术频道</a>
  <a href="#groups">优质交流群组</a>
  <a href="#contributing">如何贡献</a>
</nav>

<main id="main">
  <section id="about">
    <h2>⚡ 关于本项目</h2>
    <p>{site_description}</p>
  </section>

{sections_html}

  <section id="contributing">
    <h2>🤝 如何贡献</h2>
    <p>欢迎通过提交 Pull Request 补充你认为优质、且已亲自核实过的频道 / 机器人 / 群组。
      详见 <a href="{repo_url}/blob/main/CONTRIBUTING.md" target="_blank" rel="noopener noreferrer">CONTRIBUTING.md</a>。</p>
  </section>
</main>

<footer>
  {maintainer_footer}
  <p>数据源与完整文档见 <a href="{repo_url}" target="_blank" rel="noopener noreferrer">GitHub 仓库</a>。</p>
  <p>© {year} {site_name} · <a href="{repo_url}/blob/main/LICENSE" target="_blank" rel="noopener noreferrer">MIT License</a></p>
</footer>

<script>
  document.getElementById('search').addEventListener('input', function (e) {{
    var q = e.target.value.trim().toLowerCase();
    document.querySelectorAll('.card').forEach(function (card) {{
      var hay = card.getAttribute('data-search') || '';
      card.classList.toggle('hidden', q.length > 0 && hay.indexOf(q) === -1);
    }});
  }});
</script>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", default="data", type=Path)
    parser.add_argument("--out-dir", default="docs", type=Path)
    args = parser.parse_args()

    all_entries = []
    sections_html_parts = []
    for anchor, heading, desc, filename in SECTIONS:
        entries = load_json(args.data_dir / filename)
        all_entries.extend(entries)
        sections_html_parts.append(
            f'  <section id="{anchor}">\n'
            f'    <h2>{esc(heading)}</h2>\n'
            f'    <p class="section-desc">{esc(desc)}</p>\n'
            f'    {render_cards(entries)}\n'
            f'  </section>'
        )

    html_out = PAGE_TEMPLATE.format(
        site_title=esc(SITE_TITLE),
        site_description=esc(SITE_DESCRIPTION),
        site_name=esc(SITE_NAME),
        site_url=SITE_URL,
        repo_url=REPO_URL,
        json_ld=build_json_ld(all_entries),
        sections_html="\n\n".join(sections_html_parts),
        maintainer_footer=render_maintainer_footer(args.data_dir),
        year=date.today().year,
    )

    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "index.html").write_text(html_out, encoding="utf-8")
    (args.out_dir / ".nojekyll").write_text("", encoding="utf-8")
    (args.out_dir / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}sitemap.xml\n", encoding="utf-8"
    )
    (args.out_dir / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"  <url><loc>{SITE_URL}</loc><changefreq>weekly</changefreq></url>\n"
        "</urlset>\n",
        encoding="utf-8",
    )
    print(f"Wrote {args.out_dir}/index.html, robots.txt, sitemap.xml, .nojekyll")


if __name__ == "__main__":
    main()
