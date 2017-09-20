# 18 septembre 2017
# astro.py
# projet S3


"""equation de la ligne B3V pour un graphique u-g vs g-r : 0.9909 * x - 0.8901"""


import re

def lire_fichier(fichier):
    """
    :param fichier: nom du fichier en chaine de caractere. Le fichier est trie par colonnes
    :return: retourne liste de listes qui correspondent chacune a une colonne du fichier
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
    """
    :param x: abcsisse du point de la ligne B3V dont on veut obtenir l'ordonnée
    :param a: equation de la ligne B3V = a*x+b
    :param b: equation de la ligne B3V = a*x+b
    :return: ordonnée du point de la ligne B3V correspondant à l'abscisse x (dans un graphique u-g vs g-r)
    """
    return a * x + b

def find_hot_stars(u_g, g_r, a, b):
    """
    :param u_g: liste des valeurs de u-g
    :param g_r: liste des valeurs de g-r
    la valeur numero i de u_g et celle de g_r doivent correspondre a la meme etoile (celle qui est a la ligne i dans le fichier texte
    :param a: equation de la ligne B3V = a*x+b
    :param b: equation de la ligne B3V = a*x+b
    :return: listes des numeros des lignes a garder (correspondant aux etoiles chaudes), la premiere ligne est numerote 0
    """
    to_keep = []
    for i, x in enumerate(g_r): #la y a moyen d ameliorer la rapidite je pense
        if u_g[i] != "" and x[i] != "" and u_g[i] < B3V_fo(x, a, b):
            to_keep.append(i)
    return to_keep
