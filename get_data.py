"""Télécharge les données de l'enquête Stack Overflow dans data/ (jamais versionné).

Usage :
    uv run python get_data.py                # 2026 (obligatoire) + 2025 (comparaison)
    uv run python get_data.py --only-2026    # sans la comparaison
    uv run python get_data.py --force        # retélécharge même si les fichiers existent
"""
import argparse

from devia.download import ensure


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only-2026", action="store_true", help="ne pas télécharger 2025")
    ap.add_argument("--force", action="store_true", help="retélécharger")
    args = ap.parse_args()
    ensure((2026,) if args.only_2026 else (2026, 2025), force=args.force)


if __name__ == "__main__":
    main()
