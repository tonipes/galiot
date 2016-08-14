import logging
import falcon

_logger = logging.getLogger(__name__)

class Sink(object):
    """ Sink is used to catch or redirect all requests that are not catched by the resources"""
    def __init__(self):
        pass

    def get_sink(self, req, resp):
        print("Request went to sink")