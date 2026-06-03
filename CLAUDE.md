# CLAUDE.md — notes for AI coding sessions on agent-atlas

This is the **development** guidance for building `agent-atlas` itself. (Not to be
confused with [`governance/CLAUDE.md`](governance/CLAUDE.md), which is an *example*
template the tool ships for its users.)

## What this project is

`agent-atlas` is an open-source tool for designing and governing agentic AI
systems: a version-controlled registry of agents + tools, forward-engineering
scaffolding from manifests, and a static visibility graph (v1); reverse
engineering from OpenTelemetry traces plus a declared-vs-running conformance diff
(v2). See [`README.md`](README.md) and [`docs/reference-architecture.md`](docs/reference-architecture.md).

It is a credibility / SME-positioning artifact for Randy Shane — build it to be
genuinely good and demonstrably his, not to win a category. Keep it tightly
scoped; it competes with income work for time.

## Current state (2026-06-02)

- Live and public: https://github.com/Fox-River-AI/agent-atlas (org `Fox-River-AI`,
  display "Fox River AI"). Apache-2.0. CI is green.
- **Exists:** the registry (schemas + one worked agent/tool example), the
  governance pattern (example `CLAUDE.md`, `PreToolUse` hook, CI validator), and
  the reference architecture.
- **Does not exist yet:** the CLI. **v1 is scoped but not started** — see
  [`docs/v1-scope.md`](docs/v1-scope.md).

## v1 = the forward generator + the visibility graph

Full plan in [`docs/v1-scope.md`](docs/v1-scope.md). In short: a `pip`-installable
`agent-atlas` CLI with `validate`, `graph` (registry → Mermaid map), `generate`
(registry → scaffolding), and `list`. Python 3.13; deps limited to `pyyaml` +
`jsonschema`; Mermaid for the graph. Build order: **M0** package + `validate`,
**M1** `graph`, **M2** `generate`, **M3** tests + docs. Reverse / conformance is
explicitly **v2** — do not start it as part of v1.

## Conventions

- The registry under `registry/` is the source of truth. Code follows the
  manifest, never the reverse. One responsibility per agent.
- Before changing the registry schema, update the worked examples and run the
  validator so CI stays green:
  `python3 governance/ci/validate_registry.py` (needs `pip install pyyaml
  jsonschema`; the Homebrew system Python is PEP-668 externally-managed, so use a
  venv rather than `--break-system-packages`).
- Generated artifacts are produced *from* the registry; never hand-edit them.

## Identity / git

- Commits attribute to GitHub user `shanemeister` via the verified email
  `rshane@relufox.ai`. Keep using that author email.
- **Do not** put project code in `shanemeister/shanemeister` — that is Randy's
  personal GitHub *profile* repo and stays personal.

## A note on memory

Claude Code memory is keyed to the directory a session opens in. Notes written
while working in the profile repo (`~/myCodeMAC/shanemeister`) will **not**
auto-load for a session opened here in `~/myCodeMAC/agent-atlas`. **This file is
the reliable cross-session note for agent-atlas work — keep it current.**
