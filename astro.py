# 18 septembre 2017
# astro.py
# projet S3


"""equation de la ligne B3V pour un graphique u-g vs g-r : 0.9909 * x - 0.8901"""


import re

def lire_fichier(fichier):
    """
    :param fichier: nom du fichier en chaine de caractere. Le fichier est trié par colonnes
    :return: retourne liste de listes qui correspondent chacune à une colonne du fichier
    """

    nombre = re.compile('-?[0-9]+\.?[0-9]*')
    fo = open(fichier, 'r')
    data = fo.read()
    fo.close()

    nb_colonne = 1
    for char in data:
        if char == "\n":
            break
        if char == "|":
            nb_colonne += 1

    tableau = []
    for i in range(nb_colonne):
        tableau.append([])
    colonne_actuelle = 0
    chaine = ""

    for char in data:
        print(colonne_actuelle)
        if char == "|":
            if nombre.fullmatch(chaine) is not None:
                tableau[colonne_actuelle].append(float(chaine))
            else:
                tableau[colonne_actuelle].append(chaine)
            chaine = ""
            colonne_actuelle += 1
        elif char == "\n":
            if nombre.fullmatch(chaine) is not None:
                tableau[colonne_actuelle].append(float(chaine))
            else:
                tableau[colonne_actuelle].append(chaine)
            chaine = ""
            colonne_actuelle = 0
        elif char != " ":
            chaine += char

    return tableau

def B3V_fo(x, a, b):
    return a * x + b

def find_hot_stars(u_g, g_r, a, b, filename):
    to_keep = []
    for x, i in enumerate(g_r): #la y a moyen d ameliorer la rapidite je pense
        if u_g[i] < B3V_fo(x, a, b):
            to_keep.append(i)

def write_new_file():
    """ """

def read_file_lines():
    """ """
