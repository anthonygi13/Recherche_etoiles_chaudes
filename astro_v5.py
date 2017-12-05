# Authors:   Bratulic Melanie, mail: m.bratulic@laposte.net
#            Durand-Viel Albane, mail:albane.durand-viel@laposte.net
#            Giraudo Anthony, mail: anthonygi13@hotmail.fr
#            Marinho Louise, mail : louise.marinho@free.fr
# Please contact us for any question or information needed

# Creation date : 11/05/2017
# File : astro_v5.py

#a faire : crosscorrelation avec gaia, tester si ça marche bien comme il faut l extinction

# when we are talking about stars data table file, it must be a text file like a csv file, with a special character
# to separate columns and a star associated to each line

from pylab import *
import os
from datetime import datetime

def coefficient_for_g_extinction_calculation():
    """
    :return: coefficient used for g extinction coefficient calculation, A_g = coefficient_for_g_extinction_calculation() * (g-r - (g-r)_0)
    """

    return 3.56

def coefficient_for_u_extinction_calculation():
    """
    :return: coefficient used for u extinction coefficient calculation, A_u = coefficient_for_u_extinction_calculation() * (u-g - (u-g)_0)
    """

    return 4.15

def director_coefficient_B3V_line():
    """
    :return: director coefficient of the line where the B3V stars can be founded on a u-g vs g-r plot because of the extinction
    """

    return 0.9909

def B3V_line(g_r):
    """
    We are calling B3V line the line where the B3V stars can be founded on a u-g vs g-r plot because of the extinction
    Function which allows plotting the B3V line on the graph
    :param x: abscissa of a point of the B3V line
    :return: ordinate of the point which abscissa is x in a graph of (u-g) as a function of (g-r)
    """

    return director_coefficient_B3V_line() * g_r - 0.8901

class Main_sequence_points():
    """
    self.g_r_values and self.u_g_values are in that order an increasing g-r values list and the associated main-sequence stars u-g values list, without considerate extinction
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
    :return: the theoretic u-g value approximation of a main-sequence star with the inputted g-r value, without considerate extinction
             if we are giving a g-r value of a star which can't be find on the main sequence this function returns None
    """

    main_sequence_points = Main_sequence_points()
    if g_r < main_sequence_points.g_r_values[0]:
        return None
    for i in range(1, main_sequence_points.point_number):
        if g_r <= main_sequence_points.g_r_values[i]:
            return (g_r - main_sequence_points.g_r_values[i]) * ((main_sequence_points.u_g_values[i] - main_sequence_points.u_g_values[i - 1]) /
                                                                 (main_sequence_points.g_r_values[i] - main_sequence_points.g_r_values[i - 1])) + \
                   main_sequence_points.u_g_values[i]
    return None


def string_for_link(string):
    """
    :param string: a string
    :return: the inputted string with "  " replacing by "+" and the "+" replacing by "%2b"
             it will be useful to use wget to download data
    """
    final_str = ""
    for char in string:
        if char == " ":
            final_str += "+"
        elif char == "+":
            final_str += "%2b"
        else:
            final_str += char
    return final_str


def lines(filename, n_c1, n_c2, column_separator, begining_str=None, comentary_char=None):
    """
    :param filename : name of the inputted file, where the stars data are, it must be a text file
                      it must be a file like a csv file, with a special character to separate columns and a star associated to each line
    :param n_c1: number of the column c1 in the inputted file
    :param n_c2: number of the column c2 in the inputted file
    :param column_separator: character which separates the columns in the inputted file
    :param begining_str: string which indicates where is the data begining, it must be the last line of the header
    :param comentary_char: character which indicates, at a line begining, that this line is not part of the stars data, to allow comentaries
    :return: it's a generator : generate for each line of the file the data contained in the column c1 and in the column c2
    """

    data = open(filename, 'r')
    line = data.readline()

    if begining_str is not None and begining_str:
        while line[0:len(begining_str)] != begining_str:
            line = data.readline()

    line = data.readline()

    while line != "":
        if comentary_char is None or line[0] != comentary_char:
            c1 = ""
            c2 = ""
            column_number = 1
            for char in line:
                if char == column_separator:
                    column_number += 1
                if column_number == n_c1:
                    if char != " " and char != column_separator and char != "\n":
                        c1 += char
                if column_number == n_c2:
                    if char != " " and char != column_separator and char != "\n":
                        c2 += char
                if column_number > max([n_c1, n_c2]):
                    break
            if c1 == "":
                c1 = None
            if c2 == "":
                c2 = None
            yield c1, c2


        line = data.readline()

    data.close()


