<img src="assets/logo.svg" align="right" width="120" alt="Awesome Telegram Chinese 2026 logo" />

# Awesome Telegram Chinese 2026 [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> 中文 Telegram 优质资源导航：机器人、频道、群组分类整理。
> A curated, community-maintained directory of Chinese-language Telegram bots, channels, and groups.

## ⚡ 关于本项目 / About

本项目致力于分类整理真实可用、无垃圾信息的中文 Telegram 资源，帮助大家更快找到有价值的机器人、频道与交流群组。所有条目在收录前应经过维护者或提交者的实际核实。

<!-- MAINTAINER:START -->

[![Telegram](https://img.shields.io/badge/Telegram-%E5%8A%A0%E5%85%A5%E9%A2%91%E9%81%93-blue?logo=telegram&logoColor=white)](https://t.me/ezsoua)

本项目由 **易搜搜索| @ezsou_bot** 维护。项目相关讨论 / 联系方式：[易搜搜索 | Telegram资源导航](https://t.me/ezsoua)

<!-- MAINTAINER:END -->

## 🛠️ 分类目录 / Categories

### 🤖 实用机器人 (Top Bots)

AI 助理、格式转换、下载工具等。

<!-- BOTS:START -->

#### AI

| 名称 | 链接 | 简介 |
| --- | --- | --- |
| AI图片&提示词机器人 | [https://t.me/aitiwen_bot](https://t.me/aitiwen_bot) | AI图片欣赏,高质量提示词&Prompt 下载。 |

#### 工具

| 名称 | 链接 | 简介 |
| --- | --- | --- |
| 易搜中文搜索 | [https://t.me/ezsou_bot](https://t.me/ezsou_bot) | 全媒体搜索机器人, 易搜中文搜索，一搜就有！ |

<!-- BOTS:END -->

### 📢 资讯与技术频道 (Channels)

科技新闻、开发者社区、行业动态等。

<!-- CHANNELS:START -->

#### AI应用

| 名称 | 链接 | 简介 |
| --- | --- | --- |
| 🎬 AI+ ｜AI视频制作工具｜流程｜视频分享 | [https://t.me/longxiasq](https://t.me/longxiasq) | AI视频展示，AI视频制作流程拆解，工具分享！ |
| 🤖 AI+｜AI编程&程序开发 | [https://t.me/clawstaffs](https://t.me/clawstaffs) | 用 AI 自动化开发技术构建 AI Agent,数字员工 提效你的业务！ |
| 🎨 AI+｜AI做图 & 提示词分享 | [https://t.me/ailibrarya](https://t.me/ailibrarya) | 分享 GPT Image、Midjourney、FLUX、Nano Banana、Grok提示词/Prompt与做图技巧,每周更新！ |
| 👷 AI+ ｜AI提效工具&Tools推荐 | [https://t.me/skillslib](https://t.me/skillslib) | 用 AI 把你的工作效率提高 10 倍，每周分享实战工作流、skills、Agent、AI工具、AI应用案例！ |

#### 资讯与技术

| 名称 | 链接 | 简介 |
| --- | --- | --- |
| AI中文社区｜AI新闻｜ AI赚钱 | [https://t.me/aipluscn](https://t.me/aipluscn) | AI中文社区，AI行业动态，AI工具，大模型趋势与情报，  AI赚钱案例分享！ |

#### 音乐

| 名称 | 链接 | 简介 |
| --- | --- | --- |
| 流行音乐 \| 听歌吧 \| @tingeb | [https://t.me/tingeb](https://t.me/tingeb) | 分享流行音乐，推荐好歌，一起听歌吧！ |

<!-- CHANNELS:END -->

### 💬 优质交流群组 (Groups)

以禁止发广告、纯技术 / 内容交流为特色的群组。

<!-- GROUPS:START -->

#### 优质交流群组

| 名称 | 链接 | 简介 |
| --- | --- | --- |
| 出海创业交流群 | [https://t.me/NewAICommunity](https://t.me/NewAICommunity) | 🚀 出海创业者交流平台, 商机共享, 商业合作! |

<!-- GROUPS:END -->

## 🤝 如何贡献 / Contributing

欢迎通过提交 Pull Request 补充你认为优质、且已亲自核实过的频道 / 机器人 / 群组。提交前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)，包括收录标准与数据格式。

## 🔍 链接有效性检测 / Link Validation

仓库内置 [`scripts/link_checker.py`](scripts/link_checker.py)，用于批量检测 `data/*.json` 中登记的 Telegram 链接是否仍然有效：

```bash
pip install -r requirements.txt  # 目前无第三方依赖，仅使用标准库
python3 scripts/link_checker.py
```

**关于可靠性**：对于公开 `@username` 类型的机器人 / 频道，Telegram 的网页预览（t.me）即使对着一个编造但格式合法的用户名，也会乐观地渲染出"可联系 / 可加入"的页面，并不会在网页层做真实存在性校验。因此脚本默认的抓取模式只能标记为 `UNCONFIRMED`（可访问但未确认存在），无法保证条目真实有效。若需要真正可靠的校验，请通过 [@BotFather](https://t.me/BotFather) 免费申请一个 Bot Token，并设置环境变量后再运行：

```bash
export TELEGRAM_BOT_TOKEN="123456:AAExampleTokenFromBotFather"
python3 scripts/link_checker.py
```

此时脚本会改用 Telegram 官方 Bot API 的 `getChat` 接口做服务端校验，结果标记为 `OK` / `FAIL`，可信度远高于网页抓取。私有邀请链接（`t.me/+...`）目前没有可靠的自动化校验方式，Bot API 无法解析，仍需人工确认。

修改 `data/` 下的资源文件后，运行以下脚本重新生成本 README 中的表格：

```bash
python3 scripts/generate_readme.py
```

## 📄 License

[MIT](LICENSE)
