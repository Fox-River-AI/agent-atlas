# agent-atlas

**Model your agentic system. See the one that's actually running.**

`agent-atlas` is an open, Erwin-style approach to governing an agentic AI
system: a version-controlled registry that is the single source of truth for
every agent and tool, tooling to *forward-engineer* a fleet from that registry,
and — on the roadmap — to *reverse-engineer* the running system from its
telemetry and diff reality against the design.

It exists because agentic systems tend to rot the same way: six months in,
nobody can say how many agents are running, what each one does, or which tools
they share. `agent-atlas` treats an agent fleet as the distributed system it
actually is — with a registry, typed contracts, and visibility — instead of a
pile of prompts.

> Background and rationale:
> *The Agent Registry — Governing Agentic AI Like the Microservices Estate It Actually Is* — [link]

## The model: three capabilities (the Erwin pattern)

- **Forward** — design the fleet in the registry, then generate manifests,
  schemas, and scaffolding. *(v1, in progress)*
- **Visibility** — render the registry as a live map of agents, tools, and
  their relationships. *(v1, in progress)*
- **Reverse + conformance** — recover the actual agent/tool graph from
  OpenTelemetry traces and diff it against the declared registry to show where
  reality has drifted from design. *(v2, planned)*

## What's here today

- `registry/` — the manifest schema and worked examples: an agent contract
  (single responsibility, typed I/O, tool allowlist, refusal policy, emitted
  telemetry) and a tool contract (effect class, auth scope, reuse).
- `governance/` — the build-time alignment pattern for working with an AI
  coding agent: negotiable guidance (`CLAUDE.md`) versus enforced boundaries
  (permission rules and a `PreToolUse` hook, plus a CI validator that holds
  regardless of who or what writes the code).
- `docs/` — the reference architecture.

## How it works

Every agent and tool is a declarative, versioned manifest — OpenAPI in spirit,
for agents. You generate documentation, scaffolding, and the visibility map
*from* the registry rather than maintaining them alongside the code and watching
them drift. The registry is the enumerable answer to "what do I have, what does
each thing do, and what does it touch."

## Status

Early and honest. The registry schema, the governance pattern, and the
reference architecture are defined and usable today; the forward generator and
the visibility renderer are in active development. Roadmap items are marked
above — nothing here pretends to be further along than it is.

## Contributing

Issues and discussion are welcome. This is maintained as an open reference for
agentic-system governance.

## License

[Apache-2.0](LICENSE) © 2026 Fox River AI