def get_magnitudes(filename, n_g_r, n_u_g, column_separator, begining_str=None, comentary_char=None):
    """
    :param filename: name of the inputted file (text format) containing a table with stars data
    :param n_g_r: index of the column containing the (g-r) characteristic in the file filename
    :param n_u_g: index of the column containing the (u-g) characteristic in the file filename
    :param column_separator: character which separates the columns in the inputted file
    :param begining_str: string which indicates where is the data begining, it must be the last line of the header
    :param comentary_char: character which indicates, at a line begining, that this line is not part of the stars data, to allow comentaries
    :return: 2 lists : the first one containing the data of the (g-r) column in the file filename, and the other one the (u-g) column
    """

    u_g_column = []
    g_r_column = []
    for g_r, u_g in lines(filename, n_g_r, n_u_g, column_separator, begining_str, comentary_char): #for each line of the file filename, takes the characteristic (g-r) and (u-g)
        if u_g is not None: u_g_column.append(float(u_g))
        else: u_g_column.append(u_g)
        if g_r is not None: g_r_column.append(float(g_r))
        else: g_r_column.append(g_r)
    return g_r_column, u_g_column


def find_hot_stars(input_file, output_file, n_g_r, n_u_g, column_separator, begining_str=None, comentary_char=None, output_folder=None):
    """
    :param input_file: name of the inputted file (text format) containing a table with stars data
    :param output_file: name of the output file (text format) containing a table containing only the hot stars data
    :param n_g_r: index of the column containing the (g-r) characteristic in the file input_file
    :param n_u_g: index of the column containing the (u-g) characteristic in the file input_file
    :param column_separator: character which separates the columns in the inputted file
    :param begining_str: string which indicates where is the data begining, it must be the last line of the header
    :param comentary_char: character which indicates, at a line begining, that this line is not part of the stars data, to allow comentaries
    :param output_folder: name of the folder where we want to put our new file output_file, if it doesn't exist it's created
                          if the folder name is not None and if the folder already exists we will considerate that the inputted data can be find into this folder
    :return: None
    """

    if output_folder is not None:
        if not os.path.exists(output_folder):
            os.system("mkdir '" + output_folder + "'")
        else:
            input_file = output_folder + "/" + input_file
        output_file = output_folder + "/" + output_file

    data = open(input_file, 'r')
    nfile = open(output_file, "w")

    line = data.readline()

    if begining_str is not None:
        while line[0:len(begining_str)] != begining_str:
            nfile.write(line)
            line = data.readline()

    nfile.write(line)
    line = data.readline()

    i = 0

    while line != "":

        i += 1
        if i % 10000 == 0:
            print(i, " lines already read")

        if comentary_char is None or line[0] != comentary_char:
            u_g = ""
            g_r = ""
            column_number = 1
            for char in line:
                if char == column_separator:
                    column_number += 1
                if column_number == n_u_g:
                    if char != " " and char != column_separator:
                        u_g += char
                elif column_number == n_g_r:
                    if char != " " and char != column_separator:
                        g_r += char
                if column_number > max([n_u_g, n_g_r]):
                    break
            if u_g != "" and g_r != "" and float(u_g) <= B3V_line(float(g_r)):
                nfile.write(line)

        if comentary_char is not None and line[0] == comentary_char:
            nfile.write(line)

        line = data.readline()

    data.close()
    nfile.close()


