# LLM Routing Landscape

An interactive, evidence-led map of the LLM routing and Mixture-of-Models ecosystem, built with [CNCF Landscape2](https://github.com/cncf/landscape2).

The landscape separates four decisions that are often conflated:

1. model and capability routing;
2. multi-model collaboration;
3. gateway and inference-serving execution;
4. evaluation and research.

## Local preview

```bash
make logos
make validate
make build
make serve
```

The local site is available at `http://127.0.0.1:8000`.

## Source of truth

- `data.yml` contains products, projects, and benchmarks.
- `settings.yml` contains branding, grouping, and display behavior.
- `guide.yml` explains the taxonomy and links the representative research map.
- `data/creators.json` records the creator or backing organization shown on each card.
- `brand/` contains the independent transparent Landscape identity.
- `logos/` contains the SVG assets required by Landscape2.

The build post-processing step keeps `All` as the default group in both grid and card views and injects creator metadata without misusing Landscape2's foundation-project maturity field.

Commercial state, project scope, licensing, and paper links were verified against official product documentation, official repositories, and primary publication pages on 2026-08-26.
