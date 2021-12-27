from typing import Any
from typing import Dict


class SingletonMeta(type):
    _instances: Dict[Any, Any] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

    @classmethod
    def reset(cls):
        """De-register all singleton instances"""
        cls._instances = {}

    @classmethod
    def cleanup(cls):
        """Cleanup all singletons if they expose a method for it"""
        for i in cls._instances.values():
            if hasattr(i, "_cleanup"):
                i._cleanup()
