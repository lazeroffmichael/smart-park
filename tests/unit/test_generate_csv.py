"""
Testing module for /simulations/generate_csv.py
"""

import os
import shutil  # for removing directories that contain files
from simulations import generate_csv


class TestGetFileNames:

    def test_get_file_names(self):
        """
        Tests that the filenames in a directory are returned properly
        """
        directory = 'test_dir'

        # create a directory
        try:
            os.mkdir(directory)
        except FileExistsError:
            shutil.rmtree(directory)
            os.mkdir(directory)

        # create some files in the directory
        f = open(os.path.join(directory, 'file1.txt'), 'w')
        f.close()

        f2 = open(os.path.join(directory, 'file2.txt'), 'w')
        f2.close()

        # expected filenames
        filenames = ['file1.txt', 'file2.txt']

        actual = generate_csv.get_filenames(directory)

        for filename in actual:
            assert filename in filenames

        # delete the directory
        shutil.rmtree(directory)


class TestConvertKMLToXML:

    def test_convert_kml_to_xml(self):
        """
        Tests that kml files are converted to xml files
        """
        kml_dir = 'kml_dir'
        xml_dir = 'xml_dir'
        csv_dir = 'csv_dir'

        # create the directory
        try:
            os.mkdir(kml_dir)
        except FileExistsError:
            shutil.rmtree(kml_dir)
            os.mkdir(kml_dir)

        # create the directory
        try:
            os.mkdir(xml_dir)
        except FileExistsError:
            shutil.rmtree(xml_dir)
            os.mkdir(xml_dir)

        # create the directory
        try:
            os.mkdir(csv_dir)
        except FileExistsError:
            shutil.rmtree(csv_dir)
            os.mkdir(csv_dir)

        # create two files in the kml dir
        f = open(os.path.join(kml_dir, 'file1.kml'), 'w')
        f.close()

        f2 = open(os.path.join(kml_dir, 'file2.kml'), 'w')
        f2.close()

        # call method
        generate_csv.convert_kml_to_xml(kml_dir, xml_dir, csv_dir)

        # in the xml dir, there should now be two files of xml
        filenames = generate_csv.get_filenames(xml_dir)

        assert len(filenames) == 2

        expected = ['file1.xml', 'file2.xml']

        for name in filenames:
            assert name in expected

        # assert kml files still exist
        kml = generate_csv.get_filenames(kml_dir)

        assert len(kml) == 2

        expected_kml = ['file1.kml', 'file2.kml']

        for n in kml:
            assert n in expected_kml

        # assert .csv files exist
        csv = generate_csv.get_filenames(csv_dir)

        assert len(csv) == 2

        expected_csv = ['file1.csv', 'file2.csv']

        # delete the directories
        shutil.rmtree(kml_dir)
        shutil.rmtree(xml_dir)


class TestWriteToDataFile:

    def test_write_to_data_file(self):
        """
        Tests getting coordinates from xml file and writing to csv file in two different paths
        """

        xml_dir = 'xml_directory'
        csv_dir = 'csv_directory'

        # create the directory
        try:
            os.mkdir(xml_dir)
        except FileExistsError:
            shutil.rmtree(xml_dir)
            os.mkdir(xml_dir)

        # create the directory
        try:
            os.mkdir(csv_dir)
        except FileExistsError:
            shutil.rmtree(csv_dir)
            os.mkdir(csv_dir)

        # create two files in the xml dir
        f = open(os.path.join(xml_dir, 'file1.xml'), 'w')
        f.close()

        f2 = open(os.path.join(xml_dir, 'file2.xml'), 'w')
        f2.close()

        generate_csv.write_to_data_file(xml_dir, csv_dir)

        expected = ['file1.csv', 'file2.csv']

        actual = generate_csv.get_filenames(csv_dir)

        for name in expected:
            assert name in actual

        expected_xml = ['file1.xml', 'file2.xml']

        actual_xml = generate_csv.get_filenames(xml_dir)

        for xml_name in expected_xml:
            assert xml_name in actual_xml

        # delete the directories
        shutil.rmtree(csv_dir)
        shutil.rmtree(xml_dir)
