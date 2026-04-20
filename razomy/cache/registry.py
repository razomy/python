import uuid
from typing import Any, Optional, Callable


class CacheRegistry(object):
    def __init__(self):
        # Initialize an empty dictionary to act as our cache storage
        self._cache = {}

    def generate_unique_id(self) -> str:
        """Generates and returns a universally unique identifier (UUID)."""
        return str(uuid.uuid4())

    def put(self, data: Any, key: Optional[str] = None) -> str:
        """
        Puts data into the cache.
        If a key is not provided, a unique ID is generated automatically.

        Returns the key used to store the data.
        """
        if key is None:
            key = self.generate_unique_id()

        self._cache[key] = data
        return key

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieves data from the cache by its key.
        Returns the 'default' value (usually None) if the key doesn't exist.
        """
        return self._cache.get(key, default)

    def has(self, key: str | None) -> Any:
        return key in self._cache

    def get_or_put(self, key: str | None, creator_lambda: Callable[[], Any], is_dispose=False) -> Any:
        """
        Gets the data if it exists. If not, runs the lambda function,
        saves the result to the cache, and returns it.
        """

        if self.has(key):
            return key, self._cache[key]
        else:
            new_data = creator_lambda()
            id = self.put(new_data, key)
            return id, new_data

    def delete(self, key: str) -> bool:
        """
        Deletes data from the cache.
        Returns True if the item was successfully deleted, False if it wasn't found.
        """
        if key in self._cache:
            del self._cache[key]
            return True
        return False

    # --- Helpful Bonus Methods ---

    def clear(self):
        """Empties the entire cache."""
        self._cache.clear()

    def __contains__(self, key: str) -> bool:
        """Allows using the 'in' keyword (e.g., 'if my_key in cache:')"""
        return key in self._cache


global_cache_registry = CacheRegistry()


def global_cache_delete(key: str):
    global_cache_registry.delete(key)
