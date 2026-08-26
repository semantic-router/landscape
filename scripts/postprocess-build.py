#!/usr/bin/env python3
"""Apply the small data and branding layer shared by local and Netlify builds."""

from __future__ import annotations

import json
import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
BUILD_DIR = REPO_ROOT / "build"
CREATORS_FILE = REPO_ROOT / "data" / "creators.json"

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


def inject_overrides() -> None:
    for html_path in (BUILD_DIR / "index.html", BUILD_DIR / "404.html"):
        if not html_path.is_file():
            continue

        html = html_path.read_text(encoding="utf-8")
        additions = ""
        if "intelligent-routing-landscape-overrides" not in html:
            additions += STYLE_TAG
        if "intelligent-routing-landscape-ordering" not in html:
            additions += SCRIPT_TAG
        if additions:
            html_path.write_text(html.replace("</head>", f"{additions}</head>", 1), encoding="utf-8")


def main() -> None:
    update_creator_metadata()
    copy_brand_assets()
    inject_overrides()
    print("Applied creator metadata, brand assets, and consistent category ordering.")


if __name__ == "__main__":
    main()
