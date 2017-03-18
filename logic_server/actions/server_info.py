import sys
import datetime
from ._register import register


@register('server_info')
def server_info(data):
    return {
        'echo': data,
        'python': sys.version,
        'now': str(datetime.datetime.now())
    }
