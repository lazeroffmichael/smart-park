"""
Class for parsing XML files
"""
import pandas as pd
import numpy as np
import os
import xml.etree.ElementTree as et


class XMLParse:
    """
    Class for parsing XML Files
    """

    def __init__(self, path: str):
        """
        Pass in the path to the XML file to be parsed
        Initializes the class tree member
        :param path: Path of the file
        """
        f = open(path)
        self.tree = et.parse(f)
        self.root = self.get_root()

    def get_root(self):
        """
        Returns the root of the xml tree
        :return: Root of the xml tree
        """
        return self.tree.getroot()


class ParseGoogleEarthPathXML(XMLParse):
    """
    Methods for parsing Google Earth XML Files
    """
    COORDS_TAG = '{http://www.opengis.net/kml/2.2}coordinates'
    COORDS_PARENT = '{http://www.opengis.net/kml/2.2}Placemark'

    def get_coordinates(self):
        """
        Gets the coordinates from the XML file
        :return: List of coordinates
        """
        coord_str = ""

        for item in self.root.iter():
            if item.tag == self.COORDS_TAG:
                coord_str = item.text   # String of coordinates

        # Remove escape characters from beginning
        modified_coord = self._slice_escape_characters(coord_str)

        # Remove spaces and add commas
        final = self._remove_spaces_add_commas(modified_coord)

        return final

    @staticmethod
    def _slice_escape_characters(coords):
        """
        The same escape characters are present in front of the coordinate string. Slice the coordinate
        string to return just the coordinates
        :param coords: Coordinates string
        :return: str
        """
        return coords.replace('\n', "").replace('\t', "")

    @staticmethod
    def _remove_spaces_add_commas(coords):
        """
        Replace spaces between the coordinates with commas, and strip the last comma
        :param coords:
        :return: str
        """
        new_coords = coords.replace(" ", ",")
        return new_coords.rstrip(new_coords[-1])





