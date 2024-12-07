import networkx as nx
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
    return graph_inverted

# test = [[1, 1, 1, 1],
#         [1, 1, 1, 0],
#         [1, 1, 1, 0],
#         [1, 0, 0, 1]]

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

test_mat = read_matrix_from_file("test/message.txt")
test_mat.remove([])

cpt = 0
for i in test_mat:
    for j in i:
        cpt += j

print(cpt)


print(len(inverse_node_edge(test_mat).keys()))
newG = nx.from_dict_of_dicts(inverse_node_edge(test_mat), create_using=nx.DiGraph)
print(newG)
# print(newG.edges)