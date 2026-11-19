---
contract_version: "0.1"
contract_mode: full
status: draft
product: "{{product_name}}"
updated: "{{YYYY-MM-DD}}"
---

# {{product_name}} 交互契约

## 1. 决策摘要

- **产品：** {{one_sentence_product}}
- **第一用户：** {{primary_user}}
- **核心任务：** {{core_job}}
- **本版取舍：** {{primary_tradeoff}}
- **当前状态：** draft
- **关键未知：** {{critical_unknown_or_none}}

## 2. 用户与任务

| 用户角色 | 目标 | 当前替代方案 | 关键痛点 | 成功信号 |
| --- | --- | --- | --- | --- |
| {{role}} | {{goal}} | {{current_workaround}} | {{pain}} | {{success_signal}} |

核心任务链：

```text
{{entry}} → {{action}} → {{feedback}} → {{result}} → {{next_step}}
```

## 3. 范围

### P0

- {{p0_item_1}}
- {{p0_item_2}}

### P1

- {{p1_item_1}}

### 非目标

- {{non_goal_1}}
- {{non_goal_2}}

### 约束

- {{constraint_1}}
- {{constraint_2}}

## 4. 信息架构

| 界面/表面 | 用户任务 | 首屏重点 | 进入方式 | 离开方式 |
| --- | --- | --- | --- | --- |
| {{surface_1}} | {{job_1}} | {{first_screen_priority}} | {{entry_1}} | {{exit_1}} |

渐进披露：

- 首屏：{{first_layer}}
- 次级：{{second_layer}}
- 详情/设置：{{third_layer}}

## 5. 核心流程与状态

### 流程：{{flow_name}}

| 流程 | 状态 | 进入条件 | 用户看到什么 | 可执行动作 | 退出/下一状态 | 证据 |
| --- | --- | --- | --- | --- | --- | --- |
| {{flow_name}} | 空/初始 | {{empty_condition}} | {{empty_ui}} | {{empty_action}} | {{empty_next}} | {{empty_evidence}} |
| {{flow_name}} | 加载 | {{loading_condition}} | {{loading_ui}} | {{loading_action}} | {{loading_next}} | {{loading_evidence}} |
| {{flow_name}} | 成功 | {{success_condition}} | {{success_ui}} | {{success_action}} | {{success_next}} | {{success_evidence}} |
| {{flow_name}} | 错误 | {{error_condition}} | {{error_ui}} | {{error_action}} | {{error_next}} | {{error_evidence}} |
| {{flow_name}} | 恢复 | {{recovery_condition}} | {{recovery_ui}} | {{recovery_action}} | {{recovery_next}} | {{recovery_evidence}} |

## 6. 交互规则

- **主操作：** {{primary_action}}
- **次操作：** {{secondary_action}}
- **键盘/触控：** {{input_rules}}
- **校验时机：** {{validation_rules}}
- **成功反馈：** {{success_feedback}}
- **失败反馈：** {{failure_feedback}}
- **重复提交：** {{duplicate_submit_rule}}
- **保存：** {{save_rule}}
- **撤销/删除：** {{undo_delete_rule}}
- **空/错误帮助：** {{help_rule}}
- **响应式：** {{responsive_rule}}

## 7. 数据与恢复

- **数据位置：** {{data_location}}
- **联网/上云：** {{network_rule}}
- **账号与权限：** {{auth_rule}}
- **导入/导出：** {{import_export_rule}}
- **备份与恢复：** {{backup_rule}}
- **存储失败：** {{storage_failure_rule}}
- **隐私/版权：** {{privacy_copyright_rule}}
- **删除与保留：** {{deletion_rule}}

## 8. 可访问性与跨端

- **键盘：** {{keyboard_rule}}
- **焦点：** {{focus_rule}}
- **对比度：** {{contrast_rule}}
- **文本替代：** {{alt_rule}}
- **状态通知：** {{status_announcement_rule}}
- **移动端返回/触控：** {{mobile_rule}}
- **离线/断网：** {{offline_rule}}
- **跨设备连续性：** {{continuity_rule}}

## 9. 验收标准

验收测试见 `ACCEPTANCE_TESTS.csv`。

测试摘要：

- 主成功路径：{{main_success_test}}
- 空状态：{{empty_test}}
- 错误恢复：{{error_test}}
- 持久化：{{persistence_test}}
- 非目标：{{non_goal_test}}

## 10. 假设、风险与未知

| 类型 | 内容 | 影响 | 当前处理 | 确认责任人/方式 |
| --- | --- | --- | --- | --- |
| 已知 | {{known}} | {{known_impact}} | {{known_handling}} | {{known_owner}} |
| 派生 | {{derived}} | {{derived_impact}} | {{derived_handling}} | {{derived_owner}} |
| 推断 | {{inference}} | {{inference_impact}} | {{inference_handling}} | {{inference_owner}} |
| 未知 | {{unknown}} | {{unknown_impact}} | {{unknown_handling}} | {{unknown_owner}} |