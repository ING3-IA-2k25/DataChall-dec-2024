import networkx as nx
from itertools import combinations
import random
import matplotlib.pyplot as plt
from metroGraph import load_metro_graph
import pickle
from pathlib import Path


def is_connected_after_removal(graph, edges_to_remove):
    """
    Vérifie si un graphe reste connecté après suppression d'une liste d'arêtes.
    
    :param graph: Le graphe NetworkX initial.
    :param edges_to_remove: Une liste d'arêtes à supprimer.
    :return: True si le graphe reste connecté, sinon False.
    """
    graph_copy = graph.copy()
    graph_copy.remove_edges_from(edges_to_remove)
    return nx.is_connected(graph_copy)

def create_data_set(graph, num_graphs, max_edges_to_remove=2):
    """
    Crée un dataset contenant un nombre spécifique de graphes connectés
    après suppression aléatoire d'arêtes.
    
    :param graph: Le graphe NetworkX initial.
    :param num_graphs: Nombre de graphes à générer.
    :param max_edges_to_remove: Nombre maximum d'arêtes à supprimer par graphe.
    :return: Une liste de tuples (graphe connecté, arêtes supprimées).
    """
    all_edges = list(graph.edges())
    connected_graphs = set()

    while len(connected_graphs) < num_graphs:
        # Choisir aléatoirement le nombre d'arêtes à supprimer (1 à max_edges_to_remove)
        num_edges_to_remove = random.randint(1, max_edges_to_remove)
        edges_to_remove = random.sample(all_edges, num_edges_to_remove)
        
        # Vérifier si le graphe reste connecté après suppression
        if is_connected_after_removal(graph, edges_to_remove):
            graph_copy = graph.copy()
            graph_copy.remove_edges_from(edges_to_remove)
            # Utiliser un ensemble pour éviter les doublons
            connected_graphs.add((frozenset(edges_to_remove), graph_copy))

    # Retourner la liste des graphes avec les arêtes supprimées
    
    return [graph for _, graph in connected_graphs]
    # return [(graph_copy, list(edges)) for edges, graph_copy in connected_graphs]

def load_data_set(filename = "connected_graphs_1000.pkl"):
    """
    Charge un dataset de graphes connectés à partir d'un fichier pickle.
    
    :param filename: Le nom du fichier pickle.
    :return: Le dataset de graphes connectés.
    """
    # get number of connected graphs in filename "connected_graphs_{NUM_GRAPHS}.pkl"
    number = filename.split('_')[-1].split('.')[0]
    save_dir = Path("./data")
    save_path = save_dir / filename
    
    with open(save_path, "rb") as f:
        return pickle.load(f)

def save_dataset(dataset, filename = "connected_graphs_1000.pkl"):
    """
    Sauvegarde un dataset de graphes connectés dans un fichier pickle.
    
    :param dataset: Le dataset de graphes connectés.
    :param filename: Le nom du fichier pickle.
    """
    save_dir = Path("./data")
    save_path = save_dir / filename
    
    with open(save_path, "wb") as f:
        pickle.dump(dataset, f)

def test_dataset(dataset, G):
    """
    Teste le dataset en comparant les graphes générés avec le graphe initial.
    Passe par la conversion matrice pour valider la correspondance.
    """
    # Conserver la liste ordonnée des nœuds
    nodelist = list(G.nodes())

    for idx, graph in enumerate(dataset[:2]):  # Comparer les 2 premiers graphes avec le graphe initial
        # Convertir le graphe en matrice d'adjacence en utilisant l'ordre des nœuds
        array = nx.convert_matrix.to_numpy_array(graph, nodelist=nodelist)

        # Reconstruire le graphe à partir de la matrice avec le même ordre des nœuds
        newG = nx.convert_matrix.from_numpy_array(array)
        newG = nx.relabel_nodes(newG, {i: nodelist[i] for i in range(len(nodelist))})

        print(f"\nComparaison du graphe {idx + 1} avec le graphe initial:")
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

# Exemple d'utilisation
if __name__ == "__main__":
    # dataset = load_data_set("connected_graphs_1000.pkl")
    
    G = load_metro_graph()

    # # Spécifier le nombre de graphes à générer et les arêtes max à supprimer
    NUM_GRAPHS = 1000
    MAX_EDGES_TO_REMOVE = 20

    # # Générer le dataset de graphes connectés
    dataset = create_data_set(G, NUM_GRAPHS, MAX_EDGES_TO_REMOVE)
    print(f"\nNombre total de graphes connectés générés : {len(dataset)}")

    # # sauvegarder les graphes dans un fichier pickle
    save_dataset(dataset, f"connected_graphs_{NUM_GRAPHS}.pkl")
    # with open(f"connected_graphs_{NUM_GRAPHS}.pkl", "wb") as f:
    #     pickle.dump(dataset, f)
    
    