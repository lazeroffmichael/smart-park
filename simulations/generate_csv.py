"""
Module for generating the csv files from XML files

Goal: Create .csv files for the coordinates along a path

Process:
    1. Save a path as a .kml file in a directory
    2. For all the .xml files in a directory -> change them to .xml files
    3. Extract the coordinate information from the .xml files and save to corresponding .csv file

Goal is to only need to save the KML file, and the rest is automatically handled.
"""
import os
import shutil
import os.path

from simulations.parse_xml import ParseGoogleEarthPathXML


def generate_data_files(kml_path, xml_path, csv_path, replace=False):
    """
    Main calling method for the process
    :param kml_path:
    :param xml_path:
    :param csv_path:
    :param replace:
    :return:
    """
    convert_kml_to_xml(kml_path, xml_path, csv_path, replace)


def write_to_data_file(xml_path, filename, csv_path, replace=False):
    """
    Takes the xml file, extracts the coordinates from it, and writes to csv file in the csv_path
    :param filename:
    :param replace:
    :param xml_path: XML Path
    :param csv_path: CSV Path
    :return: None
    """

    # get the csv file names
    csv_names = set(get_filenames(csv_path))

    # replace the name
    renamed = filename.replace('.xml', '.csv')

    # current path for filename
    path = f'./{xml_path}/{filename}'

    # google earth object
    earth = ParseGoogleEarthPathXML(path)

    # new path
    new_path = f'./{csv_path}/{renamed}'

    if replace or renamed not in csv_names:
        # create data object
        earth.write_to_csv(earth.get_coordinates(), new_path)


def convert_kml_to_xml(kml_path, xml_path, csv_path, replace=False):
    """
    Converts the files in the kml_path directory to .xml and saves in the xml_path directory if the corresponding
    filename does not already exist in the xml_path directory.

    :param csv_path:
    :param replace:
    :param kml_path: Path of the kml directory
    :param xml_path: Path of the xml directory
    :return: None
    """
    # get the kml names
    kml_names = get_filenames(kml_path)

    # get the xml names
    xml_names = set(get_filenames(xml_path))

    # iterate through kml_names
    for kname in kml_names:
        # replace the .kml with .xml
        renamed = kname.replace('.kml', '.xml')

        # if replace is true, then we are going to copy the file regardless if it already exists
        if replace or renamed not in xml_names:
            shutil.copyfile(f'./{kml_path}/{kname}', f'./{xml_path}/{renamed}')

            write_to_data_file(xml_path, renamed, csv_path, replace)


def get_filenames(directory):
    """
    Get's the filenames from a directory

    :param directory: Path of the directory
    :return: list of filenames
    """
    filenames = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            filenames.append(file)

    return filenames


if __name__ == '__main__':

    generate_data_files('kml_paths', 'xml_paths', 'csv_paths', replace=True)
