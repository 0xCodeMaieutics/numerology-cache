import json
import os
from selenium import webdriver
import os
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils.file import mkdir_p
from constants.common import SPLIT


class CachePaths:
    CACHE_FOLDER_NAME = "cache"
    SCRAPINGS_FOLDER_NAME = "scrapings"
    WIKIPEDIA_FOLDER_NAME = "wikipedia"
    STATE_FOLDER_NAME = "state"
    PREVIEWS_FOLDER_NAME = 'previews'

    def base_path(self):
        return self.CACHE_FOLDER_NAME

    def previews_path(self):
        folder = f"{self.CACHE_FOLDER_NAME}/previews"
        mkdir_p(folder)
        return folder

    def scrapings_wikipedia_output_folder(self):
        folder = f"{self.CACHE_FOLDER_NAME}/{self.SCRAPINGS_FOLDER_NAME}/{self.WIKIPEDIA_FOLDER_NAME}/output"
        mkdir_p(folder)
        return folder

    def scrapings_input_wiki_batch(self, category: str, batch_number: int):
        folder = f"{self.CACHE_FOLDER_NAME}/{self.SCRAPINGS_FOLDER_NAME}/{self.WIKIPEDIA_FOLDER_NAME}/input"
        mkdir_p(folder)
        return f"{folder}/{batch_number}_{category}_batch"

    def scrapings_output_wiki_batch(self, category: str, batch_number: int):
        folder = f"{self.CACHE_FOLDER_NAME}/{self.SCRAPINGS_FOLDER_NAME}/{self.WIKIPEDIA_FOLDER_NAME}/output"
        mkdir_p(folder)
        return f"{folder}/{batch_number}_{category}_batch"

    def state_batch_count(self):
        folder = f"{self.CACHE_FOLDER_NAME}/{self.STATE_FOLDER_NAME}"
        mkdir_p(folder)
        return f"{folder}/batch_count"

    def state_wikipedia_input_count(self):
        folder = f"{self.CACHE_FOLDER_NAME}/{self.STATE_FOLDER_NAME}"
        mkdir_p(folder)
        return f"{folder}/wikipedia_input_count"

    def state_wikipedia_batch_category(self):
        folder = f"{self.CACHE_FOLDER_NAME}/{self.STATE_FOLDER_NAME}"
        mkdir_p(folder)
        return f"{folder}/wikipedia_batch_category"

    def previews_wiki_batch_json_file(self, batch_number: int):
        folder = f"{self.CACHE_FOLDER_NAME}/{self.PREVIEWS_FOLDER_NAME}/{self.WIKIPEDIA_FOLDER_NAME}"
        mkdir_p(folder)
        return f"{folder}/{batch_number}_preview.json"


class CacheStateRead:

    def __init__(self, cache_paths: CachePaths):
        self.folder_path = cache_paths

    def output_batch_count(self):
        path = self.folder_path.state_batch_count()
        with open(path, 'r') as file:
            return int(file.read().strip())

    def input_batch_count(self):
        path = self.folder_path.state_wikipedia_input_count()
        with open(path, 'r') as file:
            return int(file.read().strip())

    def wikipedia_batch_category(self):
        path = self.folder_path.state_wikipedia_batch_category()
        with open(path, 'r') as file:
            return file.read().strip()


class CacheState:
    read: CacheStateRead

    def __init__(self, cache_paths: CachePaths):
        self.folder_path = cache_paths
        self.read = CacheStateRead(cache_paths)

    def update_batch_count(self, new_count: int):
        path = self.folder_path.state_batch_count()
        with open(path, 'w') as file:
            file.write(str(new_count))

    def update_input_batch_count(self, new_count: int):
        path = self.folder_path.state_wikipedia_input_count()
        with open(path, 'w') as file:
            file.write(str(new_count))

    def reset_batch_count(self):
        self.update_batch_count(1)

    def set_wikipedia_batch_count(self, count: int):
        path = self.folder_path.state_wikipedia_input_count()
        with open(path, 'w') as file:
            file.write(str(count))


class CacheWikipediaScrapings:
    def __init__(self, cache_paths: CachePaths, state: CacheState):
        self.cache_paths = cache_paths
        self.state = state

    def read_celeb_paths(self, category: str, batch: int):
        path = self.cache_paths.scrapings_input_wiki_batch(category, batch)
        with open(path, 'r') as file:
            return file.read().strip().split('\n')

    def append_batch(self, category: str, batch_number: int, content: str):
        path = self.cache_paths.scrapings_output_wiki_batch(
            category, batch_number)
        with open(path, 'a+') as file:
            file.write(content)
        print(f"Appended content to {path}")

    def clear_output_files(self):
        scrapings_folder = self.cache_paths.scrapings_wikipedia_output_folder()
        file_names = os.listdir(scrapings_folder)
        for f in file_names:
            print(os.path.join(scrapings_folder, f))
            os.remove(os.path.join(scrapings_folder, f))

    def reset_output_files(self):
        self.clear_output_files()

    def read_output_batch_list(self, category: str, batch: int):
        path = self.cache_paths.scrapings_output_wiki_batch(category, batch)
        with open(path, 'r') as file:
            splits = file.read().strip().split(SPLIT)
            return [item for item in splits if item.strip() != ""]

    def add_input_paths(self, paths: list, category: str, batch: int):
        path = self.cache_paths.scrapings_input_wiki_batch(category, batch)
        with open(path, 'a+') as file:
            file.writelines(f"{p}\n" for p in paths)
        print(f"Added input paths to {path}")


class CacheScrapings:
    wikipedia: CacheWikipediaScrapings

    def __init__(self, folder_path: CachePaths, state: CacheState):
        self.wikipedia = CacheWikipediaScrapings(folder_path, state)


class WikipediaScraper():
    driver: webdriver.Chrome
    BIO_CONTAINER_SELECTORS = [
        "table.infobox.biography.vcard", "table.infobox.vcard"]

    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver

    def find_bio_container_wrapper(self):
        for selector in self.BIO_CONTAINER_SELECTORS:
            try:
                return WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            except Exception as e:
                print(f"Error occurred: {e}")
                continue
        return None

    def find_bio_image_url(self, bio_container_wrapper):
        img = bio_container_wrapper.find_element(
            By.CSS_SELECTOR, "img.mw-file-element"
        )
        return img.get_attribute("src")


class CachePreviews():
    def __init__(self, cache_paths: CachePaths):
        self.cache_paths = cache_paths

    def dump_preview_batch_json(self, batch_number: int, data: dict):
        path = self.cache_paths.previews_wiki_batch_json_file(batch_number)
        with open(path, 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Dumped previews at {path}")


class CacheManager:
    cache_paths = CachePaths()

    previews: CachePreviews
    scrapings: CacheScrapings
    state: CacheState

    def __init__(self):
        _state = CacheState(self.cache_paths)
        self.state = _state
        self.scrapings = CacheScrapings(self.cache_paths, _state)
        self.previews = CachePreviews(self.cache_paths)
