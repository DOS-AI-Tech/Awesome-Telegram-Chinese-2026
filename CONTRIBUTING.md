# 贡献指南 / Contributing

感谢你愿意为本项目补充资源！为了保持列表质量，请遵循以下要求。

## 收录标准

- 你已经**亲自加入 / 使用过**该机器人、频道或群组，并能确认其当前仍然活跃、有效。
- 内容合法合规，不涉及博彩、色情、诈骗、违禁品交易等内容。
- 群组类条目请注明入群规则（例如是否禁止广告）。
- 不接受纯引流、无实际内容的机器人或频道。

## 提交方式

1. Fork 本仓库。
2. 编辑对应分类的数据文件：
   - 机器人 → [`data/bots.json`](data/bots.json)
   - 频道 → [`data/channels.json`](data/channels.json)
   - 群组 → [`data/groups.json`](data/groups.json)
3. 按照现有格式新增一条 JSON 对象，字段说明：

   | 字段 | 说明 |
   | --- | --- |
   | `name` | 显示名称 |
   | `username` | Telegram 用户名（不含 @），私有邀请链接可留空 |
   | `url` | 完整的 `https://t.me/...` 链接 |
   | `description` | 一句话简介，说明用途或特色 |
   | `category` | 分类名称，用于 README 中的分组 |
   | `added_by` | 你的 GitHub 用户名 |
   | `verified` | 是否已亲自核实，请如实填写为 `true` |

4. 本地运行链接检测，确认新增链接有效：

   ```bash
   python3 scripts/link_checker.py
   ```

5. 运行以下命令重新生成 README 中的表格，并将改动一并提交：

   ```bash
   python3 scripts/generate_readme.py
   ```

6. 提交 Pull Request，简单说明该资源的用途与你的核实方式。

维护者会定期运行 `link_checker.py` 清理失效链接；长期无法访问的条目可能会被移除。
