"""
Initializes the routes for the different endpoints
"""
from server.api.views.model import ModelAPI
from server.api.views.geofence import GeofenceAPI
from server.api.views.distance import DistanceAPI
from server.api.views.time import TimeAPI
from server.api.views.database import DatabaseInstantiateAPI


def initialize_routes(api):
    """
    Initializes all the api endpoints
    Args:
        api: flask api object

    Returns: None

    """
    # ModelAPI
    api.add_resource(ModelAPI, '/api/model')

    # GeofenceAPI
    api.add_resource(GeofenceAPI, '/api/geofence')

    # DistanceAPI
    api.add_resource(DistanceAPI, '/api/distance')

    # TimeAPI
    api.add_resource(TimeAPI, '/api/time')

    # Database
    api.add_resource(DatabaseInstantiateAPI, '/api/database/populate')