def write_reg_file_for_ds9(input_file, output_file, n_alpha, n_delta, column_separator, begining_str=None, comentary_char=None, output_folder=None, circle_size=5, circle_color="green"):
    """
    :param input_file: name of the inputted file (text format) containing a table with stars data
    :param output_file: name of the file containing a special file (reg format) with the inputted stars coordinates (J2000) for ds9
    :param n_alpha: index of the column containing the RAJ2000 coordinate in the file input_file
    :param n_delta: index of the column containing the DEJ2000 in the file input_file
    :param column_separator: character which separates the columns in the inputted file
    :param begining_str: string which indicates where is the data begining, it must be the last line of the header
    :param comentary_char: character which indicates, at a line begining, that this line is not part of the stars data, to allow comentaries
    :param output_folder: name of the folder where we want to put our new file output_file, if it doesn't exist it's created
                          if the folder name is not None and if the folder already exists we will considerate that the inputted data can be find into this folder
    :param circle_size: the size of the circles which will be drawn arround the inputted stars (with ds9)
    :param circle_color: the color of the circles which will be drawn arround the inputted stars (with ds9)
    :return:
    """

    if output_folder is not None:
        if not os.path.exists(output_folder):
            os.system("mkdir '" + output_folder + "'")
        else:
            input_file = output_folder + "/" + input_file
        output_file = output_folder + "/" + output_file

    nfile = open(output_file, "w")

    nfile.write('# Region file format: DS9 version 4.1\n')
    nfile.write(
        'global color=' + circle_color + ' dashlist=8 3 width=1 font=\"helvetica 10 normal roman\" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1\n')
    nfile.write('fk5')

    for alpha, delta in lines(input_file, n_alpha, n_delta, column_separator, begining_str, comentary_char):
        nfile.write("\n")
        nfile.write('circle(' + alpha + ',' + delta + ',' + str(circle_size) + '\")')

    nfile.close()


def plot_u_g_vs_g_r(title, filename, n_g_r, n_u_g, column_separator, begining_str=None, comentary_char=None,
                    hot_stars_filename=None, n_g_r_hot_stars=None, n_u_g_hot_stars=None, column_separator_hot_stars=None, begining_str_hot_stars=None, comentary_char_hot_stars=None):
    """
    :param title: title of the graphic
    :param filename: name of the inputted file (text format) containing a table with stars data
    :param n_g_r: index of the column containing the (g-r) data in the file filename
    :param n_u_g: index of the column containing the (u-g) data in the file filename
    :param column_separator: character which separates the columns in the inputted file
    :param begining_str: string which indicates where is the data begining, it must be the last line of the header
    :param comentary_char: character which indicates, at a line begining, that this line is not part of the stars data, to allow comentaries
    :param hot_stars_filename: optional, name of the file with only hot stars data
    :param n_u_g_hot_stars: index of the column containing the (u-g) data in the file filename
    :param n_g_r_hot_stars: index of the column containing the (g-r) data in the file filename
    :param column_separator_hot_stars: character which separates the columns in the inputted file hot_stars_filename
                                       by default it will be the same as column_separtor
    :param begining_str_hot_stars: string which indicates where is the data begining, it must be the last line of the header in the file hot_stars_filename
                                   by default it will be the same as begining_str
    :param comentary_char_hot_stars: character which indicates, at a line begining, that this line is not part of the stars data, to allow comentaries
                                     by default default it will be the same as comentary_char
    :return: None, display a u-g vs g-r plot with the inputted data
    """

    #get data
    g_r, u_g = get_magnitudes(filename, n_g_r, n_u_g, column_separator, begining_str, comentary_char)

    #plot stars
    plt.plot(g_r, u_g, '.', c='red', label='Stars')

    if hot_stars_filename is not None:
        if n_g_r_hot_stars is None:
            n_g_r_hot_stars = n_g_r
        if n_u_g_hot_stars is None:
            n_u_g_hot_stars = n_u_g
        if column_separator_hot_stars is None:
            column_separator_hot_stars = column_separator
        if begining_str_hot_stars is None:
            begining_str_hot_stars = begining_str
        if comentary_char_hot_stars is None:
            comentary_char_hot_stars = comentary_char
        g_r_hot_stars, u_g_hot_stars = get_magnitudes(hot_stars_filename, n_g_r_hot_stars, n_u_g_hot_stars, column_separator_hot_stars, begining_str_hot_stars, comentary_char_hot_stars)
        plt.plot(g_r_hot_stars, u_g_hot_stars, '.', c='blue', label='Hot stars')

    # plot B3V_line
    m = min([x for x in g_r if x != None])
    M = max([y for y in g_r if y != None])
    x = np.linspace(m, M, 100)
    plt.plot(x, B3V_line(x), c='orange', label='B3V stars')

    # plot main sequence
    plt.plot(Main_sequence_points().g_r_values, Main_sequence_points().u_g_values, c='black', label='Main sequence')

    # graph settings
    plt.title(title)
    plt.xlabel('g-r')
    plt.ylabel('u-g')
    plt.gca().invert_yaxis()
    plt.legend()
    plt.show()
    plt.clf()


