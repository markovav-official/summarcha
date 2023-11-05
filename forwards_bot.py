import os
import faker
from pyrogram import Client, filters
from pyrogram.types import Message
from dotenv import load_dotenv
from typing import List
from pyrogram.enums import ChatAction
import summarization_api
import translation_api

# Load environment variables from .env file
load_dotenv()

# Get API ID, API hash, and chat ID from environment variables
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

# Create a Pyrogram client instance
app = Client("my_bot", api_id, api_hash)


class ProgressMessage:
    def __init__(self, message: Message):
        self.message = message

    async def update(self, text: str):
        await self.message.edit(text)


@app.on_message(filters.command("summarize"))
async def summarize_command_handler(client: Client, message: Message):
    await client.send_chat_action(message.chat.id, ChatAction.TYPING)
    # filter forwarded messages
    messages: List[Message] = [m async for m in app.get_chat_history(message.chat.id, limit=21)]
    analyzed_messages = []
    for i, message in enumerate(messages):
        if message.caption is not None:
            if message.text is None:
                message.text = message.caption
            message.text += ' ' + message.caption

        if message.text is None:
            continue
        if message.text == "/summarize":
            if i != 0:
                break
            continue
        if message.forward_date:
            analyzed_messages.append(message)
    if len(analyzed_messages) == 0:
        await message.reply("No forwarded messages found")
        return
    message = await client.send_message(message.chat.id, "Analyzing messages...")
    await proccess_messages(analyzed_messages, ProgressMessage(message))

def get_user_name(message: Message):
    if message.forward_signature:
        return message.forward_signature
    if message.forward_sender_name:
        return message.forward_sender_name
    if message.forward_from:
        return message.forward_from.first_name + ((" " + message.forward_from.last_name) if message.forward_from.last_name else "")
    return 'Anonymous'

async def transform_to_model_input(messages: List[Message], progress_message: ProgressMessage):
    unique_users = set(map(get_user_name, messages))

    fake = faker.Faker()
    fake_names = [fake.first_name() for _ in range(len(unique_users))]
    from_fake = dict(zip(fake_names, unique_users))
    to_fake = dict(zip(unique_users, fake_names))

    lines = [to_fake[get_user_name(m)] + ": " + m.text for m in messages]
    print("Number of input messages:", len(lines))
    await progress_message.update("Preparing messages... (0/" + str(len(lines)) + ")")

    for i in range(len(lines)):
        lines[i] = lines[i].replace('\n', ' ')
        if any(['а' <= c <= 'я' for c in lines[i].lower()]):
            lines[i] = await translation_api.query_wrapper(lines[i], "ru_RU", "en_XX")
        await progress_message.update("Preparing messages... (" + str(i + 1) + "/" + str(len(lines)) + ")")

    return from_fake, '\n'.join(lines)

async def proccess_messages(analyzed_messages: List[Message], progress_message: ProgressMessage):
    fake_dict, model_input = await transform_to_model_input(analyzed_messages, progress_message)
    await progress_message.update("Summarizing...")
    model_output = await summarization_api.query_wrapper(model_input)
    for fake_name, real_name in fake_dict.items():
        model_output = model_output.replace(fake_name, real_name)
    await progress_message.update(model_output)

app.run()
