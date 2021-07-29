"""
Handles the views for running the whole ML pipeline of the system.
"""
from flask import Blueprint
from flask_restful import Resource, reqparse

# Functions for use in the pipeline
from .geofence import determine_if_in_outer_geofence
from .model import run_model
from .distance import calculate_distance_between_two_coordinates
from .time import determine_time

import requests

pipeline = Blueprint('pipeline', __name__)

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


class PipelineAPI(Resource):
    """
    Routes that handle all of the application API calls.
    """

    def post(selfs):
        """
        Handles the routing for the pipeline endpoint which handles processing all the endpoints.

        Returns:

        """
        args = pipeline_post_args.parse_args()

        coordinates = [[
            args['latitude_1'],
            args['longitude_1'],
            args['latitude_2'],
            args['longitude_2'],
            args['latitude_3'],
            args['longitude_3'],
            args['latitude_4'],
            args['longitude_4']
        ]]

        # Determine if the newest points (latitude_4 and longitude_4)
        if determine_if_in_outer_geofence((args['latitude_4'], args['longitude_4'])):
            # Make the ML Prediction
            if run_model(coordinate_list=coordinates):
                # TODO: This part
                # Determine which regional point in the garage that the user parked in
                # Calculate the distance
                distance = calculate_distance_between_two_coordinates()
                # Make the time prediction














