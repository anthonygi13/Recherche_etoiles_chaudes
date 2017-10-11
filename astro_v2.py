# 21 septembre 2017
# astro_v2.py

from pylab import *
import os


def B3V_eq(x):
    """
    :param x: abcsisse du point de la ligne B3V dont on veut obtenir l'ordonnee
    :return: ordonnee du point de la ligne B3V correspondant a l'abscisse x (dans un graphique u-g vs g-r)
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
    :return: liste avec les donnees de la colonne g-r dans le fichier filename, et une autre avec celles de u-g
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
    nfile = open(output_file, "w")
    line = data.readline()

    i = 0

    while line != "":
        i += 1
        if i % 10000 == 0:
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


def fichier_reg(input_file, output_file, n_alpha, n_delta):
    """

    :param input_file: fichier avec les etoiles chaudes
    :param output_file: fichier en .reg
    :param n_alpha: colonne avec les coordonees alpha de l'etoile
    :param n_delta: colonne avec les coordonnees delta de l'etoile
    :return: None
    """
    data = open(input_file, 'r')
    nfile = open(output_file, "w")
    line = data.readline()

    nfile.write('# Region file format: DS9 version 4.1\n')
    nfile.write('global color=green dashlist=8 3 width=1 font=\"helvetica 10 normal roman\" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1\n')
    nfile.write('fk5\n')

    while line != "":
        alpha = ""
        delta = ""
        n_colonne = 1

        for char in line:
            if char == "|":
                n_colonne += 1
            if n_colonne == n_alpha:
                if char != " " and char != "|":
                    alpha += char
            elif n_colonne == n_delta:
                if char != " " and char != "|":
                    delta += char
            if n_colonne > max(n_alpha, n_delta):
                break

        nfile.write('circle(' + alpha + ',' + delta + ',5\")\n')
        line = data.readline()

    data.close()
    nfile.close()


def trace_graphique(titre, data_filename, SP_filename, n_g_r_data, n_u_g_data, n_g_r_SP, n_u_g_SP,
                    hot_stars_filename=None):
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

    # recupere donnees
    g_r_data, u_g_data = recupere_magnitudes(data_filename, n_g_r_data, n_u_g_data)
    g_r_SP, u_g_SP = recupere_magnitudes(SP_filename, n_g_r_SP, n_u_g_SP)

    # parametre le graphique
    plt.xlabel('g-r')
    plt.ylabel('u-g')
    plt.gca().invert_yaxis()

    # trace u-g vs g-r avec nos donnees
    plt.plot(g_r_data, u_g_data, '.', c='red', label='Étoiles')
    if hot_stars_filename != None:
        g_r_hot_stars, u_g_hot_stars = recupere_magnitudes(hot_stars_filename, n_g_r_data, n_u_g_data)
        plt.plot(g_r_hot_stars, u_g_hot_stars, '.', c='blue', label='Étoiles chaudes')

    # trace ligne B3V
    m = min([x for x in g_r_data if x != None])
    M = max([y for y in g_r_data if y != None])
    x = np.linspace(m, M, 100)
    plt.plot(x, B3V_eq(x), c='orange', label='Ligne B3V')

    # trace sequence principale
    plt.plot(g_r_SP, u_g_SP, c='black', label='Séquence principale')

    # met le titre et affiche le tout
    title(titre)
    plt.legend()
    plt.show()

def traiter_data(input_file, output_file_hot_stars, output_file_reg, output_folder=None ,n_g_r=7, n_u_g=6, n_alpha=1, n_delta=2):
    if output_folder is not None:
        if not os.path.exists(output_folder):
            os.system("mkdir " + output_folder)
        input_file = output_folder + "/" + input_file
        output_file_hot_stars = output_folder + "/" + output_file_hot_stars
        output_file_reg = output_folder + "/" + output_file_reg
    if not os.path.exists(input_file):
        print("le fichier ", input_file, " n'existe pas")
    if os.path.exists(output_file_hot_stars):
        reponse = input("Le fichier " + output_file_hot_stars + " existe deja : voulez vous l'ecraser ? (o/n) ")
        if reponse == "n":
            while os.path.exists(output_file_hot_stars):
                output_file_hot_stars = "new_" + output_file_hot_stars
    if os.path.exists(output_file_reg):
        reponse = input("Le fichier " + output_file_reg + " existe deja : voulez vous l'ecraser ? (o/n) ")
        if reponse == "n":
            while os.path.exists(output_file_reg):
                output_file_reg = "new_" + output_file_reg


    print("\noutput_file_hot_stars = ", output_file_hot_stars)
    print("output_file_reg = ", output_file_reg)

    find_hot_stars(input_file, output_file_hot_stars, n_g_r, n_u_g)
    print("\ncatalogue d'etoiles chaudes ecrit")

    fichier_reg(output_file_hot_stars, output_file_reg, n_alpha, n_delta)
    print("\nfichier .reg ecrit")


def get_picture(output_file, region_name, x_size, y_size, output_folder=None, coordinate_system="J2000", survey="DSS2-red", ra="", dec=""):
    output_file_for_terminal = ""
    for char in output_file:
        if char == " ":
            output_file_for_terminal += "\ "
        else:
            output_file_for_terminal += char

    if output_folder is not None:
        output_folder_for_terminal = ""
        for char in output_folder:
            if char == " ":
                output_folder_for_terminal += "\ "
            else:
                output_folder_for_terminal += char
        print(output_folder_for_terminal)
        if not os.path.exists(output_folder):
            os.system("mkdir " + output_folder_for_terminal)
        output_file_for_terminal = output_folder_for_terminal + "/" + output_file_for_terminal

    region_name_for_link = ""
    region_name_for_terminal = ""
    for char in region_name:
        if char == " ":
            region_name_for_link += "+"
            region_name_for_terminal += "\ "
        else:
            region_name_for_link += char
            region_name_for_terminal += char

    os.system("wget 'archive.eso.org/dss/dss/image?ra=" + ra + "&dec=" + dec + "&equinox=" + coordinate_system + "&name="
              + region_name_for_link + "&x=" + str(x_size) + "&y=" + str(y_size) + "&Sky-Survey=" + survey
              + "&mime-type=download-fits&statsmode=WEBFORM' -O " + output_file_for_terminal)


def recup_catalogue(region_name, output_file, cone_size, output_folder=None, size_unit='arcmin'):
    output_file_for_terminal = ""
    for char in output_file:
        if char == " ":
            output_file_for_terminal += "\ "
        else:
            output_file_for_terminal += char
    if output_folder is not None:
        output_folder_for_terminal = ""
        for char in output_folder:
            if char == " ":
                output_folder_for_terminal += "\ "
            else:
                output_folder_for_terminal += char
        if not os.path.exists(output_folder):
            os.system("mkdir " + output_folder_for_terminal)
        output_file_for_terminal = output_folder_for_terminal + "/" + output_file_for_terminal

    region_name_for_link = ""
    region_name_for_terminal = ""
    for char in region_name:
        if char == " ":
            region_name_for_link += "+"
            region_name_for_terminal += "\ "
        else:
            region_name_for_link += char
            region_name_for_terminal += char

    os.system("wget '" + 'http://vizier.cfa.harvard.edu/viz-bin/asu-tsv/VizieR?-source=II/341/&-oc.form=dec&-out.max=unlimited&-c='
              + region_name_for_link + '&-c.eq=J2000&-c.r=' + cone_size + '&-c.u=' + size_unit
              + '&-c.geom=r&-out=RAJ2000&-out=DEJ2000&-out=u-g&-out=g-r2&-out=umag&-out=e_umag&-out=gmag&-out=e_gmag&-out=r2mag&-out=e_r2mag&-out=Hamag&-out=e_Hamag&-out=rmag&-out=e_rmag&-out=imag&-out=e_imag&-out.add=_Glon,_Glat&-oc.form=dec&-out.form=|+-Separated-Values'
              + "' -O " + output_file_for_terminal)

"""
def traiter_data(region_name, output_file_picture, output_file_data, output_file_data_reg, xsize_picture, ysize_picture ,size, output_folder=None, coordinate_system="J2000", survey="DSS2-red", ra="", dec="", n_g_r=7, n_u_g=6, n_alpha=1, n_delta=2):
    if output_folder is not None:
        if not os.path.exists(output_folder):
            os.system("mkdir " + output_folder)

        #ici il faut changer les noms des fichiers
        output_file_picture = output_folder + "/" + output_file_picture
        output_file_data = output_folder + "/" + output_file_data
        output_file_data_reg = output_folder + "/" + output_file_data_reg


    recup_catalogue(region_name, 'data', str(size), output_folder)

    get_picture(output_file_picture, region_name, str(xsize_picture), str(ysize_picture), output_folder, coordinate_system, survey, ra, dec)
    traiter_data('data', output_file_data, output_file_data_reg, output_folder, n_g_r, n_u_g, n_alpha, n_delta)
