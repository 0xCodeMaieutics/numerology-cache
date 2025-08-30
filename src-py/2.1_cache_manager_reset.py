from utils.cache_manager.cache_manager import CacheManager


number = int(input("Script number:"))
cache_manager = CacheManager()
if number == 1:
    cache_manager.scrapings.wikipedia.reset_output_files()
    cache_manager.state.reset_batch_count()
elif number == 2:
    cache_manager.state.set_wikipedia_batch_count(1)
