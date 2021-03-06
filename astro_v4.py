# S3 Projet 2017
# Licence MPCI
# Authors:   Bratulic Melanie, mail: m.bratulic@laposte.net
#            Durand-Viel Albane, mail:
#            Giraudo Anthony, mail: anthonygi13@hotmail.fr
#            Marinho Louise, mail : louise.marinho@free.fr
# Creation date : 10/20/2017
# File : astro_v4.py

from pylab import *
import os


def B3V_line(g_r):
    """
    Function which allow plotting the B3V line on the graph
    :param x: abscissa of a point of the line
    :return: ordinate of the point which abscissa is x in a graph of (u-g) as a function of (g-r)
    """

    return 0.9909 * g_r - 0.8901

class Main_sequence_points():
    """
    self.g_r_values and self.u_g_values are in that order an increasing g-r values list and the associated main-sequence stars u-g values list
    """
    def __init__(self):
        self.g_r_values = [-0.299, -0.287, -0.282, -0.271, -0.24, -0.218, -0.186, -0.139, -0.121, -0.1, -0.076, -0.046, -0.005, 0.005,
            0.025, 0.059, 0.125, 0.199, 0.329, 0.387, 0.495, 0.576, 0.63, 0.67, 0.756, 0.845, 0.904, 0.939, 0.978,
            1.049, 1.092, 1.198, 1.386, 1.394, 1.422, 1.425]
        self.u_g_values = [-1.494, -1.463, -1.446, -1.433, -1.324, -1.209, -1.053, -0.828, -0.728, -0.58, -0.388, -0.198, -0.053,
            -0.019, 0.021, 0.038, 0.067, 0.044, -0.026, -0.049, -0.066, -0.04, -0.001, 0.042, 0.162, 0.355, 0.451,
            0.523, 0.602, 0.756, 0.841, 1.064, 1.364, 1.348, 1.311, 1.238]
        assert len(self.g_r_values) == len(self.u_g_values)
        self.point_number = len(self.g_r_values)

def main_sequence(g_r):
    """
    :param g_r: a g-r value
    :return: the theoretic u-g value approximation of a main-sequence star with the inputted g-r value
    """

    main_sequence_points = Main_sequence_points()
    if g_r < main_sequence_points.g_r_values[0]:
        return None
    for i in range(1, main_sequence_points.point_number):
        if g_r <= main_sequence_points.g_r_values[i]:
            return (g_r - main_sequence_points.g_r_values[i]) * ((main_sequence_points.u_g_values[i] - main_sequence_points.u_g_values[i - 1]) / (main_sequence_points.g_r_values[i] - main_sequence_points.g_r_values[i - 1])) + main_sequence_points.u_g_values[i]
    return None


def lines(filename, n_c1, n_c2):
    """
    :param filename: name of file, where the data of the stars are. We want the values of c1 and c2
    :param n_c1: number of column c1 in our file
    :param n_c2: number of column c1 in our file
    :return: nothing, it's a generator
    """

    data = open(filename, 'r')
    line = data.readline()

    while line[0:2] != "--": # the columns start after a line of '-----'
        line = data.readline()

    line = data.readline()

    while line != "":
        c1 = ""
        c2 = ""
        n_colonne = 1
        for char in line:
            if char == "|":
                n_colonne += 1
            if n_colonne == n_c1:
                if char != " " and char != "|":
                    c1 += char
            elif n_colonne == n_c2:
                if char != " " and char != "|":
                    c2 += char
            if n_colonne > max([n_c1, n_c2]):
                break
        if c1 == "":
            c1 = None
        if c2 == "":
            c2 = None
        yield c1, c2
        line = data.readline()

    data.close()


def get_magnitudes(filename, n_g_r, n_u_g):
    """
    Mélanie
    :param filename: name of the file (txt format) containing a table with the data of the scars
    :param n_g_r: index of the column containing the (g-r) characteristic in the file filename
    :param n_u_g: index of the column containing the (u-g) characteristic in the file filename
    :return: 2 lists : the first one containing the data of the (g-r) column in the file filename, and the other one the (u-g) column
    """

    colonne_u_g = []
    colonne_g_r = []
    for g_r, u_g in lines(filename, n_g_r, n_u_g): #for each line of the file filename, takes the characteristic (g-r) and (u-g)
        if u_g is not None: colonne_u_g.append(float(u_g))
        else: colonne_u_g.append(u_g)
        if g_r is not None: colonne_g_r.append(float(g_r))
        else: colonne_g_r.append(g_r)
    return colonne_g_r, colonne_u_g


