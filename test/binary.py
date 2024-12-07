from math import log2
import sys

def compressMat(mat : list) -> list:
    max_int_log2 = int(log2(sys.maxsize))
    compressed_mat = []
    compressed_len = len(mat[0]) // max_int_log2 + (len(mat[0]) % max_int_log2 != 0)
    for i in range(len(mat)):
        compressed_mat.append([])
        to_add = 0
        for j in range(len(mat[i])):
            to_add <<= 1
            to_add += mat[i][j]
            if (j+1) % max_int_log2 == 0:
                compressed_mat[i].append(to_add)
                to_add = 0
        if len(compressed_mat[i]) < compressed_len:
            compressed_mat[i].append(to_add)
    return compressed_mat

def decompressMat(mat : list) -> list:
    max_int_log2 = int(log2(sys.maxsize))
    decompressed_mat = []
    for i in range(len(mat)):
        decompressed_mat.append([])
        for idx in range(len(mat[i])):
            integer = mat[i][idx]
            temp = []
            for j in range(max_int_log2):
                if j + idx * max_int_log2 >= len(mat):
                    break
                temp.append(integer%2)
                integer >>= 1
            j = 0
            # print(temp)
            temp.reverse()
            decompressed_mat[i]+=temp
            
    return decompressed_mat

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
# test_mat = [[1, 1, 1, 1, 1],
#             [0, 0, 0, 0, 0],
#             [1, 1, 1, 0, 0],
#             [0, 0, 0, 0, 1],
#             [1, 0, 0, 0, 0]]
comp = compressMat(test_mat)
decomp = decompressMat(comp)
# print(test_mat)
print(comp)
# print(decomp)
egal(test_mat, decomp)