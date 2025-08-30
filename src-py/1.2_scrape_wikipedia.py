
from selenium import webdriver
from dotenv import load_dotenv
from constants.common import SPLIT
from utils.cache_manager.cache_manager import CacheManager
from utils.scrapers.wikipedia_scraper import WikipediaScraper
from utils.inputs import input_category, input_batch_count

driver = webdriver.Chrome()

cache_manager = CacheManager()
wikipedia_scraper = WikipediaScraper(driver)

category = input_category()
print(f"Current category: {category}")

batch_count = input_batch_count()

print(f"Current input count for {category}: {batch_count}")

names_to_search_for = cache_manager.scrapings.wikipedia.read_celeb_paths(
    category, batch_count)

batch_count = cache_manager.state.read.output_batch_count()

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
