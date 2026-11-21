#!/usr/bin/env python3
"""Entry program for news-image-20261120 (v3, polished).

Writes the bundled broadsheet image to the output directory.
The image is a 1024x1024 PNG rendered from broadsheet.html
during the build session; this program only copies it,
byte for byte, so repeated runs are identical.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def output_dir() -> Path:
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = Path(raw)
    path.mkdir(parents=True, exist_ok=True)
    return path


def main() -> int:
    if not SOURCE.is_file():
        print(f"missing bundled image: {SOURCE}", file=sys.stderr)
        return 1
    data = SOURCE.read_bytes()
    if not data.startswith(PNG_MAGIC):
        print("bundled image is not a PNG", file=sys.stderr)
        return 1
    if len(data) > 1024 * 1024:
        print("bundled image exceeds the 1 MiB gate", file=sys.stderr)
        return 1
    target = output_dir() / "entry.png"
    shutil.copyfile(SOURCE, target)
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {target} ({len(data)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