def find_hot_stars(input_file, output_file, output_folder=None, n_g_r=6, n_u_g=5):
    """
    :param input_file: input file with lines of data separated by
    :param output_file: nom du fichier qui contiendra les donnees correspondant uniquement aux etoiles chaudes
    :param n_u_g: numero de la colonne correspondant a u-g dans le fichier d'entree
    :param n_g_r: numero de la colonne correspondant a g-r dans le fichier d'entree
    :param output_folder: nom du dossier dans lequel on va travailler (la ou y a le fichier d entree et la ou on veut mettre le fichier de sortie)
    :return: None : cree juste le nouveau fichier dans le meme repertoire que celui dans lequel se trouve le programme
    """

    if output_folder is not None:
        output_folder_for_terminal = ""
        for char in output_folder:
            if char == " ":
                output_folder_for_terminal += "\ "
            elif char == "(":
                output_folder_for_terminal += "\("
            elif char == ")":
                output_folder_for_terminal += "\)"
            else:
                output_folder_for_terminal += char
        if not os.path.exists(output_folder):
            os.system("mkdir " + output_folder_for_terminal)
        input_file = output_folder + "/" + input_file
        output_file = output_folder + "/" + output_file

    data = open(input_file, 'r')
    nfile = open(output_file, "w")

    nfile.write("HOT STARS\n")

    line = data.readline()

    while line[0:2] != "--":
        nfile.write(line)
        line = data.readline()

    nfile.write(line)
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
            if n_colonne > max([n_u_g, n_g_r]):
                break
        if u_g != "" and g_r != "" and float(u_g) <= B3V_line(float(g_r)):
            nfile.write(line)
        line = data.readline()

    data.close()
    nfile.close()


def fichier_reg(input_file, output_file, output_folder=None, n_alpha=3, n_delta=4):
    """
    moi
    :param input_file: fichier avec les etoiles chaudes
    :param output_file: fichier en .reg
    :param n_alpha: colonne avec les coordonees alpha de l'etoile
    :param n_delta: colonne avec les coordonnees delta de l'etoile
    :param output_folder: nom du dossier dans lequel on va travailler (la ou y a le fichier d entree et la ou on veut mettre le fichier de sortie)
    :return: None
    """

    if output_folder is not None:
        output_folder_for_terminal = ""
        for char in output_folder:
            if char == " ":
                output_folder_for_terminal += "\ "
            elif char == "(":
                output_folder_for_terminal += "\("
            elif char == ")":
                output_folder_for_terminal += "\)"
            else:
                output_folder_for_terminal += char
        if not os.path.exists(output_folder):
            os.system("mkdir " + output_folder_for_terminal)
        input_file = output_folder + "/" + input_file
        output_file = output_folder + "/" + output_file

    nfile = open(output_file, "w")

    nfile.write('# Region file format: DS9 version 4.1\n')
    nfile.write(
        'global color=green dashlist=8 3 width=1 font=\"helvetica 10 normal roman\" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1\n')
    nfile.write('fk5')

    for alpha, delta in lines(input_file, n_alpha, n_delta):
        nfile.write("\n")
        nfile.write('circle(' + alpha + ',' + delta + ',5\")')

    nfile.close()


def plot_graphic(title, data_filename, SP_filename="SP.txt", n_g_r_data=6, n_u_g_data=5, n_g_r_SP=4, n_u_g_SP=3,
                    hot_stars_filename=None):
    """
    :param title: title of the graphic
    :param data_filename: name of the file, where the input data (the stars) are
    :param SP_filename: name of the file where the points of the main sequence are
    :param n_g_r_data: the number of the column (g-r) in the file 'data_filename'
    :param n_u_g_data: the number of the column (u-g) in the file 'data_filename'
    :param n_g_r_SP: the number of the column (g-r) in the file 'SP_filename' (to plot the main sequence)
    :param n_u_g_SP: the number of the column (u-g) in the file 'SP_filename' (to plot the main sequence)
    :param hot_stars_filename: optional, name of the file with only the data of the hot stars in 'data_filename', to plot with an other color the hot stars
    :return: None, plot graphic u-g vs g-r, the main sequence, B3V line
    """

    # get data
    g_r_data, u_g_data = get_magnitudes(data_filename, n_g_r_data, n_u_g_data)
    g_r_SP, u_g_SP = get_magnitudes(SP_filename, n_g_r_SP, n_u_g_SP)

    # settings of the graph
    plt.xlabel('g-r')
    plt.ylabel('u-g')
    plt.gca().invert_yaxis()

    # plot u-g vs g-r of the stars with our data
    plt.plot(g_r_data, u_g_data, '.', c='red', label='Stars')
    if hot_stars_filename != None:
        g_r_hot_stars, u_g_hot_stars = get_magnitudes(hot_stars_filename, n_g_r_data, n_u_g_data)
        plt.plot(g_r_hot_stars, u_g_hot_stars, '.', c='blue', label='Hot Stars')

    # plot B3V_line
    m = min([x for x in g_r_data if x != None])
    M = max([y for y in g_r_data if y != None])
    x = np.linspace(m, M, 100)
    plt.plot(x, B3V_line(x), c='orange', label='B3V line')

    # plot the main sequence
    plt.plot(g_r_SP, u_g_SP, c='black', label='Main Sequence')

    # add title and legends
    title(title)
    plt.legend()
    plt.show()


