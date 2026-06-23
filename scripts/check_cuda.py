"""Verifica se PyTorch enxerga GPU — rodar antes de treinar BERTimbau."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main() -> None:
    try:
        import torch
    except ImportError:
        print("PyTorch não instalado. Rode: pip install -e '.[bert]'")
        raise SystemExit(1) from None

    print(f"PyTorch {torch.__version__}")
    if torch.cuda.is_available():
        idx = torch.cuda.current_device()
        name = torch.cuda.get_device_name(idx)
        mem_gb = torch.cuda.get_device_properties(idx).total_memory / (1024**3)
        print(f"CUDA: sim — GPU {idx}: {name} ({mem_gb:.1f} GB)")
        print("\nPode treinar BERTimbau com:")
        print("  python scripts/run_train.py --config configs/classification_bert_gpu.yaml")
    else:
        print("CUDA: não — treino BERTimbau usará CPU (muito lento).")
        print("Baseline TF-IDF funciona bem em CPU:")
        print("  python scripts/run_train.py --task classification --model baseline")
        print("\nVer docs/GPU-EQUIPE.md para o fluxo do grupo.")


if __name__ == "__main__":
    main()
