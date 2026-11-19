from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from scripts.verify_interaction_spec import CSV_COLUMNS, REQUIRED_HEADINGS, analyze


VALID_SPEC = """---
contract_version: "0.1"
contract_mode: quick
status: draft
product: "测试产品"
updated: "2026-11-20"
---

# 测试产品 交互契约

## 1. 决策摘要

- 产品：测试产品
- 用户：测试者
- 核心任务：完成一次操作

## 2. 用户与任务

| 用户角色 | 目标 | 当前替代方案 | 关键痛点 | 成功信号 |
| --- | --- | --- | --- | --- |
| 测试者 | 完成操作 | 手工 | 慢 | 一次完成 |

## 3. 范围

### P0

- 打开

### 非目标

- 不做账号

## 4. 信息架构

| 界面/表面 | 用户任务 | 首屏重点 | 进入方式 | 离开方式 |
| --- | --- | --- | --- | --- |
| 主界面 | 完成操作 | 主按钮 | 打开应用 | 关闭 |

## 5. 核心流程与状态

### 流程：打开

| 流程 | 状态 | 进入条件 | 用户看到什么 | 可执行动作 | 退出/下一状态 | 证据 |
| --- | --- | --- | --- | --- | --- | --- |
| 打开 | 空 | 无数据 | 空状态 | 新建 | 加载 | 截图 |
| 打开 | 加载 | 点击新建 | 处理中 | 等待 | 成功 | 录屏 |
| 打开 | 成功 | 创建完成 | 成功信息 | 继续 | 结束 | 截图 |
| 打开 | 错误 | 创建失败 | 错误信息 | 重试 | 恢复 | 截图 |
| 打开 | 恢复 | 重试成功 | 结果 | 继续 | 结束 | 截图 |

## 6. 交互规则

- 主操作：新建

## 7. 数据与恢复

- 数据位置：本地

## 8. 可访问性与跨端

- 键盘：可达

## 9. 验收标准

见 CSV。

## 10. 假设、风险与未知

| 类型 | 内容 | 影响 | 当前处理 | 确认责任人/方式 |
| --- | --- | --- | --- | --- |
| 未知 | 浏览器 | 兼容性 | 真机测试 | 测试者 |
"""

VALID_ROWS = [
    {
        "id": "AT-001",
        "flow": "打开",
        "priority": "P0",
        "precondition": "无数据",
        "action": "点击新建",
        "expected": "显示处理中并最终成功",
        "evidence": "截图与录屏",
        "status": "planned",
    },
    {
        "id": "AT-002",
        "flow": "打开",
        "priority": "P0",
        "precondition": "已打开",
        "action": "刷新",
        "expected": "错误或状态可恢复",
        "evidence": "截图",
        "status": "planned",
    },
]


def write_artifacts(root: Path, spec: str, rows: list[dict[str, str]]) -> tuple[Path, Path]:
    spec_path = root / "INTERACTION_SPEC.md"
    tests_path = root / "ACCEPTANCE_TESTS.csv"
    spec_path.write_text(spec, encoding="utf-8")
    with tests_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    return spec_path, tests_path


class VerifyInteractionSpecTests(unittest.TestCase):
    def test_valid_contract_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            spec_path, tests_path = write_artifacts(Path(tmp), VALID_SPEC, VALID_ROWS)
            errors, warnings, stats = analyze(spec_path, tests_path)
            self.assertEqual(errors, [])
            self.assertEqual(stats, {"tests": 2, "p0": 2, "flows": 1})
            self.assertFalse(any("未覆盖" in item for item in warnings))

    def test_missing_required_heading_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            broken = VALID_SPEC.replace(REQUIRED_HEADINGS[-1], "## 其他")
            spec_path, tests_path = write_artifacts(Path(tmp), broken, VALID_ROWS)
            errors, _, _ = analyze(spec_path, tests_path)
            self.assertTrue(any("缺少必填章节" in item for item in errors))

    def test_placeholder_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            broken = VALID_SPEC.replace("测试产品", "{{product_name}}")
            spec_path, tests_path = write_artifacts(Path(tmp), broken, VALID_ROWS)
            errors, _, _ = analyze(spec_path, tests_path)
            self.assertTrue(any("占位符" in item for item in errors))

    def test_duplicate_ids_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            rows = [dict(VALID_ROWS[0]), dict(VALID_ROWS[1])]
            rows[1]["id"] = rows[0]["id"]
            spec_path, tests_path = write_artifacts(Path(tmp), VALID_SPEC, rows)
            errors, _, _ = analyze(spec_path, tests_path)
            self.assertTrue(any("测试 ID 重复" in item for item in errors))

    def test_flow_without_p0_test_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            rows = [dict(VALID_ROWS[0]), dict(VALID_ROWS[1])]
            rows[0]["flow"] = "其他流程"
            rows[1]["flow"] = "其他流程"
            spec_path, tests_path = write_artifacts(Path(tmp), VALID_SPEC, rows)
            errors, _, _ = analyze(spec_path, tests_path)
            self.assertTrue(any("核心流程没有 P0 验收测试" in item for item in errors))

    def test_invalid_priority_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            rows = [dict(VALID_ROWS[0]), dict(VALID_ROWS[1])]
            rows[0]["priority"] = "HIGH"
            spec_path, tests_path = write_artifacts(Path(tmp), VALID_SPEC, rows)
            errors, _, _ = analyze(spec_path, tests_path)
            self.assertTrue(any("priority 非法" in item for item in errors))

    def test_invalid_csv_columns_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "INTERACTION_SPEC.md").write_text(VALID_SPEC, encoding="utf-8")
            (root / "ACCEPTANCE_TESTS.csv").write_text("id,flow\nAT-001,打开\n", encoding="utf-8")
            errors, _, _ = analyze(root / "INTERACTION_SPEC.md", root / "ACCEPTANCE_TESTS.csv")
            self.assertTrue(any("列不匹配" in item for item in errors))


if __name__ == "__main__":
    unittest.main()