"""
Testing module for server.py
"""

from cloud import backend


class TestDetermineGeofenceBounds:

    def test_determine_if_outer_geofence_works(self):
        """
        Tests that the outer geofence detection works
        """
        valid_point = (36.1104694444, -115.1408361111)

        assert backend.determine_if_in_outer_geofence(valid_point)

    def test_determine_if_outer_geofence_not_inside(self):
        """
        Tests that the function detects when the point is not inside the polygon
        """
        outside_point = (36.110598, -115.138839)

        assert not backend.determine_if_in_outer_geofence(outside_point)
