#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
logos_dir="$repo_root/logos"
assets_tmp_dir="$(mktemp -d)"

cleanup() {
  rm -rf "$assets_tmp_dir"
}
trap cleanup EXIT

mkdir -p "$logos_dir"

curl_bin="curl"
curl_uses_windows_paths=false
if [[ -x /mnt/c/Windows/System32/curl.exe ]]; then
  curl_bin="/mnt/c/Windows/System32/curl.exe"
  curl_uses_windows_paths=true
fi

curl_output_path() {
  local target_path="$1"
  if [[ "$curl_uses_windows_paths" == true ]]; then
    wslpath -w "$target_path"
  else
    printf '%s\n' "$target_path"
  fi
}

curl_download() {
  local source_url="$1"
  local output_path="$2"
  printf 'Fetching %s\n' "$(basename "$output_path")"
  if [[ "$curl_uses_windows_paths" == true ]]; then
    "$curl_bin" --ssl-no-revoke --proto '=https' --tlsv1.2 -fsSL "$source_url" -o "$(curl_output_path "$output_path")"
  else
    "$curl_bin" --proto '=https' --tlsv1.2 -fsSL "$source_url" -o "$output_path"
  fi
}

fetch_svg() {
  local output_name="$1"
  local source_url="$2"
  local output_path="$logos_dir/$output_name"
  curl_download "$source_url" "$output_path"
}

fetch_raster_as_svg() {
  local output_name="$1"
  local source_url="$2"
  local mime_type="${3:-image/png}"
  local raster_path="$assets_tmp_dir/${output_name%.svg}.asset"
  local encoded_asset

  curl_download "$source_url" "$raster_path"
  encoded_asset="$(base64 -w 0 "$raster_path")"
  printf '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><image width="512" height="512" preserveAspectRatio="xMidYMid meet" href="data:%s;base64,%s"/></svg>\n' \
    "$mime_type" "$encoded_asset" > "$logos_dir/$output_name"
}

# Company and platform marks from official artwork or Simple Icons.
fetch_svg microsoft.svg "https://upload.wikimedia.org/wikipedia/commons/4/44/Microsoft_logo.svg"
fetch_svg aws.svg "https://upload.wikimedia.org/wikipedia/commons/9/93/Amazon_Web_Services_Logo.svg"
fetch_svg google-cloud.svg "https://cdn.simpleicons.org/googlecloud/4285F4"
fetch_svg digitalocean.svg "https://cdn.simpleicons.org/digitalocean/0080FF"
fetch_svg databricks.svg "https://cdn.simpleicons.org/databricks/FF3621"
fetch_svg cloudflare.svg "https://cdn.simpleicons.org/cloudflare/F38020"
fetch_svg openrouter.svg "https://cdn.simpleicons.org/openrouter/6467F2"
fetch_svg kong.svg "https://cdn.simpleicons.org/kong/003459"
fetch_svg cursor.svg "https://cdn.simpleicons.org/cursor/000000"
fetch_svg kubernetes.svg "https://cdn.simpleicons.org/kubernetes/326CE5"
fetch_svg envoy.svg "https://cdn.simpleicons.org/envoyproxy/AC6199"
fetch_svg amd.svg "https://cdn.simpleicons.org/amd/ED1C24"
fetch_svg nvidia.svg "https://cdn.simpleicons.org/nvidia/76B900"
fetch_svg arxiv.svg "https://cdn.simpleicons.org/arxiv/B31B1B"