def get_sky_picture(region_name, output_file, x_size, y_size, output_folder=None, coordinate_system="J2000",
                survey="DSS2-red", ra="", dec=""):
    """
    Mélanie
    :param region_name:
    :param output_file:
    :param x_size:
    :param y_size:
    :param output_folder:
    :param coordinate_system:
    :param survey:
    :param ra:
    :param dec:
    :return:
    """

    output_file_for_terminal = ""
    for char in output_file:
        if char == " ":
            output_file_for_terminal += "\ "
        elif char == "(":
            output_file_for_terminal += "\("
        elif char == ")":
            output_file_for_terminal += "\)"
        else:
            output_file_for_terminal += char

    if output_folder is not None:
        output_folder_for_terminal = ""
        for char in output_folder:
            if char == " ":
                output_folder_for_terminal += "\ "
            elif char == "(":
                output_folder_for_terminal += "\("
            elif char == ")":
                output_folder_for_terminal += "\)"
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

    os.system(
        "wget 'archive.eso.org/dss/dss/image?ra=" + ra + "&dec=" + dec + "&equinox=" + coordinate_system + "&name="
        + region_name_for_link + "&x=" + str(x_size) + "&y=" + str(y_size) + "&Sky-Survey=" + survey
        + "&mime-type=download-fits&statsmode=WEBFORM' -O " + output_file_for_terminal)


def recup_catalogue(region_name, output_file, cone_size, output_folder=None, size_unit='arcmin'):
    output_file_for_terminal = ""
    for char in output_file:
        if char == " ":
            output_file_for_terminal += "\ "
        elif char == "(":
            output_file_for_terminal += "\("
        elif char == ")":
            output_file_for_terminal += "\)"
        else:
            output_file_for_terminal += char

    if output_folder is not None:
        output_folder_for_terminal = ""
        for char in output_folder:
            if char == " ":
                output_folder_for_terminal += "\ "
            elif char == "(":
                output_folder_for_terminal += "\("
            elif char == ")":
                output_folder_for_terminal += "\)"
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

    os.system(
        "wget '" + 'http://vizier.u-strasbg.fr/viz-bin/asu-tsv/VizieR?-source=II/341/&-oc.form=dec&-out.max=unlimited&-c='
        + region_name_for_link + '&-c.eq=J2000&-c.r=' + str(cone_size) + '&-c.u=' + size_unit
        + '&-c.geom=r&-out=RAJ2000&-out=DEJ2000&-out=u-g&-out=g-r2&-out=umag&-out=e_umag&-out=gmag&-out=e_gmag&-out=r2mag&-out=e_r2mag&-out=Hamag&-out=e_Hamag&-out=rmag&-out=e_rmag&-out=imag&-out=e_imag&-out.add=_Glon,_Glat&-oc.form=dec&-out.form=|+-Separated-Values'
        + "' -O " + output_file_for_terminal)


