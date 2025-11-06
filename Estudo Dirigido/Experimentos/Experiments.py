from Model import * 

def run_experiment(depth: int, dataset_path: str, data: pd.DataFrame):
    #pegar as informacoes e parsear os dados do dataset (por enquanto ta nulo)
    data = pd.read_csv(dataset_path)
    #criar a arvore
    tree = Tree(depth)
    #criar o modelo
    model = Model(depth, tree, data)
    #rodar modelo
    #coletar resultados e preparar o formato de output

def main():
    #setar a profundidade
    #obter os datasets e rodar para cada um os arquivos
    #chamar run_experiment para cada dataset
    pass

if __name__ == "__main__":
    main()