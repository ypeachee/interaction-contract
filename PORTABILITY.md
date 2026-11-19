# Portability

`interaction-contract` is designed as a host-agnostic Agent Skill.

## Compatibility contract

The repository follows the common Agent Skills layout:

```text
interaction-contract/
├── SKILL.md
├── workflows/
├── references/
├── assets/
├── scripts/
└── examples/
```

Requirements for a compatible host:

1. It can discover `SKILL.md` under a skills root.
2. It reads YAML frontmatter, especially `name` and `description`.
3. It can load referenced files relative to the skill directory.
4. It supports Markdown instructions and relative paths.

## Host examples

| Host | Typical skills root |
| --- | --- |
| Codex | `~/.codex/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |
| Other Agent Skills host | the host's configured skills root |

Paths vary by version and operating system; the host's documentation is authoritative.

## Runtime dependencies

- `SKILL.md` and Markdown workflows: no runtime dependencies.
- `scripts/verify_interaction_spec.py`: Python 3.10+ standard library only.
- Unit tests: Python standard library `unittest`.
- Network: not required.
- External packages: none.
- MCP servers: none.
- Host-specific APIs: none.

## No hidden side effects

The skill itself:

- does not upload data;
- does not call remote services;
- does not modify system settings;
- does not delete files;
- does not require credentials.

The validator reads two files and reports errors/warnings. It does not execute imported product code.

## Portability rules for contributors

- Use relative paths only.
- Do not add absolute machine paths.
- Do not add secrets, tokens or personal data.
- Keep each workflow independently loadable.
- Keep `SKILL.md` under the 40,000-byte budget.
- Keep new capability names synchronized with frontmatter `description`.
- Add a validator or a test when a new claim becomes machine-checkable.
- Preserve the distinction between verified facts and assumptions.