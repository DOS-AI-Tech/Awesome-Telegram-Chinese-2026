# Awesome Telegram Chinese 2026

> 中文 Telegram 优质资源导航：机器人、频道、群组分类整理。
> A curated, community-maintained directory of Chinese-language Telegram bots, channels, and groups.

## ⚡ 关于本项目 / About

本项目致力于分类整理真实可用、无垃圾信息的中文 Telegram 资源，帮助大家更快找到有价值的机器人、频道与交流群组。所有条目在收录前应经过维护者或提交者的实际核实。

<!-- MAINTAINER:START -->

本项目由 **易搜搜索| @ezsou_bot** 维护。项目相关讨论 / 联系方式：[易搜搜索 | Telegram资源导航](https://t.me/ezsoua)

<!-- MAINTAINER:END -->

## 🛠️ 分类目录 / Categories

### 🤖 实用机器人 (Top Bots)

AI 助理、格式转换、下载工具等。

<!-- BOTS:START -->

#### AI 助理

| 名称                       | 链接                                                    | 简介                                                       |
| -------------------------- | ------------------------------------------------------- | ---------------------------------------------------------- |
| 示例：AI 助理机器人 (占位) | [https://t.me/example_ai_bot](https://t.me/example_ai_bot) | 占位条目 — 请替换为你已实际核实过的真实机器人及准确介绍。 |

#### 格式转换

| 名称                        | 链接                                                              | 简介                                                       |
| --------------------------- | ----------------------------------------------------------------- | ---------------------------------------------------------- |
| 示例：格式转换机器人 (占位) | [https://t.me/example_convert_bot](https://t.me/example_convert_bot) | 占位条目 — 请替换为你已实际核实过的真实机器人及准确介绍。 |

<!-- BOTS:END -->

### 📢 资讯与技术频道 (Channels)

科技新闻、开发者社区、行业动态等。

<!-- CHANNELS:START -->

#### 资讯与技术

| 名称                      | 链接                                                                | 简介                                                                                       |
| ------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| 示例：科技资讯频道 (占位) | [https://t.me/example_tech_channel](https://t.me/example_tech_channel) | 占位条目 — 请替换为你已实际核实过的真实频道及准确介绍，避免收录无法核实内容合规性的频道。 |

<!-- CHANNELS:END -->

### 💬 优质交流群组 (Groups)

以禁止发广告、纯技术 / 内容交流为特色的群组。

<!-- GROUPS:START -->

#### 优质交流群组

| 名称                    | 链接                                                                  | 简介                                                                            |
| ----------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| 示例：纯交流群组 (占位) | [https://t.me/example_discuss_group](https://t.me/example_discuss_group) | 占位条目 — 请替换为真实、以禁止广告 / 高质量交流为特色的群组，并注明入群规则。 |

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
