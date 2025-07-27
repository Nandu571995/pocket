from telegram_bot import start_telegram_bot
from pocket_bot import run_signal_engine
import asyncio

async def main():
    # Run both the telegram bot and the signal engine concurrently
    await asyncio.gather(
        start_telegram_bot(),
        run_signal_engine()
    )

if __name__ == "__main__":
    asyncio.run(main())
