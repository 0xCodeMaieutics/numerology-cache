from .cache_manager.cache_manager import CacheManager


cache_manager = CacheManager()


def input_category():
    default_value = cache_manager.state.read.wikipedia_batch_category()
    category = input(
        f"Enter category (default: {default_value}): ") or default_value
    return category


def input_batch_count():
    default_input_batch_count = cache_manager.state.read.input_batch_count() - 1
    input_batch_count = input(
        f"Enter input batch count (default {default_input_batch_count}): ") or default_input_batch_count
    try:
        input_batch_count = int(input_batch_count)
    except ValueError:
        input_batch_count = default_input_batch_count
    return input_batch_count
