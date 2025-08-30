
import os
from openai import OpenAI
from dotenv import load_dotenv
from constants.common import SPLIT
from utils.cache_manager.cache_manager import CacheManager
import os
from openai import OpenAI
from utils.models import UserInformation
from utils.inputs import input_batch_count, input_category

load_dotenv()
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

cache_manager = CacheManager()

category = input_category()
print(f"Category: {category}")
cached_batch_count = cache_manager.state.read.output_batch_count() - 1
batch_count = input_batch_count()
print(f"Batch count: {batch_count}")

batch_list = cache_manager.scrapings.wikipedia.read_output_batch_list(
    category, batch_count)


batch_result_list = []
i = 1
print(f"Processing batch {batch_count} with {len(batch_list)} items")
for batch in batch_list:
    print(f"Processing {i}/{len(batch_list)}")
    response = openai.responses.parse(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": "Extract the event information."},
            {
                "role": "user",
                "content": batch,
            },
        ],
        text_format=UserInformation
    )
    batch_result_list.append(response.output_parsed.model_dump())
    i += 1

cache_manager.previews.dump_preview_batch_json(batch_count, batch_result_list)
