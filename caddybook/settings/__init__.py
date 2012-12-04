from .default_settings import *
from .caddybook_settings import *
from .deployment_settings import *

try:
    from .local_settings import *
except ImportError:
    pass