def save_plot(title, input_file, output_file, n_g_r, n_u_g, column_separator, begining_str=None, comentary_char=None, output_folder=None,
              input_file_hot_stars=None, n_g_r_hot_stars=None, n_u_g_hot_stars=None, column_separator_hot_stars=None, begining_str_hot_stars=None, comentary_char_hot_stars=None):
    """
    :param title: the title of the plot
    :param input_file: name of the inputted file (text format) containing a table with stars data
    :param output_file: string, the plot will be save with this name
    :param n_g_r: index of the column containing the (g-r) data in the file filename
    :param n_u_g: index of the column containing the (u-g) data in the file filename
    :param column_separator: character which separates the columns in the inputted file
    :param begining_str: string which indicates where is the data begining, it must be the last line of the header
    :param comentary_char: character which indicates, at a line begining, that this line is not part of the stars data, to allow comentaries
    :param output_folder: name of the folder where we want to put our new file output_file, if it doesn't exist it's created
                          if the folder name is not None and if the folder already exists we will considerate that the inputted data are placed into this folder
    :param hot_stars_filename: optional, name of the file with only hot stars data
    :param n_u_g_hot_stars: index of the column containing the (u-g) data in the file filename
    :param n_g_r_hot_stars: index of the column containing the (g-r) data in the file filename
    :param column_separator_hot_stars: character which separates the columns in the inputted file hot_stars_filename
                                       by default it will be the same as column_separtor
    :param begining_str_hot_stars: string which indicates where is the data begining, it must be the last line of the header in the file hot_stars_filename
                                   by default it will be the same as begining_str
    :param comentary_char_hot_stars: character which indicates, at a line begining, that this line is not part of the stars data, to allow comentaries
                                     by default default it will be the same as comentary_char
    :return: None, save a u-g vs g-r plot with the inputted data
    """

    if output_folder is not None:
        if not os.path.exists(output_folder):
            os.system("mkdir '" + output_folder + "'")
        else:
            input_file = output_folder + "/" + input_file
            if input_file_hot_stars is not None:
                input_file_hot_stars = output_folder + "/" + input_file_hot_stars
        output_file = output_folder + "/" + output_file

    g_r, u_g = get_magnitudes(input_file, n_g_r, n_u_g, column_separator, begining_str, comentary_char)
    plt.plot(g_r, u_g, '.', c='red', label='Stars')

    if input_file_hot_stars is not None:
        if n_g_r_hot_stars is None:
            n_g_r_hot_stars = n_g_r
        if n_u_g_hot_stars is None:
            n_u_g_hot_stars = n_u_g
        if column_separator_hot_stars is None:
            column_separator_hot_stars = column_separator
        if begining_str_hot_stars is None:
            begining_str_hot_stars = begining_str
        if comentary_char_hot_stars is None:
            comentary_char_hot_stars = comentary_char
        g_r_hot_stars, u_g_hot_stars = get_magnitudes(input_file_hot_stars, n_g_r_hot_stars, n_u_g_hot_stars,
                                                      column_separator_hot_stars, begining_str_hot_stars,
                                                      comentary_char_hot_stars)
        plt.plot(g_r_hot_stars, u_g_hot_stars, '.', c='blue', label='Hot stars')

    # plot B3V_line
    m = min([x for x in g_r if x != None])
    M = max([y for y in g_r if y != None])
    x = np.linspace(m, M, 100)
    plt.plot(x, B3V_line(x), c='orange', label='B3V stars')

    # plot main sequence
    plt.plot(Main_sequence_points().g_r_values, Main_sequence_points().u_g_values, c='black', label='Main sequence')

    # graph settings
    plt.title(title)
    plt.xlabel('g-r')
    plt.ylabel('u-g')
    plt.gca().invert_yaxis()
    plt.legend()
    plt.savefig(output_file)
    plt.clf()