"""

def analyser_region(region_name, cone_size, output_folder, output_file_data, output_file_data_hot_stars, output_file_reg, output_file_fit, output_file_plot):
    """garder que les deux premiers parametres completer les autres automatiquement en fonctino du nom de la region et de la taille du ciel"""
    output_folder = region_name + "\ (" + cone_size + "arcmin)"









get_picture("image.fits", "RCW 49", 10, 10, output_folder = "dossier test")

#traiter_data("data_modifie.txt", "etoiles_chaudes_et_massives.txt", "catalogue.reg")

#trace_graphique("u-g vs g-r, région HII RCW 49, cone search : 3\'", "data_modifie.txt", "SP.txt", 7, 6, 4, 3,
                #"etoiles_chaudes_et_massives.txt")


#os.system("wget 'archive.eso.org/dss/dss/image?ra=&dec=&equinox=J2000&name=RCW+49&x=10&y=10&Sky-Survey=DSS2-red&mime-type=download-fits&statsmode=WEBFORM' -O image.fits")

#os.system("wget 'http://vizier.cfa.harvard.edu/viz-bin/asu-tsv/VizieR?-source=II/341/&-oc.form=dec&-out.max=unlimited&-c=RCW+49&-c.eq=J2000&-c.r=3&-c.u=arcmin&-c.geom=r&-out=RAJ2000&-out=DEJ2000&-out=u-g&-out=g-r2&-out=umag&-out=e_umag&-out=gmag&-out=e_gmag&-out=r2mag&-out=e_r2mag&-out=Hamag&-out=e_Hamag&-out=rmag&-out=e_rmag&-out=imag&-out=e_imag&-out.add=_Glon,_Glat&-oc.form=dec&-out.form=|+-Separated-Values' -O test.txt")

#os.system("ds9 image.fits -regions catalogue.reg")

#fonction("RCW 49", "image.fits", "etoiles_chaudes_et_massives.txt", "catalogue.reg", 10, 10, 3, output_folder="nouveau_dossier_test_3_42")




