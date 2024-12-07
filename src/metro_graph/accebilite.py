import networkx as nx
from itertools import combinations
import random
from metroGraph import load_metro_graph

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
    return [(graph_copy, list(edges)) for edges, graph_copy in connected_graphs]

# Exemple d'utilisation
if __name__ == "__main__":
    G = load_metro_graph()

    # Spécifier le nombre de graphes à générer et les arêtes max à supprimer
    NUM_GRAPHS = 5
    MAX_EDGES_TO_REMOVE = 2

    # Générer le dataset de graphes connectés
    dataset = create_data_set(G, NUM_GRAPHS, MAX_EDGES_TO_REMOVE)
    print(f"\nNombre total de graphes connectés générés : {len(dataset)}")

    # Afficher quelques exemples
    for i, (subgraph, removed_edges) in enumerate(dataset):
        print(f"\nExemple {i + 1}: Arêtes supprimées : {removed_edges}")