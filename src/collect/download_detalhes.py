"""Download das páginas HTML de detalhe do ComprasNet (sem CAPTCHA)."""

from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

import requests

from src.collect.load_licitacoes import LicitacaoRecord, load_licitacoes

DEFAULT_USER_AGENT = (
    "deep-learning-pln-project/1.0 (+https://github.com/primodeckers/deep-learning-pln-project; uso acadêmico)"
)


@dataclass
class DownloadResult:
    numero: str
    edital_url: str
    output_file: str | None
    status: str
    http_status: int | None
    error: str | None
    skipped: bool


def _download_one(
    session: requests.Session,
    record: LicitacaoRecord,
    output_dir: Path,
    *,
    overwrite: bool,
    timeout: float,
) -> DownloadResult:
    output_path = output_dir / f"{record.file_stem}.html"
    rel_output = str(Path("data/raw/detalhes") / output_path.name)

    if output_path.exists() and not overwrite:
        return DownloadResult(
            numero=record.numero,
            edital_url=record.edital_url,
            output_file=rel_output,
            status="skipped",
            http_status=None,
            error=None,
            skipped=True,
        )

    try:
        response = session.get(record.edital_url, timeout=timeout)
        response.raise_for_status()
        output_path.write_bytes(response.content)
        return DownloadResult(
            numero=record.numero,
            edital_url=record.edital_url,
            output_file=rel_output,
            status="ok",
            http_status=response.status_code,
            error=None,
            skipped=False,
        )
    except requests.RequestException as exc:
        return DownloadResult(
            numero=record.numero,
            edital_url=record.edital_url,
            output_file=None,
            status="error",
            http_status=getattr(getattr(exc, "response", None), "status_code", None),
            error=str(exc),
            skipped=False,
        )


def download_detalhes_html(
    csv_path: Path,
    output_dir: Path,
    *,
    delay_seconds: float = 1.0,
    timeout: float = 30.0,
    overwrite: bool = False,
    limit: int | None = None,
) -> dict:
    records = load_licitacoes(csv_path)
    if limit is not None:
        records = records[:limit]

    output_dir.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update({"User-Agent": DEFAULT_USER_AGENT})

    results: list[DownloadResult] = []
    for index, record in enumerate(records, start=1):
        result = _download_one(
            session,
            record,
            output_dir,
            overwrite=overwrite,
            timeout=timeout,
        )
        results.append(result)

        tag = result.status.upper()
        print(f"[{index}/{len(records)}] {tag} {record.numero} -> {result.output_file or result.error}")

        if index < len(records) and not result.skipped:
            time.sleep(delay_seconds)

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "csv_path": str(csv_path),
        "output_dir": str(output_dir),
        "total": len(results),
        "ok": sum(1 for r in results if r.status == "ok"),
        "skipped": sum(1 for r in results if r.status == "skipped"),
        "errors": sum(1 for r in results if r.status == "error"),
        "items": [asdict(r) for r in results],
    }

    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return summary
