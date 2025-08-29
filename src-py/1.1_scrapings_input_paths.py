from lib.cache_manager import CacheManager


cache_manager = CacheManager()

category = input("Enter Wikipedia category: ")
if category.strip() == "":
    category = cache_manager.state.read_wikipedia_batch_category()

input_count = cache_manager.state.read_input_batch_count()

batches = [
    "Donald_Trump",
    "Joe_Biden",
    "Kamala_Harris",
    "Bernie_Sanders",
    "Elizabeth_Warren",
    "Ted_Cruz",
    "Nikki_Haley",
    "Andrew_Yang",
    "Tulsi_Gabbard"
]

cache_manager.scrapings.wikipedia.add_input_paths(
    batches, category, input_count)
cache_manager.state.update_input_batch_count(input_count + 1)
