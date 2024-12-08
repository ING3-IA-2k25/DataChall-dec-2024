
from src.simulation.passenger_flow import PassengerFlow, PassengerDataLoader, PassengerFlowRepository
from src.metro_graph.metroGraph import load_metro_graph, GpsCoordinate
import networkx as nx
import numpy as np
import cupy as cp
from scipy.sparse.csgraph import dijkstra
from typing import List


def build_graph_gpu(adj_matrix):
    return cp.array(adj_matrix) 

def dijkstras_matrix(W_d):
    # Convertir la matrice GPU en CPU
    W = cp.asnumpy(W_d)
    
    # Calculer distances et prédécesseurs
    dist, predecessors = dijkstra(W, directed=False, return_predecessors=True)
    
    # Fonction helper pour reconstruire le chemin
    def get_path(start, end, predecessors):
        path = []
        current = end
        while current != -9999:  # -9999 est la valeur par défaut pour indiquer pas de prédécesseur
            path.append(current)
            current = predecessors[start][current]
        return path[::-1]  # Inverse le chemin pour avoir start->end
    
    # Retourner distances et fonction pour obtenir les chemins
    return cp.array(dist), get_path, predecessors
  
class Dijkstra_GPU:
    def __init__(self, matrix_adj: np.array):
        self.adj_matrix = matrix_adj
    
    
    def process_passenger_flows(self, flows):
        # Obtenir distances et fonction get_path
        distances, get_path, predecessors = dijkstras_matrix(build_graph_gpu(self.adj_matrix))
        
        return distances, get_path, predecessors


class FlowUpdaterMatrix:
    """Updates graph edges with passenger flow data"""
    def __init__(self, adj_matrix: np.ndarray):
        self.adj_matrix = adj_matrix

                
    def update_flow(self, path_idx: List[int], counter: int) -> None:
        """Update flow counters for a specific path"""
    
        for i,j in zip(path_idx[0:-1] ,path_idx[1:]):
            self.adj_matrix[i,j] += counter
            

 
    
def main():
    G = load_metro_graph()
    
    # Charger le graph et les données passagers
    data_loader = PassengerDataLoader()
    repository = PassengerFlowRepository(data_loader)
    flows = repository.get_all_flows()
    
    station_to_idx = {name: idx for idx, name in enumerate(G.nodes()) }
    
    # Initialiser le processeur GPU
    processor = Dijkstra_GPU(nx.to_numpy_array(G))  # Remplacer your_graph par votre instance de graphe
    
    # Calculer tous les chemins
    distances, get_path, predecessors = processor.process_passenger_flows(flows)
    
    updater = FlowUpdaterMatrix(processor.adj_matrix)
    
    # Afficher les résultats
  
    for flow in flows:
        #print(f"{flow.source} ({processor.station_to_idx[flow.source]})-> {flow.destination} ({processor.station_to_idx[flow.destination]}) : {' -> '.join(list(map(lambda idx: processor.idx_to_station[idx], get_path(processor.station_to_idx[flow.source], processor.station_to_idx[flow.destination] , predecessors))))}")
        local_path = get_path(station_to_idx[flow.source], station_to_idx[flow.destination] , predecessors)
        
        updater.update_flow(local_path, flow.count)
    
    print(updater.adj_matrix)
        
if __name__ == "__main__":
    main()