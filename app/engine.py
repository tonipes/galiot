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
    def __init__(self, address, port, actions):
        self.address = address
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

    def add_subscription(self, address, port, actions):
        slave_id = "{}:{}".format(address, port)
        self.storage[slave_id] = SlaveEngineObject(address, port, actions)

        print("Added slave: {}, {}".format(slave_id, actions))

    def get_matches(self, action_id):
        matches = []
        for key, slave_obj in self.storage.items():
            if re.match(slave.actions, action_id):
                matches.append(slave_obj)
        return matches


class ActionEngine(Engine):
    def __init__(self, actions):
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

        for key, action_obj in self.storage.items():
            if re.match(action_obj.regex, action_id):
                matches.append(action_obj)

        return matches