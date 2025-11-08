from Model import * 
import sys
import time
import argparse

def run_experiment(depth: int, dataset_path: str, time_limit: int):
    #pegar as informacoes e parsear os dados do dataset (por enquanto ta nulo)
    data = pd.read_csv(dataset_path)
    #criar a arvore
    tree = Tree(depth)
    #criar o modelo
    flowAghaei = Model(depth, tree, data, time_limit)
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
    #obter os datasets e rodar para cada um os arquivos
    #chamar run_experiment para cada dataset
    parser = argparse.ArgumentParser(description="Run Aghaei flow-based experiment.")
    parser.add_argument("--dataset", type=str, required=True, help="Path to dataset CSV file")
    parser.add_argument("--depth", type=int, default=2, help="Tree depth")
    parser.add_argument("--timelimit", type=int, default=300, help="Time limit for solver (seconds)")
    args = parser.parse_args()

    run_experiment(args.depth, args.dataset, args.timelimit)

if __name__ == "__main__":
    main()