def get_sky_picture(region_name, output_file, x_size, y_size, output_folder=None, coordinate_system="J2000",
                survey="DSS2-red", ra=None, dec=None):
    """
    :param region_name: string, sky region name, can be None if ra and dec are not None
    :param output_file: string, we will obtain a sky picture of the region region_name, it will be saved with the name output_file
    :param x_size: x image size (arcmin)
    :param y_size: y image size (arcmin)
    :param output_folder: name of the folder where we want to put our new file output_file, if it doesn't exist it's created
    :param coordinate_system: string, indicate the coordinate system that will be used for ra or dec
    :param survey: filter used, please see archive.eso.org/dss/dss/
    :param ra: ra of the central point of the picture, can be None if region_name is not None
    :param dec: dec of the central point of the picture, can be None if region_name is not None
    :return: None, download and save a fits picture for ds9
    """

    assert coordinate_system == "J2000" or coordinate_system == "B1950"

    if ra is None:
        ra = ""
    if dec is None:
        dec = ""
    if region_name is None:
        region_name = ""

    assert region_name != "" or ra != "" and dec != ""


    if output_folder is not None:
        if not os.path.exists(output_folder):
            os.system("mkdir '" + output_folder + "'")
        output_file = output_folder + "/" + output_file

    region_name_for_link = string_for_link(region_name)
    ra_for_link = string_for_link(ra)
    dec_for_link = string_for_link(dec)

    os.system(
        "wget 'archive.eso.org/dss/dss/image?ra=" + ra_for_link + "&dec=" + dec_for_link + "&equinox=" + coordinate_system + "&name="
        + region_name_for_link + "&x=" + str(x_size) + "&y=" + str(y_size) + "&Sky-Survey=" + survey
        + "&mime-type=download-fits&statsmode=WEBFORM' -O " + "'" + output_file + "'")


def download_stars_data(position, region_name, output_file, cone_size, coordinate_system = "J2000", output_folder=None, size_unit='arcmin'):
    """
    please have a look to http://vizier.u-strasbg.fr/viz-bin/VizieR-2
    :param position: please have a look to http://vizier.u-strasbg.fr/viz-bin/VizieR-2
    :param region_name: please have a look to http://vizier.u-strasbg.fr/viz-bin/VizieR-2
    :param output_file: the name of the file where we put the downloaded data
    :param cone_size: please have a look to http://vizier.u-strasbg.fr/viz-bin/VizieR-2
    :param coordinate_system: please have a look to http://vizier.u-strasbg.fr/viz-bin/VizieR-2
    :param output_folder: where we want to put our file
    :param size_unit: please have a look to http://vizier.u-strasbg.fr/viz-bin/VizieR-2
    :return: None, download a csv stars data file containing RAJ2000, DEJ2000, u-g, g-r2, umag, e_umag, gmag, e_gmag, Glon, Glat (please have a look to http://vizier.u-strasbg.fr/viz-bin/VizieR-2)
    """

    assert size_unit == "deg" or size_unit == "arcmin" or size_unit == "arcsec"

    if position is None:
        position = ""
    if region_name is None:
        region_name = ""

    assert position != "" or region_name != ""

    if position != "":
        target = position
    else:
        target = region_name

    if output_folder is not None:
        if not os.path.exists(output_folder):
            os.system("mkdir '" + output_folder + "'")
        output_file = output_folder + "/" + output_file

    target_for_link = string_for_link(target)

    os.system(
        "wget '" + 'http://vizier.u-strasbg.fr/viz-bin/asu-tsv/VizieR?-source=II/341/&-oc.form=dec&-out.max=unlimited&-c='
        + target_for_link + '&-c.eq=' + coordinate_system + '&-c.r=' + str(cone_size) + '&-c.u=' + size_unit
        + '&-c.geom=r&-out=RAJ2000&-out=DEJ2000&-out=u-g&-out=g-r2&-out=umag&-out=e_umag&-out=gmag&-out=e_gmag&'
          '-out=r2mag&-out=e_r2mag&-out=Hamag&-out=e_Hamag&-out=rmag&-out=e_rmag&-out=imag&-out=e_imag&'
          '-out.add=_Glon,_Glat&-oc.form=dec&-out.form=;+-Separated-Values'
        + "' -O " + "'" + output_file + "'")


