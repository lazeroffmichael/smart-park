"""

"""
import pandas as pd
import pytest
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


def create_polygon(path):
    """
    Creates a polygon shapely object using the coordinate data of the defining geofence polygon.

    Args:
        path: Path to the csv containing the polygon coordinate data

    Returns: Polygon object

    """

    # read csv from the location
    df = pd.read_csv(path)
    extracted_df = df[df.columns[2:58]]

    counter = 0
    list_of_polygon_coordinates = []
    temp = tuple()
    for column in extracted_df:
        # Get the current value and make a tuple
        current = tuple(extracted_df[column].values)
        # Add it to the temp tuple
        temp += current
        # If the len of temp is 2, then we have a pair so append it to the final list
        if len(temp) == 2:
            list_of_polygon_coordinates.append(temp)
            temp = tuple()

    return Polygon(list_of_polygon_coordinates)


def main():
    location = './data/polygon.csv'
    polygon = create_polygon(location)
    inside_point = Point(36.1104694444, -115.1408361111)
    inside_point_2 = Point(36.110791, -115.140464)
    inside_point_3 = Point( 36.110174, -115.140403)
    outside_point = Point(36.1109694444, -115.1410805556)
    outside_point_2 = Point(36.110598, -115.138839)
    outside_point_3 = Point(36.109884, -115.140435)
    print(polygon.contains(inside_point))
    print(polygon.contains(inside_point_2))
    print(polygon.contains(inside_point_3))
    print(polygon.contains(outside_point))
    print(polygon.contains(outside_point_2))
    print(polygon.contains(outside_point_3))



if __name__ == '__main__':
    main()
