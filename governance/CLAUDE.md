# Project guidance for the AI builder

This file is the **negotiable layer**. Claude Code loads it as context at the
start of every session; it shapes how you build, but it does not bind you. The
boundaries that *must* hold live in permissions and the `PreToolUse` hook (see
`governance/`), not here. Guidance persuades; hooks enforce.

## The one rule everything else follows

The registry under `registry/` is the source of truth. Code follows the
manifest, never the other way around. Before you create or change an agent or
tool, read its manifest. If there is no manifest, there is no agent — add the
manifest through review first.

## Build workflow

- Read `registry/agents/<id>.agent.yaml` before touching `src/agents/<id>`.
- Honor the manifest's tool allowlist. An agent may call only the tools it
  declares. If it needs another, that is a registry change, not a code change.
- Treat refusal as a real output path. Implement the manifest's refusal
  conditions; do not let the agent guess when it should decline.
- Use the model pinned in the manifest. Do not silently upgrade it.
- Emit the telemetry the manifest declares, with those attribute names.
- Generated artifacts (scaffolding, docs, the visibility map) are produced
  *from* the registry. Regenerate them; do not hand-edit them and let them drift.

## House style

- One responsibility per agent. If you reach for "and" to describe it, split it.
- Keep `read` tools separate from anything that writes or has external effects.
- Prefer small, typed boundaries over clever shared state.

## What you may not do (and why this file can't stop you)

You may not edit the registry freehand, write an agent that has no manifest, or
touch production. Those are not requests — they are enforced by permission rules
and the hook in `governance/`, which hold even in modes that skip prompts. This
section is here so the *why* is legible; the *enforcement* is deterministic and
lives elsewhere.
