import numpy as np
def compressMat(mat: np.ndarray) -> list:
    """
    Compresse une matrice numpy en une représentation sparse sous forme de liste :
    [
        [nb_lignes, nb_colonnes],
        [liste_des_indices_non_nuls],
        [liste_des_valeurs_non_nuls]
    ]
    """
    rows, cols = mat.shape
    # Aplatir la matrice en un vecteur
    flat_mat = mat.ravel()
    # Obtenir les indices des éléments non-nuls
    indices = np.nonzero(flat_mat)[0]
    # Extraire les valeurs correspondantes
    values = flat_mat[indices]

    # On retourne la structure sous forme de liste
    # (Les indices et valeurs sont convertis en liste pour être conforme à la structure initiale)
    return [[rows, cols], indices.tolist(), values.tolist()]

def decompressMat(cmat: list) -> np.ndarray:
    """
    Décompresse la représentation compressée en une matrice numpy.
    """
    # Récupération de la taille
    rows, cols = cmat[0]
    indices = np.array(cmat[1])
    values = np.array(cmat[2])

    # Crée une matrice de zéros, puis réinsère les valeurs
    res = np.zeros((rows, cols), dtype=values.dtype)
    res.flat[indices] = values
    return res