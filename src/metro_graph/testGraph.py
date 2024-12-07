import matplotlib.pyplot as plt
import networkx as nx
from accebilite import create_data_set, graphs_to_array

def test_dataset(dataset, G):
    """
    Teste le dataset en comparant les graphes générés avec le graphe initial.
    Passe par la conversion matrice pour valider la correspondance.
    """
    # Conserver la liste ordonnée des nœuds
    nodelist = list(G.nodes())

    for idx, matrice in enumerate(dataset):  # Comparer les 2 premiers graphes avec le graphe initial
        # Reconstruire le graphe à partir de la matrice avec le même ordre des nœuds
        newG = nx.from_numpy_array(matrice, create_using=nx.DiGraph)
        newG = nx.relabel_nodes(newG, {i: nodelist[i] for i in range(len(nodelist))})

        print(f"\nComparaison du graphe {idx + 1} avec le graphe initial:")
        
        print(G)
        compare_graphs(G, newG, title=f"Graphe Initial vs Modifié {idx + 1}")

def compare_graphs(graph1, graph2, title="Comparaison des Graphes"):
    """
    Compare deux graphes et affiche les arêtes différentes en rouge.
    
    :param graph1: Premier graphe NetworkX (référence).
    :param graph2: Deuxième graphe NetworkX (modifié).
    :param title: Titre de la visualisation.
    """
    pos = nx.spring_layout(graph1)  # Positionnement des nœuds
    
    # Déterminer les différences d'arêtes
    edges_graph1 = set(graph1.edges())
    edges_graph2 = set(graph2.edges())

    missing_edges = edges_graph1 - edges_graph2  # Arêtes supprimées

    plt.figure(figsize=(10, 8))
    # Dessiner le graphe initial en bleu clair
    nx.draw(graph1, pos, with_labels=True, edge_color="lightblue", node_color="skyblue", node_size=700, font_size=12, font_weight="bold")
    
    # Dessiner les arêtes supprimées en rouge
    if missing_edges:
        nx.draw_networkx_edges(graph1, pos, edgelist=missing_edges, edge_color="red", width=2, style="dashed", label="Arêtes supprimées")
    

    plt.title(title)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    graph = {}
    graph["0"] = {"1" : {"weight" : 1}}
    graph["1"] = {"0" : {"weight" : 1}, "2" : {"weight" : 1}}

    graph["2"] = {"1" : {"weight" : 1}, "3" : {"weight" : 1}, "4" : {"weight" : 1}}
    graph["3"] = {"2" : {"weight" : 1}, "4" : {"weight" : 1}}
    graph["4"] = {"2" : {"weight" : 1}, "3" : {"weight" : 1}}

    G = nx.from_dict_of_dicts(graph, create_using=nx.DiGraph)
    NUM_GRAPHS = 20
    MAX_EDGES_TO_REMOVE = 3
    nodelist = list(G.nodes())
    # # Générer le dataset de graphes connectés
    dataset = create_data_set(G, NUM_GRAPHS, MAX_EDGES_TO_REMOVE)
    dataset = graphs_to_array(dataset, G)
    test_dataset(dataset, G)