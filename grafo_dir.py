import heapq
import time
import tracemalloc

def dijkstra_completo(grafo, origem, destino):
    distancias = {no: float('inf') for no in grafo}
    anteriores = {no: None for no in grafo}
    distancias[origem] = 0
    visitados = set()
    fila = [(0, origem)]

    while fila:
        distancia_atual, no_atual = heapq.heappop(fila)

        if no_atual in visitados:
            continue
        visitados.add(no_atual)

        for vizinho, peso in grafo.get(no_atual, []):
            if vizinho in visitados:
                continue
            nova_distancia = distancia_atual + peso
            if nova_distancia < distancias[vizinho]:
                distancias[vizinho] = nova_distancia
                anteriores[vizinho] = no_atual
                heapq.heappush(fila, (nova_distancia, vizinho))

    caminho = []
    atual = destino
    while atual is not None:
        caminho.insert(0, atual)
        atual = anteriores[atual]

    return {
        "distancia": distancias[destino],
        "caminho": caminho,
        "visitados": len(visitados)
    }

# Grafo direcionado
grafo = {
    0: [(1, 4), (2, 1)],
    1: [(4, 3)],
    2: [(5, 3)],
    3: [(0, 7), (6, 2)],
    4: [(3, 2), (12, 6), (6, 10)],
    5: [(3, 8), (11, 7)],
    6: [(7, 3), (5, 6)],
    7: [(4, 1), (8, 9), (9, 1)],
    8: [(9, 3), (6, 1)],
    9: [(10, 10)],
    10: [(7, 8)],
    11: [(8, 7)],
    12: [(10, 2)]
}

origem = int(input("Digite o vértice de origem: "))
destino = int(input("Digite o vértice de destino: "))

tracemalloc.start()
inicio_tempo = time.time()

resultado = dijkstra_completo(grafo, origem, destino)

fim_tempo = time.time()
memoria_usada, _ = tracemalloc.get_traced_memory()
tracemalloc.stop()

# Impressão dos resultados
print("\n--- Resultado grafo direcionado ---")
print(f"Caminho percorrido: {' -> '.join(map(str, resultado['caminho']))}")
print(f"Custo total: {resultado['distancia']}")
print(f"Nós percorridos: {resultado['visitados']}")
print(f"Tempo de execução: {fim_tempo - inicio_tempo:.6f} segundos")
print(f"Memória usada: {memoria_usada / 1024:.2f} KB")
