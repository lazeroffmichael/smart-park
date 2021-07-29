from flask import Blueprint
from flask_restful import Resource, reqparse
from haversine import haversine, Unit

# Blueprint for the endpoint
distance = Blueprint('distance', __name__)

"""
Garage Regional Coordinates

These are the set coordinates in the garage of different regions. Parking spaces are assigned to the region based on 
their location.
"""

# Front of the garage regions
HANDICAPPED_1 = (36.11069997965747, -115.1404478903625)
BOX_OFFICE_RESERVED = (36.11071209978293, -115.1400687528217)
HANDICAPPED_2 = (36.11071638843368, -115.1397890512707)

# Middle of the garage regions
MIDDLE_1 = (36.1108496227119, -115.1403193938467)
MIDDLE_2 = (36.11103899273078, -115.1403272306211)
MIDDLE_3 = (36.11119829380773, -115.1403308453176)
MIDDLE_4 = (36.11135321406704, -115.1403346917111)
MIDDLE_5 = (36.1115334369977, -115.14035023662)
MIDDLE_6 = (36.11084964608833, -115.1401010797195)
MIDDLE_7 = (36.11103712114207, -115.1401249244285)
MIDDLE_8 = (36.1112045870257, -115.1401381140184)
MIDDLE_9 = (36.11135903712993, -115.1401523474531)
MIDDLE_10 = (36.1115393669109, -115.1401574457783)
MIDDLE_11 = (36.11084714214764, -115.139912243349)
MIDDLE_12 = (36.11105418477895, -115.1399184774152)
MIDDLE_13 = (36.11120616544017, -115.1399537018262)
MIDDLE_14 = (36.11136203924969, -115.139964250657)
MIDDLE_15 = (36.11154805805855, -115.1399651453322)

# Under Ramp Entrance C and D regions
BOX_C = (36.11155995576119, -115.1405549112171)
BOX_D = (36.11158078770687, -115.1397778394763)


def calculate_distance_between_two_coordinates(coordinate_1, coordinate_2):
    """
    Calculates the distance between two coordinates using the Haversine formula.
    Args:
        coordinate_1: The first coordinate pair
        coordinate_2: The second coordinate pair

    Returns: The distance between the two coordinates
    """
    return haversine(coordinate_1, coordinate_2, unit=Unit.METERS)


distance_post_args = reqparse.RequestParser()

distance_post_args.add_argument("latitude_1",
                                type=float,
                                help="latitude_1 is required",
                                required=True)

distance_post_args.add_argument("longitude_1",
                                type=float,
                                help="longitude_1 is required",
                                required=True)

distance_post_args.add_argument("latitude_2",
                                type=float,
                                help="latitude_2 is required",
                                required=True)

distance_post_args.add_argument("longitude_2",
                                type=float,
                                help="longitude_2 is required",
                                required=True)


class DistanceAPI(Resource):
    """
    Routes that handle the distance between points
    """

    def post(self):
        """
        Make a post request to this endpoint to get the result
        Returns:

        """
        args = distance_post_args.parse_args()

        coordinate_1 = (args['latitude_1'], args['longitude_1'])
        coordinate_2 = (args['latitude_2'], args['longitude_2'])

        result = calculate_distance_between_two_coordinates(coordinate_1, coordinate_2)

        return {'distance': result}, 200
