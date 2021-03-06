"""
Geofence Model Handling
"""
from flask import Blueprint
from flask_restful import Resource, reqparse

# Shapely libraries
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

geofence = Blueprint('geofence', __name__)

OUTER_GEOFENCE_COORDINATES = [(36.11065520071664, -115.1413569181608), (36.11041270846913, -115.1412612478405),
                              (36.1101251919676, -115.1410413590561), (36.11012030230018, -115.1407566635276),
                              (36.11015948091683, -115.1404425362364), (36.11017176569752, -115.1398860941599),
                              (36.11020136533601, -115.1393849495107), (36.11030611904795, -115.1390365786721),
                              (36.11055757076942, -115.1389608683003), (36.11079484281115, -115.1390865918553),
                              (36.11092650420038, -115.1391719226508), (36.1112066426608, -115.1391744952599),
                              (36.11146887403076, -115.1392326638728), (36.1116826711911, -115.1393415579082),
                              (36.11185521872428, -115.1395304695078), (36.11191440741155, -115.139816799257),
                              (36.11195465442004, -115.1401507022453), (36.11195804176385, -115.1405226803823),
                              (36.11182615983655, -115.1408305523376), (36.11166158383364, -115.1410009530831),
                              (36.11145749303476, -115.1410296164964), (36.11124488218533, -115.1411004872609),
                              (36.11110200101439, -115.1409124351216), (36.11095500732118, -115.1408770919192),
                              (36.11080567303696, -115.1409264203645), (36.11073014186738, -115.1410693679338),
                              (36.11069919887746, -115.1412294882786), (36.11065520071664, -115.1413569181608)]

# A polygon is created that is bounded by the geofence coordinates
OUTER_GEOFENCE_POLYGON = Polygon(OUTER_GEOFENCE_COORDINATES)


def determine_if_in_outer_geofence(last_coordinate):
    """
    Determines if the coordinate is inside of the outer geofence.
    Args:
       last_coordinate: The fourth coordinate that should have been included in the request. This should be an
       iterable object of length two.
            example: (36.1104694444, -115.1408361111)

    Returns: The boolean determination of if the coordinate is inside the geofence.
    """

    # Check if the coordinate is contained within the polygon.
    return OUTER_GEOFENCE_POLYGON.contains(Point(last_coordinate))


geofence_post_args = reqparse.RequestParser()
geofence_post_args.add_argument("latitude",
                                type=float,
                                help="latitude is required",
                                required=True)

geofence_post_args.add_argument("longitude",
                                type=float,
                                help="longitude is required",
                                required=True)


class GeofenceAPI(Resource):
    """
    Routes that handle geofence calculations
    """

    def post(self):
        """
        Make a post request to this endpoint to determine if the coordinate is inside the outer geofence
        Returns: json {'inside': BOOLEAN}, status_code

        """
        args = geofence_post_args.parse_args()

        coordinates = (
            args['latitude'],
            args['longitude']
        )

        result = determine_if_in_outer_geofence(coordinates)

        return {'inside': result}, 200




