import falcon
import json
import urllib
import re
import threading
import json

class ActionResource(object):
    def __init__(self, actions):
        self.actions = actions

    def _get_body_json(self, stream):
        s = ""
        for line in stream:
            s += line.decode("utf-8")
            print(s)
        return json.loads(s)

    def _run_actions(self, action_id, params):
        for action_tuple in self.actions:
            if re.match(action_tuple[0], action_id):
                # Run action in a daemon thread so client doesn't have to wait action to get an response
                t = threading.Thread(
                    name=action_tuple[0],
                    target=action_tuple[1].run_action,
                    args=(action_id, params)
                )
                t.setDaemon(True)
                t.start()

    def on_post(self, req, resp, **kwargs):
        params = dict(urllib.parse.parse_qsl(req.query_string))
        action_id = kwargs.get('action_id', None)
        self._run_actions(action_id, params)

class MultiActionResource(ActionResource):
    def __init__(self, actions):
        self.actions = actions

    def on_post(self, req, resp, **kwargs):
        try:
            json = self._get_body_json(req.stream)
        except Exception as e:
            json = {}
            print("Couldn't parse body")

        for action in json['actions']:
            self._run_actions(action['action_id'], action['params'])
