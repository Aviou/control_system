# startup.py
import asyncio
from .telegram_bot import main as start_telegram_bot_main

def start_bot():
    asyncio.run(start_telegram_bot_main())
