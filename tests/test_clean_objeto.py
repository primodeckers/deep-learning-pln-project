"""Testes de limpeza do campo objeto."""

from src.preprocess.clean_objeto import get_text_for_field, limpar_objeto


def test_limpar_objeto_remove_prefixos() -> None:
    raw = "Objeto: Pregão Eletrônico - Aquisição de seringas hospitalares"
    assert limpar_objeto(raw) == "Aquisição de seringas hospitalares"


def test_limpar_objeto_remove_orgao() -> None:
    raw = (
        "Aquisição de equipamentos para a SECRETARIA DE ESTADO DE SAÚDE - DF "
        "conforme edital"
    )
    orgao = "SECRETARIA DE ESTADO DE SAÚDE - DF"
    limpo = limpar_objeto(raw, orgao=orgao)
    assert "SECRETARIA DE ESTADO DE SAÚDE" not in limpo.upper()
    assert "Aquisição de equipamentos" in limpo


def test_limpar_objeto_remove_orgaos_csv_e_html() -> None:
    raw = "Serviços para SECRETARIA DE ESTADO DE SAÚDE - DF e hospital"
    limpo = limpar_objeto(
        raw,
        orgaos=[
            "SECRETARIA DE ESTADO DE SAÚDE - DF",
            "Secretaria de Estado de Saúde do Distrito Federal",
        ],
    )
    assert "SECRETARIA DE ESTADO DE SAÚDE" not in limpo.upper()
    assert "Serviços para" in limpo


def test_get_text_for_field_objeto_html_limpo() -> None:
    rec = {
        "objeto_html": "Objeto: Pregão Eletrônico - Compra de tintas",
        "orgao_csv": "COMPANHIA DE SANEAMENTO AMBIENTAL DO DF CAESB",
    }
    assert get_text_for_field(rec, "objeto_html_limpo") == "Compra de tintas"


def test_get_text_for_field_passthrough() -> None:
    rec = {"objeto_html": "texto bruto", "orgao_csv": "X"}
    assert get_text_for_field(rec, "objeto_html") == "texto bruto"
