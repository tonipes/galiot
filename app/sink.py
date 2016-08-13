import logging
import falcon

_logger = logging.getLogger(__name__)

class Sink(object):
    def __init__(self):
        pass

    def get_sink(self, req, resp):
        _logger.info("Request went to sink")