import networkx as nx
import numpy as np
def inverse_node_edge(mat_adj_input : list) -> list:
    graph = []
    for i in range(len(mat_adj_input)):
        graph.append([])
        for j in range(len(mat_adj_input[0])):
            if mat_adj_input[i][j]:
                graph[i].append(j)
    graph_inverted = {}
    for i in range(len(graph)):
        for j in range(len(graph[i])):
            graph_inverted[f"{i},{graph[i][j]}"] = {}
    for k in graph_inverted.keys():
        k2 = k.split(",")
        for i in range(len(mat_adj_input[int(k2[1])])):
            if mat_adj_input[int(k2[1])][i]:
                graph_inverted[k][f"{k2[1]},{i}"] = {"weight" : 1}
            
    return nx.from_dict_of_dicts(graph_inverted, create_using=nx.DiGraph)

def inverse_node_edge_mat2mat(mat_adj_input: np.ndarray) -> np.ndarray:
    """
    Convertit une matrice d'adjacence nœud-nœud en une matrice d'adjacence arête-arête.
    
    :param mat_adj_input: Matrice d'adjacence (numpy.ndarray) pour un graphe orienté.
                          mat_adj_input[i, j] = 1 si arête de i vers j, 0 sinon.
    :return: Matrice d'adjacence arête-arête (numpy.ndarray).
    """
    # Récupération de la liste des arêtes à partir de la matrice d'adjacence
    # np.nonzero(mat_adj_input) renvoie les indices (i, j) où mat_adj_input[i, j] != 0
    edges = np.transpose(np.nonzero(mat_adj_input))  # edges est un tableau de shape (nb_arêtes, 2)

    # edges[:,0] : nœuds de départ de chaque arête
    # edges[:,1] : nœuds d'arrivée de chaque arête
    starts = edges[:, 0]
    ends = edges[:, 1]

    # Nombre d'arêtes
    num_edges = edges.shape[0]

    # Création de la matrice résultat : arête -> arête
    # On veut mat_res[i,j] = 1 si l'arête i se termine là où l'arête j commence
    # C'est-à-dire si ends[i] == starts[j]
    # On peut vectoriser cette opération :
    mat_res = (ends[:, np.newaxis] == starts[np.newaxis, :]).astype(int)

    return mat_res
        

test = [[1, 1, 1, 1],
        [1, 1, 1, 0],
        [1, 1, 1, 0],
        [1, 0, 0, 1]]

def read_matrix_from_file(file_path):
    matrix = []
    with open(file_path, 'r') as file:
        content = file.read()
        # Remove square brackets
        content = content.replace('[', '').replace(']', '')
        # Split the content into rows
        rows = content.split('\n')
        for row in rows:
            # Split the row into individual elements and convert them to integers
            row_elements = list(map(int, row.split()))
            # Append the row to the matrix
            matrix.append(row_elements)
    return matrix

if __name__ == '__main__':
    #test_mat = read_matrix_from_file("test/message.txt")
    #test_mat.remove([])

    # cpt = 0
    # for i in test_mat:
    #     for j in i:
    #         cpt += j

    # print(cpt)
    print(inverse_node_edge_mat2mat(test))

    # print(len(inverse_node_edge(test).keys()))
    # newG = nx.from_dict_of_dicts(inverse_node_edge(test_mat), create_using=nx.DiGraph)
    # print(newG)
