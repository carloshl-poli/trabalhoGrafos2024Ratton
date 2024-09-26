
from enum import Enum
from random import randint


#Funções de teste (A maioria deles feito com auxílio de IA mas foram comentadas para melhor entendimento)

import graph_library as gh
from functions import *

import timeit
import tracemalloc
import cProfile
import pstats
import io
from memory_profiler import memory_usage
import os

class Constants(Enum):
    BFS = "BFS"
    DFS = "DFS"
    MATRIX = 0
    VECTOR = 1

def measure_execution_and_memory(graph_type, grafo_filename):
    # Função anônima que será usada para medir memória e tempo
    def create_graph():
        return gh.Graph(graph_type, grafo_filename)
    
    # Medir uso de memória ao criar o grafo
    mem_usage = memory_usage(create_graph, interval=0.1, retval=True)
    
    # Inicia a medição de tempo
    start_time = timeit.default_timer()
    graph_instance = create_graph()  # Criar a instância do grafo
    end_time = timeit.default_timer()

    return {
        "result": graph_instance,
        "execution_time": end_time - start_time,
        "memory_usage": max(mem_usage[0]) - min(mem_usage[0]),
        "size": graph_instance.size,
        "edgeAmount": graph_instance.edgeAmount
    }

# Função para escrever no arquivo
def write_to_file(file, text):
    with open(file, 'a') as f:
        f.write(text + "\n")

def main():
    output_file = "grafo_resultados_teste2.txt"  # Nome do arquivo de saída

    # Carregar o grafo de um arquivo
    grafo_filename = "grafo_6.txt"
    # Criação dos grafos
    #matrix_graph = gh.Graph(gh.Constants.MATRIX, grafo_filename)
    vector_graph = gh.Graph(gh.Constants.VECTOR, grafo_filename)
    for tupla in [(10,20),(10,30),(20,30)]:
        #print(number)
        #start_time = timeit.default_timer()
        distance_BFS = vector_graph.get_distance_Vi_Vj(tupla[0], tupla[1])  # Criar a instância do grafo
        #end_time = timeit.default_timer()
        print(f"Distance from {tupla[0]} to {tupla[1]} = {distance_BFS} using BFS")
        write_to_file(f"distance_BFS.txt",f"Distance from {tupla[0]} to {tupla[1]} = {distance_BFS}")
        #distance_DFS = vector_graph.get_distance_Vi_Vj(start, end, False)  # Criar a instância do grafo
        #end_time = timeit.default_timer()
        #print(f"Distance from {start} to {end} = {distance_DFS} using DFS")
        #write_to_file(f"distance_DFS.txt",f"Distance from {start} to {end} = {distance_DFS}")


        #bfs_time_matrixVec.append(end_time - start_time)
        #start_time = timeit.default_timer()
        #matrix_graph.DFS_tree(number)  # Criar a instância do grafo
        #end_time = timeit.default_timer()
        #print(f"matrix_graph_DFS_tree: {end_time - start_time}")
        #write_to_file(f"matrix_graph_DFS_tree.txt", f"Tempo médio de execução Matriz: {end_time - start_time} segundos")
        #dfs_time_matrixVec.append(end_time - start_time)
write_to_file("distance_BFS.txt", "########################")

            


'''
    # Escreve no arquivo: Medição da memória e tempo para as representações
    write_to_file(output_file, "\nMedindo a memória e tempo para as representações de grafos:")

    # Lista de Adjacência
    write_to_file(output_file, "\nLista de Adjacência:")
    list_results = measure_execution_and_memory(gh.Constants.VECTOR, grafo_filename)
    write_to_file(output_file, f"Tempo de execução: {list_results['execution_time']:.6f} segundos")
    write_to_file(output_file, f"Uso de memória: {list_results['memory_usage']:.6f} MiB")
    write_to_file(output_file, f"Numero de vertices: {list_results['size']:.6f} vertices")
    write_to_file(output_file, f"Numero de arestas: {list_results['edgeAmount']:.6f} arestas")



    # Matriz de Adjacência
    write_to_file(output_file, "\nMatriz de Adjacência:")
    matrix_results = measure_execution_and_memory(gh.Constants.MATRIX, grafo_filename)
    write_to_file(output_file, f"Tempo de execução: {matrix_results['execution_time']:.6f} segundos")
    write_to_file(output_file, f"Uso de memória: {matrix_results['memory_usage']:.6f} MiB")
    write_to_file(output_file, f"Numero de vertices: {matrix_results['size']:.6f} vertices")
    write_to_file(output_file, f"Numero de arestas: {matrix_results['edgeAmount']:.6f} arestas")

    # Criação dos grafos
    matrix_graph = matrix_results['result']
    vector_graph = list_results['result']

    # Medir busca em largura (BFS)
    write_to_file(output_file, "\nBusca em Largura (BFS) - Tempo médio de 100 execuções:")
    bfs_time = timeit.timeit(lambda: matrix_graph.BFS_tree(1), number=100)
    write_to_file(output_file, f"Tempo médio de execução: {bfs_time / 100:.6f} segundos")

    # Medir busca em profundidade (DFS)
    write_to_file(output_file, "\nBusca em Profundidade (DFS) - Tempo médio de 100 execuções:")
    dfs_time = timeit.timeit(lambda: matrix_graph.DFS_tree(1), number=100)
    write_to_file(output_file, f"Tempo médio de execução: {dfs_time / 100:.6f} segundos")

    # Medir distâncias e diâmetro do grafo
    write_to_file(output_file, "\nDistância entre vértices (10, 20):")
    write_to_file(output_file, f"Distância: {matrix_graph.get_distance_Vi_Vj(10, 20)}")

    write_to_file(output_file, "\nDiâmetro do grafo:")
    write_to_file(output_file, f"Diâmetro: {matrix_graph.get_diameter()}")

    # Medir componentes conexos
    write_to_file(output_file, "\nComponentes Conexos:")
    connected_components = matrix_graph.get_diameter(False, True)
    write_to_file(output_file, f"Número de componentes conexos: {len(connected_components)}")
    write_to_file(output_file, f"Tamanho da maior componente: {max(connected_components, key=lambda node: node.size)}")
    write_to_file(output_file, f"Tamanho da menor componente: {min(connected_components, key=lambda node: node.size)}")

    # Profiler CPU
    write_to_file(output_file, "\nMedição de CPU com cProfile:")
    profiler = cProfile.Profile()
    profiler.enable()
    matrix_graph.BFS_tree(1)  # Exemplo de busca BFS
    profiler.disable()

    # Resultados detalhados do cProfile
    profiler_output = io.StringIO()
    pstats.Stats(profiler, stream=profiler_output).sort_stats(pstats.SortKey.TIME).print_stats()
    write_to_file(output_file, profiler_output.getvalue()
    '''



if __name__ == "__main__":
    main()