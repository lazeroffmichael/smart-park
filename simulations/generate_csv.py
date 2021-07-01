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
import numpy as np
import pandas as pd

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


def convert_kml_to_xml(kml_path, xml_path, replace=False):
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


def create_dataframe(data, index_names=None, coordinate_amount=20):
    """
    Creates the data frame based on the array of the data
    :param index_names:
    :param coordinate_amount:
    :param data:
    :return:
    """
    columns = []
    columns.append('name')
    for index in range(1, coordinate_amount + 1):
        latitude = 'latitude_' + str(index)
        longitude = 'longitude_' + str(index)
        altitude = 'altitude_relative_to_ground_' + str(index)
        columns.append(latitude)
        columns.append(longitude)
        columns.append(altitude)

    columns.append('enter-parking')

    if index_names is not None:
        data_frame = pd.DataFrame(data, index=index_names, columns=columns)

    else:
        data_frame = pd.DataFrame(data, columns=columns)

    return data_frame


def write_to_csv(data_frame, path):
    """
    Writes the data_frame to a csv file
    :param data_frame: Pandas dataframe
    :param path: Filename
    :return: none
    """
    data_frame.to_csv(path)


def delete_files_from_directory(directory):
    """
    Deletes the files from a directory.
    """
    # TODO: Implement for generate csv so xml files are deleted before new creation

    for root, dirs, files in os.walk(directory):
        for file in files:
            os.remove(f'{directory}/{file}')


def generate_csv():
    # Convert the kml files in the directory to xml in the xml paths folder
    convert_kml_to_xml('test_kml_paths', 'test_xml_paths', replace=True)

    # Get the filenames from the xml paths
    xml_files = get_filenames('test_xml_paths')

    df = None  # Final dataframe to be used

    # For each file in the directory
    for xml in xml_files:
        # Create the object for the file
        earth = ParseGoogleEarthPathXML(f'./test_xml_paths/{xml}')
        # Get the coordinates from the file in a list
        data = earth.get_coordinates()
        # create the dataframe with the coordinates
        temp = create_dataframe(data, coordinate_amount=20)
        # concat the dataframe to the existing dataset
        df = pd.concat([df, temp], axis=0)

    # Write the dataframe to the file
    df.to_csv('./test_csv_paths/test_paths.csv')


if __name__ == '__main__':
    delete_files_from_directory('./test_xml_paths')
    generate_csv()
