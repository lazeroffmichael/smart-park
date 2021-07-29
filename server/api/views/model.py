"""
Views for making the model prediction
"""
from flask import Blueprint
from flask_restful import Resource, reqparse
import tensorflow as tf
import joblib

# Blueprint for the model endpoint
model = Blueprint('model', __name__)

MODEL = tf.keras.models.load_model('./resources/saved-model')
SCALER = joblib.load('./resources/scaler.gz')

model_post_args = reqparse.RequestParser()
model_post_args.add_argument("latitude_1",
                             type=float,
                             help="latitude_1 is required",
                             required=True)

model_post_args.add_argument("longitude_1",
                             type=float,
                             help="longitude_1 is required",
                             required=True)

model_post_args.add_argument("latitude_2",
                             type=float,
                             help="latitude_2 is required",
                             required=True)

model_post_args.add_argument("longitude_2",
                             type=float,
                             help="longitude_2 is required",
                             required=True)

model_post_args.add_argument("latitude_3",
                             type=float,
                             help="latitude_3 is required",
                             required=True)

model_post_args.add_argument("longitude_3",
                             type=float,
                             help="longitude_3 is required",
                             required=True)

model_post_args.add_argument("latitude_4",
                             type=float,
                             help="latitude_4 is required",
                             required=True)

model_post_args.add_argument("longitude_4",
                             type=float,
                             help="longitude_4 is required",
                             required=True)


def run_model(coordinate_list):
    """
    Runs the model
    Args:
        coordinate_list: list of 4 latitude and longitude pairs

    Returns:

    """
    # Scale the data
    scaled_data = SCALER.transform(coordinate_list).tolist()

    # Make the prediction
    prediction = (MODEL.predict(scaled_data) > 0.5).astype("int32")

    # Return the boolean value based on the prediction
    if prediction[0][0] == 1:
        return_value = True

    else:
        return_value = False

    return return_value


class ModelAPI(Resource):
    """
    Routes that handle the prediction model
    """

    def post(self):
        """
        Make a post request to this endpoint to get the result of the model.
        Returns: json {'result': BOOLEAN}, status_code

        """
        args = model_post_args.parse_args()

        coordinate_list = [[
            args['latitude_1'],
            args['longitude_1'],
            args['latitude_2'],
            args['longitude_2'],
            args['latitude_3'],
            args['longitude_3'],
            args['latitude_4'],
            args['longitude_4'],
        ]]

        return_value = run_model(coordinate_list)

        return {'result': return_value}, 200
