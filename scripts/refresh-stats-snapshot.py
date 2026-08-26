#!/usr/bin/env python3
"""Refresh the committed stats fallback from an authenticated Landscape2 build."""

from __future__ import annotations

import json
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
BUILD_INDEX = REPO_ROOT / "build" / "index.html"
SNAPSHOT_FILE = REPO_ROOT / "data" / "stats-snapshot.json"
STATS_PATTERN = re.compile(r"window\.statsDS\s*=\s*(\{.*?\});", re.DOTALL)


def main() -> None:
    html = BUILD_INDEX.read_text(encoding="utf-8")
    match = STATS_PATTERN.search(html)
    if not match:
        raise SystemExit(f"Stats dataset not found in: {BUILD_INDEX}")

    stats = json.loads(match.group(1))
    repositories = stats.get("repositories", {})
    missing = [field for field in ("bytes", "contributors", "stars") if not repositories.get(field)]
    if missing:
        raise SystemExit(f"Refusing to save an incomplete stats snapshot; missing: {', '.join(missing)}")

    SNAPSHOT_FILE.write_text(
        json.dumps(stats, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        "Updated stats snapshot: "
        f"{repositories.get('repositories', 0)} repositories, "
        f"{repositories['stars']:,} stars, {repositories['contributors']:,} contributors."
    )


if __name__ == "__main__":
    main()
