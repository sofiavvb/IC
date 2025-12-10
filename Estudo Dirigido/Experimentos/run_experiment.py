#!/usr/bin/env -S uv run --script
#
# /// script
# dependencies = [
#   "gurobipy==12.0.0",
#   "pandas",
# ]
# ///
from Model import * 
import os
import time
import argparse

def run_experiment(depth: int, dataset_path: str):
    #pegar as informacoes e parsear os dados do dataset (por enquanto ta nulo)
    data = pd.read_csv(dataset_path)
    #criar a arvore
    tree = Tree(depth)
    #criar o modelo
    flowAghaei = Model(depth, tree, data)
    #rodar modelo
    start = time.time()
    flowAghaei.model.update()
    flowAghaei.model.optimize()
    end = time.time()

    #coletar resultados e preparar o formato de output
    print("--------------------------------------------------")
    print(f"Tempo de execução: {end - start} segundos")
    print(f"Profundidade {depth} encerrada. Obj = {flowAghaei.model.getAttr('ObjVal')}")
    print(f"Pontos misclassificados: {len(data) - flowAghaei.model.getAttr('Objval')}")
    print("--------------------------------------------------")

def main():
    parser = argparse.ArgumentParser()

    # positional argument (dataset path)
    parser.add_argument("-i", "--input", type=str, required=True, help="Path to dataset CSV")

    # optional parameters
    parser.add_argument("--depth", type=int, required=True)

    args = parser.parse_args()

    run_experiment(args.depth, args.input)

if __name__ == "__main__":
    main()