def analyse_region(region_name, cone_size, n_g_r=6, n_u_g=5, column_separator=";", begining_str="--", comentary_char=None,
                    circle_size=5, circle_color="green", output_folder=None, output_file_data=None, output_file_hot_stars_data=None,
                    output_file_reg=None, output_file_fits=None, output_file_plot=None, output_file_sky_picture=None, plot_title=None):
    """
    :param region_name: a region name to analyse
    :param cone_size: the cone size in the sky we want to analyse (arcmin), please have a look to http://vizier.u-strasbg.fr/viz-bin/VizieR-2
    :param n_g_r: the number of the column (g-r) in the data file that will be dowloaded and analysed
    :param n_u_g: the number of the column (u-g) in the data file that will be dowloaded and analysed
    :param column_separator: character which separates the columns in the inputted file
    :param begining_str: string which indicates where is the data begining, it must be the last line of the header
    :param comentary_char: character which indicates, at a line begining, that this line is not part of the stars data, to allow comentaries
    :param circle_size: the size of the circles which will be drawn arround the hot stars on a sky picture (with ds9)
    :param circle_color: the color of the circles which will be drawn arround the hot stars on a sky picture (with ds9)
    :param output_folder: the name of the folder where we put the output files
    :param output_file_data: the name of the stars data file
    :param output_file_hot_stars_data: the name of the hot stars data file
    :param output_file_reg: REG file that will be used for ds9 in order to draw circles arround hot stars, on a sky picture
    :param output_file_fits: sky picture for ds9
    :param output_file_plot: u-g vs g-r plot
    :param output_file_sky_picture: result of the ds9 utilisation, to draw circles arround hot stars, on a sky picture
    :param plot_title: graphic title
    :return: None, creates the ouput file described in commentaries and add (u-g)_0, (g-r)_0 and the extinction coefficients to the stars data files
    """

    region_name_for_filenames = ""
    for char in region_name:
        if char == " ":
            region_name_for_filenames += "_"
        else:
            region_name_for_filenames += char
    if output_folder is None or output_folder == "": output_folder = region_name_for_filenames + " (" + str(cone_size) + " arcmin)"
    if output_file_data is None or output_file_data == "": output_file_data = region_name_for_filenames + ".data.txt"
    if output_file_hot_stars_data is None or output_file_hot_stars_data == "": output_file_hot_stars_data = region_name_for_filenames + ".hot_stars_data.txt"
    if output_file_reg is None or output_file_reg == "": output_file_reg = region_name_for_filenames + ".reg"
    if output_file_fits is None or output_file_fits == "": output_file_fits = region_name_for_filenames + ".fits"
    if output_file_plot is None or output_file_plot == "": output_file_plot = region_name_for_filenames + ".plot.png"
    if output_file_sky_picture is None or output_file_sky_picture == "": output_file_sky_picture = region_name_for_filenames + ".sky_picture.png"
    if plot_title is None:
        plot_title = region_name + " (cone search : " + str(cone_size) + " arcmin)"

    download_stars_data(None, region_name, output_file_data + "old", cone_size, output_folder=output_folder)
    get_sky_picture(region_name, output_file_fits, 2 * cone_size, 2 * cone_size, output_folder)
    write_extinction(output_file_data + "old", output_file_data, n_g_r, n_u_g, column_separator, begining_str, comentary_char, output_folder)
    os.system("rm " + "'" + output_folder + "/" + output_file_data + "old" + "'")
    find_hot_stars(output_file_data, output_file_hot_stars_data, n_g_r, n_u_g, column_separator=column_separator, begining_str=begining_str, comentary_char=comentary_char, output_folder=output_folder)
    write_reg_file_for_ds9(output_file_hot_stars_data, output_file_reg, n_alpha=3, n_delta=4, column_separator=column_separator, begining_str=begining_str,
                           comentary_char=comentary_char, output_folder=output_folder, circle_size=circle_size, circle_color=circle_color)
    save_plot(plot_title, output_file_data, output_file_plot, n_g_r, n_u_g, column_separator=column_separator, begining_str=begining_str, comentary_char=comentary_char, output_folder=output_folder,
              input_file_hot_stars=output_file_hot_stars_data, n_g_r_hot_stars=n_g_r, n_u_g_hot_stars=n_u_g,
              column_separator_hot_stars=column_separator, begining_str_hot_stars=begining_str, comentary_char_hot_stars=comentary_char)
    oldpwd = os.getcwd()
    os.chdir(output_folder)
    os.system("ds9 " + output_file_fits + " -regions " + output_file_reg + " -saveimage " + output_file_sky_picture + " -exit")
    os.chdir(oldpwd)


