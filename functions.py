from data_structures import *
import numpy as np
import timeit
import sys
import time


def graph_read_source(file_name):
    with open(file_name, 'r') as archive:
        #yield o número de vértices do grafo
        yield int(archive.readline().strip().split()[0])
        # Gera tuplas de números a partir da segunda linha
        for line in archive:
            # Divide a linha em números e converte para inteiro
            edge = tuple(map(int, line.strip().split()))
            yield edge


def read_bfs_graph_to_component_node(file_name):
    with open(file_name, 'r') as file:
        # Primeira linha contém o número de vértices
        vertex = int(file.readline().strip())

        edges = []
        for line in file:
            # Cada linha contém dois inteiros separados por espaço, formando uma aresta
            vi, vj = map(int, line.strip().split())
            edges.append(f"{vi} {vj}\n")

    # Retorna o ComponentNode com o número de vértices e as arestas
    return SubgraphNode(vertex, edges)


def memory_and_time_of_class_instantiation(ClassType, *args, **kwargs):
    # Medir o tempo de execução da instanciação
    start_time = time.perf_counter()  # Começar a contagem de tempo
    instance = ClassType(*args, **kwargs)  # Criar a instância
    end_time = time.perf_counter()  # Fim da contagem de tempo
    
    # Calcular o tempo de execução
    execution_time = end_time - start_time
    
    # Calcular o uso de memória da instância
    memory_usage = sys.getsizeof(instance)
    
    return memory_usage, execution_time
