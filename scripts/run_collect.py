"""Ponto de entrada para coleta de dados."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.collect.download_detalhes import download_detalhes_html

DEFAULT_CSV = ROOT / "data" / "raw" / "licitacoes2025.csv"
DEFAULT_OUTPUT = ROOT / "data" / "raw" / "detalhes"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Coleta páginas HTML de detalhe dos editais (ComprasNet, sem CAPTCHA)."
    )
    parser.add_argument(
        "--csv",
        type=Path,
        default=DEFAULT_CSV,
        help="Caminho do CSV de licitações",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Pasta de saída dos HTMLs",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Intervalo em segundos entre downloads (padrão: 1.0)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="Timeout HTTP em segundos",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Baixar novamente mesmo se o arquivo já existir",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limitar quantidade de registros (útil para teste)",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()

    if not args.csv.exists():
        raise SystemExit(f"CSV não encontrado: {args.csv}")

    summary = download_detalhes_html(
        args.csv,
        args.output,
        delay_seconds=args.delay,
        timeout=args.timeout,
        overwrite=args.overwrite,
        limit=args.limit,
    )

    print(
        f"\nConcluído: {summary['ok']} baixados, "
        f"{summary['skipped']} ignorados, {summary['errors']} erros."
    )
    print(f"Manifesto: {args.output / 'manifest.json'}")


if __name__ == "__main__":
    main()
