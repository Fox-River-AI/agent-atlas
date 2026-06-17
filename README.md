# agent-atlas

**Model your agentic system. See the one that's actually running.**

`agent-atlas` is an open, Erwin-style approach to governing an agentic AI
platform: a version-controlled **registry** that is the single source of truth
for every object in the system, **schemas + validators** that keep it honest,
and **governance** that keeps an AI coding agent building to the spec. It treats
an agent fleet as the distributed system it actually is — with a registry, typed
contracts, and visibility — instead of a pile of prompts.

This repo is the **engine** (the schema + validators + governance). The visual
modeler built on it is **[agent-atlas-studio](https://github.com/Fox-River-AI/agent-atlas-studio)**
— **▶ [try it live](https://fox-river-ai.github.io/agent-atlas-studio/)** (in your
browser, no install).

> Background and rationale: see [`docs/reference-architecture.md`](docs/reference-architecture.md).

## The object model

Every object in the platform is a declarative, versioned manifest — OpenAPI in
spirit, for agents. Seven first-class **component** kinds (the system), plus a separate
**controls layer** — the gate (controls over the system's consequential transitions):

| Kind | Manifest | Role |
|---|---|---|
| **Orchestrator** | `*.orchestrator.yaml` | the single control plane — which task/agent runs, in what order, on what condition; externalizes run state; **owns the gates** |
| **Task** | _(orchestration-level grouping)_ | a stage of the workflow that groups the agents carrying it out |
| **Agent** | `*.agent.yaml` | single-responsibility **LLM** worker; a **pinned model OR a router reference**; refusal as a first-class output; typed I/O; tool allowlist; declared telemetry |
| **MCP Tool** | `*.tool.yaml` | the typed, audited call boundary — effect class (`read` / `write` / `external`), auth scope, `reused_by`; owned by an agent or the orchestrator |
| **Job** | `*.job.yaml` | long-running / async work — queue, timeout, retries |
| **Router** | `*.router.yaml` | dynamic model selection — candidate models + a routing policy (complexity / quality / cost) |
| **System** | `*.system.yaml` | datastores & external systems agents touch — relational / vector / graph / document store, FHIR, external API, state store |

**Controls layer** — a different axis (assets vs controls), not an eighth component kind:

| Kind | Manifest | Role |
|---|---|---|
| **Gate** | `*.gate.yaml` | a control over one consequential transition. Binds the transition to a **pluggable deterministic reasoner** (`{engine, impl, version}` — ASP/Clingo today, SMT reservable; **never an LLM**), the rules + fact-schema it proves against, and a `mode` (`shadow`/`live`). The proof spine's home and the conformance-evidence surface. Owned by the orchestrator; a gated stage references it. No LLM/agent in the proof's path — the schema's `additionalProperties:false` on `reasoner` enforces it. |

You generate documentation, scaffolding, and the visibility map *from* the
registry rather than maintaining them alongside the code and watching them
drift. The registry is the enumerable answer to "what do I have, what does each
thing do, and what does it touch."

## What's here

- **`registry/`** — the manifest **schemas** (`registry/schema/`, the single
  source of truth) and worked examples.
- **`governance/`** — the build-time alignment pattern for working with an AI
  coding agent: negotiable guidance (`CLAUDE.md`) versus enforced boundaries
  (permission rules and a `PreToolUse` hook), plus a **CI validator** that holds
  regardless of who or what writes the code — per-manifest schema checks plus
  cross-manifest consistency (tool allowlists resolve, `reused_by` is
  bidirectional, ids match filenames).
- **`docs/`** — the reference architecture.

## The loop — design ⇄ build ⇄ verify

- **Model** — design the platform in the registry (the [studio](https://github.com/Fox-River-AI/agent-atlas-studio)
  does this visually and validates live). ✅
- **Build handoff** — generate the contract (`CLAUDE.md`) + enforcement hooks an
  AI coding agent builds the system against; the registry says what each object
  becomes (an agent module, a tool integration, a queued job, a model-selection
  policy, the orchestrator's control flow). 🔜
- **Reverse + conformance** — recover the *running* system's agent/tool graph
  from OpenTelemetry traces and diff it against the declared registry, to show
  where reality has drifted from design. 📋

The registry is the **spec**, `CLAUDE.md` is the **contract**, the hooks are the
**enforcement**, and conformance proves the model is *true* — not just drawn.

## Status

Honest and current. The **schemas, the governance pattern, and the CI validator
are usable today**, and the [studio](https://github.com/Fox-River-AI/agent-atlas-studio)
models the full object set against them with live validation and registry
export. The build-handoff generator and reverse-engineering / conformance are on
the roadmap above.

## Contributing

Issues and discussion welcome. Maintained as an open reference for
agentic-system governance.

## License

[Apache-2.0](LICENSE) © 2026 Fox River AI
