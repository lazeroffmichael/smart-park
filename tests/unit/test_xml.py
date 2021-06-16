"""
Testing module for proper parsing of Google Earth XML files
"""
import pytest
import os

from pandas import DataFrame
from simulations.parse_xml import XMLParse, ParseGoogleEarthPathXML

TEST_XML_NAME = 'xml_test.xml'


@pytest.yield_fixture(scope="module")
def xml_object():
    path = get_absolute_path()
    yield XMLParse(path)


@pytest.yield_fixture(scope="module")
def earth():
    path = get_absolute_path()
    yield ParseGoogleEarthPathXML(path)


def get_absolute_path():
    """
    Trys to get the absolute path of the test xml file
    :return: Path string
    """
    try:
        # Check if the file is in the current directory
        file = os.path.abspath('xml_test.xml')
        f = open(file)
        return file
    # File is not in the current directory, go to the next directory
    except FileNotFoundError:
        return os.path.abspath('./unit/xml_test.xml')


class TestInit:

    def test_init_method(self, xml_object):
        """
        Tests the init method sets the tree member
        """
        assert xml_object.tree
        assert xml_object.root


class TestGetRoot:

    def test_get_root(self, xml_object):
        """
        Tests getting the root works
        """
        root = xml_object.get_root()
        assert root


class TestGoogleEarth:

    def test_get_coordinates(self, earth):
        """
        Tests getting the coordinates from google earth xml path
        """

        frame = earth.get_coordinates()
        assert isinstance(frame, DataFrame)

    def test_write_to_csv(self, earth):
        """
        Tests writing to csv
        """
        frame = earth.get_coordinates()
        filename = "test.csv"
        earth.write_to_csv(frame, filename)
        f = open(filename)
        assert f
        f.close()
        os.remove(filename)
