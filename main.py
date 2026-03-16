import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.client.session.aiohttp import AiohttpSession

BOT_TOKEN = "YOU_BOT"


dp = Dispatcher(storage=MemoryStorage())

tasks = []



class TaskState(StatesGroup):
    waiting_for_task = State()


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Привет! Я бот для задач.\n\n"
        "/add - добавить задачу\n"
        "/tasks - показать задачи\n"
        "/done - выполнить задачу\n"
        "/delete - удалить задачу\n"
        "/stats - статистика"
    )

@dp.message(Command("add"))
async def add_task(message: Message, state: FSMContext):
    await message.answer("Напиши задачу")
    await state.set_state(TaskState.waiting_for_task)

@dp.message(TaskState.waiting_for_task)
async def save_task(message: Message, state: FSMContext):

    task = {
        "text": message.text,
        "done": False
    }

    tasks.append(task)

    await message.answer("Задача добавлена!")
    await state.clear()


@dp.message(Command("tasks"))
async def show_tasks(message: Message):

    if not tasks:
        await message.answer("Список задач пуст")
        return

    text = "Ваши задачи:\n\n"

    for i, task in enumerate(tasks, start=1):
        status = "✅" if task["done"] else "❌"
        text += f"{i}. {task['text']} {status}\n"

    await message.answer(text)


@dp.message(Command("done"))
async def done_task(message: Message):

    try:
        number = int(message.text.split()[1])
        tasks[number - 1]["done"] = True

        await message.answer("Задача выполнена ✅")

    except:
        await message.answer("Напиши номер задачи. Пример: /done 2")


@dp.message(Command("delete"))
async def delete_task(message: Message):

    try:
        number = int(message.text.split()[1])
        tasks.pop(number - 1)

        await message.answer("Задача удалена")

    except:
        await message.answer("Напиши номер задачи. Пример: /delete 1")


@dp.message(Command("stats"))
async def stats(message: Message):

    total = len(tasks)
    done = sum(1 for task in tasks if task["done"])
    left = total - done

    text = (
        f"Всего задач: {total}\n"
        f"Выполнено: {done}\n"
        f"Осталось: {left}"
    )

    await message.answer(text)

async def main():
    session = AiohttpSession(proxy="http://oNKKt5:H0ET6w@161.115.231.116:9019")
    bot = Bot(
        token=BOT_TOKEN,
        session=session
    )

    print("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())



