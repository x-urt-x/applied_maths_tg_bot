from aiogram.types import Message
from aiogram import Router
from aiogram.filters import CommandStart

user_router = Router()

@user_router.message(CommandStart())
async def hello_world(message: Message):
    await message.answer("hello world")