# Project-owned artwork. Raster originals are embedded without redrawing them.
fetch_raster_as_svg vllm-sr.svg "https://raw.githubusercontent.com/vllm-project/semantic-router/main/dashboard/frontend/public/vllm-sr-logo.social.png"
fetch_raster_as_svg switchyard.svg "https://raw.githubusercontent.com/NVIDIA-NeMo/Switchyard/main/assets/logo.png"
fetch_svg plano.svg "https://raw.githubusercontent.com/katanemo/plano/main/apps/www/public/LogoMarkSquare.svg"
fetch_raster_as_svg llmrouter.svg "https://raw.githubusercontent.com/ulab-uiuc/LLMRouter/main/assets/logo.png"
fetch_raster_as_svg orbit.svg "https://raw.githubusercontent.com/LAMDA-Model-Reuse/ORBIT/main/resources/logo.jpg" "image/jpeg"
fetch_raster_as_svg routerarena.svg "https://raw.githubusercontent.com/RouteWorks/RouterArena/main/images/routerarena_logo_v2.png"
fetch_raster_as_svg llmrouterbench.svg "https://raw.githubusercontent.com/ynulihao/LLMRouterBench/main/assets/logo.png"
fetch_raster_as_svg routereval.svg "https://raw.githubusercontent.com/MilkThink-Lab/RouterEval/main/figure/logo.png"

# Organization or product-owned avatars and favicons for projects without SVG artwork.
fetch_raster_as_svg ramp.svg "https://www.google.com/s2/favicons?domain=router.com&sz=256"
fetch_raster_as_svg not-diamond.svg "https://www.google.com/s2/favicons?domain=notdiamond.ai&sz=256"
fetch_raster_as_svg orcarouter.svg "https://github.com/Continuum-AI-Corp.png?size=512"
fetch_raster_as_svg nadir.svg "https://github.com/NadirRouter.png?size=512"
fetch_raster_as_svg weave.svg "https://www.google.com/s2/favicons?domain=workweave.ai&sz=256"
fetch_raster_as_svg sqwish.svg "https://www.google.com/s2/favicons?domain=sqwish.ai&sz=256"
fetch_raster_as_svg kilo.svg "https://www.google.com/s2/favicons?domain=kilo.ai&sz=256"
fetch_raster_as_svg sakana.svg "https://github.com/SakanaAI.png?size=512"
fetch_raster_as_svg thesean.svg "https://www.google.com/s2/favicons?domain=thesean.ai&sz=256"
fetch_raster_as_svg litellm.svg "https://github.com/BerriAI.png?size=512"
fetch_raster_as_svg routellm.svg "https://github.com/lm-sys.png?size=512"
fetch_raster_as_svg openbmb.svg "https://github.com/OpenBMB.png?size=512"
fetch_raster_as_svg aurelio.svg "https://github.com/aurelio-labs.png?size=512"
fetch_raster_as_svg commonstack.svg "https://github.com/CommonstackAI.png?size=512"
fetch_raster_as_svg blockrun.svg "https://github.com/BlockRunAI.png?size=512"
fetch_raster_as_svg uiuc-ulab.svg "https://github.com/ulab-uiuc.png?size=512"
fetch_raster_as_svg irt-router.svg "https://github.com/Mercidaiha.png?size=512"
fetch_raster_as_svg carrot.svg "https://github.com/somerstep.png?size=512"
fetch_raster_as_svg routerdc.svg "https://github.com/shuhao02.png?size=512"
fetch_raster_as_svg tsrouter.svg "https://github.com/tianyi-lab.png?size=512"
fetch_raster_as_svg portkey.svg "https://github.com/Portkey-AI.png?size=512"
fetch_raster_as_svg bifrost.svg "https://github.com/maximhq.png?size=512"
fetch_raster_as_svg aisix.svg "https://github.com/api7.png?size=512"
fetch_raster_as_svg agentgateway.svg "https://github.com/agentgateway.png?size=512"
fetch_raster_as_svg kgateway.svg "https://github.com/kgateway-dev.png?size=512"
fetch_raster_as_svg openziti.svg "https://github.com/openziti.png?size=512"
fetch_raster_as_svg smg.svg "https://github.com/smg-project.png?size=512"
fetch_raster_as_svg llm-d.svg "https://github.com/llm-d.png?size=512"
fetch_raster_as_svg aibrix.svg "https://github.com/vllm-project.png?size=512"
fetch_raster_as_svg martian.svg "https://github.com/withmartian.png?size=512"
fetch_raster_as_svg mmr-bench.svg "https://github.com/Hunter-Wrynn.png?size=512"

printf 'Fetched %s landscape logos.\n' "$(find "$logos_dir" -maxdepth 1 -name '*.svg' | wc -l)"
