import os
import aiohttp
import asyncio
from dotenv import load_dotenv


load_dotenv()
hugging_face_auth_token = os.getenv("HUGGING_FACE_AUTH_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/kabita-choudhary/finetuned-bart-for-conversation-summary"
headers = {"Authorization": hugging_face_auth_token}


async def query(payload):
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, headers=headers, json=payload) as resp:
            return await resp.json()
        
async def query_wrapper(text):
    answer = await query({"inputs": text})
    print("HuggingFace API:", answer)
    return answer[0]["summary_text"]


if __name__ == "__main__":
    output = asyncio.run(
        query(
            {
                "inputs": """"""
            }
        )
    )

    print(output)