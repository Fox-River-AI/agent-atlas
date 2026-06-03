#!/usr/bin/env python3
"""CI validator for the agent-atlas registry.

Holds regardless of who or what writes the code: run it in CI and as a local
pre-push check. It enforces the registry as the source of truth by verifying
that every manifest is well-formed and internally consistent.

Checks:
  1. Every registry/agents/*.agent.yaml validates against the agent schema.
  2. Every registry/tools/*.tool.yaml validates against the tool schema.
  3. The filename id matches the manifest id (no drift between path and body).
  4. Every tool in an agent's allowlist resolves to a real tool manifest.
  5. Every tool's reused_by lists exactly the agents that allowlist it
     (bidirectional consistency -- this is what surfaces redundant agents).
  6. Every agent's declared input/output schema file exists.

Dependencies: pyyaml, jsonschema. Exit code is nonzero on any violation.
"""
import json
import sys
from pathlib import Path

try:
    import yaml
    from jsonschema import Draft202012Validator
except ImportError as exc:  # pragma: no cover
    print(f"missing dependency: {exc}. Run: pip install pyyaml jsonschema", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[2]
REG = ROOT / "registry"


def load_yaml(path: Path):
    with open(path) as fh:
        return yaml.safe_load(fh)


def load_schema(name: str):
    with open(REG / "schema" / name) as fh:
        return json.load(fh)


def main() -> None:
    errors: list[str] = []
    agent_validator = Draft202012Validator(load_schema("agent.schema.json"))
    tool_validator = Draft202012Validator(load_schema("tool.schema.json"))

    agents: dict[str, dict] = {}
    tools: dict[str, dict] = {}

    for path in sorted((REG / "agents").glob("*.agent.yaml")):
        doc = load_yaml(path) or {}
        file_id = path.name[: -len(".agent.yaml")]
        for err in agent_validator.iter_errors(doc):
            errors.append(f"{path.relative_to(ROOT)}: {err.message}")
        if doc.get("id") != file_id:
            errors.append(f"{path.relative_to(ROOT)}: id '{doc.get('id')}' does not match filename '{file_id}'")
        agents[doc.get("id")] = doc
        for slot in ("input", "output"):
            ref = (doc.get("io") or {}).get(slot)
            if ref and not (ROOT / ref).exists():
                errors.append(f"{path.relative_to(ROOT)}: io.{slot} schema not found: {ref}")

    for path in sorted((REG / "tools").glob("*.tool.yaml")):
        doc = load_yaml(path) or {}
        file_id = path.name[: -len(".tool.yaml")]
        for err in tool_validator.iter_errors(doc):
            errors.append(f"{path.relative_to(ROOT)}: {err.message}")
        if doc.get("id") != file_id:
            errors.append(f"{path.relative_to(ROOT)}: id '{doc.get('id')}' does not match filename '{file_id}'")
        tools[doc.get("id")] = doc

    # Allowlisted tools must resolve to real manifests.
    for agent_id, doc in agents.items():
        for tool_id in doc.get("tools", []):
            if tool_id not in tools:
                errors.append(f"agent '{agent_id}' allowlists unknown tool '{tool_id}'")

    # reused_by must match the agents that actually allowlist the tool.
    callers: dict[str, set] = {tool_id: set() for tool_id in tools}
    for agent_id, doc in agents.items():
        for tool_id in doc.get("tools", []):
            if tool_id in callers:
                callers[tool_id].add(agent_id)
    for tool_id, doc in tools.items():
        declared = set(doc.get("reused_by", []))
        actual = callers[tool_id]
        if declared != actual:
            errors.append(
                f"tool '{tool_id}': reused_by {sorted(declared)} does not match "
                f"the agents that allowlist it {sorted(actual)}"
            )

    if errors:
        print(f"registry invalid -- {len(errors)} problem(s):", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)
    print(f"registry OK: {len(agents)} agent(s), {len(tools)} tool(s) validated.")


if __name__ == "__main__":
    main()
