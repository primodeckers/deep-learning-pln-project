"""Testes da taxonomia de 9 setores."""

from src.preprocess.labels_setores import (
    SETOR_INDETERMINADO,
    SETORES,
    SETORES_COM_INDETERMINADO,
    setor_for_objeto,
    setor_label_for_objeto,
    setor_label_with_org_fallback,
)


def test_setor_saude() -> None:
    assert setor_for_objeto("Aquisição de medicamentos hospitalares") == "Saude"


def test_setor_ti() -> None:
    assert setor_for_objeto("Licença de software e hospedagem") == "TI/Administracao"


def test_setor_prioridade_saude_antes_ti() -> None:
    assert setor_for_objeto("Medicamentos e sistema informatizado") == "Saude"


def test_sem_sinal() -> None:
    assert setor_for_objeto("Material diverso") is None


def test_nove_setores() -> None:
    assert len(SETORES) == 9


def test_indeterminado_fallback() -> None:
    assert setor_label_for_objeto("Material diverso", unlabeled=SETOR_INDETERMINADO) == SETOR_INDETERMINADO
    assert len(SETORES_COM_INDETERMINADO) == 10


def test_org_fallback() -> None:
    label, src = setor_label_with_org_fallback(
        "credenciamento conforme edital",
        "FUNDACAO NACIONAL DE SAUDE",
    )
    assert label == "Saude"
    assert src == "orgao"

    label, src = setor_label_with_org_fallback(
        "credenciamento conforme edital",
        "MINISTERIO DE PORTOS E AEROPORTOS",
    )
    assert label == SETOR_INDETERMINADO
    assert src == "indeterminado"

    label, src = setor_label_with_org_fallback(
        "Aquisicao de medicamentos hospitalares",
        "QUALQUER ORGAO",
    )
    assert label == "Saude"
    assert src == "objeto"
