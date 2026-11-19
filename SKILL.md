---
name: interaction-contract
description: >
  Turn fuzzy software requests into an auditable interaction contract before
  coding or prototyping. Use for 交互契约, 交互规格, 需求澄清, 需求拷问,
  UI spec, interaction design, acceptance criteria, wireframe planning, product
  scope definition, 工作台设计, 网页/桌面/移动端/PWA/APK 原型, or when an agent
  needs to convert “我想要一个……” into users, jobs, information architecture,
  flows, UI states, non-goals, P0 scope, interaction rules, data persistence,
  accessibility, responsive behavior, risks, unknowns, and testable
  Given/When/Then acceptance tests. Outputs INTERACTION_SPEC.md and
  ACCEPTANCE_TESTS.csv; supports quick and full contract modes. Do not use for
  visual polish alone, pure code review, or implementation after the contract is
  already approved.
metadata:
  version: "0.1.0"
  created: "2026-11-20"
---

# Interaction Contract

把“我想要一个工作台/网页/App”变成**可执行、可验收、可交接**的交互契约。

入口只负责执行纪律、路由和输出契约；具体流程由被选中的 workflow 拥有。

## 强制加载顺序

1. 读本文件。
2. 读 `workflows/routing.md`，按其中规则选择唯一路线。
3. 只读被选中的一份 workflow：`workflows/quick.md` 或 `workflows/full.md`。
4. 只读该 workflow 明确要求的 references。
5. 产出前运行 `scripts/verify_interaction_spec.py`；结构错误不得静默通过。

## 全局执行纪律

1. **先契约，后实现**：默认不写产品代码、不生成最终 UI，不替用户冻结未确认的关键决策。
2. **唯一路由**：路线选择只服从 `workflows/routing.md`，冲突时 routing 赢。
3. **不做问卷轰炸**：只问会改变范围、信息架构、状态模型或验收结果的问题。
4. **门禁必须停**：遇到 `⛔ BLOCKING`，等待用户确认；不得用“先做起来再说”绕过。
5. **未知不是空白**：无法确认的内容写入“假设、风险与未知”，不得伪装成事实。
6. **先执行，后评估**：每个核心动作都要有可见反馈；每个核心流程都要有成功、空、加载、错误和恢复状态。
7. **可逆假设可以继续，不可逆假设必须停下**：例如文案可先假设，数据删除策略不可擅自假设。
8. **输出必须可机器检查**：固定标题、固定 CSV 列、唯一测试 ID、明确优先级和状态。

## 术语表

| 术语 | 唯一含义 |
| --- | --- |
| **交互契约** | 连接“用户意图”和“实现行为”的书面规格，不等于视觉稿 |
| **核心任务** | 用户为达成目标必须完成的一条完整任务链 |
| **界面状态** | 同一界面在加载、空、成功、错误、恢复等条件下的可见表现 |
| **非目标** | 本版明确不做的能力，用于阻止范围漂移 |
| **P0** | 没有它，核心任务无法完成 |
| **验收测试** | 可由第三方执行并判定通过/失败的 Given/When/Then 或等价动作断言 |
| **证据** | 截图、日志、测试输出、录屏、导出的文件等可复核材料 |
| **未知项** | 当前没有足够信息确认、且会影响实现或验收的事项 |

## 路线选择表

| 路线 | 适用 | 输出 |
| --- | --- | --- |
| **Quick Contract** | 单流程、小改动、一次会话可完成、已有明确上下文 | 精简版 `INTERACTION_SPEC.md` + 6–10 条验收测试 |
| **Full Contract** | 多屏、多状态、长期维护、新工作台、跨端或多人协作 | 完整版 `INTERACTION_SPEC.md` + 状态矩阵 + 12–25 条验收测试 |

用户不需要选择路线；先根据 routing 规则判定，只有真正歧义时才问一个判别问题。

## 输出契约

默认在工作目录创建：

```text
interaction-contract/
├── INTERACTION_SPEC.md
└── ACCEPTANCE_TESTS.csv
```

用户只要求聊天内结果时，可以不落盘，但仍使用同一结构与测试 ID。

`INTERACTION_SPEC.md` 必须包含 `references/spec-schema.md` 规定的十个一级章节；  
`ACCEPTANCE_TESTS.csv` 必须包含：

```csv
id,flow,priority,precondition,action,expected,evidence,status
```

## 什么时候不该用

- 只需要改颜色、字号、间距或视觉风格；应使用视觉设计或 UI styling 技能。
- 已经有经过确认的交互契约，只剩实现；应直接写计划或代码。
- 只是审查代码质量、安全或性能；应使用对应工程技能。
- 需求涉及违法、欺骗、绕过授权或伤害性交互；停止并说明边界。

## 反模式

| 反模式 | 后果 |
| --- | --- |
| 一上来画页面 | 页面很多，但核心任务没有闭环 |
| 只写正常流程 | 空、加载、错误和恢复状态全部在实现时爆炸 |
| 把“非目标”省略 | 范围持续膨胀 |
| 用“体验流畅”当验收 | 无法判定通过或失败 |
| 让 AI 替用户决定删除、支付、授权等不可逆行为 | 风险不可接受 |
| 把未知项藏进正文 | 后续实现者误把它当事实 |
| 验收测试没有证据要求 | “完成”只能靠口头声明 |

## It's working if…

- 只加载本文件、`routing.md`、一个 workflow 和该 workflow 指定的少量 references。
- 每个 P0 核心任务都有入口、动作、反馈、退出和恢复路径。
- 每个 P0 流程至少覆盖空、加载、成功、错误、恢复中的相关状态。
- 所有 P0 验收测试都有唯一 ID、可执行动作和预期结果。
- 每个未知项都说明影响、当前假设和确认责任人。
- `python scripts/verify_interaction_spec.py <产物目录>` 输出 `OK`；警告已人工判断。