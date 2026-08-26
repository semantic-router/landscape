<div align="center">

<a href="https://the-semantic.ai/">
  <img src="brand/intelligent-routing-mark-512.png" alt="Intelligent Routing Landscape" width="168" />
</a>

<h1>Intelligent Routing Landscape</h1>

<p><strong>Map the fragmentation. Build the routing layer.</strong></p>

<p>
  A living map of the systems making fragmented models, compute,<br />
  locations, and preferences work as one intelligent system.
</p>

<p>
  <a href="https://the-semantic.ai/"><strong>Explore</strong></a> ·
  <a href="https://the-semantic.ai/guide">Guide</a> ·
  <a href="https://the-semantic.ai/stats">Stats</a> ·
  <a href="https://github.com/semantic-router/landscape/issues">Suggest a project</a>
</p>

</div>

---

## About

The AI stack is moving beyond one model and one kind of compute. Intelligent routing is becoming the decision layer between agents and an expanding pool of models, providers, runtimes, and hardware.

This project makes that fast-moving ecosystem easier to see. It tracks open routing systems, commercial routing products, evaluation infrastructure, gateways, and serving systems in one evidence-led map built with [CNCF Landscape2](https://github.com/cncf/landscape2).

## Explore the landscape

| Layer | What belongs here |
| --- | --- |
| **Open Routing Systems** | Programmable routers, research toolboxes, and reusable routing methods. |
| **Routing Products** | Managed routers, embedded model selection, and multi-model collaboration products. |
| **Evaluation & Community** | Benchmarks, leaderboards, datasets, and shared evaluation infrastructure. |
| **Gateway & Execution** | AI gateways, policy planes, inference routers, schedulers, and serving systems. |

Start with the [interactive landscape](https://the-semantic.ai/), then use the [guide](https://the-semantic.ai/guide) for taxonomy and scope or [stats](https://the-semantic.ai/stats) for ecosystem activity.

## Inclusion standard

The landscape is curated, not scraped. An entry must have a public artifact that can be verified today: maintained code, reproducible evaluation, a primary research publication, or official product documentation. It must make a meaningful decision across models, capabilities, providers, agents, or inference endpoints—not only normalize APIs.

Research implementations in personal repositories are included when they support a substantive paper or benchmark. Project-owned artwork is preferred; personal avatars are never used as project logos. Unverifiable announcements, abandoned demos, and products without a public evidence surface are held until stronger evidence appears.

Placement describes system role, not rank or endorsement. Product claims remain attributed to their publishers unless independently benchmarked.

## Contributing

See something missing, outdated, or misclassified? [Open an issue](https://github.com/semantic-router/landscape/issues) with the project name, primary link, proposed layer, and the evidence supporting it. Pull requests that update the source files directly are also welcome.

The main sources of truth are:

- `data.yml` — projects, products, benchmarks, links, and descriptions.
- `settings.yml` — branding, groups, navigation, and display behavior.
- `guide.yml` — taxonomy, scope, and the representative research map.
- `data/creators.json` — the creator or backing organization shown on each card.
- `logos/` — official project and organization artwork.
- `brand/` — the independent Intelligent Routing Landscape identity and UI overrides.

## Local development

```bash
make logos
make validate
make build
make serve
```

Open `http://127.0.0.1:8000` to preview the site. Run `make validate` before submitting data or logo changes.

## Deployment

The repository is ready for Netlify through `netlify.toml`. Netlify installs the pinned Landscape2 release, builds the site, publishes `build/`, and preserves client-side routes such as `/guide` and `/stats`.

For complete GitHub activity statistics, configure `GITHUB_TOKENS` as a Netlify secret. The site can build without it, but repository activity metadata will be limited.

## Evidence and maintenance

Official repositories, product documentation, and primary publication pages are preferred over secondary summaries. The project records creator identity separately from product identity and uses a neutral fallback mark only when a project has no official artwork.

The ecosystem changes quickly. Completeness is a maintained target, not a permanent claim—and that is exactly why this landscape exists.
