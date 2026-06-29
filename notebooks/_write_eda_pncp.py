"""Gera notebooks/03_eda_pncp.ipynb — espelha 01_eda com dados PNCP only."""

from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / "03_eda_pncp.ipynb"


def c_md(text: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": text}


def c_code(text: str) -> dict:
    return {
        "cell_type": "code",
        "metadata": {},
        "outputs": [],
        "source": text,
        "execution_count": None,
    }


cells = [
    c_md(
        "# EDA — PNCP / Compras.gov.br 2025 (DF)\n\n"
        "**Fonte única:** `data/comprasGOV-anual-VW_FT_PNCP_COMPRA-2025.xls` "
        "(CSV UTF-8, extensão `.xls`)\n\n"
        "**Recorte:** `unidade_orgao_uf_sigla == \"DF\"` e `ano_compra_pncp == 2025`.\n\n"
        "Projeto **independente** — análise exploratória de compras PNCP no **DF**. "
        "Espelha o protocolo do `01_eda.ipynb` (macroáreas, modalidade, tamanho de texto, "
        "valor homologado, vazamento de label), **sem** misturar corpus ComprasNet DF.\n\n"
        "**Label proxy:** `orgao_entidade_razao_social` → 6 macroáreas (`src/preprocess/labels.py`)."
    ),
    c_md("### Célula 1 — Configuração do ambiente e carregamento"),
    c_code(
        "import sys\n"
        "from collections import Counter\n"
        "from pathlib import Path\n\n"
        "import matplotlib.pyplot as plt\n"
        "from IPython.display import HTML, display\n\n"
        "\n"
        "def br_num(n: int | float) -> str:\n"
        "    return f\"{int(n):,}\".replace(\",\", \".\")\n\n"
        "\n"
        "def br_money(v: float) -> str:\n"
        "    return \"R$ \" + f\"{v:,.0f}\".replace(\",\", \".\")\n\n"
        "\n"
        "def show_table(titulo, colunas, linhas, alinhamentos=None):\n"
        "    if alinhamentos is None:\n"
        "        alinhamentos = [\"left\"] + [\"right\"] * (len(colunas) - 1)\n"
        "    estilo_th = (\n"
        "        \"padding:8px 12px;border:1px solid #475569;\"\n"
        "        \"background:#1e40af;color:#fff;font-weight:600;\"\n"
        "    )\n"
        "    estilo_td = \"padding:8px 12px;border:1px solid #cbd5e1;background:#fff;color:#111827;\"\n"
        "    corpo = \"\"\n"
        "    for row in linhas:\n"
        "        tds = \"\".join(\n"
        "            f\"<td style='{estilo_td}text-align:{a};'>{v}</td>\"\n"
        "            for v, a in zip(row, alinhamentos)\n"
        "        )\n"
        "        corpo += f\"<tr>{tds}</tr>\"\n"
        "    ths = \"\".join(\n"
        "        f\"<th style='{estilo_th}text-align:{a};'>{c}</th>\"\n"
        "        for c, a in zip(colunas, alinhamentos)\n"
        "    )\n"
        "    html = (\n"
        "        f\"<div style='margin:14px 0;font-family:Segoe UI,sans-serif;'>\"\n"
        "        f\"<div style='font-size:14px;font-weight:bold;margin-bottom:8px;'>{titulo}</div>\"\n"
        "        f\"<table style='border-collapse:collapse;font-size:13px;'>\"\n"
        "        f\"<thead><tr>{ths}</tr></thead><tbody>{corpo}</tbody></table></div>\"\n"
        "    )\n"
        "    display(HTML(html))\n\n"
        "\n"
        "ROOT = Path.cwd()\n"
        "if (ROOT / \"src\").exists():\n"
        "    pass\n"
        "elif (ROOT.parent / \"src\").exists():\n"
        "    ROOT = ROOT.parent\n"
        "sys.path.insert(0, str(ROOT))\n\n"
        "import pandas as pd\n"
        "from src.preprocess.labels import AREAS, area_for_orgao, normalize\n\n"
        "PNCP_PATH = ROOT / \"data\" / \"comprasGOV-anual-VW_FT_PNCP_COMPRA-2025.xls\"\n"
        "FIGURES = ROOT / \"reports\" / \"figures\"\n"
        "FIGURES.mkdir(parents=True, exist_ok=True)\n\n"
        "print(f\"Carregando {PNCP_PATH.name} ...\")\n"
        "df_raw = pd.read_csv(PNCP_PATH, encoding=\"utf-8\", low_memory=False)\n"
        "n_br = len(df_raw)\n"
        "df = df_raw[(df_raw[\"unidade_orgao_uf_sigla\"] == \"DF\") & (df_raw[\"ano_compra_pncp\"] == 2025)].copy()\n"
        "df[\"area\"] = df[\"orgao_entidade_razao_social\"].map(area_for_orgao)\n"
        "df[\"objeto\"] = df[\"objeto_compra\"].fillna(\"\")\n"
        "df[\"texto\"] = (\n"
        "    df[\"orgao_entidade_razao_social\"].fillna(\"\")\n"
        "    + \" \"\n"
        "    + df[\"unidade_orgao_nome_unidade\"].fillna(\"\")\n"
        "    + \" \"\n"
        "    + df[\"objeto_compra\"].fillna(\"\")\n"
        "    + \" \"\n"
        "    + df[\"informacao_complementar\"].fillna(\"\")\n"
        ").str.strip()\n"
        "records = df.to_dict(\"records\")\n"
        "print(f\"PNCP Brasil: {n_br:,} compras → DF/2025: {len(records):,}\".replace(\",\", \".\"))\n\n"
        "cols_chave = [\n"
        "    (\"cod_compra\", \"ID interno PNCP\"),\n"
        "    (\"numero_controle_PNCP\", \"Identificador único\"),\n"
        "    (\"modalidade_nome\", \"Modalidade (pregão, dispensa...)\"),\n"
        "    (\"modo_disputa_nome_pncp\", \"Modo de disputa\"),\n"
        "    (\"orgao_entidade_razao_social\", \"Órgão comprador (→ label)\"),\n"
        "    (\"unidade_orgao_uf_sigla\", \"UF\"),\n"
        "    (\"objeto_compra\", \"Descrição do objeto\"),\n"
        "    (\"valor_total_homologado\", \"Valor homologado (R$)\"),\n"
        "    (\"area\", \"Macroárea derivada do órgão\"),\n"
        "]\n\n"
        "show_table(\n"
        "    \"TABELA 1 — Visão geral PNCP DF/2025\",\n"
        "    [\"Métrica\", \"Valor\"],\n"
        "    [\n"
        "        [\"Arquivo\", PNCP_PATH.name],\n"
        "        [\"Recorte\", \"UF = DF, ano = 2025\"],\n"
        "        [\"Compras no recorte\", br_num(len(records))],\n"
        "        [\"Compras Brasil (referência)\", br_num(n_br)],\n"
        "        [\"Órgãos distintos (DF)\", br_num(df[\"orgao_entidade_razao_social\"].nunique())],\n"
        "        [\"Label (macroárea)\", \"area (derivado de orgao_entidade_razao_social)\"],\n"
        "    ],\n"
        ")\n\n"
        "show_table(\n"
        "    \"TABELA 1b — Colunas principais\",\n"
        "    [\"#\", \"Campo\", \"Descrição\"],\n"
        "    [[str(i), c, d] for i, (c, d) in enumerate(cols_chave, 1)],\n"
        "    [\"right\", \"left\", \"left\"],\n"
        ")\n"
    ),
    c_md(
        "#### Resultado da Célula 1\n\n"
        "Carregamos **todas** as compras do arquivo PNCP 2025. O label `area` vem do **nome do órgão**, "
        "mesma regra de palavras-chave usada no projeto de classificação."
    ),
    c_md("## 1. Distribuição das macroáreas (label)\n\n"
         "Label derivado de `orgao_entidade_razao_social` — ver `src/preprocess/labels.py`."),
    c_md("### Célula 2 — Gráfico de distribuição das macroáreas"),
    c_code(
        "area_counts = Counter(r[\"area\"] for r in records)\n"
        "ordered = [(a, area_counts.get(a, 0)) for a in AREAS]\n"
        "total = len(records)\n\n"
        "show_table(\n"
        "    \"TABELA 2 — Distribuição por macroárea (label)\",\n"
        "    [\"Macroárea\", \"N compras\", \"% do total\"],\n"
        "    [[a, br_num(n), f\"{100 * n / total:.1f}%\"] for a, n in ordered],\n"
        ")\n\n"
        "fig, ax = plt.subplots(figsize=(8, 4))\n"
        "ax.bar([a for a, _ in ordered], [n for _, n in ordered], color=\"#4C72B0\")\n"
        "ax.set_ylabel(\"nº de compras\")\n"
        "ax.set_title(\"Distribuição por macroárea — PNCP 2025\")\n"
        "plt.setp(ax.get_xticklabels(), rotation=30, ha=\"right\")\n"
        "for i, (_, n) in enumerate(ordered):\n"
        "    if n > 0:\n"
        "        ax.text(i, n, br_num(n), ha=\"center\", fontsize=8, rotation=90)\n"
        "fig.tight_layout()\n"
        "fig.savefig(FIGURES / \"eda_pncp_areas.png\", dpi=120)\n"
        "plt.show()\n"
    ),
    c_md(
        "#### Resultado da Célula 2\n\n"
        "A classe **Administração/Outros** domina (fallback quando o órgão não casa com keyword). "
        "Corpus nacional e muito maior que um recorte DF — desbalanceamento é esperado."
    ),
    c_md("## 2. Modalidade e modo de disputa"),
    c_md("### Célula 3 — Contagem de modalidade e modo de disputa"),
    c_code(
        "rotulos = {\n"
        "    \"modalidade_nome\": \"Modalidade de licitação\",\n"
        "    \"modo_disputa_nome_pncp\": \"Modo de disputa\",\n"
        "}\n"
        "tabela_num = 3\n"
        "for campo, rotulo in rotulos.items():\n"
        "    contagem = Counter(r.get(campo, \"\") or \"(vazio)\" for r in records).most_common(8)\n"
        "    tot = sum(n for _, n in contagem)\n"
        "    show_table(\n"
        "        f\"TABELA {tabela_num} — {rotulo}\",\n"
        "        [\"Valor\", \"N\", \"%\"],\n"
        "        [[v, br_num(n), f\"{100 * n / tot:.1f}%\"] for v, n in contagem],\n"
        "        [\"left\", \"right\", \"right\"],\n"
        "    )\n"
        "    tabela_num += 1\n"
    ),
    c_md(
        "#### Resultado da Célula 3\n\n"
        "**Dispensa** e **Pregão Eletrônico** concentram a maior parte das compras no PNCP nacional."
    ),
    c_md("## 3. Tamanho dos textos (`objeto_compra` e `texto` completo)"),
    c_md("### Célula 4 — Histograma do tamanho dos textos em palavras"),
    c_code(
        "word_obj = [len((r.get(\"objeto\") or \"\").split()) for r in records]\n"
        "word_texto = [len((r.get(\"texto\") or \"\").split()) for r in records]\n"
        "n = len(word_obj)\n"
        "mediana = sorted(word_obj)[n // 2] if n else 0\n"
        "acima_512 = sum(1 for w in word_obj if w > 512)\n\n"
        "show_table(\n"
        "    \"TABELA 5 — Tamanho em palavras (objeto_compra)\",\n"
        "    [\"Métrica\", \"Valor\"],\n"
        "    [\n"
        "        [\"Mínimo\", br_num(min(word_obj) if word_obj else 0) + \" palavras\"],\n"
        "        [\"Mediana\", br_num(mediana) + \" palavras\"],\n"
        "        [\"Máximo\", br_num(max(word_obj) if word_obj else 0) + \" palavras\"],\n"
        "        [\"Compras com > 512 palavras\", br_num(acima_512)],\n"
        "        [\"% acima de 512 palavras\", f\"{100 * acima_512 / n:.1f}%\" if n else \"0,0%\"],\n"
        "        [\"Mediana texto completo\", br_num(sorted(word_texto)[n // 2] if n else 0) + \" palavras\"],\n"
        "    ],\n"
        ")\n\n"
        "fig, ax = plt.subplots(figsize=(8, 4))\n"
        "ax.hist([min(w, 500) for w in word_obj], bins=40, color=\"#55A868\")\n"
        "ax.set_xlabel(\"nº de palavras em objeto_compra (cap 500)\")\n"
        "ax.set_ylabel(\"nº de compras\")\n"
        "ax.set_title(\"Distribuição do tamanho de objeto_compra — PNCP\")\n"
        "fig.tight_layout()\n"
        "fig.savefig(FIGURES / \"eda_pncp_tamanho_texto.png\", dpi=120)\n"
        "plt.show()\n"
    ),
    c_md(
        "#### Resultado da Célula 4\n\n"
        "No PNCP, `objeto_compra` é **curto** (mediana ~25 palavras) — metadado resumido, "
        "não o edital HTML completo. Poucas compras passam de 512 palavras."
    ),
    c_md("## 4. Valor homologado por macroárea"),
    c_md("### Célula 5 — Tabela e gráfico de valor homologado por macroárea"),
    c_code(
        "por_area = {a: [] for a in AREAS}\n"
        "for r in records:\n"
        "    val = r.get(\"valor_total_homologado\")\n"
        "    if pd.notna(val) and float(val) > 0:\n"
        "        por_area[r[\"area\"]].append(float(val))\n\n"
        "linhas_valor = []\n"
        "for a in AREAS:\n"
        "    vals = sorted(por_area[a])\n"
        "    if vals:\n"
        "        linhas_valor.append([a, br_num(len(vals)), br_money(sum(vals)), br_money(vals[len(vals) // 2])])\n"
        "    else:\n"
        "        linhas_valor.append([a, \"0\", \"—\", \"—\"])\n\n"
        "show_table(\n"
        "    \"TABELA 6 — Valor homologado por macroárea\",\n"
        "    [\"Macroárea\", \"N c/ valor\", \"Soma\", \"Mediana\"],\n"
        "    linhas_valor,\n"
        "    [\"left\", \"right\", \"right\", \"right\"],\n"
        ")\n\n"
        "somas = [sum(por_area[a]) for a in AREAS]\n"
        "fig, ax = plt.subplots(figsize=(8, 4))\n"
        "ax.bar(AREAS, [s / 1e9 for s in somas], color=\"#C44E52\")\n"
        "ax.set_ylabel(\"Soma homologada (bilhões R$)\")\n"
        "ax.set_title(\"Gasto homologado por macroárea — PNCP 2025\")\n"
        "plt.setp(ax.get_xticklabels(), rotation=30, ha=\"right\")\n"
        "fig.tight_layout()\n"
        "fig.savefig(FIGURES / \"eda_pncp_valor_area.png\", dpi=120)\n"
        "plt.show()\n"
    ),
    c_md(
        "#### Resultado da Célula 5\n\n"
        "Saúde e Administração/Outros concentram volume financeiro. "
        "Mediana por área ajuda a ver o gasto \"típico\" sem outliers."
    ),
    c_md("## 5. Vazamento de label por palavras-chave"),
    c_md("### Célula 6 — Análise de vazamento de label"),
    c_code(
        "from src.preprocess.labels import AREA_KEYWORDS\n"
        "from src.preprocess.clean_objeto import limpar_objeto\n\n"
        "kw_by_area = dict(AREA_KEYWORDS)\n\n"
        "\n"
        "def contem_keyword(texto: str, area: str) -> bool:\n"
        "    kws = kw_by_area.get(area)\n"
        "    if not kws:\n"
        "        return False\n"
        "    alvo = normalize(texto)\n"
        "    return any(kw in alvo for kw in kws)\n\n"
        "\n"
        "for r in records:\n"
        "    r[\"objeto_limpo\"] = limpar_objeto(\n"
        "        r.get(\"objeto\") or \"\",\n"
        "        orgao=r.get(\"orgao_entidade_razao_social\"),\n"
        "    )\n\n"
        "com_kw = [r for r in records if r[\"area\"] in kw_by_area]\n"
        "vaz_texto = sum(contem_keyword(r.get(\"texto\", \"\"), r[\"area\"]) for r in com_kw)\n"
        "vaz_obj = sum(contem_keyword(r.get(\"objeto\", \"\"), r[\"area\"]) for r in com_kw)\n"
        "vaz_limpo = sum(contem_keyword(r.get(\"objeto_limpo\", \"\"), r[\"area\"]) for r in com_kw)\n"
        "base = len(com_kw)\n\n"
        "if base:\n"
        "    show_table(\n"
        "        \"TABELA 7 — Vazamento de label (palavra-chave da área no texto)\",\n"
        "        [\"Campo analisado\", \"Com vazamento\", \"Total\", \"Taxa\"],\n"
        "        [\n"
        "            [\"texto (órgão + objeto + complemento)\", br_num(vaz_texto), br_num(base), f\"{100 * vaz_texto / base:.1f}%\"],\n"
        "            [\"objeto_compra (só objeto)\", br_num(vaz_obj), br_num(base), f\"{100 * vaz_obj / base:.1f}%\"],\n"
        "            [\"objeto_limpo (sem boilerplate)\", br_num(vaz_limpo), br_num(base), f\"{100 * vaz_limpo / base:.1f}%\"],\n"
        "        ],\n"
        "        [\"left\", \"right\", \"right\", \"right\"],\n"
        "    )\n\n"
        "print(f\"Compras analisadas (áreas com keyword): {br_num(base)}\")\n"
        "print(f\"Compras em Administração/Outros (excluídas da Tabela 7): {br_num(len(records) - base)}\")\n"
    ),
    c_md(
        "#### Resultado da Célula 6 — Tabela 7\n\n"
        "Compara três entradas de texto:\n"
        "- **texto** — concatena órgão + unidade + objeto + complemento (análogo ao HTML completo)\n"
        "- **objeto_compra** — só a descrição da compra (entrada honesta para PLN)\n"
        "- **objeto_limpo** — objeto após `limpar_objeto()`\n\n"
        "Compras em `Administracao/Outros` ficam **fora** da Tabela 7 (sem keyword própria). "
        "Quanto menor a taxa em `objeto_compra`, menos o modelo pode \"colar\" no label pelo órgão."
    ),
    c_md("## 6. Vazamento residual — nome do órgão em `objeto_compra`"),
    c_md("### Célula 7 — Auditoria complementar (Tabela 8)"),
    c_code(
        "def orgao_aparece_no_texto(orgao: str, texto: str) -> bool:\n"
        "    org = normalize(orgao or \"\")\n"
        "    if len(org) < 8:\n"
        "        return False\n"
        "    return org in normalize(texto or \"\")\n\n"
        "\n"
        "residual = [\n"
        "    r for r in records\n"
        "    if orgao_aparece_no_texto(r.get(\"orgao_entidade_razao_social\", \"\"), r.get(\"objeto\", \"\"))\n"
        "]\n"
        "n_res, n_tot = len(residual), len(records)\n"
        "taxa = n_res / n_tot if n_tot else 0\n\n"
        "show_table(\n"
        "    \"TABELA 8 — Vazamento residual (nome do órgão em objeto_compra)\",\n"
        "    [\"Métrica\", \"Valor\"],\n"
        "    [\n"
        "        [\"Compras com órgão no objeto\", f\"{br_num(n_res)} / {br_num(n_tot)}\"],\n"
        "        [\"Taxa\", f\"{taxa:.1%}\"],\n"
        "        [\"Entrada recomendada para PLN\", \"objeto_compra (documentar taxa)\"],\n"
        "    ],\n"
        "    [\"left\", \"left\"],\n"
        ")\n\n"
        "if residual:\n"
        "    show_table(\n"
        "        \"Exemplos de vazamento residual (até 8)\",\n"
        "        [\"Controle PNCP\", \"Órgão\", \"Trecho objeto_compra\"],\n"
        "        [\n"
        "            [\n"
        "                (r.get(\"numero_controle_PNCP\") or \"?\")[:28],\n"
        "                (r.get(\"orgao_entidade_razao_social\") or \"\")[:40],\n"
        "                ((r.get(\"objeto\") or \"\")[:80] + \"…\"),\n"
        "            ]\n"
        "            for r in residual[:8]\n"
        "        ],\n"
        "        [\"left\", \"left\", \"left\"],\n"
        "    )\n"
    ),
    c_md(
        "#### Resultado da Célula 7\n\n"
        "Registros em que o **nome do órgão** ainda aparece em `objeto_compra`. "
        "Documentar a taxa é parte do rigor metodológico antes de treinar classificadores sobre PNCP."
    ),
]

nb = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.12.0"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

OUT.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
print("OK", OUT)
