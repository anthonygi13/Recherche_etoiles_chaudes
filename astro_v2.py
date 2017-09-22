# 21 septembre 2017
# astro_v2.py

# import matplotlib.pyplot as plt
# import numpy as np
from pylab import *


def B3V_eq(x):
    """
    :param x: abcsisse du point de la ligne B3V dont on veut obtenir l'ordonnée
    :return: ordonnée du point de la ligne B3V correspondant à l'abscisse x (dans un graphique u-g vs g-r)
    """
    return 0.9909 * x - 0.8901



def lignes(filename, n_u_g, n_g_r):
    """
    :param filename:
    :param n_u_g:
    :param n_g_r:
    :return:
    """

    data = open(filename, 'r')
    line = data.readline()

    while line != "":
        u_g = ""
        g_r = ""
        n_colonne = 1
        for char in line:
            if char == "|":
                n_colonne += 1
            if n_colonne == n_u_g:
                if char != " " and char != "|":
                    u_g += char
            elif n_colonne == n_g_r:
                if char != " " and char != "|":
                    g_r += char
            if n_colonne > max(n_u_g, n_g_r):
                break
        if u_g == "":
            u_g = None
        else:
            u_g == float(u_g)
        if g_r == "":
            g_r = None
        else:
            g_r == float(g_r)
        yield u_g, g_r

    data.close()
    nfile.close()


def recupere_magnitudes(filename, n_u_g, n_g_r):
    colonne_u_g = []
    colonne_g_r = []
    for u_g, g_r in lignes(filename, n_u_g, n_u_r):
        colonne_u_g.append(u_g)
        colonne_g_r.append(g_r)
    return colonne_u_g, colonne_g_r


def find_hot_stars(input_file, output_file, n_u_g, n_g_r):
    """
    :param input_file: nom du fichier qui contient les donnees d'entree correspondant a des etoiles
    :param output_file: nom du fichier qui contiendra les donnees correspondant uniquement aux etoiles chaudes
    :param n_u_g: numero de la colonne correspondant a u-g dans le fichier d'entree
    :param n_g_r: numero de la colonne correspondant a g-r dans le fichier d'entree
    :return: None : cree juste le nouveau fichier dans le meme repertoire que celui dans lequel se trouve le programme
    """
    data = open(input_file, 'r')
    line = data.readline()

    while line != "":
        u_g = ""
        g_r = ""
        n_colonne = 1
        for char in line:
            if char == "|":
                n_colonne += 1
            if n_colonne == n_u_g:
                if char != " " and char != "|":
                    u_g += char
            elif n_colonne == n_g_r:
                if char != " " and char != "|":
                    g_r += char
            if n_colonne > max(n_u_g, n_g_r):
                break
        if u_g != "" and g_r != "" and float(u_g) <= B3V_eq(float(g_r)):
            nfile = open(output_file, "a")
            nfile.write(line)
        line = data.readline()

    data.close()
    nfile.close()


def recupere_magnitudes(input_file, n_u_g, n_g_r):
    """

    :param input_file: nom du fichier qui contient les donnees d'entree correspondant a des etoiles
    :param n_u_g: numero de la colonne correspondant a u-g dans le fichier d'entree
    :param n_g_r: numero de la colonne correspondant a g-r dans le fichier d'entree
    :return: les listes des valeurs de u-g puis celle de g-r
    """

    liste_g_r = []
    liste_u_g = []

    data = open(input_file, 'r')
    line = data.readline()

    while line != "":
        u_g = ""
        g_r = ""
        n_colonne = 1

        for char in line:
            if char == "|":
                n_colonne += 1
            if n_colonne == n_u_g:
                if char != " " and char != "|":
                    u_g += char
            elif n_colonne == n_g_r:
                if char != " " and char != "|":
                    g_r += char
            if n_colonne > max(n_u_g, n_g_r):
                break

        liste_g_r.append(float(g_r))
        liste_u_g.append(float(u_g))

    data.close()

    return liste_g_r, liste_u_g

def recupere_SP(input_file, n_u_g, n_g_r):
    """

    :param input_file: nom du fichier qui contient les donnees d'entree correspondant a des etoiles
    :param n_u_g: numero de la colonne correspondant a u-g dans le fichier d'entree
    :param n_g_r: numero de la colonne correspondant a g-r dans le fichier d'entree
    :return: les listes des valeurs de u-g puis celle de g-r
    """

    listeX_SP = []
    listeY_SP = []

    data = open(input_file, 'r')
    line = data.readline()

    while line != "":
        u_g = ""
        g_r = ""
        n_colonne = 1

        for char in line:
            if char == " ":
                n_colonne += 1
            if n_colonne == n_u_g:
                if char != " " and char != "|":
                    u_g += char
            elif n_colonne == n_g_r:
                if char != " " and char != "|":
                    g_r += char
            if n_colonne > max(n_u_g, n_g_r):
                break

        listeX_SP.append(float(g_r))
        listeY_SP.append(float(u_g))

    data.close()

    return listeX_SP, listeY_SP


def trace_graph(liste_g_r, liste_u_g, listeX_SP, listeY_SP):
    """

    :param liste_g_r: liste des valeurs de g_r
    :param liste_u_g: liste des valeurs de u_g
    :param listex_SP: liste des valeurs de g_r (axe des x) de la séquence principale
    :param listey_SP: liste des valeurs de u_g (axe des y) de la séquence principale

    """
    m1 = liste_g_r.min() #trace ligne de B3V
    M1 = liste_g_r.max()
    x = np.linspace(m1, M1, 100)
    plot(x, B3V_eq(x))


    plot(listeX_SP,listeY_SP, 'r-', lw=2)

    plt.xlabel('g-r')
    plt.ylabel('u-g')
    plt.gca().invert_yaxis()

    plt.scatter(np.array(liste_g_r), np.array(liste_u_g), s=10) #met les etoiles sur le graphe

    plt.show()



find_hot_stars("data_modifie.txt", "etoiles_chaudes_et_massives.txt", 6, 7)
liste_g_r = recupere_magnitudes("data_modifie.txt",6,7)[0]
liste_u_g = recupere_magnitudes("data_modifie.txt",6,7)[1]
listeX_SP = recupere_SP('Coord_seq_princiaple',4,5)[0]
listeY_SP = recupere_SP('Coord_seq_princiaple',4,5)[1]
trace_graph(liste_g_r,liste_u_g,listeX_SP,listeY_SP)
