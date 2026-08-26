#!/usr/bin/env python3
"""Apply the small native Research route extension to a Landscape2 checkout."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
OVERLAY_ROOT = REPO_ROOT / "framework" / "landscape2-ui"


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"Expected one framework patch target in {path}, found {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: patch-landscape2-ui.py <landscape2 checkout>")

    checkout = Path(sys.argv[1]).resolve()
    webapp = checkout / "ui" / "webapp"
    if not (webapp / "src" / "App.tsx").is_file():
        raise SystemExit(f"Landscape2 webapp not found: {webapp}")

    revision = (OVERLAY_ROOT / "REVISION").read_text(encoding="utf-8").strip()
    checkout_revision = subprocess.check_output(
        ["git", "-C", str(checkout), "rev-parse", "HEAD"],
        text=True,
    ).strip()
    if checkout_revision != revision:
        raise SystemExit(f"Landscape2 checkout does not match pinned revision {revision}")

    data_file = webapp / "src" / "data.ts"
    replace_once(
        data_file,
        "export const GUIDE_PATH = `${BASE_PATH}/guide`;\n",
        "export const GUIDE_PATH = `${BASE_PATH}/guide`;\nexport const RESEARCH_PATH = `${BASE_PATH}/research`;\n",
    )

    app_file = webapp / "src" / "App.tsx"
    replace_once(app_file, "  PROJECTS_PATH,\n", "  PROJECTS_PATH,\n  RESEARCH_PATH,\n")
    replace_once(app_file, "import Projects from './layout/projects';\n", "import Projects from './layout/projects';\nimport Research from './layout/research';\n")
    replace_once(
        app_file,
        "          <Route path={GUIDE_PATH} component={Guide} />\n",
        "          <Route path={GUIDE_PATH} component={Guide} />\n          <Route path={RESEARCH_PATH} component={Research} />\n",
    )

    header_file = webapp / "src" / "layout" / "navigation" / "Header.tsx"
    replace_once(header_file, "  SCREENSHOTS_PATH,\n", "  RESEARCH_PATH,\n  SCREENSHOTS_PATH,\n")
    stats_marker = """            <Show when={props.statsVisible}>
              <button
                class={`btn btn-link position-relative text-uppercase fw-bold text-decoration-none p-0 ${styles.link}`}
                classList={{ activeLink: isActive(STATS_PATH) }}
"""
    research_block = """            <button
              class={`btn btn-link position-relative text-uppercase fw-bold text-decoration-none p-0 ${styles.link}`}
              classList={{ activeLink: isActive(RESEARCH_PATH) }}
              onClick={() => {
                if (isActive(RESEARCH_PATH)) {
                  scrollToTop(false);
                } else {
                  navigate(prepareLink(RESEARCH_PATH), {
                    state: { from: 'header' },
                  });
                  scrollToTop(false);
                }
              }}
              aria-label='Go to "Research" page'
            >
              Research
            </button>

"""
    replace_once(header_file, stats_marker, research_block + stats_marker)

    mobile_file = webapp / "src" / "layout" / "navigation" / "MobileDropdown.tsx"
    replace_once(
        mobile_file,
        "import { EXPLORE_PATH, GAMES_PATH, GUIDE_PATH, STATS_PATH } from '../../data';",
        "import { EXPLORE_PATH, GAMES_PATH, GUIDE_PATH, RESEARCH_PATH, STATS_PATH } from '../../data';",
    )
    mobile_stats_marker = """        <Show when={props.statsVisible}>
          <div class="dropdown-item mb-2">
            <A
              class={`btn btn-link position-relative text-uppercase w-100 text-start fw-semibold text-decoration-none p-0 ${styles.link}`}
              activeClass="activeLink"
              href={STATS_PATH}
"""
    mobile_research_block = """        <div class="dropdown-item mb-2">
          <A
            class={`btn btn-link position-relative text-uppercase w-100 text-start fw-semibold text-decoration-none p-0 ${styles.link}`}
            activeClass="activeLink"
            href={RESEARCH_PATH}
            onClick={closeDropdown}
          >
            Research
          </A>
        </div>
"""
    replace_once(mobile_file, mobile_stats_marker, mobile_research_block + mobile_stats_marker)

    research_dir = webapp / "src" / "layout" / "research"
    research_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OVERLAY_ROOT / "research" / "index.tsx", research_dir / "index.tsx")

    overlay_stub = webapp / "wasm" / "overlay" / "landscape2_overlay.ts"
    overlay_stub.parent.mkdir(parents=True, exist_ok=True)
    overlay_stub.write_text(
        "export default async function init() {}\n"
        "export async function get_overlay_data(): Promise<string> { throw new Error('Overlay unavailable'); }\n",
        encoding="utf-8",
    )

    quiz_stub = webapp / "wasm" / "quiz" / "landscape2_quiz.ts"
    quiz_stub.parent.mkdir(parents=True, exist_ok=True)
    quiz_stub.write_text(
        "export default async function init() {}\n"
        "export type State = any;\n"
        "export class QuizOptions { constructor(public url: string) {} }\n"
        "export class Quiz {\n"
        "  static async new(_options: QuizOptions): Promise<Quiz> { throw new Error('Quiz unavailable'); }\n"
        "  state(): State { return undefined; }\n"
        "  questions(): any[] { return []; }\n"
        "  check_player_guess(_index: number): State { return undefined; }\n"
        "  next_question(): State { return undefined; }\n"
        "}\n",
        encoding="utf-8",
    )

    print(f"Patched Landscape2 native UI at {webapp}")


if __name__ == "__main__":
    main()
