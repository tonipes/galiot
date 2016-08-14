import falcon
import json
import logging
import urllib
import json

class Middleware(object):
    def __init__(self):
        super(Middleware, self).__init__()

    def process_request(self, req, resp):
        pass

    def process_resource(self, req, resp, resource, params):
        pass

    def process_response(self, req, resp, resource):
        pass


class JsonRequestMiddleware(Middleware):
    """ Parses request body to json object
        Json object can be found in context """
    def _get_body_json(self, stream):
        s = ""
        for line in stream:
            s += line.decode("utf-8")
        return json.loads(s)

    def process_request(self, req, resp):
        content_type = req.get_header('Content-Type')

        if content_type and 'json' in content_type:
            try:
                body_obj = self._get_body_json(req.stream)
            except Exception as e:
                body_obj = {}
                print("Couldn't parse body")
                raise falcon.HTTPBadRequest('Invalid JSON',
                    'Please provide valid JSON')

            req.context['body_obj'] = body_obj


class JsonResponseMiddleware(Middleware):
    """ Translated result from context to json string body"""

    def process_response(self, req, resp, resource):
        if 'result' not in req.context:
            return

        resp.body = json.dumps(req.context['result'])
        resp.append_header('Content-Type', 'application/json')


class AuthMiddleware(Middleware):
    """ Checks if request has valid api key.
        Raises HTTP Unauthorized exception if valid api key is not found """
    def __init__(self, apikeys):
        super(AuthMiddleware, self).__init__()
        self.keys = apikeys

    def process_request(self, req, resp):
        if req.method not in ('OPTIONS'):
            params = dict(urllib.parse.parse_qsl(req.query_string))
            token = params.get('apikey', None)
            if token is None:
                print('Unauthorized request. No token given.')
                raise falcon.HTTPUnauthorized('Authentication required',
                    'Please provide an API key as part of the request.', [])
            if not self._token_is_valid(token):
                print('Unauthorized request. Invalid token.')
                raise falcon.HTTPUnauthorized('Authentication required',
                    'The provided API key is not valid.', [])

    def _token_is_valid(self, token):
        return token in self.keys