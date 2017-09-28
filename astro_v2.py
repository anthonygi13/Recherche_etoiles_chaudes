# 21 septembre 2017
# astro_v2.py

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
            u_g = float(u_g)
        if g_r == "":
            g_r = None
        else:
            g_r = float(g_r)
        yield g_r, u_g
        line = data.readline()

    data.close()


def recupere_magnitudes(filename, n_u_g, n_g_r):
    colonne_u_g = []
    colonne_g_r = []
    for g_r, u_g in lignes(filename, n_u_g, n_g_r):
        colonne_u_g.append(u_g)
        colonne_g_r.append(g_r)
    return colonne_g_r, colonne_u_g


def find_hot_stars(input_file, output_file, n_u_g, n_g_r):
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
            print(i)
        print("avancement : ", i)
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


def trace_graph(liste_g_r, liste_u_g, listeX_SP, listeY_SP, nlistX, nlistY):
    """
    :param liste_g_r: liste des valeurs de g_r
    :param liste_u_g: liste des valeurs de u_g=
    :param listex_SP: liste des valeurs de g_r (axe des ordonnees) de la sequence principale
    :param listey_SP: liste des valeurs de u_g (axe des abcisses) de la séquence principale
    """
    m = min([x for x in liste_g_r if x!= None]) #trace ligne de B3V
    M = max([y for y in liste_g_r if y != None])
    x = np.linspace(m, M, 100)
    plot(x, B3V_eq(x))


    plot(listeX_SP,listeY_SP, 'r-', lw=2)

    plt.xlabel('g-r')
    plt.ylabel('u-g')
    plt.gca().invert_yaxis()

    plt.scatter(np.array(liste_g_r), np.array(liste_u_g), s=10 , c='orange') #met les etoiles sur le graphe
    plt.scatter(np.array(nlistX), np.array(nlistY), s=10, c='blue')

    plt.show()




#find_hot_stars("data_modifie.txt", "catalogue_etoiles_chaudes.txt", 6, 7)




for i in range(300000000):
    print(i)



















