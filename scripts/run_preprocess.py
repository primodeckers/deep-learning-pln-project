"""Pipeline de pré-processamento: HTML → texto → dataset PLN."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.preprocess.build_dataset import build_corpus_jsonl
from src.preprocess.extract_html import extract_all_html

DEFAULT_HTML = ROOT / "data" / "raw" / "detalhes"
DEFAULT_CSV = ROOT / "data" / "raw" / "licitacoes2025.csv"
DEFAULT_TEXT = ROOT / "data" / "interim" / "text"
DEFAULT_RECORDS = ROOT / "data" / "interim" / "records"
DEFAULT_OUTPUT = ROOT / "data" / "processed" / "licitacoes_corpus.jsonl"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extrai texto dos HTMLs e monta corpus PLN (JSONL)."
    )
    parser.add_argument("--html-dir", type=Path, default=DEFAULT_HTML)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--text-dir", type=Path, default=DEFAULT_TEXT)
    parser.add_argument("--records-dir", type=Path, default=DEFAULT_RECORDS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--overwrite", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()

    print("1/2 Extraindo texto dos HTMLs...")
    extract_summary = extract_all_html(
        args.html_dir,
        args.text_dir,
        args.records_dir,
        overwrite=args.overwrite,
    )
    print(
        f"   {extract_summary['ok']} extraídos, "
        f"{extract_summary['skipped']} ignorados "
        f"(total {extract_summary['total']})"
    )

    print("2/2 Montando corpus JSONL...")
    corpus_summary = build_corpus_jsonl(args.csv, args.records_dir, args.output)
    print(
        f"   {corpus_summary['records_written']} registros em {args.output.name}"
    )

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "extract": extract_summary,
        "corpus": corpus_summary,
    }
    manifest_path = args.output.parent / "preprocess_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\nManifesto: {manifest_path}")


if __name__ == "__main__":
    main()
