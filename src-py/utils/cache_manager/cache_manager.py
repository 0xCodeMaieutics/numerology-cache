
from .cache_previews import CachePreviews
from .cache_paths import CachePaths
from .cache_scrapings import CacheScrapings
from .cache_state import CacheState


class CacheManager:
    cache_paths = CachePaths()

    previews: CachePreviews
    scrapings: CacheScrapings
    state: CacheState

    def __init__(self):
        _state = CacheState(self.cache_paths)
        self.state = _state
        self.scrapings = CacheScrapings(self.cache_paths)
        self.previews = CachePreviews(self.cache_paths)
