from Model import * 
import os
import time
import argparse

def run_experiment(depth: int, dataset_path: str, time_limit: int, log_path: str):
    #pegar as informacoes e parsear os dados do dataset (por enquanto ta nulo)
    data = pd.read_csv(dataset_path)
    #criar a arvore
    tree = Tree(depth)
    #criar o modelo
    flowAghaei = Model(depth, tree, data, time_limit)
    flowAghaei.model.setParam('LogFile', log_path)
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--depth", type=int, required=True)
    parser.add_argument("--dataset", type=str, required=True)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--logdir", type=str, required=True)
    args = parser.parse_args()

    os.makedirs(args.logdir, exist_ok=True)
    dataset_name = os.path.basename(args.dataset)
    log_path = os.path.join(args.logdir, f"{dataset_name}.log")

    result = run_experiment(args.depth, args.dataset, args.timeout, log_path)
    print(result)

if __name__ == "__main__":
    main()