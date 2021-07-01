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
import pandas as pd

from simulations.parse_xml import ParseGoogleEarthPathXML


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


def delete_files_from_directory(directory):
    """
    Deletes the files from a directory.
    """
    # TODO: Implement for generate csv so xml files are deleted before new creation

    for root, dirs, files in os.walk(directory):
        for file in files:
            os.remove(f'{directory}/{file}')


def generate_csv(kml_path, xml_path, filename, replace=False):
    """
    Generates the csv file with the coordinate data.

    Args:
        filename: (str) filename of the csv file to be generated
        xml_path: (str) Path to the xml folder
        kml_path: (str) Path to the kml folder
        replace: (bool) Whether or not to replace the xml files if they already exist

    Returns: None

    """
    # Convert the kml files in the directory to xml in the xml paths folder
    convert_kml_to_xml(kml_path, xml_path, replace=replace)

    # Get the filenames from the xml paths
    xml_files = get_filenames(xml_path)

    df = None  # Final dataframe to be used

    # For each file in the directory
    for xml in xml_files:
        # Create the object for the file
        earth = ParseGoogleEarthPathXML(f'{xml_path}/{xml}')
        # Get the coordinates from the file in a list
        data = earth.get_coordinates()
        # create the dataframe with the coordinates
        temp = create_dataframe(data, coordinate_amount=20)
        # concat the dataframe to the existing dataset
        df = pd.concat([df, temp], axis=0)

    # Write the dataframe to the file
    df.to_csv(f'./{filename}')


if __name__ == '__main__':
    delete_files_from_directory('./xml_paths')
    generate_csv(kml_path='kml_paths', xml_path='xml_paths', filename='paths.csv', replace=True)
