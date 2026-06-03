#!/usr/bin/env python3
"""PreToolUse hook: no agent or tool code without a registry manifest.

Wired in .claude/settings.json on Write|Edit|MultiEdit. Claude Code passes the
tool call as JSON on stdin. We allow everything except creating or editing an
agent/tool implementation whose manifest is missing from registry/.

Convention enforced:
    src/agents/<id>.*  must have  registry/agents/<id>.agent.yaml
    src/tools/<id>.*   must have  registry/tools/<id>.tool.yaml

We emit the documented PreToolUse decision JSON. A permissionDecision of "deny"
blocks the call and shows the reason to Claude (and holds even in bypass mode);
emitting nothing falls through to the normal permission rules. The hook fails
OPEN on anything it doesn't understand, so it never blocks unrelated work.
"""
import json
import re
import sys
from pathlib import Path


def fall_through() -> None:
    # Empty output + exit 0 -> normal permission handling applies.
    sys.exit(0)


def deny(reason: str) -> None:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }))
    sys.exit(0)


def main() -> None:
    try:
        event = json.load(sys.stdin)
    except Exception:
        fall_through()  # never block on a parse error

    tool_input = event.get("tool_input") or {}
    path = tool_input.get("file_path") or tool_input.get("path") or ""
    if not path:
        fall_through()

    root = Path(event.get("cwd", "."))

    checks = (
        ("agent", "agents", "registry/agents", ".agent.yaml"),
        ("tool", "tools", "registry/tools", ".tool.yaml"),
    )
    for label, src_dir, manifest_dir, suffix in checks:
        m = re.search(rf"(?:^|/)src/{src_dir}/([A-Za-z0-9._-]+?)\.[A-Za-z0-9]+$", path)
        if not m:
            continue
        component_id = m.group(1)
        manifest = root / manifest_dir / f"{component_id}{suffix}"
        if not manifest.exists():
            deny(
                f"No manifest for {label} '{component_id}'. Add "
                f"{manifest_dir}/{component_id}{suffix} to the registry "
                f"(via the reviewed process) before implementing it. The "
                f"registry is the source of truth; code follows it, not the "
                f"other way around."
            )

    fall_through()


if __name__ == "__main__":
    main()
