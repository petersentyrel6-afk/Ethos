#!/usr/bin/env python3
"""Validate the approved Ethos Bitcoin distribution artifact and manifest."""
from __future__ import annotations

import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "distribution_manifest.json"
EXPECTED_NAME = "Copy of Ethos_Bitcoin.xlsx"
CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"
FORBIDDEN = re.compile(r"(?:xprv|yprv|zprv|private[ _-]*key|seed[ _-]*(?:phrase|words?)|mnemonic|wallet[ _-]*password|api[ _-]*key|access[ _-]*token)", re.I)


def polymod(values: list[int]) -> int:
    generators = [0x3B6A57B2, 0x26508E6D, 0x1EA119FA, 0x3D4233DD, 0x2A1462B3]
    chk = 1
    for value in values:
        top = chk >> 25
        chk = ((chk & 0x1FFFFFF) << 5) ^ value
        for i, generator in enumerate(generators):
            if (top >> i) & 1:
                chk ^= generator
    return chk


def valid_bech32_address(address: str) -> bool:
    if not address or address != address.lower() or len(address) > 90 or "1" not in address:
        return False
    pos = address.rfind("1")
    hrp, data_part = address[:pos], address[pos + 1 :]
    if hrp != "bc" or len(data_part) < 6:
        return False
    try:
        data = [CHARSET.index(char) for char in data_part]
    except ValueError:
        return False
    expanded = [ord(char) >> 5 for char in hrp] + [0] + [ord(char) & 31 for char in hrp]
    return polymod(expanded + data) == 1


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_manifest() -> dict:
    try:
        return json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Manifest error: {exc}")


def validate_artifact(path: Path, manifest: dict) -> None:
    if not path.is_file():
        raise SystemExit(f"Artifact does not exist or is not a file: {path}")
    if path.name != EXPECTED_NAME:
        raise SystemExit(f"Unexpected artifact name: {path.name!r}; expected {EXPECTED_NAME!r}")
    artifact = manifest.get("artifact", {})
    if artifact.get("filename") != EXPECTED_NAME:
        raise SystemExit("Manifest artifact filename does not match the approved filename")
    actual_hash = sha256(path)
    if actual_hash.lower() != str(artifact.get("sha256", "")).lower():
        raise SystemExit(f"SHA-256 mismatch: expected {artifact.get('sha256')}, got {actual_hash}")
    actual_size = path.stat().st_size
    if actual_size != artifact.get("size_bytes"):
        raise SystemExit(f"Size mismatch: expected {artifact.get('size_bytes')}, got {actual_size}")
    support = manifest.get("support", {})
    address = support.get("bitcoin_address", "")
    if support.get("network") != "bitcoin-mainnet" or not valid_bech32_address(address):
        raise SystemExit("Manifest Bitcoin address is not a valid lowercase mainnet Bech32 address")
    if support.get("payment_required") is not False or support.get("investment_rights_granted") is not False:
        raise SystemExit("Support policy must remain voluntary and grant no investment rights")
    try:
        with zipfile.ZipFile(path) as archive:
            for member in archive.namelist():
                if not member.endswith((".xml", ".rels", ".txt")):
                    continue
                text = archive.read(member).decode("utf-8", errors="ignore")
                if FORBIDDEN.search(text):
                    raise SystemExit(f"Credential-like marker found in spreadsheet member: {member}")
    except zipfile.BadZipFile as exc:
        raise SystemExit(f"Artifact is not a valid XLSX ZIP: {exc}")


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) == 2 else ROOT / EXPECTED_NAME
    validate_artifact(path, load_manifest())
    print(f"PASS: {path.name}")
    print(f"SHA-256: {sha256(path)}")
    print("Bitcoin address: valid mainnet Bech32")
    print("Download payment required: NO")


if __name__ == "__main__":
    main()
