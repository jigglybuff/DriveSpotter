import unittest
from flask import request

class MyTest(unittest.TestCase):
    def test_something(self):
        with app.test_request_context('/?name=Test'):

            assert flask.request.path == '/'
            assert flask.request.args['name'] == 'Test'
