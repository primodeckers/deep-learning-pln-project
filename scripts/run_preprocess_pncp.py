"""Monta corpus JSONL a partir do PNCP (GDF distrital / 2025 por padrão)."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.preprocess.build_pncp_corpus import ESFERA_DISTRITAL_GDF, build_pncp_corpus_jsonl

DEFAULT_PNCP = ROOT / "data" / "comprasGOV-anual-VW_FT_PNCP_COMPRA-2025.xls"
DEFAULT_OUTPUT = ROOT / "data" / "processed" / "pncp_corpus_gdf2025.jsonl"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Filtra PNCP e gera corpus JSONL para treino (schema ComprasNet)."
    )
    parser.add_argument("--pncp", type=Path, default=DEFAULT_PNCP)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--esfera",
        default=ESFERA_DISTRITAL_GDF,
        help='orgao_entidade_esfera_id (D=GDF distrital, F=federal). Use "" para todas.',
    )
    parser.add_argument(
        "--uf",
        default="",
        help='UF opcional (ex.: DF). Vazio = nao filtra (esfera D ja e so DF em 2025).',
    )
    parser.add_argument(
        "--ano",
        type=int,
        default=2025,
        help="Ano PNCP. Use 0 para ignorar filtro de ano.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    esfera = args.esfera.strip() or None
    uf = args.uf.strip() or None
    ano = args.ano if args.ano else None

    print(f"Montando corpus PNCP de {args.pncp.name} ...")
    parts = []
    if esfera:
        parts.append(f"esfera={esfera} (GDF distrital)" if esfera == "D" else f"esfera={esfera}")
    if uf:
        parts.append(f"UF={uf}")
    if ano:
        parts.append(f"ano={ano}")
    if parts:
        print("  " + "  ".join(parts))

    summary = build_pncp_corpus_jsonl(
        args.pncp,
        args.output,
        esfera_id=esfera,
        uf=uf,
        ano=ano,
    )
    print(
        f"  {summary['records_written']:,} registros -> {args.output.name}".replace(
            ",", "."
        )
    )

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "corpus": summary,
    }
    manifest_path = args.output.parent / "pncp_preprocess_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Manifesto: {manifest_path}")


if __name__ == "__main__":
    main()
