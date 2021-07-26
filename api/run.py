from flask import Flask, request
from flask_restful import Api, Resource, reqparse

# Geofence handline libraries
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

# Machine learning model libraries
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
import joblib
import pandas as pd

# Main flask application global variables
app = Flask(__name__)
api = Api(app)

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

pipeline_post_args = reqparse.RequestParser()
pipeline_post_args.add_argument("latitude_1",
                                type=float,
                                help="latitude_1 is required",
                                required=True)

pipeline_post_args.add_argument("longitude_1",
                                type=float,
                                help="longitude_1 is required",
                                required=True)

pipeline_post_args.add_argument("latitude_2",
                                type=float,
                                help="latitude_2 is required",
                                required=True)

pipeline_post_args.add_argument("longitude_2",
                                type=float,
                                help="longitude_2 is required",
                                required=True)

pipeline_post_args.add_argument("latitude_3",
                                type=float,
                                help="latitude_3 is required",
                                required=True)

pipeline_post_args.add_argument("longitude_3",
                                type=float,
                                help="longitude_3 is required",
                                required=True)

pipeline_post_args.add_argument("latitude_4",
                                type=float,
                                help="latitude_4 is required",
                                required=True)

pipeline_post_args.add_argument("longitude_4",
                                type=float,
                                help="longitude_4 is required",
                                required=True)

MODEL = tf.keras.models.load_model('./resources/saved-model')
SCALER = joblib.load('./resources/scaler.gz')


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


def run_model(coordinates):
    """
    Runs the machine learning model
    Args:
        coordinates: The list of 4 coordinates for the model

    Returns: A 1 or 0 depending on the moddel prediction.

    """
    # The scaler object accepts a list containg the list of coordinates
    coords = [coordinates]

    # Scale the data to be sent to the model
    scaled_data = SCALER.transform(coords).tolist()

    # Make the prediction
    prediction = (MODEL.predict(scaled_data) > 0.5).astype("int32")

    return prediction[0][0]


class Pipeline(Resource):
    """
    Main pipeline for handling the coordiate interactions
    """
    def post(self):
        args = pipeline_post_args.parse_args()

        # Determine if last coordinate is in the geofence
        result = determine_if_in_outer_geofence((args['latitude_4'], args['longitude_4']))

        # If result is true make the request to the model
        if result:
            # Obtain the list of coordinates from the request
            coordinate_list = [
                args['latitude_1'],
                args['longitude_1'],
                args['latitude_2'],
                args['longitude_2'],
                args['latitude_3'],
                args['longitude_3'],
                args['latitude_4'],
                args['longitude_4'],
            ]
            # Run the model and obtain the prediciton
            prediction = run_model(coordinate_list)

        return {'result': int(prediction)}, 200



api.add_resource(Pipeline, '/pipeline')

if __name__ == '__main__':
    app.run(debug=True)
