from aiogram import Bot, Router
from aiogram.types import CallbackQuery

from handlers.function import download_and_send_media
import url_storage as storage
import task_storage
import keyboard.inline_kb as in_kb
import asyncio

router = Router()

@router.callback_query(lambda callback: 'video' in callback.data or 'audio' in callback.data)
async def format_selection(callback: CallbackQuery, bot: Bot):
    storage.url_storage = storage.load_url_storage()
    action, url_id = callback.data.split("|")
    url = storage.url_storage.get(url_id)

    if not url:
        await callback.answer("Ошибка: URL не найден!")
        return

    await callback.answer("Подтверждено!")
    await callback.message.answer("Начинаю загрузку...")
    await callback.message.answer("⏳ Загрузка идет...", reply_markup=await in_kb.cancel_btn(url_id))

    task = asyncio.create_task(download_and_send_media(bot, callback.message.chat.id, url, media_type=action, url_id=url_id))
    task_storage.active_tasks[url_id] = task

@router.callback_query(lambda callback: callback.data.startswith("cancel|"))
async def cancel_download(callback: CallbackQuery):
    _, url_id = callback.data.split("|")
    task = task_storage.active_tasks.get(url_id)

    if task and not task.done():
        task.cancel()
        await callback.message.answer("❌ Загрузка отменена.")
    else:
        await callback.message.answer("Задача уже завершена или не найдена.")
