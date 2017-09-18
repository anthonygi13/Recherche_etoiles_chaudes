# 18 septembre 2017
# astro.py
# projet S3

from re import * #pour les expressions régulières

fo = open("data_modifié.txt", 'r')
data = fo.read()
fo.close()

def lire_fichier(fichier):
    """
    :param fichier: nom du fichier en chaine de caractere. Le fichier est trié par colonnes
    :return: retourne listes qui correspondent chacune à une colonne du fichier
    """