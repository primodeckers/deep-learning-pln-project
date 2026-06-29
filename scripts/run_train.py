"""Ponto de entrada para treino e avaliação dos modelos de PLN.  # Docstring do módulo: descreve o propósito do script

Exemplos (guia §10):  # Seção de exemplos de uso na linha de comando
    python scripts/run_train.py --task classification --model baseline  # Treina classificador baseline
    python scripts/run_train.py --task classification --model svm  # Treina classificador SVM
    python scripts/run_train.py --task classification --model bertimbau  # Treina BERTimbau
    python scripts/run_train.py --task classification --config configs/classification.yaml  # Usa arquivo YAML de config
"""

from __future__ import annotations  # Permite anotações de tipo adiantadas (forward references) sem aspas

import argparse  # Biblioteca para parsing de argumentos da linha de comando
import sys  # Acesso a variáveis e funções do interpretador Python (ex.: sys.path)
from pathlib import Path  # Classe orientada a objetos para manipular caminhos de arquivos

import yaml  # Biblioteca para ler e escrever arquivos YAML

ROOT = Path(__file__).resolve().parents[1]  # Caminho absoluto da raiz do projeto (pasta acima de scripts/)
if str(ROOT) not in sys.path:  # Verifica se a raiz já está no path de importação
    sys.path.insert(0, str(ROOT))  # Insere a raiz no início do sys.path para importar módulos de src/

import mlflow  # Biblioteca de rastreamento de experimentos de ML

from src.summarize.run_summarization import run_summarization  # Função que executa o pipeline de sumarização
from src.train.train_classification import train_classification  # Função que treina modelos de classificação
from src.utils.experiment_tracking import (  # Utilitários de integração com MLflow
    MLFLOW_EXPERIMENT,  # Nome padrão do experimento MLflow
    mlflow_tracking_uri,  # Função que monta a URI de tracking do MLflow
)

DEFAULT_CORPUS = ROOT / "data" / "processed" / "licitacoes_corpus.jsonl"  # Caminho padrão do corpus processado
DEFAULT_CONFIG = ROOT / "configs" / "classification.yaml"  # Caminho padrão do arquivo de configuração
EXPERIMENTS_DIR = ROOT / "experiments"  # Diretório onde ficam os runs/experimentos MLflow
MODELS_DIR = ROOT / "models"  # Diretório onde os modelos treinados são salvos
FIGURES_DIR = ROOT / "reports" / "figures"  # Diretório para gráficos e figuras de avaliação
PROCESSED_DIR = ROOT / "data" / "processed"  # Diretório de dados processados
SLIDES_DIR = ROOT / "reports" / "slides"  # Diretório de saída para slides/relatórios de sumarização


def build_parser() -> argparse.ArgumentParser:  # Cria e retorna o parser de argumentos CLI
    parser = argparse.ArgumentParser(  # Instancia o parser com descrição do programa
        description="Treina e avalia modelos de PLN sobre o corpus de licitações."  # Texto de ajuda exibido no --help
    )
    parser.add_argument(  # Define o argumento --task
        "--task",  # Nome do argumento: tipo de tarefa PLN
        choices=["classification", "summarization"],  # Valores permitidos
        default="classification",  # Valor padrão se não informado
    )
    parser.add_argument(  # Define o argumento --model
        "--model",  # Nome do argumento: modelo a usar
        default=None,  # Sem valor padrão; usa o definido no config YAML
        help="Sobrescreve o modelo definido no config (ex.: baseline, svm, bertimbau).",  # Texto de ajuda
    )
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)  # Caminho do arquivo YAML de configuração
    parser.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)  # Caminho do corpus JSONL de entrada
    parser.add_argument(  # Define o argumento --text-field
        "--text-field",  # Nome do argumento: campo de texto do JSON a usar
        default=None,  # Sem valor padrão; usa o definido no config
        help="Sobrescreve o campo de texto do config (ex.: texto, objeto_html).",  # Texto de ajuda
    )
    return parser  # Retorna o parser configurado


def load_config(path: Path) -> dict:  # Carrega configuração YAML de um arquivo e retorna dict
    if path.exists():  # Verifica se o arquivo de config existe
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}  # Lê UTF-8, parseia YAML; retorna {} se vazio
    return {}  # Retorna dict vazio se o arquivo não existir


def main() -> None:  # Função principal: orquestra treino de classificação ou sumarização
    mlflow.set_tracking_uri(mlflow_tracking_uri(EXPERIMENTS_DIR))  # Configura onde o MLflow grava os runs
    mlflow.set_experiment(MLFLOW_EXPERIMENT)  # Define o experimento ativo no MLflow
    mlflow.autolog()  # Ativa log automático de métricas/parâmetros dos frameworks suportados

    args = build_parser().parse_args()  # Constrói o parser e interpreta os argumentos da linha de comando

    if args.task == "summarization":  # Ramo para tarefa de sumarização de textos
        model = args.model or "extractive"  # Usa modelo informado ou padrão extractive
        if model != "extractive":  # Só sumarização extrativa está implementada
            raise NotImplementedError(  # Interrompe com erro claro para modelos não suportados
                f"Sumarização '{model}' (abstrativo mT5/LLM) ainda não implementada "  # Mensagem parte 1
                "— ver guia §7.2. Use --model extractive."  # Mensagem parte 2 com orientação
            )
        run_summarization(  # Executa pipeline de sumarização extrativa
            corpus_path=args.corpus,  # Corpus de entrada
            processed_dir=PROCESSED_DIR,  # Pasta de dados processados
            slides_dir=SLIDES_DIR,  # Pasta de saída de slides/relatórios
            experiments_dir=EXPERIMENTS_DIR,  # Pasta de tracking MLflow
        )
        return  # Encerra após sumarização (não treina classificação)

    config = load_config(args.config)  # Carrega hiperparâmetros e opções do YAML
    if args.model:  # Se --model foi passado na CLI
        config["model"] = args.model  # Sobrescreve o modelo do config
    if args.text_field:  # Se --text-field foi passado na CLI
        config["text_field"] = args.text_field  # Sobrescreve o campo de texto do config
    config.setdefault("model", "baseline")  # Garante modelo baseline se nenhum foi definido

    train_classification(  # Executa treino e avaliação do classificador
        corpus_path=args.corpus,  # Corpus JSONL de licitações
        config=config,  # Dict com modelo, text_field e demais opções
        experiments_dir=EXPERIMENTS_DIR,  # Onde registrar runs MLflow
        models_dir=MODELS_DIR,  # Onde salvar artefatos do modelo (.joblib, etc.)
        figures_dir=FIGURES_DIR,  # Onde salvar matrizes de confusão e gráficos
    )


if __name__ == "__main__":  # Executa main() apenas quando o script é chamado diretamente
    main()  # Ponto de entrada do programa
