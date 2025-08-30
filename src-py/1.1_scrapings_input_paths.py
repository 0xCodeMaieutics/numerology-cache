from utils.cache_manager.cache_manager import CacheManager
from utils.inputs import input_category

cache_manager = CacheManager()

category = input_category()
input_count = cache_manager.state.read.input_batch_count()

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
