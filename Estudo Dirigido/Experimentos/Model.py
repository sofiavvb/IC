#!/usr/bin/env python3
import gurobipy as gp
from gurobipy import GRB
import pandas as pd
from Tree import Tree

class Model:

    def __init__(self, depth: int, tree: Tree, data: pd.DataFrame):
        self.depth = depth
        self.tree = tree
        self.model = gp.Model("FlowAghaei")
        self.label = "target" #nome da coluna da previsão da categoria no dataset
        self.values = data.index 
        self.features = data.drop(self.label, axis=1).columns #nomes das colunas de features (exclui a coluna target)
        self.classes = data[self.label].unique() #valores únicos da coluna target (classes)
        self.model.setParam("Threads", 1)  # limitar a 1 thread


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
        #z_(n, t) -> quantidade de fluxo para o dado i que passa pela aresta da folha n para o sorvedouro t
        self.z_t = self.model.addVars(self.values, self.tree.leaves, vtype=GRB.BINARY, name="z_t")

        ## Restrições do modelo ##

        #cada nó de branch deve usar exatamente uma feature para branching
        #sum(b_(n,f) para f em features) == 1  para todo n em nós (1b)
        for node in self.tree.nodes:
            self.model.addConstr(gp.quicksum(self.b[node, f] for f in self.features) == 1)

        #conservação de fluxo
        #z_(i,n) ==  z_(i, left(n)) + z_(i, right(n)) para todo nó n e todo dado i (1c)
        for i in self.values:
            for node in self.tree.nodes:
                self.model.addConstr(self.z[i, node] == self.z[i, self.tree.left(node)] + self.z[i, self.tree.right(node)])
        
        #fluxo para o sorvedouro
        #z_(i,l) == z_(i, t) para toda folha l e todo dado i (1d)
        for i in self.values:
            for leaf in self.tree.leaves:
                self.model.addConstr(self.z[i, leaf] == self.z_t[i, leaf])

        #no maximo 1 unidade de fluxo por dado i pode entrar na arvore pela fonte
        #z[i, 1] <= 1 para todo dado i (1e)
        self.model.addConstrs(self.z[i, 1] <= 1 for i in self.values)

        #se o valor da feature pro dado i eh 0, vai pra esquerda
        #z[i,l(n)] <= sum(b[n,f] para f em features se x[i,f]=0) (1f)
        for i in self.values:
            self.model.addConstrs((self.z[i, self.tree.left(node)] <= gp.quicksum(self.b[node, f]
                                for f in self.features if data.at[i, f] == 0)) for node in self.tree.nodes)
            
        #se o valor da feature pro dado i eh 1, vai pra direita
        #z[i,r(n)] <= sum(b[n,f] para f em features se x[i,f]=1) (1g)
        for i in self.values:
            self.model.addConstrs((self.z[i, self.tree.right(node)] <= gp.quicksum(self.b[node, f]
                                for f in self.features if data.at[i, f] == 1)) for node in self.tree.nodes)

        #os dados cujo fluxo chega na folha l devem estar corretamente classificados
        #z_t[i,l] <= w[l, c] onde c é a classe do dado i (1h)
        for i in self.values:
            self.model.addConstrs(self.z_t[i, leaf] <= self.w[leaf, data.at[i, self.label]] for leaf in self.tree.leaves)

        #cada folha eh designada a uma classe apenas
        #sum(w[l,c] para c em classes) == 1 para toda folha l (1i)
        for leaf in self.tree.leaves:
            self.model.addConstr(gp.quicksum(self.w[leaf, c] for c in self.classes) == 1)

        ## Função objetivo ##

        #maximizar a quantidade de dados corretamente classificados
        obj = gp.quicksum(self.z_t[i, leaf] for i in self.values for leaf in self.tree.leaves)
        self.model.setObjective(obj, GRB.MAXIMIZE)
