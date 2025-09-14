# Em Utils/threadsafe.py (ou onde quiser)
import threading
from functools import wraps

_LOCK_SQLITE = threading.Lock()

def com_lock(func):
    """Decorador para aplicar lock em chamadas ao banco de dados SQLite."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        with _LOCK_SQLITE:
            return func(*args, **kwargs)
    return wrapper
