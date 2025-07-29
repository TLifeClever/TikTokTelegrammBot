from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def format_btn(url_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎬 Видео", callback_data=f"video|{url_id}")],
        [InlineKeyboardButton(text="🎵 Аудио", callback_data=f"audio|{url_id}")]
    ])

async def cancel_btn(url_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отменить загрузку", callback_data=f"cancel|{url_id}")]
    ])
