#!/usr/bin/env python3
"""Validate an interaction contract artifact folder.

Usage:
    python verify_interaction_spec.py <artifact_dir> [--json]
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

REQUIRED_HEADINGS = [
    "## 1. 决策摘要",
    "## 2. 用户与任务",
    "## 3. 范围",
    "## 4. 信息架构",
    "## 5. 核心流程与状态",
    "## 6. 交互规则",
    "## 7. 数据与恢复",
    "## 8. 可访问性与跨端",
    "## 9. 验收标准",
    "## 10. 假设、风险与未知",
]

CSV_COLUMNS = [
    "id",
    "flow",
    "priority",
    "precondition",
    "action",
    "expected",
    "evidence",
    "status",
]

VALID_PRIORITIES = {"P0", "P1", "P2"}
VALID_STATUSES = {"planned", "passed", "failed", "blocked", "not-applicable"}
VALID_MODES = {"quick", "full"}
VALID_CONTRACT_STATUSES = {"draft", "review", "approved", "superseded"}
PLACEHOLDER_RE = re.compile(r"\{\{[^{}\n]+\}\}|\bTODO\b|\bTBD\b", re.IGNORECASE)
ID_RE = re.compile(r"^AT-\d{3,}$")
FLOW_HEADING_RE = re.compile(r"^###\s*流程：(.+?)\s*$", re.MULTILINE)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def _parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end]
    values: dict[str, str] = {}
    for raw_line in block.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip().strip('"').strip("'")
        values[key.strip()] = value
    return values


def _section(text: str, heading: str) -> str:
    start = text.find(heading)
    if start == -1:
        return ""
    next_heading = text.find("\n## ", start + len(heading))
    return text[start:] if next_heading == -1 else text[start:next_heading]


def analyze(spec_path: Path, tests_path: Path) -> tuple[list[str], list[str], dict[str, int]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not spec_path.is_file():
        return [f"缺少文件：{spec_path.name}"], warnings, {}
    if not tests_path.is_file():
        return [f"缺少文件：{tests_path.name}"], warnings, {}

    text = _read_text(spec_path)
    frontmatter = _parse_frontmatter(text)

    mode = frontmatter.get("contract_mode", "")
    status = frontmatter.get("status", "")
    if not frontmatter:
        errors.append("INTERACTION_SPEC.md 缺少 YAML frontmatter")
    else:
        if mode not in VALID_MODES:
            errors.append(f"contract_mode 必须是 quick/full，当前为：{mode or '空'}")
        if status not in VALID_CONTRACT_STATUSES:
            errors.append(
                f"status 必须是 draft/review/approved/superseded，当前为：{status or '空'}"
            )

    for heading in REQUIRED_HEADINGS:
        if heading not in text:
            errors.append(f"缺少必填章节：{heading}")

    placeholders = sorted(set(PLACEHOLDER_RE.findall(text)))
    if placeholders:
        errors.append("INTERACTION_SPEC.md 仍有未填占位符：" + "、".join(placeholders))

    scope = _section(text, "## 3. 范围")
    if "非目标" not in scope:
        warnings.append("范围章节没有明确写出“非目标”")

    flow_section = _section(text, "## 5. 核心流程与状态")
    for state_word in ("空", "加载", "成功", "错误", "恢复"):
        if state_word not in flow_section:
            warnings.append(f"核心流程与状态章节没有出现状态词：{state_word}")

    flow_names = [name.strip() for name in FLOW_HEADING_RE.findall(text)]
    if not flow_names:
        errors.append("没有发现 `### 流程：<名称>` 形式的核心流程")
    if len(flow_names) != len(set(flow_names)):
        errors.append("核心流程名称重复")

    rows: list[dict[str, str]] = []
    with tests_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != CSV_COLUMNS:
            errors.append(
                "ACCEPTANCE_TESTS.csv 列不匹配；必须依次为：" + ",".join(CSV_COLUMNS)
            )
        else:
            for row_number, row in enumerate(reader, start=2):
                cleaned = {key: (row.get(key) or "").strip() for key in CSV_COLUMNS}
                rows.append(cleaned)
                test_id = cleaned["id"]
                if not ID_RE.fullmatch(test_id):
                    errors.append(f"第 {row_number} 行测试 ID 非法：{test_id or '空'}")
                if cleaned["priority"] not in VALID_PRIORITIES:
                    errors.append(
                        f"{test_id or f'第 {row_number} 行'} priority 非法：{cleaned['priority']}"
                    )
                if cleaned["status"] not in VALID_STATUSES:
                    errors.append(
                        f"{test_id or f'第 {row_number} 行'} status 非法：{cleaned['status']}"
                    )
                for field in ("flow", "precondition", "action", "expected", "evidence"):
                    if not cleaned[field]:
                        errors.append(f"{test_id or f'第 {row_number} 行'} 缺少 {field}")
                joined = " ".join(cleaned.values())
                if PLACEHOLDER_RE.search(joined):
                    errors.append(f"{test_id or f'第 {row_number} 行'} 仍有未填占位符")

    ids = [row["id"] for row in rows if row["id"]]
    duplicates = sorted({value for value in ids if ids.count(value) > 1})
    if duplicates:
        errors.append("测试 ID 重复：" + "、".join(duplicates))
    if not any(row["priority"] == "P0" for row in rows):
        errors.append("ACCEPTANCE_TESTS.csv 至少需要一条 P0 测试")

    for flow_name in flow_names:
        if not any(row["flow"] == flow_name and row["priority"] == "P0" for row in rows):
            errors.append(f"核心流程没有 P0 验收测试：{flow_name}")

    searchable = " ".join(
        " ".join(row.values()).lower() for row in rows
    )
    if rows and not any(word in searchable for word in ("刷新", "重开", "持久", "恢复")):
        warnings.append("验收测试未覆盖刷新、重开、持久化或恢复")
    if rows and not any(word in searchable for word in ("错误", "失败", "非法", "超时", "断网")):
        warnings.append("验收测试未覆盖错误或失败路径")

    stats = {
        "tests": len(rows),
        "p0": sum(1 for row in rows if row["priority"] == "P0"),
        "flows": len(flow_names),
    }
    return errors, warnings, stats


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate interaction contract artifacts")
    parser.add_argument("target", help="包含 INTERACTION_SPEC.md 与 ACCEPTANCE_TESTS.csv 的目录")
    parser.add_argument("--json", action="store_true", help="以 JSON 输出结果")
    args = parser.parse_args(argv)

    target = Path(args.target).expanduser().resolve()
    spec_path = target / "INTERACTION_SPEC.md"
    tests_path = target / "ACCEPTANCE_TESTS.csv"
    errors, warnings, stats = analyze(spec_path, tests_path)
    ok = not errors

    if args.json:
        print(
            json.dumps(
                {
                    "ok": ok,
                    "target": str(target),
                    "errors": errors,
                    "warnings": warnings,
                    "stats": stats,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        if ok:
            print(
                f"OK  tests={stats.get('tests', 0)}  "
                f"p0={stats.get('p0', 0)}  flows={stats.get('flows', 0)}"
            )
        else:
            print("FAILED")
        for message in errors:
            print(f"ERROR: {message}")
        for message in warnings:
            print(f"WARN: {message}")

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())