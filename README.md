# Intelligent Routing Landscape

A living map of the intelligent-routing ecosystem across fragmented models, devices, locations, and preferences, built with [CNCF Landscape2](https://github.com/cncf/landscape2).

The premise is simple: intelligence is fragmenting, and routing is becoming the system that makes the pieces work together. The landscape maps the products, open systems, evaluation, and execution layers emerging around that shift.

The index is neutral by design: grouping describes system role, not rank or endorsement. Commercial claims remain attributed to their publishers unless independently benchmarked.

## Inclusion standard

This is a curated, auditable landscape rather than a scrape of every repository containing the word “router.” An entry needs a public artifact that can be checked today: maintained code, a reproducible benchmark, a primary research publication, or official product documentation. It must make a real decision across models, capabilities, providers, agents, or inference endpoints—not merely normalize APIs.

Research implementations can live in personal repositories when they are tied to a substantive paper or benchmark, but personal avatars are never used as project marks. Private announcements, unmaintained demos, generic gateways without routing behavior, and products without a verifiable public surface are excluded until stronger evidence appears.

The landscape separates four layers that are often conflated:

1. open programmable routing systems and research methods;
2. routing products and multi-model collaboration;
3. evaluation, benchmarks, and community infrastructure;
4. gateways and inference-serving execution.

## Local preview

```bash
make logos
make validate
make build
make serve
```

The local site is available at `http://127.0.0.1:8000`.

## Netlify deployment

Connect this repository to Netlify and use the default settings from
`netlify.toml`. Netlify will install the pinned Landscape2 release, build the
site, publish `build/`, and preserve client-side routes such as `/guide` and
`/stats`.

For complete GitHub activity statistics, add a secret environment variable
named `GITHUB_TOKENS` in Netlify. The value can be one or more comma-separated
GitHub tokens with read access to public repositories. The site still builds
without it; only repository activity metadata will be limited.

## Source of truth

- `data.yml` contains products, projects, and benchmarks.
- `settings.yml` contains branding, grouping, and display behavior.
- `guide.yml` explains the taxonomy and links the representative research map.
- `data/creators.json` records the creator or backing organization shown on each card.
- `brand/` contains the independent transparent Landscape identity.
- `logos/` contains the SVG assets required by Landscape2.

Official project or organization artwork is used when available. Repositories without a project-owned mark use a clearly documented neutral fallback under `brand/project-marks/`; personal profile images are never used as project logos.

The build post-processing step keeps `All` as the default group in both grid and card views and injects creator metadata without misusing Landscape2's foundation-project maturity field.

Commercial state, project scope, licensing, and paper links were verified against official product documentation, official repositories, and primary publication pages on 2026-08-26. Completeness is therefore defined against this public-evidence standard and remains a moving target as the category evolves.
