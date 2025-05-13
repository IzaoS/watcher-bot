import requests
from bs4 import BeautifulSoup
import hashlib
import asyncio
from telegram import Bot
import logging

TOKEN = '7784636064:AAGXfXfunLC7yIBcYYQM4fVoIfNBXU2v9wc'
USER_ID = 833793492
URL = 'https://лмх.com/capsule'

bot = Bot(token=TOKEN)
last_hash = None

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s — %(message)s'
)

def get_page_hash():
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(URL, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.get_text(strip=True)
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    except Exception as e:
        logging.error(f"Ошибка при загрузке: {e}")
        asyncio.create_task(
            bot.send_message(chat_id=USER_ID, text=f"❌ Ошибка при проверке сайта:\n{e}")
        )
        return None

async def check_for_changes():
    global last_hash
    current_hash = get_page_hash()
    if current_hash and current_hash != last_hash:
        last_hash = current_hash
        await bot.send_message(chat_id=USER_ID, text="⚠️ Обновление на странице: " + URL)
        logging.info("Обновление отправлено.")
    else:
        logging.info("Без изменений.")

async def main():
    logging.info("Бот запущен.")
    while True:
        await check_for_changes()
        await asyncio.sleep(300)

if __name__ == "__main__":
    asyncio.run(main())
