#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
github_tokens="${GITHUB_TOKENS:-}"
settings_file="${LANDSCAPE_SETTINGS_FILE:-$repo_root/settings.yml}"

if [[ -z "$github_tokens" && "${NETLIFY:-}" != "true" ]]; then
  if command -v gh >/dev/null 2>&1; then
    github_tokens="$(gh auth token 2>/dev/null || true)"
  elif [[ -x "/mnt/c/Program Files/GitHub CLI/gh.exe" ]]; then
    github_tokens="$("/mnt/c/Program Files/GitHub CLI/gh.exe" auth token 2>/dev/null || true)"
  fi
fi

build_args=(
  build
  --data-file "$repo_root/data.yml"
  --settings-file "$settings_file"
  --guide-file "$repo_root/guide.yml"
  --logos-path "$repo_root/logos"
  --output-dir "$repo_root/build"
  --cache-dir "$repo_root/.cache"
)

if [[ -n "$github_tokens" ]]; then
  printf 'Building with authenticated GitHub metadata.\n'
  GITHUB_TOKENS="$github_tokens" landscape2 "${build_args[@]}"
else
  printf 'GitHub credentials unavailable; repository activity stats will be incomplete.\n' >&2
  landscape2 "${build_args[@]}"
fi
