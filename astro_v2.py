# 21 septembre 2017
# astro_v2.py

from pylab import *


def B3V_eq(x):
    """
    :param x: abcsisse du point de la ligne B3V dont on veut obtenir l'ordonnee
    :return: ordonnée du point de la ligne B3V correspondant à l'abscisse x (dans un graphique u-g vs g-r)
    """

    return 0.9909 * x - 0.8901


def lignes(filename, n_g_r, n_u_g):
    """
    :param filename: nom du fichier qui contient les donnees des etoiles dont on veut connaitre
    les caracteristique u-g et g-r
    :param n_g_r: numero de la colonne correspondant a u-g dans le fichier d'entree
    :param n_u_g: numero de la colonne correspondant a g-r dans le fichier d'entree
    :return: que dalle, c'est un generateur
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
            u_g = float(u_g)
        if g_r == "":
            g_r = None
        else:
            g_r = float(g_r)
        yield g_r, u_g
        line = data.readline()

    data.close()


def recupere_magnitudes(filename, n_g_r, n_u_g):
    """
    :param filename: nom du fichier qui contient les donnees des etoiles dont on veut connaitre
    les caracteristique u-g et g-r
    :param n_g_r: numero de la colonne correspondant a u-g dans le fichier d'entree
    :param n_u_g: numero de la colonne correspondant a g-r dans le fichier d'entree
    :return: liste avec les données de la colonne g-r dans le fichier filename, et une autre avec celles de u-g
    """

    colonne_u_g = []
    colonne_g_r = []
    for g_r, u_g in lignes(filename, n_g_r, n_u_g):
        colonne_u_g.append(u_g)
        colonne_g_r.append(g_r)
    return colonne_g_r, colonne_u_g


def find_hot_stars(input_file, output_file, n_g_r, n_u_g):
    """
    :param input_file: nom du fichier qui contient les donnees d'entree correspondant a des etoiles
    :param output_file: nom du fichier qui contiendra les donnees correspondant uniquement aux etoiles chaudes
    :param n_u_g: numero de la colonne correspondant a u-g dans le fichier d'entree
    :param n_g_r: numero de la colonne correspondant a g-r dans le fichier d'entree
    :return: None : cree juste le nouveau fichier dans le meme repertoire que celui dans lequel se trouve le programme
    """

    data = open(input_file, 'r')
    nfile = open(output_file, "a")
    line = data.readline()

    i = 0

    while line != "":
        i += 1
        if i % 10000 == 0:
            print(print("avancement : ", i))
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
            nfile.write(line)
        line = data.readline()

    data.close()
    nfile.close()


def trace_graphique(titre, data_filename, SP_filename, n_g_r_data, n_u_g_data, n_g_r_SP, n_u_g_SP, hot_stars_filename=None):
    """
    :param titre: titre que l'on veut donner au graphique
    :param data_filename: nom du fichier qui contient les donnees d'entree correspondant a des etoiles
    :param SP_filename: nom du fichier qui contient des coordonnees de points de la sequence principale
    :param n_g_r_data: numero de la colonne correspondant a g-r dans le fichier data_filename
    :param n_u_g_data: numero de la colonne correspondant a u-g dans le fichier data_filename
    :param n_g_r_SP: numero de la colonne correspondant a g-r dans le fichier SP_filename
    :param n_u_g_SP: numero de la colonne correspondant a u-g dans le fichier SP_filename
    :param hot_stars_filename: facultatif, nom du fichier contenant uniquement les donnees des etoiles chaudes
    dans data_filename pour afficher d'une autre couleur les points correspondant aux etoiles chaudes
    :return: None, trace le graphique u-g vs g-r avec la sequance principale et la ligne B3V
    """

    #recupere donnees
    g_r_data, u_g_data = recupere_magnitudes(data_filename, n_g_r_data, n_u_g_data)
    g_r_SP, u_g_SP = recupere_magnitudes(SP_filename, n_g_r_SP, n_u_g_SP)

    #parametre le graphique
    plt.xlabel('g-r')
    plt.ylabel('u-g')
    plt.gca().invert_yaxis()

    #trace u-g vs g-r avec nos donnees
    plt.plot(g_r_data, u_g_data, '.', c='blue', label='Étoiles')
    if hot_stars_filename != None:
        g_r_hot_stars, u_g_hot_stars = recupere_magnitudes(hot_stars_filename, n_g_r_data, n_u_g_data)
        plt.plot(g_r_hot_stars, u_g_hot_stars, '.', c='red', label='Étoiles chaudes')

    # trace ligne B3V
    m = min([x for x in g_r_data if x != None])
    M = max([y for y in g_r_data if y != None])
    x = np.linspace(m, M, 100)
    plt.plot(x, B3V_eq(x), c='orange', label='Ligne B3V')

    # trace sequence principale
    plt.plot(g_r_SP, u_g_SP, c='black', label='Séquence principale')

    #met le titre et affiche le tout
    title(titre)
    plt.legend()
    plt.show()



#find_hot_stars("data_modifie.txt", "etoiles_chaudes_et_massives.txt", 7, 6)

trace_graphique("u-g vs g-r, région HII RCW 49, cone search : 2\'", "data_modifie.txt", "SP.txt", 7, 6, 4, 3, "etoiles_chaudes_et_massives.txt")


















