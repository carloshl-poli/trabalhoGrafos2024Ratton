from data_structures import *
import numpy as np
import timeit
import tracemalloc
import cProfile
import pstats
import io
from memory_profiler import memory_usage


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



# Função para medir tempo de execução e memória
def measure_execution_and_memory(func, *args):
    # Medindo uso de memória com memory-profiler
    mem_usage = memory_usage((func, args), interval=0.1, retval=True)
    
    # Calculando tempo de execução com timeit
    start_time = timeit.default_timer()
    result = func(*args)
    end_time = timeit.default_timer()

    # Retorna tempo de execução e o resultado da função
    return {
        "result": result,
        "execution_time": end_time - start_time,
        "memory_usage": max(mem_usage[0]) - min(mem_usage[0])
    }