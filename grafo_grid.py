import heapq
import time
import tracemalloc

linhas, colunas = 5, 5
n = linhas * colunas

coordenadas = {i: (i // colunas, i % colunas) for i in range(n)}

# grafo
pesos_fixos_embaralhados = {
    (0, 1): 7, (1, 2): 2, (2, 3): 9, (3, 4): 5,
    (0, 5): 6, (1, 6): 8, (2, 7): 3, (3, 8): 10, (4, 9): 4,
    (5, 6): 1, (6, 7): 7, (7, 8): 2, (8, 9): 9,
    (5,10): 5, (6,11): 4, (7,12): 6, (8,13): 1, (9,14): 8,
    (10,11): 3, (11,12): 2, (12,13): 10, (13,14): 7,
    (10,15): 6, (11,16): 9, (12,17): 1, (13,18): 5, (14,19): 4,
    (15,16): 3, (16,17): 7, (17,18): 8, (18,19): 2,
    (15,20): 9, (16,21): 2, (17,22): 5, (18,23): 6, (19,24): 1,
    (20,21): 4, (21,22): 10, (22,23): 3, (23,24): 7
}

def peso_entre(u, v):
    return pesos_fixos_embaralhados.get((u, v)) or pesos_fixos_embaralhados.get((v, u)) or 1

def criar_grafo_com_pesos_embaralhados():
    grafo = {}
    for i in range(n):
        vizinhos = []
        x, y = coordenadas[i]
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < linhas and 0 <= ny < colunas:
                j = nx * colunas + ny
                peso = peso_entre(i, j)
                vizinhos.append((j, peso))
        grafo[i] = vizinhos
    return grafo

grafo = criar_grafo_com_pesos_embaralhados()

def heuristica_manhattan(u, v):
    x1, y1 = coordenadas[u]
    x2, y2 = coordenadas[v]
    return abs(x1 - x2) + abs(y1 - y2)

def a_estrela(grafo, inicio, fim):
    dist = {v: float('inf') for v in grafo}
    dist[inicio] = 0
    prev = {v: None for v in grafo}
    fila = [(heuristica_manhattan(inicio, fim), inicio)]
    visitados = 0

    while fila:
        _, atual = heapq.heappop(fila)
        visitados += 1
        if atual == fim:
            break
        for vizinho, peso in grafo[atual]:
            novo_custo = dist[atual] + peso
            if novo_custo < dist[vizinho]:
                dist[vizinho] = novo_custo
                prev[vizinho] = atual
                prioridade = novo_custo + heuristica_manhattan(vizinho, fim)
                heapq.heappush(fila, (prioridade, vizinho))

    caminho = []
    atual = fim
    while atual is not None:
        caminho.insert(0, atual)
        atual = prev[atual]

    return dist[fim], caminho, visitados

def main():
    print(f"\n--- GRAFO GRID 5x5 ---")
    for i in range(linhas):
        print("  ".join(f"{i * colunas + j:2}" for j in range(colunas)))

    inicio = int(input("\nDigite o nó de partida (0 a 24): "))
    fim = int(input("Digite o nó de chegada (0 a 24): "))

    tracemalloc.start()
    t0 = time.time()
    dist_a, cam_a, nos_a = a_estrela(grafo, inicio, fim)
    t1 = time.time()
    mem_a, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("\n--- Resultado grafo grid com A* ---")
    print(f"   Caminho: {' -> '.join(map(str, cam_a))}")
    print(f"   Custo total: {dist_a}")
    print(f"   Nós percorridos: {nos_a}")
    print(f"   Tempo: {t1 - t0:.6f} s")
    print(f"   Memória: {mem_a / 1024:.2f} KB")

if __name__ == "__main__":
    main()
