from accebilite import save_dataset, load_data_set, create_data_set, graphs_to_array
from metroGraph_oriented import load_metro_graph, GpsCoordinate
from binary import decompressMat

def create_data_set(num_graphs, max_edge_to_remove):
    # Load the graph
    G = load_metro_graph()

    # Create the dataset
    dataset = create_data_set(G, num_graphs, max_edge_to_remove)
    dataset = graphs_to_array(dataset, G)
    # Save the dataset
    save_dataset(dataset, f"connected_graphs_{num_graphs}.pkl")

def dataloader(filename = f"connected_graphs_10000.pkl"):
    matrices_compressed = load_data_set(filename)
    matrices = []
    for matrice_compressed in matrices_compressed:
        matrices.append(decompressMat(matrice_compressed))
        
