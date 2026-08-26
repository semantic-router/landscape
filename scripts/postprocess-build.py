#!/usr/bin/env python3
"""Apply the small data and branding layer shared by local and Netlify builds."""

from __future__ import annotations

import json
import html
import os
import re
import shutil
from collections import defaultdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
BUILD_DIR = REPO_ROOT / "build"
CREATORS_FILE = REPO_ROOT / "data" / "creators.json"
STATS_SNAPSHOT_FILE = REPO_ROOT / "data" / "stats-snapshot.json"
RESEARCH_FILE = REPO_ROOT / "data" / "research.json"
STATS_PATTERN = re.compile(r"window\.statsDS\s*=\s*(\{.*?\});", re.DOTALL)

THEME_COLORS = {
    "Predictive routing": "#339df1",
    "Cascades & test-time": "#ffb61b",
    "Dynamic pools": "#8a6df1",
    "Online learning": "#17b897",
    "Agents & collaboration": "#ef6f93",
    "Evaluation & safety": "#ec7957",
    "Systems co-design": "#55a36d",
}
NATIVE_UI_DIR = REPO_ROOT / "framework" / "landscape2-ui" / "dist"

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


def generate_research_guide() -> None:
    """Build the native Guide-shaped dataset consumed by the Research route."""
    research = json.loads(RESEARCH_FILE.read_text(encoding="utf-8"))
    papers = research["papers"]
    papers_by_year: dict[int, list[dict]] = defaultdict(list)
    for paper in papers:
        papers_by_year[paper["year"]].append(paper)

    venue_count = len({paper["venue"] for paper in papers})
    landscape_count = sum(bool(paper.get("landscape")) for paper in papers)
    intro_content = f'''
      <p class="lead fw-semibold mb-3">How intelligent routing became a field.</p>
      <p>From choosing one model to coordinating dynamic pools, reasoning budgets, agents, serving state, and heterogeneous hardware. This index tracks peer-reviewed papers, workshops, technical reports, and standards drafts without flattening publication status.</p>
      <div class="row g-3 my-3">
        <div class="col-6 col-xl-3"><div class="border p-3 h-100"><div class="fs-3 fw-bold text-primary">{len(papers)}</div><div class="small text-uppercase fw-semibold text-secondary">Selected papers</div></div></div>
        <div class="col-6 col-xl-3"><div class="border p-3 h-100"><div class="fs-3 fw-bold text-primary">{venue_count}</div><div class="small text-uppercase fw-semibold text-secondary">Venues</div></div></div>
        <div class="col-6 col-xl-3"><div class="border p-3 h-100"><div class="fs-3 fw-bold text-primary">3</div><div class="small text-uppercase fw-semibold text-secondary">Research years</div></div></div>
        <div class="col-6 col-xl-3"><div class="border p-3 h-100"><div class="fs-3 fw-bold text-primary">{landscape_count}</div><div class="small text-uppercase fw-semibold text-secondary">Mapped projects</div></div></div>
      </div>
      <blockquote><strong>Scope.</strong> Request-level routing across external models is the core. Token-, layer-, adapter-, and internal MoE expert routing remain adjacent and are not mixed into the same evidence set.</blockquote>
    '''

    categories: list[dict] = [{"category": "Research Map", "content": intro_content, "subcategories": []}]
    for year in sorted(papers_by_year, reverse=True):
        papers_for_year = papers_by_year[year]
        subcategories: list[dict] = []
        for theme in THEME_COLORS:
            theme_papers = sorted(
                (paper for paper in papers_for_year if paper["theme"] == theme),
                key=lambda paper: (paper["venue"], paper.get("short_title", paper["title"])),
            )
            if not theme_papers:
                continue

            cards: list[str] = []
            for paper in theme_papers:
                title = html.escape(paper.get("short_title") or paper["title"])
                full_title = html.escape(paper["title"])
                subtitle = f'<div class="small text-secondary mb-2">{full_title}</div>' if title != full_title else ""
                mapped = '<span class="badge text-bg-warning ms-1">Mapped project</span>' if paper.get("landscape") else ""
                code_link = (
                    f'<a class="ms-3" href="{html.escape(paper["code_url"])}" target="_blank" rel="noreferrer">Code ↗</a>'
                    if paper.get("code_url")
                    else ""
                )
                cards.append(
                    f'''
                    <div class="col-12 col-xxl-6">
                      <article class="card h-100 rounded-0 border shadow-sm">
                        <div class="card-body d-flex flex-column p-3 p-lg-4">
                          <div class="mb-3">
                            <span class="badge text-bg-primary">{html.escape(paper["venue"])} · {year}</span>
                            <span class="badge text-bg-light border text-secondary ms-1">{html.escape(paper["status"])}</span>
                            {mapped}
                          </div>
                          <h3 class="fs-5 fw-semibold mt-0 mb-2">{title}</h3>
                          {subtitle}
                          <p class="small lh-lg mb-3">{html.escape(paper["summary"])}</p>
                          <div class="mt-auto small fw-semibold">
                            <a href="{html.escape(paper["paper_url"])}" target="_blank" rel="noreferrer">Paper ↗</a>{code_link}
                          </div>
                        </div>
                      </article>
                    </div>
                    '''
                )
            subcategories.append(
                {
                    "subcategory": theme,
                    "content": f'<div class="row g-3 mb-4">{"".join(cards)}</div>',
                }
            )

        categories.append(
            {
                "category": str(year),
                "content": f'<p><strong>{len(papers_for_year)} selected papers.</strong> Organized by the research problem each paper primarily advances.</p>',
                "subcategories": subcategories,
            }
        )

    output = {"categories": categories}
    (BUILD_DIR / "data" / "research-guide.json").write_text(
        json.dumps(output, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )


def apply_native_ui_bundle() -> None:
    """Overlay the pinned Landscape2 bundle that contains the native Research route."""
    bundle_index = NATIVE_UI_DIR / "index.html"
    bundle_assets = NATIVE_UI_DIR / "assets"
    if not bundle_index.is_file() or not bundle_assets.is_dir():
        raise SystemExit(f"Pinned Landscape2 UI bundle not found: {NATIVE_UI_DIR}")

    for source in bundle_assets.iterdir():
        if source.is_file():
            shutil.copy2(source, BUILD_DIR / "assets" / source.name)

    bundle_html = bundle_index.read_text(encoding="utf-8")
    script_match = re.search(r'\./assets/(index-[^"/]+\.js)', bundle_html)
    style_match = re.search(r'\./assets/(index-[^"/]+\.css)', bundle_html)
    if not script_match or not style_match:
        raise SystemExit("Unable to resolve native Landscape2 bundle assets")

    script_name = script_match.group(1)
    style_name = style_match.group(1)
    for html_path in (BUILD_DIR / "index.html", BUILD_DIR / "404.html"):
        if not html_path.is_file():
            continue
        page = html_path.read_text(encoding="utf-8")
        page = re.sub(r'\./assets/index-[^"/]+\.js', f'./assets/{script_name}', page)
        page = re.sub(r'\./assets/index-[^"/]+\.css', f'./assets/{style_name}', page)
        html_path.write_text(page, encoding="utf-8")


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
    generate_research_guide()
    apply_native_ui_bundle()
    inject_overrides()
    apply_stats_fallback()
    print("Applied creator metadata, brand assets, native Research route, stats fallback, and category ordering.")


if __name__ == "__main__":
    main()
