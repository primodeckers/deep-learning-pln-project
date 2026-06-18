"""Testes de carregamento do corpus e split estratificado."""

from tests.conftest import CORPUS_PATH, FIXTURE_CORPUS, requires_corpus

from src.preprocess.dataset import load_records, make_dataset


def test_load_records_adds_area_label() -> None:
    records = load_records(FIXTURE_CORPUS)
    assert len(records) == 30
    areas = {rec["area"] for rec in records}
    assert "Saude" in areas
    assert "Administracao/Outros" in areas


def test_make_dataset_splits_are_disjoint() -> None:
    dataset = make_dataset(
        FIXTURE_CORPUS,
        text_field="objeto_html",
        seed=42,
        val_size=0.2,
        test_size=0.2,
    )
    train_ids = set(dataset.train.ids)
    val_ids = set(dataset.val.ids)
    test_ids = set(dataset.test.ids)

    assert len(dataset.train) + len(dataset.val) + len(dataset.test) == 30
    assert train_ids.isdisjoint(val_ids)
    assert train_ids.isdisjoint(test_ids)
    assert val_ids.isdisjoint(test_ids)


def test_make_dataset_same_seed_is_reproducible() -> None:
    first = make_dataset(
        FIXTURE_CORPUS,
        text_field="objeto_html",
        seed=7,
        val_size=0.2,
        test_size=0.2,
    )
    second = make_dataset(
        FIXTURE_CORPUS,
        text_field="objeto_html",
        seed=7,
        val_size=0.2,
        test_size=0.2,
    )
    assert first.train.ids == second.train.ids
    assert first.val.ids == second.val.ids
    assert first.test.ids == second.test.ids


def test_make_dataset_objeto_html_limpo() -> None:
    dataset = make_dataset(
        FIXTURE_CORPUS,
        text_field="objeto_html_limpo",
        seed=42,
        val_size=0.2,
        test_size=0.2,
    )
    assert len(dataset.train.texts) > 0
    assert all(isinstance(t, str) for t in dataset.train.texts)


@requires_corpus
def test_real_corpus_has_expected_scale() -> None:
    records = load_records(CORPUS_PATH)
    assert len(records) >= 100
