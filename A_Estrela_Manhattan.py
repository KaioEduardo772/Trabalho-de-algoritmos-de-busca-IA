import heapq
import time
import tracemalloc

linhas, colunas = 10, 10
n = linhas * colunas

coordenadas = {i: (i // colunas, i % colunas) for i in range(n)}

# grafo 10x10
pesos_fixos_embaralhados = {
    (0, 1): 7, (1, 2): 2, (2, 3): 9, (3, 4): 5, (4, 5): 3, (5, 6): 6, (6, 7): 4, (7, 8): 8, (8, 9): 1,
    (0, 10): 6, (1, 11): 8, (2, 12): 3, (3, 13): 10, (4, 14): 4, (5, 15): 5, (6, 16): 4, (7, 17): 6, (8, 18): 1, (9, 19): 8,
    (10, 11): 3, (11, 12): 2, (12, 13): 10, (13, 14): 7, (14, 15): 9, (15, 16): 3, (16, 17): 7, (17, 18): 8, (18, 19): 2,
    (10, 20): 6, (11, 21): 9, (12, 22): 1, (13, 23): 5, (14, 24): 4, (15, 25): 7, (16, 26): 10, (17, 27): 3, (18, 28): 7, (19, 29): 6,
    (20, 21): 4, (21, 22): 10, (22, 23): 3, (23, 24): 7, (24, 25): 2, (25, 26): 1, (26, 27): 9, (27, 28): 4, (28, 29): 5,
    (20, 30): 8, (21, 31): 2, (22, 32): 6, (23, 33): 4, (24, 34): 3, (25, 35): 5, (26, 36): 7, (27, 37): 1, (28, 38): 8, (29, 39): 9,
    (30, 31): 3, (31, 32): 7, (32, 33): 2, (33, 34): 6, (34, 35): 9, (35, 36): 4, (36, 37): 8, (37, 38): 1, (38, 39): 10,
    (30, 40): 5, (31, 41): 9, (32, 42): 4, (33, 43): 7, (34, 44): 3, (35, 45): 2, (36, 46): 6, (37, 47): 8, (38, 48): 7, (39, 49): 1,
    (40, 41): 6, (41, 42): 8, (42, 43): 3, (43, 44): 1, (44, 45): 9, (45, 46): 7, (46, 47): 2, (47, 48): 5, (48, 49): 4,
    (40, 50): 2, (41, 51): 5, (42, 52): 10, (43, 53): 6, (44, 54): 8, (45, 55): 3, (46, 56): 1, (47, 57): 4, (48, 58): 9, (49, 59): 7,
    (50, 51): 1, (51, 52): 9, (52, 53): 4, (53, 54): 7, (54, 55): 2, (55, 56): 6, (56, 57): 10, (57, 58): 3, (58, 59): 5,
    (50, 60): 8, (51, 61): 7, (52, 62): 1, (53, 63): 5, (54, 64): 4, (55, 65): 9, (56, 66): 2, (57, 67): 6, (58, 68): 3, (59, 69): 10,
    (60, 61): 3, (61, 62): 6, (62, 63): 7, (63, 64): 2, (64, 65): 8, (65, 66): 1, (66, 67): 5, (67, 68): 9, (68, 69): 4,
    (60, 70): 7, (61, 71): 2, (62, 72): 10, (63, 73): 3, (64, 74): 6, (65, 75): 8, (66, 76): 4, (67, 77): 1, (68, 78): 5, (69, 79): 9,
    (70, 71): 2, (71, 72): 9, (72, 73): 4, (73, 74): 7, (74, 75): 3, (75, 76): 6, (76, 77): 10, (77, 78): 1, (78, 79): 5,
    (70, 80): 8, (71, 81): 1, (72, 82): 3, (73, 83): 6, (74, 84): 9, (75, 85): 4, (76, 86): 7, (77, 87): 2, (78, 88): 10, (79, 89): 5,
    (80, 81): 4, (81, 82): 7, (82, 83): 2, (83, 84): 5, (84, 85): 10, (85, 86): 1, (86, 87): 8, (87, 88): 3, (88, 89): 6,
    (80, 90): 9, (81, 91): 6, (82, 92): 1, (83, 93): 8, (84, 94): 7, (85, 95): 2, (86, 96): 3, (87, 97): 5, (88, 98): 4, (89, 99): 10,
    (90, 91): 3, (91, 92): 9, (92, 93): 5, (93, 94): 2, (94, 95): 7, (95, 96): 8, (96, 97): 1, (97, 98): 6, (98, 99): 4,
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


pesos = list(pesos_fixos_embaralhados.values())
PESO_MEDIO = sum(pesos) / len(pesos)

def heuristica_peso_medio(u, v):
    x1, y1 = coordenadas[u]
    x2, y2 = coordenadas[v]
    dist_manhattan = abs(x1 - x2) + abs(y1 - y2)
    return dist_manhattan * PESO_MEDIO

def a_estrela(grafo, inicio, fim):
    dist = {v: float('inf') for v in grafo}
    dist[inicio] = 0
    prev = {v: None for v in grafo}
    fila = [(heuristica_peso_medio(inicio, fim), inicio)]
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
                prioridade = novo_custo + heuristica_peso_medio(vizinho, fim)
                heapq.heappush(fila, (prioridade, vizinho))

    caminho = []
    atual = fim
    while atual is not None:
        caminho.insert(0, atual)
        atual = prev[atual]

    return dist[fim], caminho, visitados

def dijkstra(grafo, inicio, fim):
    dist = {v: float('inf') for v in grafo}
    dist[inicio] = 0
    prev = {v: None for v in grafo}
    fila = [(0, inicio)]
    visitados = 0

    while fila:
        custo_atual, atual = heapq.heappop(fila)
        visitados += 1
        if atual == fim:
            break
        for vizinho, peso in grafo[atual]:
            novo_custo = dist[atual] + peso
            if novo_custo < dist[vizinho]:
                dist[vizinho] = novo_custo
                prev[vizinho] = atual
                heapq.heappush(fila, (novo_custo, vizinho))

    caminho = []
    atual = fim
    while atual is not None:
        caminho.insert(0, atual)
        atual = prev[atual]

    return dist[fim], caminho, visitados

def main():
    print(f"\n--- GRAFO GRID {linhas}x{colunas} ---")
    for i in range(linhas):
        print("  ".join(f"{i * colunas + j:2}" for j in range(colunas)))

    inicio = int(input("\nDigite o nó de partida (0 a 99): "))
    fim = int(input("Digite o nó de chegada (0 a 99): "))

    print("\nExecutando A* com heurística mais forte...")
    tracemalloc.start()
    t0 = time.time()
    dist_a, cam_a, nos_a = a_estrela(grafo, inicio, fim)
    t1 = time.time()
    mem_a, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("\n--- Resultado A* ---")
    print(f"   Caminho: {' -> '.join(map(str, cam_a))}")
    print(f"   Custo total: {dist_a}")
    print(f"   Nós percorridos: {nos_a}")
    print(f"   Tempo: {t1 - t0:.6f} s")
    print(f"   Memória: {mem_a / 1024:.2f} KB")

    print("\nExecutando Dijkstra...")
    tracemalloc.start()
    t0 = time.time()
    dist_d, cam_d, nos_d = dijkstra(grafo, inicio, fim)
    t1 = time.time()
    mem_d, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("\n--- Resultado Dijkstra ---")
    print(f"   Caminho: {' -> '.join(map(str, cam_d))}")
    print(f"   Custo total: {dist_d}")
    print(f"   Nós percorridos: {nos_d}")
    print(f"   Tempo: {t1 - t0:.6f} s")
    print(f"   Memória: {mem_d / 1024:.2f} KB")

if __name__ == "__main__":
    main()
