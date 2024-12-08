from accebilite import save_dataset, load_data_set, create_data_set, create_data_set_part, graphs_to_array, load_data_set, load_dataset_part, save_dataset_part, create_data_set_part_tmp
from metroGraph_oriented import load_metro_graph, GpsCoordinate
from binary import decompressMat

def create_data_set2(num_graphs, max_edge_to_remove):
    # Load the graph
    G = load_metro_graph()

    # Create the dataset
    create_data_set_part(G, num_graphs, max_edge_to_remove)

def dataloader(filename = f"connected_graphs_10000.pkl"):
    matrices_compressed = load_data_set(filename)
    matrices = []
    for matrice_compressed in matrices_compressed:
        matrices.append(decompressMat(matrice_compressed))
    return matrices

def dataloader_compressed(filename = f"connected_graphs_1000.pkl"):
    return load_data_set(filename)

def check_doublon(compressed_matrix):
    seen = set()
    unique_data = []
    for matrice in compressed_matrix:
        key = tuple(matrice[1])
        if key not in seen:
            seen.add(key)
            unique_data.append(matrice)
    return unique_data

def add_unique_data(unique_data, new_data):
    for matrice in new_data:
        unique_data.append(matrice)
    return unique_data

def save_new_dataset_part(new_mat, size):
    for matrice in new_mat:
        save_dataset_part(matrice, f"connected_graphs_{size}.pkl" )
                    
if __name__ == '__main__':
    NUM_GRAPH = 64000
    #create_data_set2(NUM_GRAPH, 30)
    #matrice_compressed = dataloader_compressed()
    #matrice_compressed = check_doublon(matrice_compressed)
    #print(len(matrice_compressed))
    #G = load_metro_graph()
    #while len(matrice_compressed) < NUM_GRAPH:
    #    dataset = create_data_set(G, NUM_GRAPH - len(matrice_compressed), 30)
    #    dataset = graphs_to_array(dataset, G)
    #    matrice_compressed = add_unique_data(matrice_compressed, dataset)
    #    matrice_compressed = check_doublon(matrice_compressed)
    #    print(len(matrice_compressed))
    #print(len(check_doublon(matrice_compressed)))
    #save_dataset(dataset, f"connected_graphs_{NUM_GRAPH}.pkl")
    #create_data_set2(10, 30)

    #G = load_metro_graph()
    #dataset = load_dataset_part(f"connected_graphs_{300}.pkl")
    #dataset = check_doublon(dataset)
    #size = NUM_GRAPH - len(dataset)
    #create_data_set_part_tmp(G, size, 1 ,45)

    #G = load_metro_graph()
    #dataset = load_dataset_part(f"connected_graphs_{300}.pkl")
    #dataset = check_doublon(dataset)
    #new_dataset = load_dataset_part(f"connected_graphs_{1}.pkl")
    #matrice_compressed = add_unique_data(dataset, new_dataset)
    #for matrix in matrice_compressed:
    #    save_dataset_part(matrix, f"connected_graphs_{400}.pkl")
    #matrice_compressed = check_doublon(matrice_compressed)
    #print(len(matrice_compressed))

    #dataset = load_dataset_part(f"connected_graphs_{400}.pkl")
    #dataset = check_doublon(dataset)
    #size = NUM_GRAPH - len(dataset)
    #print(size)
    # On va créer 6 chunks de 10 000 éléments et 1 chunk de 4 000 éléments
    #chunk_sizes = [10000] * 6 + [4000]  # [10000, 10000, 10000, 10000, 10000, 10000, 4000]
    #dataset = load_dataset_part(f"connected_graphs_{64000}.pkl")
    #start_index = 0
    #part_index = 1
#
    #for size in chunk_sizes:
    #    chunk = dataset[start_index:start_index + size]
    #    start_index += size
#
    #    # Nom du fichier pour ce chunk
    #    # Par exemple : "connected_graphs_1_64000_part1.pkl", "connected_graphs_1_64000_part2.pkl", etc.
    #    chunk_filename = f"connected_graphs_{part_index}_{64000}.pkl"
#
    #    # Sauvegarde progressive de chaque élément du chunk
    #    for data in chunk:
    #        save_dataset_part(data, chunk_filename)
#
    #    part_index += 1
    
    chunk_sizes = [10000] * 6 + [4000]
    for i in range(len(chunk_sizes)):
        dataset = load_dataset_part(f"connected_graphs_{i+1}_{64000}.pkl")
        print (len(dataset))
    #size = NUM_GRAPH - len(dataset)
    #create_data_set_part_tmp(G, size, 1 ,45)
    #matrice_compressed = add_unique_data(dataset, new_dataset)
    #matrice_compressed = check_doublon(matrice_compressed)
    #print(len(matrice_compressed))

    # dataloader(), 30)
    # dataloader()
