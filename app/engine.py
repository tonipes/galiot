import re
import logging
import uuid
import falcon


class Engine(object):
    def __init__(self):
        pass

    def get_new_uuid(self):
        return str(uuid.uuid4())


class SlaveEngineObject(object):
    """ Model for slave """
    def __init__(self, host, port, actions):
        self.host = host
        self.port = port
        self.actions = actions


class ActionEngineObject(object):
    """ Model for action """
    def __init__(self, regex, action):
        self.regex = regex
        self.action = action


class SubscriptionEngine(Engine):
    def __init__(self):
        self.storage = {}

    def add_subscription(self, host, port, actions):
        slave_id = "{}:{}".format(host, port)
        old_slave = self.storage.get(slave_id, None)
        self.storage[slave_id] = SlaveEngineObject(host, port, actions)
        if old_slave:
            print("Updated slave: {}, {}".format(slave_id, actions))
        else:
            print("Added slave: {}, {}".format(slave_id, actions))

    def get_matches(self, action_id):
        matches = []
        for key, slave in self.storage.items():
            if re.match(slave.actions, action_id):
                matches.append(slave)
        return matches


class ActionEngine(Engine):
    def __init__(self):
        self.storage = {}

    def add_action(self, regex, action):
        uuid = self.get_new_uuid()
        action_obj = ActionEngineObject(
            regex=regex,
            action=action
        )

        self.storage[uuid] = action_obj

    def get_matches(self, action_id):
        matches = []

        for key, action in self.storage.items():
            if re.match(action.regex, action_id):
                matches.append(action)

        return matches