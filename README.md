# Interaction Contract

> Turn fuzzy software requests into auditable interaction contracts before coding.

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-portable-2ea44f)](https://github.com/ypeachee/interaction-contract)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

`interaction-contract` 是一个可迁移的 Agent Skill，用来把“我想要一个工作台/网页/App”变成可执行、可验收、可交接的交互规格。

它不先写代码，而是先固定：

- 第一用户与核心任务；
- 信息架构与界面表面；
- 正常、空、加载、错误、恢复状态；
- P0、P1、非目标与约束；
- 数据、持久化、隐私和不可逆操作；
- 可执行的验收测试与证据要求。

## 输出

默认生成两个文件：

```text
INTERACTION_SPEC.md     # 交互权威
ACCEPTANCE_TESTS.csv    # 可执行验收清单
```

`INTERACTION_SPEC.md` 使用固定十章结构：决策摘要、用户与任务、范围、信息架构、核心流程与状态、交互规则、数据与恢复、可访问性与跨端、验收标准、假设/风险/未知。

## 适用场景

- 网页、工作台、桌面应用、移动端、PWA、APK；
- 单流程小工具；
- 多界面、有持久化或跨端需求的新产品；
- 需要跨会话交接的原型；
- AI 生成代码之前的范围与验收澄清；
- 已有产品但要重建交互契约。

## 不适用

- 只做颜色、字体、间距等视觉美化；
- 已有批准契约后的纯实现；
- 代码安全、性能或兼容性审查；
- 违法、欺骗、绕过授权或伤害性交互。

## 安装

本仓库采用标准 Agent Skills 结构：根目录包含 `SKILL.md`，详细流程按需从 `workflows/` 和 `references/` 加载。

### Codex

```powershell
$dest = "$env:USERPROFILE\.codex\skills\interaction-contract"
New-Item -ItemType Directory -Force $dest | Out-Null
Copy-Item -Recurse -Force .\* $dest
```

Windows 也可以用 Junction，让项目目录成为唯一源：

```powershell
New-Item -ItemType Junction `
  -Path "$env:USERPROFILE\.codex\skills\interaction-contract" `
  -Target "C:\path\to\interaction-contract"
```

### Claude Code

```bash
mkdir -p ~/.claude/skills/interaction-contract
cp -R . ~/.claude/skills/interaction-contract/
```

### Cursor

```bash
mkdir -p ~/.cursor/skills/interaction-contract
cp -R . ~/.cursor/skills/interaction-contract/
```

### 其他 Agent Skills 宿主

把整个仓库目录复制到该宿主的 skills 根目录，确保最终路径下直接存在：

```text
SKILL.md
workflows/
references/
```

安装后新开一个会话，让宿主重新扫描技能。

## 使用

直接用自然语言描述任务：

```text
用 interaction-contract 把“个人考研英语练习工作台”整理成完整交互契约，
先不要写代码。重点覆盖导入题库、练习提交、刷新恢复和错题复习。
```

无需手动选择 Quick/Full；技能会按范围自动路由。

也可以点名：

```text
$interaction-contract 帮我澄清这个桌面工具的需求，输出规格和验收测试。
```

## Quick 与 Full

| 路线 | 适用 | 输出 |
| --- | --- | --- |
| **Quick Contract** | 单核心流程、一个主界面、小范围改动 | 精简十章规格 + 6–10 条验收测试 |
| **Full Contract** | 多界面、持久化、跨端、权限或长期维护 | 完整十章规格 + 状态矩阵 + 12–25 条验收测试 |

路由由 `workflows/routing.md` 唯一决定，不把路线菜单丢给用户。

## 示例

完整示例在 [examples/exam-workbench](examples/exam-workbench)：

- [INTERACTION_SPEC.md](examples/exam-workbench/INTERACTION_SPEC.md)
- [ACCEPTANCE_TESTS.csv](examples/exam-workbench/ACCEPTANCE_TESTS.csv)

示例来自 2026-10-17 的考研英语工作台实践，已去除受版权保护的真题正文，只保留交互结构和验收方法。

## 验证

```bash
python -m unittest discover -s tests -v
python scripts/verify_interaction_spec.py examples/exam-workbench
```

示例预期输出：

```text
OK  tests=20  p0=20  flows=4
```

## 可迁移性

- 标准 `SKILL.md` + YAML frontmatter；
- 不依赖 Codex 私有 API；
- 不依赖网络、MCP、外部服务或第三方 Python 包；
- 脚本只使用 Python 标准库；
- 不包含绝对路径、密钥、个人数据；
- 没有校验器时，技能仍可阅读和执行，但无法自动检查契约结构。

详见 [PORTABILITY.md](PORTABILITY.md)。

## 目录

```text
SKILL.md
workflows/
  routing.md
  quick.md
  full.md
references/
  interrogation-bank.md
  spec-schema.md
  acceptance-patterns.md
assets/
  INTERACTION_SPEC.template.md
  ACCEPTANCE_TESTS.template.csv
examples/exam-workbench/
scripts/verify_interaction_spec.py
tests/test_verify_interaction_spec.py
docs/
  case-study-outline.md
  DECISIONS.md
```

## 设计原则

- 先执行、后评估；
- 每个核心动作都有反馈；
- 每个错误都有恢复路径；
- 未知项显式记录；
- 不可逆操作必须确认；
- 验收结论必须有证据；
- 构建成功不等于真实可用。

## License

MIT