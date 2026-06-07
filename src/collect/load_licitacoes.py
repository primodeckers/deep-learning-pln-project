"""Leitura do CSV de licitações exportado do ComprasNet."""

from __future__ import annotations

import csv
import io
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import parse_qs, urlparse


@dataclass(frozen=True)
class LicitacaoRecord:
    numero: str
    modalidade: str
    situacao: str
    orgao: str
    codigo_comprasnet: str
    tipo: str
    objeto: str
    edital_url: str
    total_homologado: str

    @property
    def file_stem(self) -> str:
        """Identificador único: coduasg + modprp + numprp da URL."""
        params = parse_qs(urlparse(self.edital_url).query)
        coduasg = params.get("coduasg", [""])[0]
        modprp = params.get("modprp", [""])[0]
        numprp = params.get("numprp", [""])[0]
        if coduasg and numprp:
            suffix = f"{coduasg}_{modprp}_{numprp}" if modprp else f"{coduasg}_{numprp}"
            return suffix

        numero_limpo = re.sub(r"[^\w\-/]", "", self.numero).replace("/", "_")
        return numero_limpo or "sem_id"


def load_licitacoes(csv_path: Path) -> list[LicitacaoRecord]:
    raw = csv_path.read_text(encoding="utf-8-sig")
    lines = raw.splitlines()

    # Linha 1 costuma ser título ("Licitacoes2025", às vezes com BOM); linha 2 é o cabeçalho.
    first_line = lines[0].strip().lstrip("\ufeff").lower() if lines else ""
    if first_line == "licitacoes2025":
        content = "\n".join(lines[1:])
    else:
        content = raw

    reader = csv.DictReader(io.StringIO(content), delimiter=";")
    records: list[LicitacaoRecord] = []

    for row in reader:
        url = (row.get("Edital") or "").strip().strip('"')
        if not url.startswith("http"):
            continue

        records.append(
            LicitacaoRecord(
                numero=(row.get("Nº da Licitação") or "").strip().strip('"'),
                modalidade=(row.get("Modalidade") or "").strip().strip('"'),
                situacao=(row.get("Situação") or "").strip().strip('"'),
                orgao=(row.get("Órgão") or "").strip().strip('"'),
                codigo_comprasnet=(row.get("Código COMPRASNET") or "").strip().strip('"'),
                tipo=(row.get("Tipo") or "").strip().strip('"'),
                objeto=(row.get("Objeto") or "").strip().strip('"'),
                edital_url=url,
                total_homologado=(row.get("Total Homologado") or "").strip().strip('"'),
            )
        )

    return records
