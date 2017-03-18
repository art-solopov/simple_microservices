import pytoml

CONFIG = {}

def load_configs(*files):
    config = {}
    for cf in files:
        with open(cf, 'r') as cff:
            config.update(pytoml.load(cff))
    CONFIG['queue'] = config['queues']['base']
