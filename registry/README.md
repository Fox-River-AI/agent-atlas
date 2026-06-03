# Registry — the source of truth

Every agent and every tool is a declarative, versioned manifest. Code follows
the manifest, never the reverse.

## Layout

```
registry/
  schema/   meta-schemas every manifest validates against
    agent.schema.json
    tool.schema.json
  agents/   one <id>.agent.yaml per agent
  tools/    one <id>.tool.yaml per tool
  io/       typed input/output JSON Schemas referenced by agent manifests
```

## Naming convention

```
registry/agents/<id>.agent.yaml   <->   src/agents/<id>.*
registry/tools/<id>.tool.yaml     <->   src/tools/<id>.*
```

The `PreToolUse` hook in `governance/` denies writing `src/agents/<id>.*` unless
`registry/agents/<id>.agent.yaml` already exists. The registry comes first.

## What a manifest carries

An **agent** states a single responsibility, pins its model, points to typed I/O
schemas, allowlists exactly the tools it may call, treats refusal as a
first-class output, and declares the telemetry it emits.

A **tool** states its effect class (`read` / `write` / `external`), its auth
scope and rate limit, and the agents that reuse it.

Worked examples: [`agents/intake-classifier.agent.yaml`](agents/intake-classifier.agent.yaml)
and [`tools/knowledge-base-search.tool.yaml`](tools/knowledge-base-search.tool.yaml).

## Validate

```
pip install pyyaml jsonschema
python3 governance/ci/validate_registry.py
```
