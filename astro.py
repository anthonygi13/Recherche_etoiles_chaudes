# 18 septembre 2017
# astro.py
# projet S3

def lire_fichier(fichier):
    """
    :param fichier: nom du fichier en chaine de caractere. Le fichier est trié par colonnes
    :return: retourne listes qui correspondent chacune à une colonne du fichier
    """
    fo = open(fichier, 'r')
    data = fo.read()
    fo.close()
    for i in data:
        if i == "\n":
            print("c bon il detecte les sauts à la ligne")

lire_fichier("data_modifié.txt")