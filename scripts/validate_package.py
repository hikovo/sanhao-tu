#!/usr/bin/env python3
"""Validate the public Sanhao Rabbit v1 package."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image, ImageChops


ROOT = Path(__file__).resolve().parents[1]
CELL_WIDTH = 192
CELL_HEIGHT = 208
COLUMNS = 8
ROWS = 9
FRAME_COUNTS = (6, 8, 8, 4, 5, 8, 6, 6, 6)


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
        atlas = source.convert("RGBA")
        if source.format != "WEBP":
            fail(f"spritesheet format is {source.format}, expected WEBP")
    expected_size = (CELL_WIDTH * COLUMNS, CELL_HEIGHT * ROWS)
    if atlas.size != expected_size:
        fail(f"spritesheet size is {atlas.size}, expected {expected_size}")

    for row, used_frames in enumerate(FRAME_COUNTS):
        for column in range(used_frames, COLUMNS):
            box = (
                column * CELL_WIDTH,
                row * CELL_HEIGHT,
                (column + 1) * CELL_WIDTH,
                (row + 1) * CELL_HEIGHT,
            )
            if atlas.crop(box).getchannel("A").getbbox() is not None:
                fail(f"unused cell row {row}, column {column} is not transparent")

    with Image.open(static_path) as source:
        static = source.convert("RGBA")
    if static.size != (CELL_WIDTH, CELL_HEIGHT):
        fail(f"static lock size is {static.size}, expected {(CELL_WIDTH, CELL_HEIGHT)}")

    first_cell = atlas.crop((0, 0, CELL_WIDTH, CELL_HEIGHT))
    if ImageChops.difference(first_cell, static).getbbox() is not None:
        fail("static image differs from spritesheet row 0, frame 0")

    print("Sanhao Rabbit package validation passed.")
    print(f"- pet id: {manifest['id']}")
    print(f"- atlas: {atlas.size[0]}x{atlas.size[1]} RGBA WEBP")
    print(f"- grid: {COLUMNS}x{ROWS}; frames: {'/'.join(map(str, FRAME_COUNTS))}")
    print("- static image matches row 0, frame 0")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
