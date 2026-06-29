"""Fine-tuning BERTimbau para classificação por macroárea (Fase 2).

Interface compatível com o orquestrador em ``train_classification.py``
(``fit`` / ``predict``). Requer dependências opcionais::

    pip install -e ".[bert]"

Hiperparâmetros padrão: ``configs/classification.yaml`` (bloco bertimbau).
"""

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

from src.preprocess.labels import AREAS

_LABELS_FILE = "label_config.json"


def _require_bert_deps() -> tuple[Any, Any, Any, Any, Any, Any]:
    try:
        import torch
        from torch.utils.data import Dataset as TorchDataset
        from transformers import (
            AutoModelForSequenceClassification,
            AutoTokenizer,
            EarlyStoppingCallback,
            Trainer,
            TrainingArguments,
        )
    except ImportError as exc:
        raise ImportError(
            "BERTimbau requer torch e transformers. Instale com: "
            'pip install -e ".[bert]"'
        ) from exc
    return (
        torch,
        TorchDataset,
        AutoModelForSequenceClassification,
        AutoTokenizer,
        EarlyStoppingCallback,
        Trainer,
        TrainingArguments,
    )


@dataclass
class BertTextClassifier:
    """Classificador de texto com BERTimbau (fine-tuning via Hugging Face Trainer)."""

    model_name: str
    max_length: int
    batch_size: int
    learning_rate: float
    epochs: int
    early_stopping_patience: int
    seed: int
    label_list: list[str]
    model: Any = None
    tokenizer: Any = None

    def __post_init__(self) -> None:
        self.label2id = {label: i for i, label in enumerate(self.label_list)}
        self.id2label = {i: label for label, i in self.label2id.items()}

    def fit(
        self,
        texts: list[str],
        labels: list[str],
        *,
        val_texts: list[str] | None = None,
        val_labels: list[str] | None = None,
        output_dir: Path | None = None,
    ) -> BertTextClassifier:
        """Fine-tune no treino; usa val para early stopping quando fornecido."""
        (
            torch,
            TorchDataset,
            AutoModelForSequenceClassification,
            AutoTokenizer,
            EarlyStoppingCallback,
            Trainer,
            TrainingArguments,
        ) = _require_bert_deps()

        if val_texts is None or val_labels is None:
            raise ValueError("BERTimbau exige val_texts e val_labels para early stopping.")

        train_dir = Path(output_dir) if output_dir else Path(".bert_train_cache")
        train_dir.mkdir(parents=True, exist_ok=True)

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.model_name,
            num_labels=len(self.label_list),
            id2label=self.id2label,
            label2id=self.label2id,
        )

        use_cuda = torch.cuda.is_available()
        device = torch.device("cuda" if use_cuda else "cpu")
        if use_cuda:
            self.model.to(device)
        print(
            f"BERTimbau: dispositivo={device}"
            + (f" ({torch.cuda.get_device_name(0)})" if use_cuda else " (CPU — lento)")
        )

        class _EncDataset(TorchDataset):
            def __init__(
                self,
                xs: list[str],
                ys: list[str] | None,
                tokenizer: Any,
                max_length: int,
                label2id: dict[str, int],
            ) -> None:
                self.xs = xs
                self.ys = ys
                self.tokenizer = tokenizer
                self.max_length = max_length
                self.label2id = label2id

            def __len__(self) -> int:
                return len(self.xs)

            def __getitem__(self, idx: int) -> dict[str, Any]:
                enc = self.tokenizer(
                    self.xs[idx],
                    truncation=True,
                    padding="max_length",
                    max_length=self.max_length,
                    return_tensors="pt",
                )
                item = {k: v.squeeze(0) for k, v in enc.items()}
                if self.ys is not None:
                    item["labels"] = torch.tensor(
                        self.label2id[self.ys[idx]], dtype=torch.long
                    )
                return item

        train_ds = _EncDataset(
            texts, labels, self.tokenizer, self.max_length, self.label2id
        )
        val_ds = _EncDataset(
            val_texts, val_labels, self.tokenizer, self.max_length, self.label2id
        )

        def _compute_metrics(eval_pred: tuple[np.ndarray, np.ndarray]) -> dict[str, float]:
            logits, y_true = eval_pred
            preds = np.argmax(logits, axis=-1)
            from sklearn.metrics import f1_score

            macro = f1_score(
                y_true,
                preds,
                average="macro",
                zero_division=0,
                labels=list(range(len(self.label_list))),
            )
            return {"f1_macro": float(macro)}

        args = TrainingArguments(
            output_dir=str(train_dir),
            learning_rate=self.learning_rate,
            per_device_train_batch_size=self.batch_size,
            per_device_eval_batch_size=self.batch_size,
            num_train_epochs=self.epochs,
            eval_strategy="epoch",
            save_strategy="epoch",
            load_best_model_at_end=True,
            metric_for_best_model="f1_macro",
            greater_is_better=True,
            logging_steps=20,
            save_total_limit=1,
            seed=self.seed,
            report_to="none",
            weight_decay=0.01,
            fp16=use_cuda,
            dataloader_pin_memory=use_cuda,
        )

        callbacks = []
        if self.early_stopping_patience > 0:
            callbacks.append(
                EarlyStoppingCallback(early_stopping_patience=self.early_stopping_patience)
            )

        trainer = Trainer(
            model=self.model,
            args=args,
            train_dataset=train_ds,
            eval_dataset=val_ds,
            compute_metrics=_compute_metrics,
            callbacks=callbacks,
        )
        trainer.train()
        self.model = trainer.model
        return self

    def predict(self, texts: list[str]) -> list[str]:
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("Modelo não treinado — chame fit() antes de predict().")

        torch, TorchDataset, *_ = _require_bert_deps()

        class _InferDs(TorchDataset):
            def __init__(
                self,
                xs: list[str],
                tokenizer: Any,
                max_length: int,
            ) -> None:
                self.xs = xs
                self.tokenizer = tokenizer
                self.max_length = max_length

            def __len__(self) -> int:
                return len(self.xs)

            def __getitem__(self, idx: int) -> dict[str, Any]:
                enc = self.tokenizer(
                    self.xs[idx],
                    truncation=True,
                    padding="max_length",
                    max_length=self.max_length,
                    return_tensors="pt",
                )
                return {k: v.squeeze(0) for k, v in enc.items()}

        infer_ds = _InferDs(texts, self.tokenizer, self.max_length)
        loader = torch.utils.data.DataLoader(
            infer_ds, batch_size=self.batch_size, shuffle=False
        )

        self.model.eval()
        all_preds: list[int] = []
        device = next(self.model.parameters()).device
        with torch.no_grad():
            for batch in loader:
                batch = {k: v.to(device) for k, v in batch.items()}
                logits = self.model(**batch).logits
                all_preds.extend(logits.argmax(dim=-1).cpu().tolist())

        return [self.id2label[i] for i in all_preds]

    def save(self, path: Path) -> None:
        """Persiste tokenizer, pesos e mapeamento de labels em ``path/``."""
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("Nada para salvar — modelo não treinado.")

        path = Path(path)
        if path.exists():
            shutil.rmtree(path)
        path.mkdir(parents=True, exist_ok=True)

        self.model.save_pretrained(path)
        self.tokenizer.save_pretrained(path)
        meta = {
            "model_name": self.model_name,
            "max_length": self.max_length,
            "batch_size": self.batch_size,
            "learning_rate": self.learning_rate,
            "epochs": self.epochs,
            "early_stopping_patience": self.early_stopping_patience,
            "seed": self.seed,
            "label_list": self.label_list,
            "label2id": self.label2id,
            "id2label": {str(k): v for k, v in self.id2label.items()},
        }
        (path / _LABELS_FILE).write_text(
            json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    @classmethod
    def load(cls, path: Path) -> BertTextClassifier:
        """Carrega um classificador salvo com ``save()``."""
        (
            _torch,
            _TorchDataset,
            AutoModelForSequenceClassification,
            AutoTokenizer,
            *_,
        ) = _require_bert_deps()

        path = Path(path)
        meta = json.loads((path / _LABELS_FILE).read_text(encoding="utf-8"))
        obj = cls(
            model_name=meta["model_name"],
            max_length=meta["max_length"],
            batch_size=meta["batch_size"],
            learning_rate=meta["learning_rate"],
            epochs=meta["epochs"],
            early_stopping_patience=meta["early_stopping_patience"],
            seed=meta["seed"],
            label_list=meta["label_list"],
        )
        obj.tokenizer = AutoTokenizer.from_pretrained(path)
        obj.model = AutoModelForSequenceClassification.from_pretrained(path)
        return obj


def build_bert_classifier(
    label_list: list[str] | None = None,
    model_name: str = "neuralmind/bert-base-portuguese-cased",
    max_length: int = 512,
    batch_size: int = 16,
    learning_rate: float = 2.0e-5,
    epochs: int = 4,
    early_stopping_patience: int = 2,
    seed: int = 42,
) -> BertTextClassifier:
    """Monta o classificador BERTimbau (não treinado)."""
    return BertTextClassifier(
        model_name=model_name,
        max_length=max_length,
        batch_size=batch_size,
        learning_rate=learning_rate,
        epochs=epochs,
        early_stopping_patience=early_stopping_patience,
        seed=seed,
        label_list=list(label_list or AREAS),
    )
