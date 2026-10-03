#!/usr/bin/env python3
"""Prepare a release directory from the already-approved artifact."""
from datetime import datetime, timezone
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_distribution import load_manifest, validate_artifact  # noqa: E402


def main() -> None:
    source = Path(sys.argv[1]) if len(sys.argv) == 2 else ROOT / "Copy of Ethos_Bitcoin.xlsx"
    manifest = load_manifest()
    validate_artifact(source, manifest)
    version = manifest["artifact"]["version"]
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    release_dir = ROOT / "release" / f"{version}-{stamp}"
    release_dir.mkdir(parents=True, exist_ok=False)
    shutil.copy2(source, release_dir / source.name)
    shutil.copy2(ROOT / "distribution_manifest.json", release_dir / "distribution_manifest.json")
    print(f"PASS: release prepared at {release_dir}")


if __name__ == "__main__":
    main()
