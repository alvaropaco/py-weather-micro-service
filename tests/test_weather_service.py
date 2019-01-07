# -*- coding: utf-8 -*-
import unittest
import requests
import json

from ..api import app


class ZipCodeTestCase(unittest.TestCase):
    """This class represents the Weather test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.app.testing = True
        self.assertEqual(app.debug, False)

    def test_zipcode_happy_flow(self):
        res = self.app.get('http://127.0.0.1:5000/playlists?city=sao+carlos')

        jsonObj = json.loads(res.data)

        assert jsonObj['street'] == "R Ruth B Souto"
    
    def test_zipcode_without_parameter(self):
        res = self.app.get('http://127.0.0.1:5000/zipcode?code=')

        jsonObj = json.loads(res.data)

        assert jsonObj['Message'] == "Not Found"

    def tearDown(self):
        """teardown all initialized variables."""
        pass


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
