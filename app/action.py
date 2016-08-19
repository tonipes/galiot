import falcon
import http.client
import json

class Action(object):
    def __init__(self):
        pass

    def run_action(self, params):
        pass


class RelayAction(Action):
    def __init__(self, db):
        self.db = db

    def create_body(self, action_id, params):
        b = {'actions':[{
                'action_id': action_id,
                'params': json.dumps(params)
            }]}
        return json.dumps(b)

    def relay_action(self, slave, action_id, params):
        body = self.create_body(action_id, params)

        conn = http.client.HTTPConnection(slave.host, slave.port)
        req = conn.request("POST", "/action/", body=body, headers={})
        res = conn.getresponse()

        print(res.status, res.reason)

    def run_action(self, action_id, params):
        matches = self.db.get_matches(action_id)
        for slave in matches:
            self.relay_action(slave, action_id, params)