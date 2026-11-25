"""Téléchargement des CSV (utilisé par get_data.py et, au premier lancement, par l'application)."""
from __future__ import annotations

import urllib.request
from pathlib import Path

from .config import DATA_DIR, SOURCES

MIN_BYTES = {"responses": 50_000_000, "schema": 10_000}  # garde-fou contre un pointeur LFS (~130 octets)


def is_ready(year: int) -> bool:
    return all(dest.exists() and dest.stat().st_size >= MIN_BYTES[kind] for kind, (_, dest) in SOURCES[year].items())


def download(url: str, dest: Path, kind: str, force: bool = False, log=print) -> None:
    if dest.exists() and dest.stat().st_size >= MIN_BYTES[kind] and not force:
        log(f"  déjà présent : {dest.relative_to(DATA_DIR.parent)}")
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    log(f"  téléchargement : {url}")
    tmp = dest.with_suffix(dest.suffix + ".part")
    with urllib.request.urlopen(url, timeout=300) as resp, open(tmp, "wb") as out:
        while chunk := resp.read(1 << 20):
            out.write(chunk)
    if tmp.stat().st_size < MIN_BYTES[kind]:
        tmp.unlink()
        raise RuntimeError(f"Fichier trop petit ({url}) : pointeur Git LFS ? "
                           "Utilisez l'adresse media.githubusercontent.com, pas « raw ».")
    tmp.replace(dest)
    log(f"  ok ({dest.stat().st_size / 1e6:.1f} Mo)")


def ensure(years=(2026, 2025), force: bool = False, log=print) -> None:
    for year in years:
        log(f"Enquête {year}")
        for kind, (url, dest) in SOURCES[year].items():
            download(url, dest, kind, force, log)