def find_g_r_0_u_g_0(g_r, u_g):
    """
    :param g_r: a star g-r value
    :param u_g: the same star u-g value
    :return: g-r0 : the (g-r)_0 value of the star if it's a main sequence star
             u-g0 : the (u-g)_0 value of the star if it's a main sequence star
             None if it's not possible to determinate the results or if the star cannot be a main sequence star
    """

    g_r_0 = None
    u_g_0 = None

    a = director_coefficient_B3V_line()
    b = u_g - a * g_r

    main_sequence_points = Main_sequence_points()
    for i in range(0, main_sequence_points.point_number - 1):
        a_ms = (main_sequence_points.u_g_values[i + 1] - main_sequence_points.u_g_values[i]) / (main_sequence_points.g_r_values[i + 1] - main_sequence_points.g_r_values[i])
        b_ms = main_sequence_points.u_g_values[i] - a_ms * main_sequence_points.g_r_values[i]
        if a == a_ms:
            if b == b_ms:
                if g_r_0 is None and u_g_0 is None:
                    g_r_0, u_g_0 = main_sequence_points.g_r_values[i], main_sequence_points.u_g_values[i]
                else:
                    return None, None
        else:
            g_r_intersection = (b_ms - b) / (a - a_ms)
            if min([main_sequence_points.g_r_values[i], main_sequence_points.g_r_values[i + 1]]) <= g_r_intersection and \
                            g_r_intersection <= max([main_sequence_points.g_r_values[i], main_sequence_points.g_r_values[i + 1]]) and \
                            g_r_intersection <= g_r:
                if main_sequence(g_r_intersection) is not None:
                    if g_r_0 is None and u_g_0 is None:
                        g_r_0, u_g_0 = g_r_intersection, main_sequence(g_r_intersection)
                    else:
                        return None, None
    return g_r_0, u_g_0


def g_extinction_coefficient(g_r, g_r_0):
    """
    :param g_r: a g-r star value
    :param g_r_0: the (g-r)_0 same star value
    :return: A_g, the g extinction coefficient value associated to the star
    """

    return coefficient_for_g_extinction_calculation() * (g_r - g_r_0)

def u_extinction_coefficient(u_g, u_g_0):
    """
    :param u_g: a u-g star value
    :param u_g_0: the (u-g)_0 same star value
    :return: A_u, the u extinction coefficient value associated to the star
    """

    return coefficient_for_u_extinction_calculation() * (u_g - u_g_0)

