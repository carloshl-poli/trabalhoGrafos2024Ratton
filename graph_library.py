import numpy as np
#import data_structures as ds
from functions import *
import os
from enum import Enum

class Constants(Enum):
    BFS = "BFS"
    DFS = "DFS"
    MATRIX = 0
    VECTOR = 1



class Graph:
    def __init__(self, representationType, path):
        self.size = 0
        self.edgeAmount = 0
        self.representation = 0
        self.representationType = representationType
        self.degreeVec = np.zeros(self.size, dtype=int)
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


    def graph_export_stats(self, file_name, get_components = False):
        with open(file_name, 'w') as file:
            file.write("Graph Statistics\n\n")
            if self.size == 0:
                file.write("Graph is empty. No vertices or edges to display.\n")
                return
            file.write(f"Number of vertices:     {self.size}\n")
            file.write(f"Number of edges:        {self.edgeAmount}\n")
            file.write(f"Minimum degree:         {self.get_min_degree()}\n")
            file.write(f"Maximum degree:         {self.get_max_degree()}\n")
            file.write(f"Mean degree:            {self.get_mean_degree():.2f}\n")
            file.write(f"Median degree:          {self.get_median_degree():.2f}\n")
            if get_components:
            
                components_list = self.get_subcomponents()
                components_Amount = len(components_list)
                file.write(f"Number of Connected Components: {components_Amount}\n\n")
                file.write("Connected Components:\n\n")
                for index, component in enumerate(components_list):
                    file.write(f"Component number:       {index + 1}\n")
                    file.write(f"Number of vertices:     {component.size}\n")
                    file.write(f"List of edges:                          \n")
                    for edge in component.edges:
                        file.write(f"Edge: {edge[0]} -- {edge[1]}\n")




    def BFS_tree(self, root, give_subgraph = False, give_gen_tree = True):
        if self.degreeVec[root - 1] == 0:
            # Retorna o vértice isolado como um subgrafo de um único vértice
            if give_subgraph and not give_gen_tree:
                return SubgraphNode(1, [])
            elif give_gen_tree and not give_subgraph:
                return Queue().enqueue(root)
            else:
                return Queue().enqueue(root), SubgraphNode(1, [])
        elif (self.size == 0 or root > self.size):
            raise ValueError("Invalid root or Graph")
        
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
                        if {W,V} not in edges_list and give_subgraph == True: edges_list += [{W,V}]
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
                    if {W,V} not in edges_list and give_subgraph == True: edges_list += [{W,V}]
                    if self.is_marked_to(W, 0):  # Se W não foi marcado
                        self.mark_vertice(W)
                        queue.enqueue(W)
                        level[w] = level[v] + 1
                        parent[w] = V
                        gen_tree.enqueue(W, level[w], parent[w])

        # Caso give_subgraph == True, ele irá retornar um node com as informações
        # necessárias para immprimir esse subgrafo
        if give_subgraph == True:
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
        #caso esse vértice seja isolado
        if self.degreeVec[root - 1] == 0:
            return Queue()
        #caso o grafo esteja vazio ou root não esteja no grafo
        elif (self.size == 0 or root > self.size):
            raise ValueError("Invalid root or Graph")
        
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
        if gen_tree.is_empty():
            print("A árvore geradora está vazia. Nenhum arquivo será gerado.")
            return

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

    def get_distance_Vi_Vj(self, VI, VJ, use_BFS_search = True):
        if VI < 1 or VI > self.size or VJ < 1 or VJ > self.size:
            raise ValueError("Invalid arguments for VI or VJ or both")
        if VI == VJ: return 0
        if use_BFS_search:
            VI_tree = self.BFS_tree(VI)
        else:
            VI_tree = self.DFS_tree(VI)
        if VI_tree.is_empty(): return -1

        while not VI_tree.is_empty():
            node = VI_tree.dequeue(True)  # Armazena todos os níveis
            if VJ == node.data:
                return node.level
        return -1
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

    def get_subcomponent_diameter(self, vertice):
        # Primeira BFS a partir do vértice atual
        index_tree = self.BFS_tree(vertice)
        if index_tree.size <= 1: return 0
        # Encontra o vértice mais distante
        index_diameter = 0
        farthest = vertice
        while not index_tree.is_empty():
            node = index_tree.dequeue(True)
            if node.level > index_diameter:
                index_diameter = node.level
                farthest = node.data
        
        # Segunda BFS a partir do vértice mais distante
        index_tree = self.BFS_tree(farthest)
        index_diameter = 0  # Reinicializa o diâmetro para a segunda BFS
        while not index_tree.is_empty():
            node = index_tree.dequeue(True)
            if node.level > index_diameter:
                index_diameter = node.level
        
        return index_diameter

    def get_graph_diameter(self, get_exact_value = False):
        current_diameter = 0
        discovered_vec = np.zeros(self.size, dtype=int)
        
        for index in range(self.size):
            if discovered_vec[index] == 0 and not get_exact_value:
                vertice = index + 1
                
                # Calcular o diâmetro da subcomponente
                subcomponent_diameter = self.get_subcomponent_diameter(vertice)
                discovered_vec += self.mark
                # Atualizar o diâmetro global, se necessário
                if subcomponent_diameter > current_diameter:
                    current_diameter = subcomponent_diameter
            elif get_exact_value:
                vertice = index + 1
                index_tree = self.BFS_tree(vertice)
                while not index_tree.is_empty():
                    node = index_tree.dequeue(True)
                    if node.level > current_diameter:
                        current_diameter = node.level
        
        return current_diameter
      
    def get_subcomponents(self):
        discovered_vec = np.zeros(self.size, dtype=int)
        components_list = []

        for index in range(self.size):
            if discovered_vec[index] == 0:
                vertice = index + 1

                #Obter a subcomponente usando BFS
                _, subgraph = self.BFS_tree(vertice, True, True)
                components_list.append(subgraph)

                #Marcar todos os vértices dessa subcomponente como descobertos
                for edge in subgraph.edges:
                    for v in edge:
                        vertices = map(int, v.split())
                        for vertex in vertices:
                            discovered_vec[vertex - 1] = 1

        return sorted(components_list, key=lambda node: node.size, reverse=True)

    def get_level_from_tree(self, value, gen_tree):
        while not gen_tree.is_empty():
            node = gen_tree.dequeue(True)  # Armazena todos os níveis
            if value == node.data:
                return node.level
        return -1


                
                
                






            
        






