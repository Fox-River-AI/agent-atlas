# Reference architecture

`agent-atlas` is the working embodiment of one idea: **an agent fleet is a
distributed system, and the discipline that governs a microservices estate
governs it too** — a registry to enumerate what exists, typed contracts at every
boundary, and tracing to follow a decision across hops.

The full argument is in the essay *The Agent Registry — Governing Agentic AI
Like the Microservices Estate It Actually Is* (link forthcoming). This document
is the architecture that essay describes, in the form the tooling implements.

## The layers

Read top to bottom as a single argument.

**Source of truth.** A version-controlled registry of every agent and every
tool. Everything below it reads from it. This is `registry/`.

**Runtime.**

- A single **orchestrator** owns control flow as a deterministic graph (a state
  machine or DAG); the model makes decisions at well-defined nodes. There is no
  free-form, agent-calling-agent chatter — that emergent crosstalk is where
  traceability goes to die.
- **Agents** are single-responsibility workers the orchestrator dispatches to.
- A **tool catalog** is the typed, audited boundary to the outside world, with
  read operations separated from anything that writes or causes side effects.
- **Run state is externalized** to a durable store, keyed by run and step, never
  trusted to the model's context window — which is what makes a failed run
  resumable.
- Long-running and asynchronous work goes to a **task queue**, not the reasoning
  loop.

**Cross-cutting concerns** wrap the whole runtime:

- **Governance & trust** — guardrails, refusal handling, human-in-the-loop
  checkpoints on consequential actions.
- **Observability & lineage** — distributed tracing and provenance for every
  decision.

## The three disciplines the tooling enforces

1. **The registry is the contract.** Every agent and tool is a declarative,
   versioned manifest — OpenAPI in spirit, for agents. Documentation,
   scaffolding, and the visibility map are generated *from* it rather than
   maintained alongside the code and left to drift. The `reused_by` field earns
   its keep: it surfaces redundant, near-duplicate agents before they
   metastasize. See [`registry/`](../registry/).

2. **Documentation is the alignment contract — and instructions are not
   enforcement.** When you build with an AI coder, the negotiable layer (the
   build workflow, conventions) lives in `CLAUDE.md`; the non-negotiable layer
   (no agent without a manifest, no freehand registry edits, no production
   access) lives in permission rules and a `PreToolUse` hook that holds even in
   modes that skip prompts. Guidance persuades; hooks enforce. See
   [`governance/`](../governance/).

3. **Observe the decision, not just the response.** Instrument with the
   OpenTelemetry GenAI semantic conventions: a workflow span containing agent
   spans containing the individual model and tool calls. Read top to bottom,
   that hierarchy *is* the decision graph. In regulated settings, prompts and
   completions belong in droppable span events, never indexed attributes. This
   is the telemetry `agent-atlas` reverse-engineering will consume in v2.
