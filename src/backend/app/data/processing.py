from app.schemas import Message
from ml.T5_summarizer import summarize
from collections import Counter


def extract_bot_commands(messages: list[Message]) -> (list[Message], Counter[str]):
    bot_commands = Counter()
    filtered_messages = []
    for message in messages:
        if message.text.startswith("/"):
            bot_commands.update([message.text])
        else:
            filtered_messages.append(message)

    return filtered_messages, bot_commands


def truncate_each(
    messages: list[Message], min_length: int = 2, max_length: int = 256
) -> list[Message]:
    return [
        Message(
            username=message.username,
            text=message.text[:max_length],
            user_id=message.user_id,
        )
        for message in messages
        if min_length <= len(message.text)
    ]


def summarize_messages(messages: list[Message]) -> str:
    grouped_messages = []
    for message in messages:
        if len(grouped_messages) > 0 and grouped_messages[-1].user_id == message.user_id:
            grouped_messages[-1].text += "\n" + message.text
        else:
            grouped_messages.append(message)


    text = "\n".join(message.username + message.text for message in grouped_messages)
    summarized = summarize(text)

    return summarized


def process_messages(
    messages: list[Message], include_command_stats: bool = True
) -> str:
    messages, bot_commands = extract_bot_commands(messages)
    messages = truncate_each(messages)
    res = summarize_messages(messages)

    if include_command_stats and bot_commands:
        res += "\n\nCommand stats:\n" + "\n".join(
            f"{command}: {count}" for command, count in bot_commands.items()
        )

    return res


if __name__ == "__main__":
    messages = [
        Message(username="user1", text="Hel", user_id=1),
        Message(username="user2", text="/summarize", user_id=2),
        Message(username="user3", text="/summarize", user_id=3),
        Message(username="user4", text="/summarize", user_id=4),
        Message(username="user5", text="Some text", user_id=5),
        Message(username="user6", text="/chel_s_dr", user_id=6),
    ]

    print(process_messages(messages, include_command_stats=True))
