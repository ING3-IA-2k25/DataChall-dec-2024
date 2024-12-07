import networkx as nx
from itertools import combinations
import random
from src.metro_graph.metroGraph import load_metro_graph, GpsCoordinate, save_metro_graph
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
    print(f"Number of connected graphs in {filename} : {number}")
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

# Exemple d'utilisation
if __name__ == "__main__":
    dataset = load_data_set()
    print(f"\nNombre total de graphes connectés chargés : {len(dataset)}")
    
    g = dataset[3]
    
    save_metro_graph(g, "graph_3")
    
    # first = dataset[0]
    # print first edga data
    # print(first.edges.data())    
    # G = load_metro_graph()

    # # # Spécifier le nombre de graphes à générer et les arêtes max à supprimer
    # NUM_GRAPHS = 10
    # MAX_EDGES_TO_REMOVE = 20

    # # # Générer le dataset de graphes connectés
    # dataset = create_data_set(G, NUM_GRAPHS, MAX_EDGES_TO_REMOVE)
    # print(f"\nNombre total de graphes connectés générés : {len(dataset)}")

    # # # sauvegarder les graphes dans un fichier pickle
    # save_dataset(dataset, f"connected_graphs_{NUM_GRAPHS}.pkl")
    # # with open(f"connected_graphs_{NUM_GRAPHS}.pkl", "wb") as f:
    # #     pickle.dump(dataset, f)
    