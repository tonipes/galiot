import yaml
import falcon

from . import resource
from . import middleware
from . import sink
from . import engine
from . import action

def get_config(filename):
    with open(filename, 'r') as f:
        return yaml.load(f)

config = get_config('config.yml')

app = falcon.API(middleware=[
    middleware.AuthMiddleware(config['api_keys']),
    middleware.JsonRequestMiddleware(),
    middleware.JsonResponseMiddleware(),
])

engine_subs = engine.SubscriptionEngine()

engine_action = engine.ActionEngine([
    ('.*', action.RelayAction(
        db=engine_subs
    ))
])

action_subs = resource.SubscriptionResource(engine_subs)

action_res = resource.ActionResource(engine_action)
action_res_multi = resource.MultiActionResource(engine_action)

sink = sink.Sink()

app.add_sink(sink.get_sink, '/')

app.add_route('/action/', action_res_multi)
app.add_route('/action/{action_id}/', action_res)
app.add_route('/subscribe/', action_subs)

