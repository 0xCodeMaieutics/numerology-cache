import os
from utils.file import mkdir_p


class CachePreviewWikipediaPaths:
    _FOLDER_NAME = 'wikipedia'

    def __init__(self, base_folder: str):
        self.base_folder = os.path.join(base_folder, self._FOLDER_NAME)

    def batch_number_preview(self, batch_number: int):
        mkdir_p(self.base_folder)
        return os.path.join(self.base_folder, f"{batch_number}_preview.json")


class CachePreviewPaths:
    _FOLDER_NAME = 'previews'
    wikipedia = CachePreviewWikipediaPaths

    def __init__(self, base_folder: str):
        self.wikipedia = CachePreviewWikipediaPaths(
            os.path.join(base_folder, self._FOLDER_NAME))


class CacheStatePaths:
    _FOLDER_NAME = "state"

    def __init__(self, base_folder: str):
        self._base_folder = os.path.join(base_folder, self._FOLDER_NAME)

    def batch_count(self):
        mkdir_p(self._base_folder)
        return os.path.join(self._base_folder, "batch_count")

    def wikipedia_input_count(self):
        mkdir_p(self._base_folder)
        return os.path.join(self._base_folder, "wikipedia_input_count")

    def wikipedia_batch_category(self):
        mkdir_p(self._base_folder)
        return os.path.join(self._base_folder, "wikipedia_batch_category")


class CacheScrapingsWikipediaOutputPaths:
    _FOLDER_NAME = "output"

    def __init__(self, base_folder: str):
        self.base_folder = os.path.join(base_folder, self._FOLDER_NAME)

    def scrapings_wikipedia_output_folder(self):
        mkdir_p(self.base_folder)
        return self.base_folder

    def batch_number_category(self, category: str, batch_number: int):
        mkdir_p(self.base_folder)
        return os.path.join(self.base_folder, f"{batch_number}_{category}_batch")


class CacheScrapingsWikipediaInputPaths:
    _FOLDER_NAME = "input"

    def __init__(self, base_folder: str):
        self.base_folder = os.path.join(base_folder, self._FOLDER_NAME)

    def base_number_category(self, category: str, batch_number: int):
        mkdir_p(self.base_folder)
        return os.path.join(self.base_folder, f"{batch_number}_{category}_batch")


class CacheScrapingsWikipediaPaths:
    _FOLDER_NAME = "wikipedia"
    input = CacheScrapingsWikipediaInputPaths
    output = CacheScrapingsWikipediaOutputPaths

    def __init__(self, base_folder: str):
        self.input = CacheScrapingsWikipediaInputPaths(
            os.path.join(base_folder, self._FOLDER_NAME))

        self.output = CacheScrapingsWikipediaOutputPaths(
            os.path.join(base_folder, self._FOLDER_NAME))


class CacheScrapingsPaths:
    _FOLDER_NAME = "scrapings"
    wikipedia = CacheScrapingsWikipediaPaths

    def __init__(self, base_folder: str):
        self.wikipedia = CacheScrapingsWikipediaPaths(
            os.path.join(base_folder, self._FOLDER_NAME))


class CachePaths:
    CACHE_FOLDER_NAME = "cache"
    WIKIPEDIA_FOLDER_NAME = "wikipedia"
    PREVIEWS_FOLDER_NAME = 'previews'
    state: CacheStatePaths
    scrapings: CacheScrapingsPaths
    previews: CachePreviewPaths

    def __init__(self):
        self.state = CacheStatePaths(self.CACHE_FOLDER_NAME)
        self.scrapings = CacheScrapingsPaths(self.CACHE_FOLDER_NAME)
        self.previews = CachePreviewPaths(self.CACHE_FOLDER_NAME)
