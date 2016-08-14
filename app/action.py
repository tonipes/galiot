import falcon


class Action(object):
    def __init__(self):
        pass

    def run_action(self, params):
        pass


class RelayAction(Action):
    def __init__(self, db):
        self.db = db

    def run_action(self, action_id, params):
        matches = self.db.get_matches(action_id)
        if matches:
            print("Relay action: {}".format(action_id))
        else:
            print("No one has subscribed to action {}".format(action_id))
