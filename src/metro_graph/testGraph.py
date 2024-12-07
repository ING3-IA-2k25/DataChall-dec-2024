import matplotlib.pyplot as plt
import networkx as nx
from accebilite import create_data_set, graphs_to_array, save_dataset, load_data_set
from inverse_node_edge import inverse_node_edge_mat2mat

def test_dataset(dataset, G):
    nodelist = list(G.nodes())

    for idx, matrice in enumerate(dataset):
        print(f"Taille matrice dataset {idx + 1} :", matrice.shape)

        # Reconstruction du graphe
        newG = nx.from_numpy_array(matrice, create_using=nx.DiGraph)
        newG = nx.relabel_nodes(newG, {i: nodelist[i] for i in range(len(nodelist))})

        print(f"\nComparaison du graphe {idx + 1} avec le graphe initial :")
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

def test_save_load_dataset(dataset, nodelist):
    # Conserver la liste ordonnée des nœuds
    save_dataset(dataset, "test_save_load_dataser.pkl")
    matrices = load_data_set("test_save_load_dataser.pkl")
    # Reconstruire les graphes à partir des matrice
    newG = nx.from_numpy_array(matrices[0], create_using=nx.DiGraph)
    newG = nx.relabel_nodes(newG, {i: nodelist[i] for i in range(len(nodelist))})
    print("\nComparaison du graphe initial avec le graphe récupéré :")
    compare_graphs(G, newG, title="Graphe Initial vs Modifié")

if __name__ == "__main__":
    graph = {}
    graph["0"] = {"1" : {"weight" : 1}}
    graph["1"] = {"0" : {"weight" : 1}, "2" : {"weight" : 1}}

    graph["2"] = {"1" : {"weight" : 1}, "3" : {"weight" : 1}, "4" : {"weight" : 1}}
    graph["3"] = {"2" : {"weight" : 1}, "4" : {"weight" : 1}}
    graph["4"] = {"2" : {"weight" : 1}, "3" : {"weight" : 1}}

    G = nx.from_dict_of_dicts(graph, create_using=nx.DiGraph)
    NUM_GRAPHS = 20
    MAX_EDGES_TO_REMOVE = 1
    nodelist = list(G.nodes())
    # # Générer le dataset de graphes connectés
    dataset = create_data_set(G, NUM_GRAPHS, MAX_EDGES_TO_REMOVE)
    dataset = graphs_to_array(dataset, G)
    #test_dataset(dataset, G)
    test_save_load_dataset(dataset, nodelist)