#!/usr/bin/env python3
"""Сборка docs/ для GitHub Pages и widget-github.json с raw-ссылками для SE."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
ASSETS_SRC = ROOT / "assets"
SE_ROOT = ROOT / "streamelements"
SE_OUT = SE_ROOT / "out"
CONFIG_PATH = ROOT / "github.config.json"

DEPLOY_FILES = ("index.html", "style.css", "script.js", "config.js")
ASSET_FILES = (
    "background.jpg",
    "cat-body-cutout.png",
    "cat-head-cutout.png",
    "alice-cutout.png",
    "channel-avatar.png",
)

SE_IMAGE_FIELDS = {
    "layerBackground": "background.jpg",
    "layerCatBody": "cat-body-cutout.png",
    "layerCatHead": "cat-head-cutout.png",
    "layerAlice": "alice-cutout.png",
}


def load_config() -> dict[str, str]:
    data: dict[str, str] = {}
    if CONFIG_PATH.exists():
        data.update(json.loads(CONFIG_PATH.read_text(encoding="utf-8")))
    data["user"] = os.environ.get("GITHUB_USER", data.get("user", "")).strip()
    data["repo"] = os.environ.get("GITHUB_REPO", data.get("repo", "")).strip()
    data["branch"] = os.environ.get("GITHUB_BRANCH", data.get("branch", "main")).strip() or "main"
    if not data["user"] or data["user"] == "ВАШ_ЛОГИН":
        raise SystemExit(
            "Укажи логин и репо в github.config.json:\n"
            '  { "user": "mylogin", "repo": "twitch-starting-soon-tenniel", "branch": "main" }'
        )
    return data


def raw_url(cfg: dict[str, str], path: str) -> str:
    return f"https://raw.githubusercontent.com/{cfg['user']}/{cfg['repo']}/{cfg['branch']}/{path}"


def pages_url(cfg: dict[str, str]) -> str:
    return f"https://{cfg['user']}.github.io/{cfg['repo']}/"


def ensure_se_out() -> None:
    if not (SE_OUT / "assets" / "background.jpg").exists():
        subprocess.run([sys.executable, str(SE_ROOT / "build_streamelements.py")], check=True)


def build_docs() -> None:
    if DOCS.exists():
        shutil.rmtree(DOCS)
    assets_out = DOCS / "assets"
    assets_out.mkdir(parents=True)

    for name in DEPLOY_FILES:
        shutil.copy2(ROOT / name, DOCS / name)

    ensure_se_out()
    for filename in ASSET_FILES:
        shutil.copy2(SE_OUT / "assets" / filename, assets_out / filename)


def build_widget_github(cfg: dict[str, str]) -> Path:
    ensure_se_out()
    widget = json.loads((SE_ROOT / "widget.json").read_text(encoding="utf-8"))
    for field, filename in SE_IMAGE_FIELDS.items():
        widget[field]["value"] = raw_url(cfg, f"docs/assets/{filename}")
    out = SE_OUT / "widget-github.json"
    out.write_text(json.dumps(widget, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return out


def write_urls_file(cfg: dict[str, str]) -> Path:
    lines = [
        "GITHUB — ссылки для StreamElements и OBS",
        "=" * 44,
        "",
        f"Превью (GitHub Pages): {pages_url(cfg)}",
        "Включи: Settings → Pages → Branch main → Folder /docs",
        "",
        "OBS Browser Source — вставь URL Pages (без SE).",
        "",
        "StreamElements — вставь widget-github.json во вкладку FIELDS:",
        f"  streamelements/out/widget-github.json",
        "",
        "Или вручную raw-ссылки на картинки:",
    ]
    for field, filename in SE_IMAGE_FIELDS.items():
        lines.append(f"  {field}: {raw_url(cfg, f'docs/assets/{filename}')}")
    lines += ["", "HTML / CSS / JS — как обычно из streamelements/out/"]
    out = ROOT / "GITHUB.txt"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def main() -> None:
    cfg = load_config()
    build_docs()
    widget_path = build_widget_github(cfg)
    urls_path = write_urls_file(cfg)

    print(f"docs/          → GitHub Pages: {pages_url(cfg)}")
    print(f"{widget_path.name} → FIELDS в SE (картинки уже по URL)")
    print(f"{urls_path.name}       → все ссылки")
    print("\nДальше: git add docs/ → commit → push")
    print("Pages: Settings → Pages → main / docs")


if __name__ == "__main__":
    main()
