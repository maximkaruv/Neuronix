from openai import OpenAI, OpenAIError
from config import OPENAI_API_KEY, OPENAI_BASE_URL
import time

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL
)

def embedder(text):
    start_time = time.perf_counter()
    try:
        res = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )

        elapsed = time.perf_counter() - start_time
        total_tokens = getattr(res.usage, 'total_tokens', None)

        if isinstance(text, list):
            return [item.embedding for item in res.data]
        
        return res.data[0].embedding
    
    except OpenAIError as e:
        raise