# v1 scope — forward generator + visibility graph

> **Superseded (2026-06-03).** This doc scoped a small agent+tool CLI before the
> object model expanded to seven kinds (orchestrator / task / agent / tool / job
> / router / system) and the visual modeler — [agent-atlas-studio](https://github.com/Fox-River-AI/agent-atlas-studio)
> — became the front end (it does the "visibility graph" goal, live). The
> per-object schemas now live in `registry/schema/`. Kept for historical context
> and the still-relevant forward-generator/CLI design; see the README and
> agent-atlas-studio's `docs/STATUS.md` for the current plan.

**Status:** scoped, not started (2026-06-02).

## Goal

Make the README's two "in progress" claims real: **Forward** (registry →
scaffolding) and **Visibility** (registry → rendered map). Ship a
`pip`-installable `agent-atlas` CLI that runs against the existing registry.
v1 does **not** touch reverse engineering or telemetry — those are v2.

Defaults: **Python 3.13** (matches the validator/hook), **Mermaid** for the graph
(renders natively in GitHub markdown, zero deps). New dependencies limited to
`pyyaml` + `jsonschema` (already in use). CLI built on stdlib `argparse`.

## CLI surface

```
agent-atlas validate                              # schema + cross-manifest consistency
agent-atlas graph    [--out docs/visibility.md]   # render the agent→tool map as Mermaid
agent-atlas generate [--agent ID | --all] [--out src/]   # forward-engineer scaffolding
agent-atlas list                                  # enumerate agents/tools
```

## Package layout

```
agent_atlas/
  cli.py          # argparse entry; console_scripts: agent-atlas = agent_atlas.cli:main
  registry.py     # load manifests -> typed Agent/Tool dataclasses (shared by all commands)
  validate.py     # current governance/ci validator logic, refactored in
  graph.py        # Mermaid renderer
  generate.py     # scaffolding generator + templates
pyproject.toml    # deps: pyyaml, jsonschema
tests/            # pytest: good/bad registry fixtures, graph output, generate snapshot
```

Migration: `governance/ci/validate_registry.py` logic moves into
`agent_atlas.validate`; CI changes to `pip install -e . && agent-atlas validate`.
The standalone `PreToolUse` hook stays as-is (intentionally dependency-free).

## `graph` (build first — highest demo-per-hour)

A Mermaid `flowchart` written to `docs/visibility.md` so it renders as a live map
on GitHub. Agents and tools are distinct shapes; tools colored by effect class
(`read` / `write` / `external`); edges from each agent's allowlist. Stretch:
inject the same block into the README between markers.

## `generate`

A split that demonstrates the article's discipline (regenerate the contract,
never hand-edit it):

- `src/agents/<id>/_generated.py` — **overwritten** each run: `MODEL` (pinned),
  `ALLOWED_TOOLS`, `Input`/`Output` TypedDicts from the I/O schemas,
  `REFUSAL_CONDITIONS`, telemetry span name + attrs.
- `src/agents/<id>/agent.py` — **created once, never clobbered**: the
  implementation skeleton importing the contract.

Tools get an analogous stub. Writing into `src/agents/<id>/` is already guarded
by the `PreToolUse` hook (no scaffolding without a manifest). v1 handles **flat
object schemas** (what the examples use) and is honest about that limit; nested /
`$ref`-heavy schemas are v2.

## Out of scope for v1

Reverse engineering, OTel trace ingestion, declared-vs-running conformance diff,
any web/dynamic UI, full arbitrary JSON-Schema→Python codegen, PyPI publish
(→ v1.1).

## Milestones (evening-sized, in order)

1. **M0** — package + `validate`/`list`: skeleton, `pyproject.toml`, move
   validator in, update CI. Repo stays green.
2. **M1** — `graph`: Mermaid → `docs/visibility.md` (+ README embed).
3. **M2** — `generate`: the generated/hand-written split for agents and tools.
4. **M3** — tests + docs: pytest in CI; flip README "in progress" → real, with a
   short usage section.

## Acceptance criteria

- `pip install -e . && agent-atlas validate` is green in CI.
- `agent-atlas graph` renders the current fleet as Mermaid that displays on GitHub.
- `agent-atlas generate --all` scaffolds `intake-classifier` +
  `knowledge-base-search`; re-running overwrites only `_generated.py` and leaves
  `agent.py` untouched.
- README no longer says "in progress" for forward + visibility; both have a
  worked example.

## Open scoping calls (defaults assumed unless changed)

- **CLI deps:** stdlib `argparse` (default, keeps deps minimal) vs. `typer`.
- **Generate granularity:** per-agent package split (default, demos the
  discipline) vs. a single flat `src/agents/<id>.py`.
