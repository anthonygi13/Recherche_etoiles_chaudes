# 21 septembre 2017
# astro_v2.py

def B3V_eq(x):
    """
    :param x: abcsisse du point de la ligne B3V dont on veut obtenir l'ordonnée
    :return: ordonnée du point de la ligne B3V correspondant à l'abscisse x (dans un graphique u-g vs g-r)
    """
    return 0.9909 * x - 0.8901

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


find_hot_stars("data_modifie.txt", "etoiles_chaudes_et_massives.txt", 6, 7)