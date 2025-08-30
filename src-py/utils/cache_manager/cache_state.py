from .cache_paths import CachePaths


class CacheStateRead:

    def __init__(self, cache_paths: CachePaths):
        self.folder_path = cache_paths

    def output_batch_count(self):
        path = self.folder_path.state.batch_count()
        with open(path, 'r') as file:
            return int(file.read().strip())

    def input_batch_count(self):
        path = self.folder_path.state.wikipedia_input_count()
        with open(path, 'r') as file:
            return int(file.read().strip())

    def wikipedia_batch_category(self):
        path = self.folder_path.state.wikipedia_batch_category()
        with open(path, 'r') as file:
            return file.read().strip()


class CacheState:
    read: CacheStateRead

    def __init__(self, cache_paths: CachePaths):
        self.folder_path = cache_paths
        self.read = CacheStateRead(cache_paths)

    def update_batch_count(self, new_count: int):
        path = self.folder_path.state.batch_count()
        with open(path, 'w') as file:
            file.write(str(new_count))

    def update_input_batch_count(self, new_count: int):
        path = self.folder_path.state.wikipedia_input_count()
        with open(path, 'w') as file:
            file.write(str(new_count))

    def reset_batch_count(self):
        self.update_batch_count(1)

    def set_wikipedia_batch_count(self, count: int):
        path = self.folder_path.state.wikipedia_input_count()
        with open(path, 'w') as file:
            file.write(str(count))
