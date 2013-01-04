from .default_settings import *  # NOQA
from .caddybook_settings import *  # NOQA

try:
    from .local_settings import *  # NOQA
except ImportError:
    pass
