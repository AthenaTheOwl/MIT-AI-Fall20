#!/usr/bin/env python3
"""Check the lab archive has not rotted: every lab file parses, and the index labels match the labs."""

from __future__ import annotations

import ast
import re
import warnings
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEADER = re.compile(r"^# MIT 6\.034 Lab (\d+): (.+)$", re.MULTILINE)


def normalise(text: str) -> str:
    text = text.lower().replace("neighbours", "neighbors")
    text = re.sub(r"\(.*?\)", "", text)
    return re.sub(r"[^a-z]+", " ", text).strip()


def index_labels() -> dict[str, str]:
    tree = ast.parse((ROOT / "streamlit_app.py").read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == "LABS" for t in node.targets):
            return ast.literal_eval(node.value)
    raise SystemExit("streamlit_app.py has no LABS table")


def main() -> int:
    warnings.simplefilter("ignore", SyntaxWarning)  # archived coursework has old escape sequences
    labs = sorted(p for p in ROOT.glob("Lab*") if p.is_dir())
    files = [f for lab in labs for f in sorted(lab.glob("*.py"))]
    for path in files:
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

    labels = index_labels()
    mismatches = []
    for lab in labs:
        header = HEADER.search((lab / f"lab{lab.name.removeprefix('Lab')}.py").read_text(encoding="utf-8"))
        label = labels.get(lab.name)
        if header is None or label is None:
            continue
        if normalise(label) != normalise(header.group(2)):
            mismatches.append(f"{lab.name}: index says {label!r}, lab says {header.group(2)!r}")
    if mismatches:
        raise SystemExit("index labels do not match the labs:\n  " + "\n  ".join(mismatches))

    print(f"parsed {len(files)} lab file(s) in {len(labs)} folder(s); index labels match")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
