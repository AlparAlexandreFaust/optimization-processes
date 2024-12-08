import networkx as nx
import random
import matplotlib.pyplot as plt
import pandas as pd

def criar_rede_aleatoria(num_nos=20, prob_ligacao=0.3, latencia_min=1, latencia_max=10, seed=None):
    """
    Cria um grafo não-direcionado com `num_nos` nós e adiciona arestas 
    entre eles com uma certa probabilidade prob_ligacao.
    Cada aresta possui um peso (latência) aleatório entre latencia_min e latencia_max.
    """
    if seed is not None:
        random.seed(seed)  # Define a semente para replicabilidade

    G = nx.Graph()
    G.add_nodes_from(range(num_nos))
    
    # Itera sobre todos os pares de nós para adicionar aresta com certa probabilidade
    for i in range(num_nos):
        for j in range(i+1, num_nos):
            if random.random() < prob_ligacao:
                latencia = random.randint(latencia_min, latencia_max)
                G.add_edge(i, j, weight=latencia)
    return G

def menor_caminho_dijkstra(G, origem, destino):
    """
    Encontra o caminho de menor latência usando o algoritmo de Dijkstra.
    Retorna o caminho e a latência total.
    """
    # Inicializa as distâncias e o caminho
    dist = {n: float('inf') for n in G.nodes}
    dist[origem] = 0
    prev = {n: None for n in G.nodes}
    Q = set(G.nodes)

    iteracoes = 0  # Inicializa a contagem de iterações

    while Q:
        iteracoes += 1  # Incrementa a contagem de iterações

        # Seleciona o nó com a menor distância
        u = min(Q, key=lambda node: dist[node])
        Q.remove(u)

        # Verifica se o destino foi alcançado
        if u == destino:
            break

        # Configura o tamanho do gráfico
        plt.figure(figsize=(19.2, 10.8))
        
        # Visualiza o estado atual do grafo
        pos = nx.spring_layout(G, seed=42)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        nx.draw_networkx_edges(G, pos, edgelist=[(prev[v], v) for v in G.nodes if prev[v] is not None], edge_color='red', width=2)
        
        # Exibe a tabela de distâncias e predecessores no gráfico
        df = pd.DataFrame({'Distância': dist, 'Predecessor': prev})
        print(df)
        plt.table(cellText=df.values, colLabels=df.columns, rowLabels=df.index, loc='bottom', cellLoc='center', colLoc='center')
        plt.subplots_adjust(left=0.2, bottom=0.3)  # Ajusta a posição da tabela

        plt.title("Processando nó: {}".format(u))
        plt.show()

        for v in G.neighbors(u):
            alt = dist[u] + G[u][v]['weight']
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u

    print("Número de iterações: {}".format(iteracoes))  # Imprime o número de iterações

    # Reconstrói o caminho
    path = []
    u = destino
    while prev[u] is not None:
        path.insert(0, u)
        u = prev[u]
    if path:
        path.insert(0, u)

    # Visualiza o caminho final
    plt.figure(figsize=(19.2, 10.8))
    path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='green', width=3)
    plt.title("Caminho de menor latência")
    plt.show()

    return path, dist[destino]

def main():
    # Configuração do experimento
    num_nos = 20
    origem = 14
    destino = 17
    prob_ligacao = 0.12  # Aumentar probabilidade para garantir conexões suficientes
    latencia_min = 1
    latencia_max = 10
    seed = 1001  # Define a semente para replicabilidade

    # Cria a rede
    G = criar_rede_aleatoria(num_nos=num_nos, prob_ligacao=prob_ligacao, 
                             latencia_min=latencia_min, latencia_max=latencia_max, seed=seed)

    # Verifica se há caminho entre origem e destino
    if nx.has_path(G, origem, destino):
        # Calcula o menor caminho
        path, dist = menor_caminho_dijkstra(G, origem, destino)
        print("Caminho de menor latência entre nós {} e {}: {}".format(origem, destino, path))
        print("Latência total: {}".format(dist))
    else:
        print("Não existe caminho entre o nó {} e o nó {} nesta rede.".format(origem, destino))

if __name__ == "__main__":
    main()
