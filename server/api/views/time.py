"""
Time prediction API Handling
"""
from flask import Blueprint
from flask_restful import Resource, reqparse

time_blueprint = Blueprint('time', __name__)

# Time predictions will be handled by using the average walking speed of a human.

AVERAGE_WALKING_SPEED = 1.5  # meters / second


def determine_time(distance, speed=AVERAGE_WALKING_SPEED):
    """
    Time is determined by factoring in the distance between the coordinates and the speed that the person is going.
    For now we are just going to assume the average walking speed of a human. In future iterations timestamps and
    distance can be used to calculate the actual speed that the person is moving.

    Time = Distance / Speed

    Args:
        distance: The distance between two coordinates
        speed: The speed at which the person is moving.

    Returns: The time it would take to travel that distance.

    """
    time = distance / speed

    return time


time_post_args = reqparse.RequestParser()
time_post_args.add_argument("distance",
                            type=float,
                            help="The distance between two coordinates is required",
                            required=True)
time_post_args.add_argument("speed",
                            type=float,
                            help="The speed they are traveling is needed")


class TimeAPI(Resource):
    """
    Routes that handle time prediction
    """

    def post(self):
        """
        Make a post request to this endpoint to determine the time it will take to travel between two points moving
        at the given speed.
        Returns:

        """
        args = time_post_args.parse_args()

        distance = args['distance']
        speed = args['speed']

        time = determine_time(distance, speed)

        return {'time': time}, 200
