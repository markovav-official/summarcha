import os
import aiohttp
import asyncio
from dotenv import load_dotenv


load_dotenv()
hugging_face_auth_token = os.getenv("HUGGING_FACE_AUTH_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/facebook/mbart-large-50-many-to-many-mmt"
headers = {"Authorization": hugging_face_auth_token}


async def query(payload):
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, headers=headers, json=payload) as resp:
            return await resp.json()
        
async def query_wrapper(text: str, src_lang: str, target_lang: str):
    answer = await query({"inputs": text, "parameters": {"src_lang": src_lang, "tgt_lang": target_lang}})
    print("Translation API:", answer)
    if 'error' in answer and 'estimated_time' in answer:
        await asyncio.sleep(answer['estimated_time'] / 10)
        return await query_wrapper(text, src_lang, target_lang)
    return answer[0]['translation_text']


if __name__ == "__main__":
    output = asyncio.run(
        query_wrapper(
            "Hello, world!",
            "en_XX",
            "ru_RU"
        )
    )

    print(output)