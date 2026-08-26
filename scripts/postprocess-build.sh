#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
build_dir="$repo_root/build"
creators_file="$repo_root/data/creators.json"

if [[ ! -f "$build_dir/data/full.json" ]]; then
  printf 'Landscape build not found: %s\n' "$build_dir" >&2
  exit 1
fi

missing_creators="$(
  jq -r --slurpfile creators "$creators_file" \
    '[.items[] | select($creators[0][.name] == null) | .name] | join(", ")' \
    "$build_dir/data/full.json"
)"

if [[ -n "$missing_creators" ]]; then
  printf 'Missing creator metadata for: %s\n' "$missing_creators" >&2
  exit 1
fi

shopt -s nullglob
full_datasets=("$build_dir/data/full.json" "$build_dir"/data/embed_full_*.json)

for dataset in "${full_datasets[@]}"; do
  dataset_tmp="$(mktemp "${dataset}.XXXXXX")"
  jq --slurpfile creators "$creators_file" \
    '.items |= map(. + {crunchbase_data: {name: $creators[0][.name]}})' \
    "$dataset" > "$dataset_tmp"
  mv "$dataset_tmp" "$dataset"
done

style_tag='<style id="llm-routing-landscape-overrides">button[title="All"]{display:none!important}select option[value="all"]~option[value="all"]{display:none}</style>'
html_files=("$build_dir/index.html" "$build_dir/404.html")

for html_file in "${html_files[@]}"; do
  [[ -f "$html_file" ]] || continue
  if ! rg -q 'llm-routing-landscape-overrides' "$html_file"; then
    html_tmp="$(mktemp "${html_file}.XXXXXX")"
    sed "s#</head>#$style_tag</head>#" "$html_file" > "$html_tmp"
    mv "$html_tmp" "$html_file"
  fi
done

printf 'Applied creator metadata and default All-view refinements.\n'
