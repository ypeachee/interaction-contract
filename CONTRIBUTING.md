# Contributing

## Before changing a workflow

1. Read `SKILL.md`.
2. Read `workflows/routing.md`.
3. Modify only the workflow that owns the behavior.
4. Keep the frontmatter `description` synchronized with any new capability name.
5. Keep `SKILL.md` under 40,000 bytes.

## Validation

Run:

```bash
python -m unittest discover -s tests -v
python scripts/verify_interaction_spec.py examples/exam-workbench
```

Both commands must pass.

## Pull request checklist

- [ ] No absolute machine paths.
- [ ] No secrets, tokens or personal data.
- [ ] No network dependency introduced.
- [ ] New capability is named in `SKILL.md` frontmatter.
- [ ] New state or acceptance claim has a test or validator check where practical.
- [ ] Unknowns remain explicit rather than being silently converted into assumptions.
- [ ] Example output still validates.