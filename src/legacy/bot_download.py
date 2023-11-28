import asyncio
import json
from pyrogram import Client
import os
from dotenv import load_dotenv
from pyrogram.raw.functions.messages.translate_text import TranslateText
from pyrogram.types import Dialog, Message
from pyrogram.errors import FloodWait
from tqdm import tqdm

# Load environment variables from .env file
load_dotenv()

# Get API ID, API hash, and chat ID from environment variables
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

zoo_v6_chat_id = -1001080678305

# Create a Pyrogram client instance
app = Client("my_bot", api_id, api_hash)

async def main():
    await app.start()
    dialogs: list =  app.get_dialogs(limit=100)
    zoo6_dialog: Dialog = None
    async for dialog in dialogs:
        if 'Зоопарк v6.0' == dialog.chat.title:
            zoo6_dialog = dialog
            break
    if zoo6_dialog is None:
        print('So sad')
        return
    await app.stop()


async def get_chat_messages():
    await app.start()

    messages = [json.loads(message.__str__()) async for message in app.get_chat_history(zoo_v6_chat_id, limit=1000)]
    messages_chunks = [messages[i:i + 20] for i in range(0, len(messages), 20)]
    translations = []
    for chunk in tqdm(messages_chunks):
        while True:
            try:
                translations.extend((await app.invoke(TranslateText(to_lang='en', peer=await app.resolve_peer(zoo_v6_chat_id), id=[message['id'] for message in chunk]))).result)
                break
            except FloodWait as e:
                print('Flood wait for', e.value, 'seconds')
                await asyncio.sleep(e.value)
                continue
    messages_translated = []
    for message, translation in zip(messages, translations):
        message['text'] = translation.text
        messages_translated.append(message)
    json.dump(messages_translated, open('datasets/translated_messages.json', 'w'), indent=4)
    await app.stop()


if __name__ == "__main__":
    app.run(get_chat_messages())

