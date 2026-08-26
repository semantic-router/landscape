#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
landscape2_version="${LANDSCAPE2_VERSION:-1.1.0}"
install_dir="$repo_root/.netlify/landscape2-$landscape2_version"
landscape2_bin="$install_dir/landscape2"

if [[ ! -x "$landscape2_bin" ]]; then
  installer="$(mktemp)"
  trap 'rm -f "$installer"' EXIT
  curl --proto '=https' --tlsv1.2 -fsSL \
    "https://github.com/cncf/landscape2/releases/download/v${landscape2_version}/landscape2-installer.sh" \
    -o "$installer"
  LANDSCAPE2_UNMANAGED_INSTALL="$install_dir" sh "$installer" --quiet
fi

deployment_url="${URL:-${DEPLOY_PRIME_URL:-http://127.0.0.1:8000}}"
settings_file="$(mktemp "$repo_root/.netlify-settings.XXXXXX.yml")"
trap 'rm -f "$settings_file" "${installer:-}"' EXIT

sed \
  -e "s|^url: .*$|url: \"$deployment_url\"|" \
  -e "s|^  open_graph: .*$|  open_graph: \"$deployment_url/images/intelligent-routing-og.png\"|" \
  "$repo_root/settings.yml" > "$settings_file"

PATH="$install_dir:$PATH" \
LANDSCAPE_SETTINGS_FILE="$settings_file" \
  bash "$repo_root/scripts/build-landscape.sh"

python3 "$repo_root/scripts/postprocess-build.py"
