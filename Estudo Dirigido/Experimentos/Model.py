import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd
from Tree import Tree

class Model:

    def __init__(self, depth: int, tree: Tree, data: pd.DataFrame):
        self.depth = depth
        self.tree = tree
        self.model = gp.Model("FlowAghaei")
        self.label = "target" # nome da coluna da previsão da categoria no dataset
        self.values = data.index 
        self.features = self.data.drop(self.label, axis=1).columns # nomes das colunas de features (exclui a coluna target)
        self.classes = data[self.label].unique() #valores únicos da coluna target (classes)

        ## Variáveis do modelo ##

        '''
            b_(n,f) -> se a feature f é usada no nó de branch n.
            gurobi ja faz o produto cartesiano com os dois vetores passados como parametro
            para mapear os indices.
        '''
        self.b = self.model.addVars(self.tree.nodes, self.features, vtype=GRB.BINARY, name="b")  
        #w_(l,c) -> se a folha l prediz a classe c.
        self.w = self.model.addVars(self.tree.leaves, self.classes, vtype=GRB.BINARY, name="w")        
        #z_(i,n) -> quantidade de fluxo do valor i que passa pelo no n.
        self.z = self.model.addVars(self.values, self.tree.nodes + self.tree.leaves, vtype=GRB.BINARY, name="z")
        #TODO: adicionar variaveis de fluxo z faltantes

        ## Restrições do modelo ##


        ## Função objetivo ##

