import heapq
import time
import tracemalloc

# grafo não direcionado
grafo = {
    0:  [(1, 1), (2, 2)],
    1:  [(0, 1), (3, 7), (5, 6)],
    2:  [(0, 2), (3, 3)],
    3:  [(2, 3), (1, 7), (4, 1)],
    4:  [(3, 1), (5, 4), (6, 2), (7, 1)],
    5:  [(1, 6), (4, 4), (10, 8)],
    6:  [(4, 2), (7, 10), (8, 4)],
    7:  [(6, 10), (4, 1), (10, 2)],
    8:  [(6, 4), (9, 6)],
    9:  [(8, 6), (12, 5)],
    10: [(5, 8), (7, 2), (11, 3), (14, 1)],
    11: [(10, 3), (12, 7), (13, 6)],
    12: [(9, 5), (11, 7)],
    13: [(11, 6), (14, 9)],
    14: [(10, 1), (13, 9)]
}

def dijkstra(g, origem, destino):
    dist = {v: float('inf') for v in g}
    dist[origem] = 0
    prev = {v: None for v in g}
    pq   = [(0, origem)]
    vis  = set()

    while pq:
        d_atual, v_atual = heapq.heappop(pq)
        if v_atual in vis:
            continue
        vis.add(v_atual)

        if v_atual == destino:
            break

        for viz, peso in g[v_atual]:
            nd = d_atual + peso
            if nd < dist[viz]:
                dist[viz] = nd
                prev[viz] = v_atual
                heapq.heappush(pq, (nd, viz))

    caminho = []
    v = destino
    while v is not None:
        caminho.insert(0, v)
        v = prev[v]
    return dist[destino], caminho, len(caminho)

# Execução
if __name__ == "__main__":
    o = int(input("Vértice de origem: "))
    d = int(input("Vértice de destino: "))

    tracemalloc.start()
    t0 = time.time()
    dist_total, caminho, n_vertices = dijkstra(grafo, o, d)
    t1 = time.time()
    mem_atual, mem_pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("\n--- Resultado grafo não direcionado ---")
    print("Caminho :", " -> ".join(map(str, caminho)))
    print("Distância total:", dist_total)
    print("Nós percorridos:", n_vertices)
    print(f"Tempo de execução: {(t1 - t0)*1000:.3f} ms")
    print(f"Pico de uso de memória: {mem_pico/1024:.2f} KB")