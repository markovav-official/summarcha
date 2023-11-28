from pydantic import BaseModel


class Message(BaseModel):
    username: str
    text: str
    user_id: int
