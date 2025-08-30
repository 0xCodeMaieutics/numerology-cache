import os
from .cache_paths import CachePaths
from .cache_state import CacheState

from constants.common import SPLIT


class CacheWikipediaScrapings:
    def __init__(self, cache_paths: CachePaths):
        self.cache_paths = cache_paths

    def read_celeb_paths(self, category: str, batch: int):
        path = self.cache_paths.scrapings.wikipedia.input.base_number_category(
            category, batch)
        with open(path, 'r') as file:
            return file.read().strip().split('\n')

    def append_batch(self, category: str, batch_number: int, content: str):
        path = self.cache_paths.scrapings.wikipedia.output.batch_number_category(
            category, batch_number)
        with open(path, 'a+') as file:
            file.write(content)
        print(f"Appended content to {path}")

    def clear_output_files(self):
        scrapings_folder = self.cache_paths.scrapings.wikipedia.output.base_folder
        file_names = os.listdir(scrapings_folder)
        for f in file_names:
            print(os.path.join(scrapings_folder, f))
            os.remove(os.path.join(scrapings_folder, f))

    def reset_output_files(self):
        self.clear_output_files()

    def read_output_batch_list(self, category: str, batch: int):
        path = self.cache_paths.scrapings.wikipedia.output.batch_number_category(
            category, batch)
        with open(path, 'r') as file:
            splits = file.read().strip().split(SPLIT)
            return [item for item in splits if item.strip() != ""]

    def add_input_paths(self, paths: list, category: str, batch: int):
        path = self.cache_paths.scrapings.wikipedia.input.base_number_category(
            category, batch)
        with open(path, 'a+') as file:
            file.writelines(f"{p}\n" for p in paths)
        print(f"Added input paths to {path}")


class CacheScrapings:
    wikipedia: CacheWikipediaScrapings

    def __init__(self, cache_path: CachePaths):
        self.wikipedia = CacheWikipediaScrapings(cache_path)