def save_plot(output_file, input_file, titre, SP_filename="SP.txt", output_folder=None, n_g_r_data=6, n_u_g_data=5, n_g_r_SP=4, n_u_g_SP=3,
              input_file_hot_stars=None):
    """
    moi
    :param titre: titre que l'on veut donner au graphique
    :param input_file: nom du fichier qui contient les donnees d'entree correspondant a des etoiles
    :param SP_filename: nom du fichier qui contient des coordonnees de points de la sequence principale
    :param output_folder: nom du dossier dans lequel on travaille (la ou y a les catalogues d entree (sauf SP) et la ou on met le fichier de sortie)
    :param n_g_r_data: numero de la colonne correspondant a g-r dans le fichier data_filename
    :param n_u_g_data: numero de la colonne correspondant a u-g dans le fichier data_filename
    :param n_g_r_SP: numero de la colonne correspondant a g-r dans le fichier SP_filename
    :param n_u_g_SP: numero de la colonne correspondant a u-g dans le fichier SP_filename
    :param input_file_hot_stars: facultatif, nom du fichier contenant uniquement les donnees des etoiles chaudes
    dans data_filename pour afficher d'une autre couleur les points correspondant aux etoiles chaudes
    :return: None, trace le graphique u-g vs g-r avec la sequence principale et la ligne B3V
    """

    if output_folder is not None:
        output_folder_for_terminal = ""
        for char in output_folder:
            if char == " ":
                output_folder_for_terminal += "\ "
            elif char == "(":
                output_folder_for_terminal += "\("
            elif char == ")":
                output_folder_for_terminal += "\)"
            else:
                output_folder_for_terminal += char
        if not os.path.exists(output_folder):
            os.system("mkdir " + output_folder_for_terminal)
        input_file = output_folder + "/" + input_file
        if input_file_hot_stars is not None:
            input_file_hot_stars = output_folder + "/" + input_file_hot_stars
        output_file = output_folder + "/" + output_file

    # recupere donnees
    g_r_data, u_g_data = get_magnitudes(input_file, n_g_r_data, n_u_g_data)
    g_r_SP, u_g_SP = get_magnitudes(SP_filename, n_g_r_SP, n_u_g_SP)

    # parametre le graphique
    plt.xlabel('g-r')
    plt.ylabel('u-g')
    plt.gca().invert_yaxis()

    # trace u-g vs g-r avec nos donnees
    plt.plot(g_r_data, u_g_data, '.', c='red', label='Etoiles')
    if input_file_hot_stars != None:
        g_r_hot_stars, u_g_hot_stars = get_magnitudes(input_file_hot_stars, n_g_r_data, n_u_g_data)
        plt.plot(g_r_hot_stars, u_g_hot_stars, '.', c='blue', label='Etoiles chaudes')

    # trace ligne B3V
    m = min([x for x in g_r_data if x != None])
    M = max([y for y in g_r_data if y != None])
    x = np.linspace(m, M, 100)
    plt.plot(x, B3V_line(x), c='orange', label='Ligne B3V')

    # trace sequence principale
    plt.plot(g_r_SP, u_g_SP, c='black', label='Séquence principale')

    # met le titre et enregistre le tout
    title(titre)
    plt.legend()
    plt.savefig(output_file)


def analyser_region(region_name, cone_size):

    region_name_for_filenames = ""
    for char in region_name:
        if char == " ":
            region_name_for_filenames += "_"
        else:
            region_name_for_filenames += char

    output_folder = region_name_for_filenames + " (" + str(cone_size) + " arcmin)"
    output_folder_for_terminal = ""
    for char in output_folder:
        if char == " ":
            output_folder_for_terminal += "\ "
        elif char == "(":
            output_folder_for_terminal += "\("
        elif char == ")":
            output_folder_for_terminal += "\)"
        else:
            output_folder_for_terminal += char
    output_file_data = region_name_for_filenames + ".data.txt"
    output_file_hot_stars_data = region_name_for_filenames + ".hot_stars_data.txt"
    output_file_reg = region_name_for_filenames + ".reg"
    output_file_fits = region_name_for_filenames + ".fits"
    output_file_plot = region_name_for_filenames + ".plot.png"
    output_file_sky_picture = region_name_for_filenames + ".sky_picture.png"

    recup_catalogue(region_name, output_file_data, cone_size, output_folder)
    get_sky_picture(region_name, output_file_fits, 2 * cone_size, 2 * cone_size, output_folder)
    find_hot_stars(output_file_data, output_file_hot_stars_data, output_folder)
    fichier_reg(output_file_hot_stars_data, output_file_reg, output_folder)
    save_plot(output_file_plot, output_file_data, region_name + " (cone search : " + str(cone_size) + " arcmin)", output_folder=output_folder, input_file_hot_stars=output_file_hot_stars_data)
    oldpwd = os.getcwd()
    os.chdir(output_folder)
    os.system("ds9 " + output_file_fits + " -regions " + output_file_reg + " -saveimage " + output_file_sky_picture + " -exit")
    os.chdir(oldpwd)


"""
plt.plot([i * 0.0001 for i in range(int(5 / 0.0001))], [main_sequence(i * 0.0001) for i in range(int(5 / 0.0001))], '.', c='red')
plt.plot([i * -0.0001 for i in range(int(5 / 0.0001))], [main_sequence(i * -0.0001) for i in range(int(5 / 0.0001))], '.', c='red')
plt.plot(Main_sequence_points().g_r_values, Main_sequence_points().u_g_values, c='black')
plt.show()
"""