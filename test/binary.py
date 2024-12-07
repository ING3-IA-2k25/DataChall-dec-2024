def compressMat(mat : list) -> list:
    tab = [[len(mat), len(mat[0])], [], []]
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j]:
                tab[1].append(j + i * len(mat[0]))
                tab[2].append(mat[i][j])
    return tab

def decompressMat2(mat : list) -> list:
    res = [[0 for _ in range(mat[0][1])] for _ in range(mat[0][0])]
    for i in range(len(mat[1])):
        x = mat[1][i] // mat[0][1]
        y = mat[1][i] % mat[0][1]
        res[x][y] = mat[2][i]
    return res
