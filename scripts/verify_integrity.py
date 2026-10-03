#!/usr/bin/env python3
"""Verify the committed Ethos Bitcoin release manifest and artifact."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_distribution import load_manifest, validate_artifact  # noqa: E402


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) == 2 else ROOT / "Copy of Ethos_Bitcoin.xlsx"
    manifest = load_manifest()
    if manifest.get("artifact", {}).get("status") != "RELEASED":
        raise SystemExit("Manifest is not marked RELEASED")
    validate_artifact(path, manifest)
    print("PASS: committed manifest matches the reviewed artifact")


if __name__ == "__main__":
    main()
