#!/usr/bin/env python3
"""Apply the small data and branding layer shared by local and Netlify builds."""

from __future__ import annotations

import json
import os
import re
import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
BUILD_DIR = REPO_ROOT / "build"
CREATORS_FILE = REPO_ROOT / "data" / "creators.json"
STATS_SNAPSHOT_FILE = REPO_ROOT / "data" / "stats-snapshot.json"
STATS_PATTERN = re.compile(r"window\.statsDS\s*=\s*(\{.*?\});", re.DOTALL)

STYLE_TAG = (
    '<link id="intelligent-routing-favicon" rel="icon" type="image/png" '
    'sizes="64x64" href="./images/intelligent-routing-favicon.png">'
    '<link id="intelligent-routing-landscape-overrides" rel="stylesheet" '
    'href="./landscape-overrides.css">'
)
SCRIPT_TAG = (
    '<script id="intelligent-routing-landscape-ordering" '
    'src="./landscape-overrides.js" defer></script>'
)
SOCIAL_META_TAGS = (
    '<meta property="og:image:type" content="image/png">'
    '<meta property="og:image:width" content="1731">'
    '<meta property="og:image:height" content="909">'
    '<meta property="og:image:alt" content="Intelligent Routing Landscape — Map the fragmentation. Build the routing layer.">'
    '<meta name="twitter:image:alt" content="Intelligent Routing Landscape — Map the fragmentation. Build the routing layer.">'
)


def update_creator_metadata() -> None:
    full_dataset = BUILD_DIR / "data" / "full.json"
    if not full_dataset.is_file():
        raise SystemExit(f"Landscape build not found: {BUILD_DIR}")

    creators = json.loads(CREATORS_FILE.read_text(encoding="utf-8"))
    datasets = [full_dataset, *sorted((BUILD_DIR / "data").glob("embed_full_*.json"))]

    for dataset_path in datasets:
        dataset = json.loads(dataset_path.read_text(encoding="utf-8"))
        missing = [item["name"] for item in dataset["items"] if item["name"] not in creators]
        if missing:
            raise SystemExit(f"Missing creator metadata for: {', '.join(missing)}")

        for item in dataset["items"]:
            item["crunchbase_data"] = {"name": creators[item["name"]]}

        dataset_path.write_text(
            json.dumps(dataset, ensure_ascii=False, separators=(",", ":")),
            encoding="utf-8",
        )


def copy_brand_assets() -> None:
    shutil.copy2(REPO_ROOT / "brand" / "landscape-overrides.css", BUILD_DIR / "landscape-overrides.css")
    shutil.copy2(REPO_ROOT / "brand" / "landscape-overrides.js", BUILD_DIR / "landscape-overrides.js")
    shutil.copy2(
        REPO_ROOT / "brand" / "intelligent-routing-favicon.png",
        BUILD_DIR / "images" / "intelligent-routing-favicon.png",
    )
    shutil.copy2(
        REPO_ROOT / "brand" / "intelligent-routing-og.png",
        BUILD_DIR / "images" / "intelligent-routing-og.png",
    )
    docs_dir = BUILD_DIR / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    for filename in ("landscape.png", "landscape.pdf"):
        generated = docs_dir / filename
        fallback = REPO_ROOT / "brand" / "downloads" / filename
        if not generated.is_file():
            shutil.copy2(fallback, generated)


def inject_overrides() -> None:
    for html_path in (BUILD_DIR / "index.html", BUILD_DIR / "404.html"):
        if not html_path.is_file():
            continue

        html = html_path.read_text(encoding="utf-8")
        additions = ""
        if 'property="og:image:width"' not in html:
            additions += SOCIAL_META_TAGS
        if "intelligent-routing-landscape-overrides" not in html:
            additions += STYLE_TAG
        if "intelligent-routing-landscape-ordering" not in html:
            additions += SCRIPT_TAG
        if additions:
            html_path.write_text(html.replace("</head>", f"{additions}</head>", 1), encoding="utf-8")


def apply_stats_fallback() -> None:
    """Use the maintained snapshot when an anonymous build has no GitHub activity data."""
    snapshot = json.loads(STATS_SNAPSHOT_FILE.read_text(encoding="utf-8"))
    snapshot_json = json.dumps(snapshot, ensure_ascii=False, separators=(",", ":"))

    for html_path in (BUILD_DIR / "index.html", BUILD_DIR / "404.html"):
        if not html_path.is_file():
            continue

        html = html_path.read_text(encoding="utf-8")
        match = STATS_PATTERN.search(html)
        if not match:
            raise SystemExit(f"Stats dataset not found in: {html_path}")

        current = json.loads(match.group(1))
        repositories = current.get("repositories", {})
        incomplete = any(not repositories.get(field) for field in ("bytes", "contributors", "stars"))
        if not incomplete:
            continue
        if os.environ.get("REQUIRE_FRESH_GITHUB_STATS") == "true":
            raise SystemExit("Authenticated GitHub stats were required but the build returned no activity data")

        html_path.write_text(
            STATS_PATTERN.sub(f"window.statsDS = {snapshot_json};", html, count=1),
            encoding="utf-8",
        )


def main() -> None:
    update_creator_metadata()
    copy_brand_assets()
    inject_overrides()
    apply_stats_fallback()
    print("Applied creator metadata, brand assets, stats fallback, and consistent category ordering.")


if __name__ == "__main__":
    main()
