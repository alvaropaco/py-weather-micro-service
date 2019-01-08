# -*- coding: utf-8 -*-
import unittest
import requests
import json
import os

from ..api import app


class ZipCodeTestCase(unittest.TestCase):
    """This class represents the Weather test case"""

    def setUp(self):
        """Define test variables and initialize app."""

        # Getting env variables to Spotify and Open Weather Map
        self.spotify_jwt = os.environ.get('X_SPOTIFY_TOKEN')
        self.openwm_appid = os.environ.get('X_OPENWM_APPID')

        #  Setting parameters to Flask app
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False

        # Setting test client
        self.app = app.test_client()
        self.app.testing = True

        # Check configurations
        self.assertEqual(app.debug, False)

    def test_city_name_happy_flow(self):
        """Test city name consult"""

        url = 'http://127.0.0.1:5000/playlists?city=sao+paulo'

        res = self.app.get(
            url,
            headers={
                'X-SPOTIFY-TOKEN': self.spotify_jwt,
                'X-OPENWM-APPID': self.openwm_appid})

        jsonObj = json.loads(res.data)

        assert res.status == '200 OK'
        assert len(jsonObj) > 0

    def test_lat_lon_happy_flow(self):
        """Test search by Lat lon"""

        url = 'http://127.0.0.1:5000/playlists?lat=-23.5506507&lon=-46.6333824'

        res = self.app.get(
            url,
            headers={
                'X-SPOTIFY-TOKEN': self.spotify_jwt,
                'X-OPENWM-APPID': self.openwm_appid})

        jsonObj = json.loads(res.data)

        assert res.status == '200 OK'
        assert len(jsonObj) > 0

    def test_without_parameter_happy_flow(self):
        """Test to error response"""

        res = self.app.get('http://127.0.0.1:5000/playlists?city=sao+paulo')

        jsonObj = json.loads(res.data)

        assert jsonObj['cod'] == 401

    def tearDown(self):
        """teardown all initialized variables."""
        pass


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
