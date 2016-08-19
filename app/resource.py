import logging
import urllib
import re
import threading
import json
import falcon


class Resource(object):
    def get_query_string_as_dict(self, req):
        return dict(urllib.parse.parse_qsl(req.query_string))


class ActionResource(Resource):
    def __init__(self, db):
        self.db = db

    def run_daemon_action(self, action_id, action, params):
        t = threading.Thread(
            target=action.run_action,
            args=(action_id, params))
        t.setDaemon(True)
        t.start()

    def _run_actions(self, action_id, params):
        matches = self.db.get_matches(action_id)
        for action_obj in matches:
            self.run_daemon_action(action_id, action_obj.action, params)

    def on_post(self, req, resp, **kwargs):
        params = self.get_query_string_as_dict(req)
        action_id = kwargs.get('action_id', None)
        self._run_actions(action_id, params)


class MultiActionResource(ActionResource):
    def on_post(self, req, resp, **kwargs):
        body_obj = req.context['body_obj']
        for action in body_obj['actions']:
            self._run_actions(action['action_id'], action['params'])


class SubscriptionResource(Resource):
    def __init__(self, db):
        self.db = db

    def on_post(self, req, resp, **kwargs):
        params = self.get_query_string_as_dict(req)
        actions = params.get('actions', None)
        port = params.get('port', None)
        address = req.remote_addr

        self.db.add_subscription(address, port, actions)
