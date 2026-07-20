from slowapi import Limiter
from slowapi.util import get_remote_address

# this will later be keyed to an API KEY instead
limiter = Limiter(key_func=get_remote_address, default_limits=["5/hour"])