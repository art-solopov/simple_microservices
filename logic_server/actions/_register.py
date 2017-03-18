registry = {}


def register(action):
    def _rg(fn):
        registry[action] = fn
        return fn
    return _rg
