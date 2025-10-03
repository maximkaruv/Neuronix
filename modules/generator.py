from openai import OpenAI, OpenAIError
from config import OPENAI_API_KEY, OPENAI_BASE_URL
import time

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL
)
    
def generator(self, text):
    start_time = time.perf_counter()
    try:
        res = self.client.embeddings.create(
            model="gpt-5-nano",
            messages=[{"role": "user", "content": text}]
        )

        elapsed = time.perf_counter() - start_time
        total_tokens = getattr(res.usage, 'total_tokens', None)

        return res.choices[0].message.content
    
    except OpenAIError as e:
        raise