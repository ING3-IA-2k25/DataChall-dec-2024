from math import log2
import sys
import numpy as np
import networkx as nx

def compressMat(mat : list) -> list:
    tab = [[len(mat), len(mat[0])], [], []]
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j]:
                tab[1].append(j + i * len(mat[0]))
                tab[2].append(mat[i][j])
    return tab

def decompressMat(mat : list) -> list:
    res = []
    for i in range(mat[0][0]):
        res.append([])
        for j in range(mat[0][1]):
            idx = binary_search(mat[1], j + i * mat[0][1])
            if idx > -1:
                res[i].append(mat[2][idx])
            else:
                res[i].append(0)
    return res

def decompressMat2(mat : list) -> list:
    res = [[0 for _ in range(mat[0][1])] for _ in range(mat[0][0])]
    for i in range(len(mat[1])):
        x = mat[1][i] // mat[0][1]
        y = mat[1][i] % mat[0][1]
        res[x][y] = mat[2][i]
    return res

def binary_search(arr, target):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1

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

def egal(mat1, mat2):
    for i in range(len(mat1)):
        for j in range(len(mat1[i])):
            if mat1[i][j] != mat2[i][j]:
                print(i, j)

test_mat = read_matrix_from_file("test/message.txt")
test_mat.remove([])

test_mat = np.array(test_mat)

truc = nx.from_numpy_array(test_mat, create_using=nx.DiGraph)
for i in range(1000):
    nx.to_numpy_array(truc)

# test_mat = [[1, 1, 1, 1, 1],
#             [0, 0, 0, 0, 0],
#             [1, 1, 1, 0, 0],
#             [0, 0, 0, 0, 1],
#             [1, 0, 0, 0, 0]]
# comp = compressMat(test_mat)
# for i in range(1000):
#     decomp = decompressMat2(comp)
# # print(comp)
# egal(test_mat, decomp)

#decomp : 4s/1000
#comp : 4s/1000