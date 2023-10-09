import os
import faker
from pyrogram import Client, filters
from pyrogram.types import Message
from dotenv import load_dotenv
from typing import List
from pyrogram.enums import ChatAction
import huggingface_api

# Load environment variables from .env file
load_dotenv()

# Get API ID, API hash, and chat ID from environment variables
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

# Create a Pyrogram client instance
app = Client("my_bot", api_id, api_hash)

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
    response = await proccess_messages(analyzed_messages)
    await message.reply(response)

def get_user_name(message: Message):
    if message.forward_signature:
        return message.forward_signature
    if message.forward_sender_name:
        return message.forward_sender_name
    if message.forward_from:
        return message.forward_from.first_name + ((" " + message.forward_from.last_name) if message.forward_from.last_name else "")
    return 'Anonymous'

def transform_to_model_input(messages: List[Message]):
    unique_users = set(map(get_user_name, messages))

    fake = faker.Faker()
    fake_names = [fake.first_name() for _ in range(len(unique_users))]
    from_fake = dict(zip(fake_names, unique_users))
    to_fake = dict(zip(unique_users, fake_names))

    lines = [to_fake[get_user_name(m)] + ": " + m.text for m in messages]
    print("Number of input messages:", len(lines))

    return from_fake, '\n'.join(lines)

async def proccess_messages(analyzed_messages: List[Message]):
    fake_dict, model_input = transform_to_model_input(analyzed_messages)
    model_output = await huggingface_api.query_wrapper(model_input)
    for fake_name, real_name in fake_dict.items():
        model_output = model_output.replace(fake_name, real_name)
    return model_output

app.run()
