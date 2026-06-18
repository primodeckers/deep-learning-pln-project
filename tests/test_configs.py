"""Testes de carregamento das configs YAML."""

import yaml
from tests.conftest import ROOT


def test_classification_config_has_required_keys() -> None:
    path = ROOT / "configs" / "classification.yaml"
    cfg = yaml.safe_load(path.read_text(encoding="utf-8"))

    assert cfg["task"] == "classification"
    assert cfg["text_field"] == "objeto_html"
    assert cfg["seed"] == 42
    assert "params" in cfg
    assert cfg["params"]["class_weight"] == "balanced"


def test_classification_config_split_sizes_sum_below_one() -> None:
    path = ROOT / "configs" / "classification.yaml"
    cfg = yaml.safe_load(path.read_text(encoding="utf-8"))

    assert cfg["val_size"] + cfg["test_size"] < 1.0
