import numpy as np
import data_structures as ds
from enum import Enum
from functions import *
import os

class Constants(Enum):
    BFS = "BFS"
    DFS = "DFS"
    MATRIX = 2
    VECTOR = 3


class Graph:
    def __init__(self, representationType, path):
        self.size = None
        self.edgeAmount = 0
        self.representation = Constants.BFS
        self.representationType = representationType
        self.degreeVec = None
        self.create_graph(path)
        self.mark = np.zeros(self.size, dtype=int)
        
    
    def create_graph(self, path):
        source = graph_read_source(path)
        match(self.representationType):
            case Constants.MATRIX:
                self.create_adjacency_matrix(source)
            case Constants.VECTOR:
                self.create_adjecency_vector(source)


    def create_adjecency_vector(self, graph_source):
        self.size = next(graph_source)

        self.representation = np.empty(self.size, dtype=object)
        self.degreeVec = np.zeros(self.size, dtype=int)

        for i in range(self.size):
            self.representation[i] = np.array([], dtype=int)

        for VI, VJ in graph_source:
            vi = VI - 1
            vj = VJ - 1
            self.representation[vi] = np.append(self.representation[vi], VJ)
            self.representation[vj] = np.append(self.representation[vj], VI)
            self.degreeVec[vi] += 1
            self.degreeVec[vj] += 1
            self.edgeAmount += 1

    def create_adjacency_matrix(self, graph_source):
        self.size = next(graph_source)
        self.representation = np.zeros((self.size, self.size), dtype=int)
        self.degreeVec = np.zeros(self.size, dtype=int)
        for VI, VJ in graph_source:
            vi = VI - 1
            vj = VJ - 1
            self.representation[vi][vj] = 1
            self.representation[vj][vi] = 1
            self.degreeVec[vi] += 1
            self.degreeVec[vj] += 1
            self.edgeAmount += 1

    def get_min_degree(self):
        return np.min(self.degreeVec)

    def get_max_degree(self):
        return np.max(self.degreeVec)

    def get_mean_degree(self):
        return np.mean(self.degreeVec)

    def get_median_degree(self):
        return np.median(self.degreeVec)
    
    def mark_vertice(self, vertice, value = 1):
        self.mark[vertice - 1] = value

    def is_marked_to(self, vertice, value = 1):
        return self.mark[vertice - 1] == value
    
    def index_to_vertice(self, index):
        return index + 1
    
    def vertice_to_index(self, vertice):
        return vertice - 1


    def graph_export_stats(self, file_name):
        with open(file_name, 'w') as file:
            file.write("Graph Statistics\n\n")
            file.write(f"Number of vertices:     {self.size}\n")
            file.write(f"Number of edges:        {self.edgeAmount}\n")
            file.write(f"Minimum degree:         {self.get_min_degree()}\n")
            file.write(f"Maximum degree:         {self.get_max_degree()}\n")
            file.write(f"Mean degree:            {self.get_mean_degree():.2f}\n")
            file.write(f"Median degree:          {self.get_median_degree():.2f}\n")

            
            components_list = self.get_diameter(False, True)
            components_Amount = len(components_list)
            file.write(f"Components Amount:          {components_Amount}\n\n")
            file.write("Connected Components:\n\n")
            for index, component in enumerate(components_list):
                file.write(f"Component number:       {index + 1}\n")
                file.write(f"Number of vertices:     {component.size}\n")
                file.write(f"List of edges:                          \n")
                for edge in component.edges:
                    file.write(f"-------------:      {edge}\n")




    def BFS_tree(self, root, give_subgraph = False, give_gen_tree = True):
        self.mark[:] = 0  # Desmarca os vértices
        queue = Queue()  # Fila para BFS
        gen_tree = Queue()  # Armazenar a árvore geradora
        level = [None] * self.size 
        parent = [None] * self.size
        level[root - 1] = 0
        queue.enqueue(root) #Insere root na fila
        self.mark_vertice(root) # Marca root
        edges_list = [] #Lista de conjuntos de arestas (para exportar subgrafo)
        gen_tree.enqueue(root, 0, None)
        while not queue.is_empty():
            V = queue.dequeue()  # Pega o próximo vértice da fila
            v = self.vertice_to_index(V)

            # Caso seja matriz de adjacência
            if self.representationType == Constants.MATRIX:
                for w in range(self.size):
                    if self.representation[v][w] == 1:
                        W = self.index_to_vertice(w)
                        if {W,V} not in edges_list: edges_list += [{W,V}]
                        if self.is_marked_to(W, 0):  # Se W não foi marcado
                            self.mark_vertice(W)
                            queue.enqueue(W)
                            level[w] = level[v] + 1
                            parent[w] = V
                            gen_tree.enqueue(W, level[w], parent[w])
            
            # Caso seja vetor de adjacência
            else:
                for W in self.representation[v]:
                    w = self.vertice_to_index(W)
                    if {W,V} not in edges_list: edges_list += [{W,V}]
                    if self.is_marked_to(W, 0):  # Se W não foi marcado
                        self.mark_vertice(W)
                        queue.enqueue(W)
                        level[w] = level[v] + 1
                        parent[w] = V
                        gen_tree.enqueue(W, level[w], parent[w])

        # Caso give_subgraph == True, ele irá retornar um node com as informações
        # necessárias para immprimir esse subgrafo
        vertices_pool = set()
        for i in edges_list:
            vertices_pool.update(i)
        BFS_vertices = len(vertices_pool)
        edges_string_list = []
        for i in edges_list:
            edges_string_list += [" ".join(map(str, i))]
        if (give_subgraph and not give_gen_tree):
            return SubgraphNode(BFS_vertices, edges_string_list)
        elif (give_gen_tree and not give_subgraph): return gen_tree
        else: return gen_tree, SubgraphNode(BFS_vertices, edges_string_list)
    
    def DFS_tree(self, root):
        self.mark[:] = 0 #Desmarcar vertices
        stack = Stack() #Definir Pilha P
        parent = [None] * self.size #Definir lista Parent
        level = [None] * self.size #Definir lista level
        stack.push(root) #inserir root em stack
        level[root - 1] = 0
        gen_tree = Queue()
        while (stack.is_empty() == False):
            U = stack.pop()
            if (self.is_marked_to(U,0)):
                self.mark_vertice(U)
                u = self.vertice_to_index(U)
                gen_tree.enqueue(U, level[u], parent[u])

                #Caso seja matriz de adjacência
                if (self.representationType == Constants.MATRIX):
                    for v in range(self.size):
                        if (self.representation[u][v] == 1):
                            V = self.index_to_vertice(v)
                            level[v] = level[u] + 1
                            parent[v] = U
                            stack.push(V)
                #Caso seja vetor de adjacência
                else:
                    for V in self.representation[u]:
                        v = self.vertice_to_index(V)
                        level[v] = level[u] + 1
                        parent[v] = U
                        stack.push(V)
        return gen_tree
        
    def export_tree(self, gen_tree, search_type):
        root = gen_tree.peek()
        filename = f"{search_type}_root_{root}.txt"
        
        # Abrir o arquivo para escrita
        with open(filename, 'w') as file:
            # Cabeçalho
            file.write(f"Árvore Gerada pela {search_type} com {root} como root\n")
            file.write(f"{'Vertice':<10} {'Nivel':<10} {'Pai':<10}\n")
            file.write(f"{'-------':<10} {'-----':<10} {'----':<10}\n")
            
            # Processar o primeiro nó (raiz)
            root_node = gen_tree.dequeue(True)
            data, level, parent = root_node.data, root_node.level, root_node.parent
            file.write(f"{data:<10} {level:<10} {'/':<10}\n")  # Raiz não tem pai
            
            # Processar o restante da árvore geradora
            while not gen_tree.is_empty():
                new_node = gen_tree.dequeue(True)
                data, level, parent = new_node.data, new_node.level, new_node.parent
                file.write(f"{data:<10} {level:<10} {parent:<10}\n")

        print(f"Árvore gerada exportada para {filename}")

    def get_distance_Vi_Vj(self, VI, VJ):
        VI_tree = self.BFS_tree(VI)
        pointer = VI_tree.dequeue(True)
        while (pointer.data != VJ):
            if (VI_tree.is_empty()):
                raise Exception
            pointer = VI_tree.dequeue(True)
        return pointer.level

    def get_diameter(self, give_diameter = True, give_subgraph = False):
        current_diameter = 0
        discovered_vec = np.zeros(self.size, dtype=int)
        components_list = []
        
        for index in range(len(discovered_vec)):
            if discovered_vec[index] == 0:
                vertice = index + 1  
                
                # Primeira BFS a partir do vértice atual
                index_tree, subgraph = self.BFS_tree(vertice, True, True)
                components_list += [subgraph]
                


                index_diameter = 0
                farthest = vertice 
                
                # Encontrar o vértice mais distante na primeira BFS
                while not index_tree.is_empty():
                    node = index_tree.dequeue(True)  
                    discovered_vec[node.data - 1] = 1  
                    if node.level > index_diameter:  
                        index_diameter = node.level  
                        farthest = node.data
                
                # Segunda BFS a partir do vértice mais distante encontrado
                index_tree = self.BFS_tree(farthest)
                index_diameter = 0  # Reinicializa o diâmetro para a segunda BFS
                
                while not index_tree.is_empty():
                    node = index_tree.dequeue(True)
                    discovered_vec[node.data - 1] = 1
                    if node.level > index_diameter:
                        index_diameter = node.level
                        farthest = node.data
                
                # Atualiza o diâmetro global se necessário
                if index_diameter > current_diameter:
                    current_diameter = index_diameter
        
        
        if (give_diameter and not give_subgraph): return current_diameter

        inverse_sorted = sorted(components_list, key=lambda node: node.size, reverse=True)
        if (give_subgraph and not give_diameter): return inverse_sorted
        return current_diameter, inverse_sorted

        
        




                
                
                






            
        






