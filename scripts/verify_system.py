#!/usr/bin/env python3
"""Validate a generated Moqi instance without third-party dependencies."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_FILES = (
    "entrypoints/AGENTS.md",
    "MSA/Memory.md",
    "MSA/Soul.md",
    "MSA/Agent.md",
    "ALIGNMENT.md",
)
RETIRED_PATHS = (
    "MSA/references",
    "references/alignment.md",
)
LINE_LIMITS = {
    "entrypoints/AGENTS.md": 150,
    "MSA/Memory.md": 60,
    "MSA/Soul.md": 80,
    "MSA/Agent.md": 60,
    "ALIGNMENT.md": 150,
}
PLACEHOLDER_PATTERN = re.compile(r"\{\{[A-Z0-9_]+\}\}")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def validate(root: Path, allow_placeholders: bool) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"Missing required file: {relative}")

    for relative in RETIRED_PATHS:
        if (root / relative).exists():
            errors.append(f"Retired path still exists: {relative}")

    for relative, limit in LINE_LIMITS.items():
        path = root / relative
        if path.is_file():
            count = len(read_text(path).splitlines())
            if count > limit:
                errors.append(f"{relative} has {count} lines; limit is {limit}")

    agents_path = root / "entrypoints/AGENTS.md"
    agents = read_text(agents_path) if agents_path.is_file() else ""
    if "canonical-entrypoint" not in agents:
        errors.append("AGENTS.md does not declare the canonical entrypoint marker")
    if "ALIGNMENT.md" not in agents:
        errors.append("AGENTS.md has no ALIGNMENT.md route")

    references = root / "references"
    if references.is_dir():
        for path in sorted(references.glob("*.md")):
            route = f"references/{path.name}"
            if route not in agents:
                errors.append(f"Reference has no AGENTS.md route: {path.name}")
            count = len(read_text(path).splitlines())
            if count > 150:
                warnings.append(f"{path.name} has {count} lines; recommended limit is 150")

    entrypoints_dir = root / "entrypoints"
    if entrypoints_dir.is_dir():
        for adapter in sorted(entrypoints_dir.glob("*.md")):
            if adapter.name == "AGENTS.md":
                continue
            text = read_text(adapter).replace("\\", "/")
            if "entrypoints/AGENTS.md" not in text:
                errors.append(f"{adapter.name} does not route to AGENTS.md")

    if not allow_placeholders:
        for path in root.rglob("*.md"):
            if ".git" not in path.parts:
                match = PLACEHOLDER_PATTERN.search(read_text(path))
                if match:
                    errors.append(f"Unresolved placeholder {match.group()} in {path.relative_to(root)}")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Moqi instance")
    parser.add_argument("root", type=Path, help="Moqi instance root")
    parser.add_argument("--allow-placeholders", action="store_true")
    args = parser.parse_args()

    root = args.root.resolve()
    errors, warnings = validate(root, args.allow_placeholders)
    print(f"Errors: {len(errors)}")
    for item in errors:
        print(f"  ERROR: {item}")
    print(f"Warnings: {len(warnings)}")
    for item in warnings:
        print(f"  WARN: {item}")
    if errors:
        return 1
    print("Moqi verification passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
