#!/usr/bin/env python3
"""Validate the public Sanhao Rabbit v1 package."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageStat


ROOT = Path(__file__).resolve().parents[1]
CELL_WIDTH = 192
CELL_HEIGHT = 208
COLUMNS = 8
ROWS = 9
FRAME_COUNTS = (6, 8, 8, 4, 5, 8, 6, 6, 6)
PREVIEW_FRAMES = {
    "blink.gif": 6,
    "swing-right.gif": 8,
    "swing-left.gif": 8,
    "hop.gif": 4,
    "wink.gif": 5,
    "dizzy.gif": 8,
    "wait.gif": 6,
    "typing.gif": 6,
    "smile.gif": 6,
}
PROMO_FILES = (
    "01-install-guide.gif",
    "02-blink.gif",
    "03-swing.gif",
    "04-hop.gif",
    "05-wink.gif",
    "06-dizzy.gif",
    "07-wait.gif",
    "08-typing.gif",
    "09-smile.gif",
)


def fail(message: str) -> None:
    raise ValueError(message)


def main() -> int:
    manifest_path = ROOT / "pet.json"
    atlas_path = ROOT / "spritesheet.webp"
    static_path = ROOT / "sanhao-tu.png"

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    required = {"id", "displayName", "description", "spritesheetPath"}
    missing = sorted(required - manifest.keys())
    if missing:
        fail(f"pet.json missing fields: {', '.join(missing)}")
    if manifest["id"] != "sanhao-tu":
        fail("pet.json id must be sanhao-tu")
    if manifest["spritesheetPath"] != "spritesheet.webp":
        fail("pet.json spritesheetPath must be spritesheet.webp")
    if "spriteVersionNumber" in manifest:
        fail("v1 package must omit spriteVersionNumber")

    with Image.open(atlas_path) as source:
        if source.format != "WEBP":
            fail(f"spritesheet format is {source.format}, expected WEBP")
        atlas = source.convert("RGBA")
    expected_size = (CELL_WIDTH * COLUMNS, CELL_HEIGHT * ROWS)
    if atlas.size != expected_size:
        fail(f"spritesheet size is {atlas.size}, expected {expected_size}")

    for row, used_frames in enumerate(FRAME_COUNTS):
        for column in range(COLUMNS):
            box = (
                column * CELL_WIDTH,
                row * CELL_HEIGHT,
                (column + 1) * CELL_WIDTH,
                (row + 1) * CELL_HEIGHT,
            )
            populated = atlas.crop(box).getchannel("A").getbbox() is not None
            if column < used_frames and not populated:
                fail(f"used cell row {row}, column {column} is empty")
            if column >= used_frames and populated:
                fail(f"unused cell row {row}, column {column} is not transparent")

    with Image.open(static_path) as source:
        static = source.convert("RGBA")
    expected_static_size = (CELL_WIDTH * 4, CELL_HEIGHT * 4)
    if static.size != expected_static_size:
        fail(f"static image size is {static.size}, expected {expected_static_size}")

    first_cell = atlas.crop((0, 0, CELL_WIDTH, CELL_HEIGHT))
    reduced_static = static.resize((CELL_WIDTH, CELL_HEIGHT), Image.Resampling.LANCZOS)
    white = Image.new("RGBA", first_cell.size, (255, 255, 255, 255))
    first_rgb = Image.alpha_composite(white, first_cell).convert("RGB")
    static_rgb = Image.alpha_composite(white, reduced_static).convert("RGB")
    rms = max(ImageStat.Stat(ImageChops.difference(first_rgb, static_rgb)).rms)
    if rms > 4.0:
        fail(f"high-resolution static image does not match row 0 frame 0 (RMS {rms:.2f})")

    previews = ROOT / "assets" / "previews"
    for filename, expected_frames in PREVIEW_FRAMES.items():
        with Image.open(previews / filename) as preview:
            if preview.size != (384, 416):
                fail(f"preview {filename} size is {preview.size}, expected (384, 416)")
            if preview.n_frames != expected_frames:
                fail(
                    f"preview {filename} has {preview.n_frames} frames, "
                    f"expected {expected_frames}"
                )

    promo_dir = ROOT / "promo"
    actual_promo = tuple(sorted(path.name for path in promo_dir.glob("*.gif")))
    if actual_promo != PROMO_FILES:
        fail("promo directory must contain exactly the nine approved GIFs")
    for filename in PROMO_FILES:
        with Image.open(promo_dir / filename) as promo:
            if promo.size != (1440, 1440):
                fail(f"promo {filename} size is {promo.size}, expected (1440, 1440)")

    print("Sanhao Rabbit package validation passed.")
    print(f"- pet id: {manifest['id']}")
    print(f"- atlas: {atlas.size[0]}x{atlas.size[1]} RGBA WEBP")
    print(f"- grid: {COLUMNS}x{ROWS}; frames: {'/'.join(map(str, FRAME_COUNTS))}")
    print("- high-resolution static image matches row 0, frame 0")
    print("- 9 animation previews and 9 square promo GIFs passed")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
