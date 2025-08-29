
from selenium import webdriver
from dotenv import load_dotenv
from constants.common import SPLIT
from lib.cache_manager import CacheManager, WikipediaScraper

driver = webdriver.Chrome()

cache_manager = CacheManager()
wikipedia_scraper = WikipediaScraper(driver)

cached_category = cache_manager.state.read_wikipedia_batch_category()
category = input(f"Enter Wikipedia category (default {cached_category}): ")
if category.strip() == "":
    category = cached_category

print(f"Current category: {category}")
cached_input_batch_count = cache_manager.state.read_input_batch_count() - 1
input_batch_count = input(
    f"Enter input batch count (default {cached_input_batch_count}): ")
if input_batch_count.strip() == "":
    input_batch_count = cached_input_batch_count
else:
    try:
        input_batch_count = int(input_batch_count)
    except ValueError:
        print("Invalid input. Using default batch count.")
        input_batch_count = cached_input_batch_count

print(f"Current input count for {category}: {input_batch_count}")

names_to_search_for = cache_manager.scrapings.wikipedia.read_celeb_paths(
    category, input_batch_count)

batch_count = cache_manager.state.read_batch_count()

for name in names_to_search_for:
    driver.get(f"https://en.wikipedia.org/wiki/{name}")
    try:
        bio_container_wrapper = wikipedia_scraper.find_bio_container_wrapper()
        if bio_container_wrapper is None:
            print(f"No bio container found for {name}, skipping.")
            continue

        bio_image_url = wikipedia_scraper.find_bio_image_url(
            bio_container_wrapper)

        wiki_batch_content = bio_container_wrapper.text + \
            f"\nIMAGE_URL: {bio_image_url}\n{SPLIT}\n"

        cache_manager.scrapings.wikipedia.append_batch(category,
                                                       batch_count, wiki_batch_content)
    except Exception as e:
        print(f"Error occurred: {e}")
        continue

batch_count += 1
cache_manager.state.update_batch_count(batch_count)
driver.quit()
