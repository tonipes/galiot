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

    def __init__(self, host, port, regex):
        self.host = host
        self.port = port
        self.regex = regex


class ActionEngineObject(object):
    """ Model for action """

    def __init__(self, action, regex):
        self.action = action
        self.regex = regex


class SubscriptionEngine(Engine):
    """ Database for subscribed slave devices """

    def __init__(self):
        self.storage = {}

    def add_subscription(self, host, port, actions_regex):
        """ Subscribe slave device for actions that match actions_regex """

        slave_id = "{}:{}".format(host, port)
        old_slave = self.storage.get(slave_id, None)
        self.storage[slave_id] = SlaveEngineObject(
            host=host,
            port=port,
            regex=actions_regex
        )
        if old_slave:
            print("Updated slave: {}, {}".format(slave_id, actions_regex))
        else:
            print("Added slave: {}, {}".format(slave_id, actions_regex))

    def get_matches(self, action_id):
        """ Return all slave devices that are interested in given action """

        matches = []
        for key, slave in self.storage.items():
            if re.match(slave.regex, action_id):
                matches.append(slave)
        return matches


class ActionEngine(Engine):
    """ Database for registered actions"""

    def __init__(self):
        self.storage = {}

    def add_action(self, regex, action):
        """ Registers action. Action will be registered to be
            interested with all actions that match the given regex  """

        uuid = self.get_new_uuid()
        action_obj = ActionEngineObject(
            action=action
            regex=regex,
        )

        self.storage[uuid] = action_obj

    def get_matches(self, action_id):
        """ Returns all actions that are registered with
            regex that matches with the action_id """

        matches = []
        for key, action in self.storage.items():
            if re.match(action.regex, action_id):
                matches.append(action)
        return matches