import os
import hashlib
import yt_dlp
import time
import uuid
import asyncio
from aiogram.types import FSInputFile
from task_storage import active_tasks


def generate_url_id(url: str):
    return hashlib.md5(url.encode()).hexdigest()


async def download_and_send_media(bot, chat_id, url, media_type, url_id):
    os.makedirs("downloads", exist_ok=True)

    url_hash = generate_url_id(url)
    unique_id = uuid.uuid4().hex[:6]
    ext = "mp4" if media_type == "video" else "m4a"
    filename = f"downloads/{url_hash}_{unique_id}.{ext}"

    ydl_opts = {
        'format': 'best[ext=mp4]' if media_type == 'video' else 'bestaudio[ext=m4a]',
        'outtmpl': filename,
        'quiet': True,
        'noplaylist': True,
    }

    try:
        start_time = time.time()

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        end_time = time.time()
        elapsed_time = end_time - start_time

        if not os.path.exists(filename):
            actual_files = [f for f in os.listdir("downloads") if f.startswith(f"{url_hash}_{unique_id}")]
            if actual_files:
                filename = os.path.join("downloads", actual_files[0])

        media_file = FSInputFile(filename)
        caption = f"Готово! Время загрузки: {elapsed_time:.2f} сек."

        if media_type == "video":
            await bot.send_video(chat_id, media_file, caption=caption)
        else:
            await bot.send_audio(chat_id, media_file, caption=caption)

    except asyncio.CancelledError:
        await bot.send_message(chat_id, "⚠️ Загрузка была отменена.")
    except Exception as e:
        await bot.send_message(chat_id, f"❌ Ошибка: {str(e)}")
    finally:
        if os.path.exists(filename):
            os.remove(filename)
        active_tasks.pop(url_id, None)
