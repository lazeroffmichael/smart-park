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
        Initializes the class tree and root members.
        :param path: Path of the file
        """
        f = open(path)
        self.path = path
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
        Gets the coordinates from the XML file and returns an array of the coordinates and whether or not the the path
        leads to the garage
        :return: Pandas data frame
        """
        coord_str = ""

        for item in self.root.iter():
            if item.tag == self.COORDS_TAG:
                coord_str = item.text  # String of coordinates

        # split up into the individual coordinate groups
        coords = coord_str.split()

        data_array = []
        # for each coordinate group
        for c in coords:
            # split to get the individual coordinates
            values = c.split(",")

            # swap latitude and longitude positions
            values[0], values[1], values[2] = float(values[1]), float(values[0]), float(values[2])

            for items in values:
                data_array.append(items)

        # append whether the path is valid or not
        if "Missed" not in self.path:   # not missed so append 1
            data_array.append(1)    # classifier for made it to garage
        else:
            data_array.append(0)    # missed

        return data_array


