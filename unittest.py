import unittest
from flask import request

class MyTest(unittest.TestCase):
    def test_something(self):
        with app.test_request_context('/?name=Peter'):
            # Create a request context, which is needed to pass the URL parameter to a request object
            # The with-statement automatically pushes on entry
            # You can now view attributes on request context stack by using 'request'.
            assert flask.request.path == '/'
            assert flask.request.args['name'] == 'Peter'
            # The with-statement automatically pops on exit

        # After the with-statement, the request context stack is empty