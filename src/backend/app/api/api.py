from fastapi.routing import APIRouter
from app.schemas import Message, Summary
from asyncio import sleep

api_router = APIRouter()


@api_router.post("/summarize", response_model=Summary)
async def summarize(messages: list[Message]):
    await sleep(2)
    return Summary(content="\n".join(message.text for message in messages))
