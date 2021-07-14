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


def convert_kml_to_xml(kml_path, xml_path):
    """
    Converts the files in the kml_path directory to .xml and saves in the xml_path directory if the corresponding
    filename does not already exist in the xml_path directory.

    :param csv_path:
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

        # copy the file to the xml directory
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
        columns.append(latitude)
        columns.append(longitude)

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


def generate_csv(kml_path, csv_path, coordinate_amount):
    """
    Generates the csv file with the coordinate data.

    Args:
        csv_path: (str) filename of the csv file to be generated
        kml_path: (str) Path to the kml folder
        replace: (bool) Whether or not to replace the xml files if they already exist

    Returns: None

    """
    xml_path = 'xml_temp'

    # Create separate directory for the xml files to be created
    try:
        os.mkdir(xml_path)
    except FileExistsError:
        # Delete the files from the
        delete_files_from_directory(xml_path)

    # Convert the kml files in the directory to xml in the xml paths folder
    convert_kml_to_xml(kml_path, xml_path)

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
        temp = create_dataframe(data, coordinate_amount=coordinate_amount)
        # concat the dataframe to the existing dataset
        df = pd.concat([df, temp], axis=0)

    # Write the dataframe to the file
    df.to_csv(csv_path)

    # Remove the temp xml directory
    shutil.rmtree(xml_path)


if __name__ == '__main__':

    # # Handles the creation of the small trajectories dataset
    # generate_csv(kml_path='small_trajectories', csv_path='./data/small_trajectories.csv', coordinate_amount=4)
    #
    # # Handles the creation of the test dataset
    # generate_csv(kml_path='test_small_trajectories', csv_path='./data/test_small_trajectories.csv', coordinate_amount=4)
    #
    # # Handles the creation of the small trajectories dataset
    # generate_csv(kml_path='kml_paths', csv_path='./data/paths.csv', coordinate_amount=20)
    #
    # # Handles the creation of the test dataset
    # generate_csv(kml_path='test_kml_paths', csv_path='./data/test_paths.csv', coordinate_amount=20)

    # Handles the creation of the poloygon geofence dataset
    generate_csv(kml_path='polygon', csv_path='./data/polygon.csv', coordinate_amount=28)