def write_extinction(input_file, output_file, n_g_r, n_u_g, column_separator, begining_str=None, comentary_char=None, output_folder=None):
    """
    :param input_file: catalogue of hot stars
    :param output_file: new catalogue of hot stars with the new cacarteristic : the extinctions values
    :param n_g_r: the number of the column (g-r) in the data file
    :param n_u_g: the number of the column (u-g) in the data file
    :param column_separator: character which separates the columns in the inputted file
    :param begining_str: string which indicates where is the data begining, it must be the last line of the header
    :param comentary_char: character which indicates, at a line begining, that this line is not part of the stars data, to allow comentaries
    :param output_folder: name of the folder where we want to put our new file output_file, if it doesn't exist it's created
                          if the folder name is not None and if the folder already exists we will considerate that the inputted data are placed into this folder
    :return: None, create the output file described in commentaries
    """

    if output_folder is not None:
        if not os.path.exists(output_folder):
            os.system("mkdir '" + output_folder + "'")
        else:
            input_file = output_folder + "/" + input_file
        output_file = output_folder + "/" + output_file

    data = open(input_file, 'r')
    nfile = open(output_file, "w")

    line = data.readline()

    if begining_str is not None and begining_str != "":
        while line[0:len(begining_str)] != begining_str:
            nfile.write(line)
            line = data.readline()
        nfile.write(str(datetime.today().year) + "/" + str(datetime.today().month) +
                    "/" + str(datetime.today().day) + " " + str(datetime.today().hour) + "h" + str(datetime.today().minute) + " Added 4 columns at the end of the file in that "
                                                            "order : g-r_0, u-g_0, g-r extinction, u-g extinction\n")

    elif comentary_char is not None and comentary_char != "":
        nfile.write(comentary_char + str(datetime.today().year) + "/" + str(datetime.today().month) +
                    "/" + str(datetime.today().day) + " " + str(datetime.today().hour) + "h" + str(datetime.today().minute) + " Added 4 columns at the end of the file in that "
                                                            "order : (g-r)_0, (u-g)_0, A_g extinction coefficient, A_u extinction coefficient\n")


    nfile.write(line)
    line = data.readline()

    i = 0

    while line != "":

        i += 1
        if i % 10000 == 0:
            print(i, " lines already read")

        if (comentary_char is None or comentary_char == "") or line[0] != comentary_char:
            u_g = ""
            g_r = ""
            column_number = 1
            for char in line:
                if char == column_separator:
                    column_number += 1
                if column_number == n_u_g:
                    if char != " " and char != column_separator:
                        u_g += char
                elif column_number == n_g_r:
                    if char != " " and char != column_separator:
                        g_r += char
                if column_number > max([n_u_g, n_g_r]):
                    break
            if u_g != "" and g_r != "":
                g_r_0, u_g_0 = find_g_r_0_u_g_0(float(g_r), float(u_g))
                if u_g_0 is not None and g_r_0 is not None:
                    nfile.write(line[:-1] + column_separator + str(g_r_0) + column_separator + str(u_g_0) +
                                column_separator + str(g_extinction_coefficient(float(g_r), g_r_0)) + column_separator +
                                str(u_extinction_coefficient(float(u_g), u_g_0)) + "\n")
                else:
                    nfile.write(line[:-1] + column_separator + "" + column_separator + "" + column_separator + "" + column_separator + "\n")
            else:
                nfile.write(
                    line[:-1] + column_separator + "" + column_separator + "" + column_separator + "" + column_separator + "\n")

        if comentary_char is not None and comentary_char != "" and line[0] == comentary_char:
            nfile.write(line)

        line = data.readline()

    data.close()
    nfile.close()

regions = [("RCW49", 60), ("RCW79", 30), ("NGC6357", int(1.5 * 60)), ("RCW97", 30), ("RCW98", 30), ("RCW94", 30), ("RCW95", 30), ("NGC6334", int(1.5 * 60)), ("RCW120", 30), ("RCW122", 60), ("RCW92", 30), ("RCW91", 30)]

for i in regions:
    analyse_region(i[0], i[1])