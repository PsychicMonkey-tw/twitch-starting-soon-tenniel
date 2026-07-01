#!/usr/bin/env python3
"""Сборка пакета StreamElements — Starting Soon Tenniel."""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
ASSETS_SRC = ROOT.parent / "assets"
OUT = ROOT / "out"
W, H = 1920, 1080

ASSETS = (
    ("background.jpg", "jpeg"),
    ("cat-body-cutout.png", "png"),
    ("cat-head-cutout.png", "png"),
    ("alice-cutout.png", "png"),
    ("channel-avatar.png", "png"),
)


def resize_cover(img: Image.Image, width: int, height: int) -> Image.Image:
    src_w, src_h = img.size
    scale = max(width / src_w, height / src_h)
    new_w = int(src_w * scale)
    new_h = int(src_h * scale)
    resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    left = (new_w - width) // 2
    top = (new_h - height) // 2
    return resized.crop((left, top, left + width, top + height))


def export_asset(src: Path, dest: Path, kind: str) -> None:
    img = Image.open(src)
    if kind == "jpeg":
        out = resize_cover(img.convert("RGB"), W, H)
        out.save(dest, format="JPEG", quality=90, optimize=True, progressive=True)
        return

    has_alpha = img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info)
    out = img.convert("RGBA" if has_alpha else "RGB")
    out.save(dest, format="PNG", optimize=True, compress_level=9)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    assets_out = OUT / "assets"
    assets_out.mkdir(exist_ok=True)

    for name in ("widget.html", "widget.css", "widget.js", "widget.json", "USTANOVKA.txt"):
        shutil.copy2(ROOT / name, OUT / name)

    print("Ассеты для загрузки в SE:")
    for filename, kind in ASSETS:
        src = ASSETS_SRC / filename
        if not src.exists():
            raise SystemExit(f"Нет файла: {src}")
        dest = assets_out / filename
        src_kb = src.stat().st_size // 1024
        export_asset(src, dest, kind)
        out_kb = dest.stat().st_size // 1024
        with Image.open(dest) as check:
            print(f"  {filename}: {check.size[0]}×{check.size[1]}, {src_kb} KB → {out_kb} KB")

    kb = sum(f.stat().st_size for f in OUT.rglob("*") if f.is_file()) // 1024
    print(f"\nГотово: {OUT}/ (~{kb} KB)")


if __name__ == "__main__":
    main()
