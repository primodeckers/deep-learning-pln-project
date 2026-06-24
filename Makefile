.PHONY: install install-dev lint lint-fix typecheck test train-baseline train-svm train-summarize mlflow-ui

install:
	python -m pip install -U pip
	python -m pip install -e .

install-dev:
	python -m pip install -U pip
	python -m pip install -e ".[dev]"

lint:
	ruff check src tests
	ruff format --check src tests

lint-fix:
	ruff check --fix src tests
	ruff format src tests

typecheck:
	mypy

test:
	pytest

train-baseline:
	python scripts/run_train.py --task classification --model baseline

train-svm:
	python scripts/run_train.py --task classification --model svm

train-bert:
	python scripts/run_train.py --task classification --model bertimbau

train-summarize:
	python scripts/run_train.py --task summarization --model extractive

mlflow-ui:
	mlflow ui --backend-store-uri sqlite:///experiments/mlflow.db
