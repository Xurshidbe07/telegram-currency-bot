import asyncio
from telegram import Bot

TOKEN = "8944904572:AAFRNA08N1GmCAXL1XytRqHHkvgSKxfCbfA"
CHAT_ID = 5170546966

async def xabar_yubor():
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text="Salom!")

asyncio.run(xabar_yubor())