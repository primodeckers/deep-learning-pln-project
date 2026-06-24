"""Gera notebooks/01_eda.ipynb a partir de células declaradas aqui.

IMPORTANTE: o notebook estilizado (tabelas HTML, interpretações por célula) é
mantido em `01_eda.ipynb` como fonte canônica. Este script NÃO deve sobrescrever
o notebook estilizado sem antes exportar as células de lá.

Para regenerar apenas após editar este arquivo manualmente com o conteúdo completo:
    python notebooks/_build_eda.py --force

Sem --force, o script apenas avisa e não altera 01_eda.ipynb.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

NB_PATH = Path(__file__).resolve().parent / "01_eda.ipynb"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--force",
        action="store_true",
        help="Sobrescreve 01_eda.ipynb (use só se _build_eda.py estiver sincronizado)",
    )
    args = parser.parse_args()

    if not args.force:
        print(
            "01_eda.ipynb é mantido estilizado no repositório.\n"
            "Edite notebooks/01_eda.ipynb diretamente.\n"
            "Para sobrescrever via script: python notebooks/_build_eda.py --force"
        )
        sys.exit(0)

    print(f"Nada a gerar — sincronize _build_eda.py com 01_eda.ipynb antes de --force.")
    print(f"Notebook atual: {NB_PATH}")


if __name__ == "__main__":
    main()
