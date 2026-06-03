# Governance — guidance that persuades, enforcement that binds

Building with an AI coder splits your rules into two registers. The split is the
discipline: guidance is the right tool for things that *should usually* happen;
law is the right tool for things that *must never* happen.

## The negotiable layer — `CLAUDE.md`

Loaded as context at the start of every session. It shapes how the builder works
— the build workflow, conventions, house style. It influences; it does not bind.
Copy [`CLAUDE.md`](CLAUDE.md) to the root of a consuming project.

## The non-negotiable layer — permissions + hook

Deterministic and trustworthy: they hold even in modes that skip permission
prompts.

- **[`hooks/validate_against_registry.py`](hooks/validate_against_registry.py)** —
  a `PreToolUse` hook. Denies writing `src/agents/<id>.*` or `src/tools/<id>.*`
  when the matching registry manifest is missing. Fails *open* on anything it
  doesn't understand, so it never blocks unrelated work.
- **[`settings.example.json`](settings.example.json)** — wires the hook on
  `Write|Edit|MultiEdit` and shows sample permission rules: registry writes are
  set to `ask` (the reviewed path), and pushes and secrets are denied. Copy or
  merge into `.claude/settings.json`.

## The CI validator — holds regardless of who writes the code

[`ci/validate_registry.py`](ci/validate_registry.py) validates every manifest
against its schema and checks cross-manifest consistency: allowlists resolve to
real tools, each tool's `reused_by` matches the agents that actually call it, and
declared I/O schemas exist. Run it in CI and before pushing.

```
pip install pyyaml jsonschema
python3 governance/ci/validate_registry.py
```

## Why two layers

A `CLAUDE.md` rule is guidance. A hook is law. Guidance persuades; hooks enforce.
The registry is the contract both your intent and the builder's output are
measured against. You don't prevent drift with better prompting — you prevent it
by making the things that must not happen impossible rather than merely
discouraged.
