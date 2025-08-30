import json
from .cache_paths import CachePaths


class CachePreviews():
    def __init__(self, cache_paths: CachePaths):
        self.cache_paths = cache_paths

    def dump_preview_batch_json(self, batch_number: int, data: dict):
        path = self.cache_paths.previews.wikipedia.batch_number_preview(
            batch_number)
        with open(path, 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Dumped previews at {path}")
