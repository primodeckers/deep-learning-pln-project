"""Métricas de classificação multiclasse (guia §6.2).

Calcula F1 macro (métrica primária de seleção de modelo), F1 por classe,
accuracy e matriz de confusão. Opcionalmente salva a matriz como figura PNG.
"""

from __future__ import annotations

from pathlib import Path

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)


def compute_metrics(
    y_true: list[str],
    y_pred: list[str],
    labels: list[str],
) -> dict:
    """Devolve um dicionário serializável com as métricas do conjunto."""
    report = classification_report(
        y_true,
        y_pred,
        labels=labels,
        output_dict=True,
        zero_division=0,
    )
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "f1_macro": f1_score(y_true, y_pred, labels=labels, average="macro", zero_division=0),
        "f1_weighted": f1_score(y_true, y_pred, labels=labels, average="weighted", zero_division=0),
        "per_class": {
            label: {
                "precision": report[label]["precision"],
                "recall": report[label]["recall"],
                "f1": report[label]["f1-score"],
                "support": int(report[label]["support"]),
            }
            for label in labels
        },
        "labels": labels,
        "confusion_matrix": cm.tolist(),
    }


def format_metrics(metrics: dict) -> str:
    """Resumo legível das métricas para imprimir no terminal."""
    lines = [
        f"  accuracy   : {metrics['accuracy']:.3f}",
        f"  F1 macro   : {metrics['f1_macro']:.3f}",
        f"  F1 ponderado: {metrics['f1_weighted']:.3f}",
        "  F1 por classe:",
    ]
    for label, m in metrics["per_class"].items():
        lines.append(f"    {label:<24} F1={m['f1']:.3f}  (n={m['support']})")
    return "\n".join(lines)


def save_confusion_matrix(metrics: dict, output_path: Path, title: str) -> None:
    """Salva a matriz de confusão como figura PNG (best-effort)."""
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return  # matplotlib é opcional; sem ele, apenas pulamos a figura.

    labels = metrics["labels"]
    cm = metrics["confusion_matrix"]
    fig, ax = plt.subplots(figsize=(7, 6))
    im = ax.imshow(cm, cmap="Blues")
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=8)
    ax.set_yticklabels(labels, fontsize=8)
    ax.set_xlabel("Predito")
    ax.set_ylabel("Verdadeiro")
    ax.set_title(title)
    for i in range(len(labels)):
        for j in range(len(labels)):
            ax.text(j, i, cm[i][j], ha="center", va="center", fontsize=8,
                    color="white" if cm[i][j] > (max(map(max, cm)) / 2) else "black")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=120)
    plt.close(fig)
