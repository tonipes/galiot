import falcon
import json
import logging
import urllib

class Middleware(object):
    def __init__(self):
        super(Middleware, self).__init__()

    def process_request(self, req, resp):
        pass

    def process_resource(self, req, resp, resource, params):
        pass

    def process_response(self, req, resp, resource):
        pass

class AuthMiddleware(Middleware):
    def __init__(self, apikeys):
        super(AuthMiddleware, self).__init__()
        self.keys = apikeys

    def process_request(self, req, resp):
        if req.method not in ('OPTIONS'):
            params = dict(urllib.parse.parse_qsl(req.query_string))
            token = params.get('apikey', None)
            if token is None:
                print('Unauthorized request. No token given.')
                raise falcon.HTTPUnauthorized('Auth token required',
                    'Please provide an auth token as part of the request.', [])
            if not self._token_is_valid(token):
                print('Unauthorized request. Invalid token.')
                raise falcon.HTTPUnauthorized('Authentication required',
                    'The provided auth token is not valid.', [])

    def _token_is_valid(self, token):
        return token in self.keys