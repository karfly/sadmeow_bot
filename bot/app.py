import logging
import asyncio
import random
import os
import time
from uuid import uuid4
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackContext,
)
from telegram import Update
from telegram.constants import ParseMode

from bot.config import config

logger = logging.getLogger(__name__)

user_last_meow_time = {}
COOLDOWN_PERIOD = 10*60  # 30 seconds cooldown

# Define the total weight for probability calculations
TOTAL_WEIGHT = 10000

# Define the meows with their weights, file names, emojis, and rarity percentages
meows = {
    # Common (Total: 5,000 in 10,000 or 50% chance)
    "General Meow": {
        "weight": 2000,
        "file_name": "General Meow.mp3",
        "emoji": "😹",
        "rarity_percentage": "20%"
    },
    "Meow Meow": {
        "weight": 2000,
        "file_name": "Meow Meow.mp3",
        "emoji": "😹",
        "rarity_percentage": "20%"
    },
    "Simple Meow": {
        "weight": 1000,
        "file_name": "Simple Meow.mp3",
        "emoji": "😹",
        "rarity_percentage": "10%"
    },

    # Above Common (Total: 4,500 in 10,000 or 45% chance)
    "Angry Meow": {
        "weight": 800,
        "file_name": "Angry Meow.mp3",
        "emoji": "😽",
        "rarity_percentage": "8%"
    },
    "Choked Meow": {
        "weight": 600,
        "file_name": "Choked Meow.mp3",
        "emoji": "😽",
        "rarity_percentage": "6%"
    },
    "Cute Meow": {
        "weight": 600,
        "file_name": "Cute Meow.mp3",
        "emoji": "😽",
        "rarity_percentage": "6%"
    },
    "Disgruntled Meow": {
        "weight": 600,
        "file_name": "Disgruntled Meow.mp3",
        "emoji": "😽",
        "rarity_percentage": "6%"
    },
    "Long Cute Meow": {
        "weight": 600,
        "file_name": "Long Cute Meow.mp3",
        "emoji": "😽",
        "rarity_percentage": "6%"
    },
    "Mimimimimimi Meow": {
        "weight": 600,
        "file_name": "Mimimimimimi Meow.mp3",
        "emoji": "😽",
        "rarity_percentage": "6%"
    },
    "Scared Meow": {
        "weight": 400,
        "file_name": "Scared Meow.mp3",
        "emoji": "😽",
        "rarity_percentage": "4%"
    },
    "Scary Meow": {
        "weight": 300,
        "file_name": "Scary Meow.mp3",
        "emoji": "😽",
        "rarity_percentage": "3%"
    },

    # Rare (Total: 479 in 10,000 or 4.79% chance)
    "Careless Whisper Meow": {
        "weight": 200,
        "file_name": "Careless Whisper Meow.mp3",
        "emoji": "😼",
        "rarity_percentage": "2%"
    },
    "Cartoon Meow": {
        "weight": 100,
        "file_name": "Cartoon Meow.mp3",
        "emoji": "😼",
        "rarity_percentage": "1%"
    },
    "Disco Meow": {
        "weight": 80,
        "file_name": "Disco Meow.mp3",
        "emoji": "😼",
        "rarity_percentage": "0.8%"
    },
    "Never Gonna Give You Meow": {
        "weight": 60,
        "file_name": "Never Gonna Give You Meow.mp3",
        "emoji": "😼",
        "rarity_percentage": "0.6%"
    },
    "Six Meows": {
        "weight": 39,
        "file_name": "Six Meows.mp3",
        "emoji": "😼",
        "rarity_percentage": "0.39%"
    },

    # Super Rare (Total: 20 in 10,000 or 0.2% chance)
    "Imposter Meow (but cute)": {
        "weight": 10,
        "file_name": "Imposter Meow (but cute).mp3",
        "emoji": "😻",  # Assigned 😻 for Super Rare
        "rarity_percentage": "0.1%"
    },
    "N Meow": {
        "weight": 10,
        "file_name": "N Meow.mp3",
        "emoji": "😻",
        "rarity_percentage": "0.1%"
    },

    # Epic (Total: 1 in 10,000 or 0.01% chance)
    "SADMEOW": {
        "weight": 1,
        "file_name": "SADMEOW.mp3",
        "emoji": "🙀",
        "rarity_percentage": "0.01%"
    },
}

async def error_handler(update: Update, context: CallbackContext) -> None:
    error_id = str(uuid4())[:8]
    logger.error(
        msg=f"Exception while handling an update ({error_id}):",
        exc_info=context.error,
    )

async def meow_handler(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    current_time = time.time()

    # Check if the user is on cooldown
    if user_id in user_last_meow_time:
        last_meow_time = user_last_meow_time[user_id]
        if current_time - last_meow_time < COOLDOWN_PERIOD:
            # User is still on cooldown, do not reply
            return

    # Update the user's last meow time
    user_last_meow_time[user_id] = current_time

    try:
        files = list(meows.keys())
        weights = [meows[meow]['weight'] for meow in files]
        selected_meow = random.choices(files, weights=weights, k=1)[0]

        meow_info = meows[selected_meow]
        file_name = meow_info['file_name']
        emoji = meow_info['emoji']
        rarity_percentage = meow_info['rarity_percentage']

        # Construct the caption
        caption = f"{emoji} <b>{selected_meow}</b>\nRarity: <code>{rarity_percentage}</code> (best: <code>0.01%</code>)\n\n<i>Cooldown: you can send another meow in 10m</i>"

        file_path = os.path.join('meows', file_name)  # Adjust if your files are stored elsewhere

        with open(file_path, 'rb') as voice_file:
            await update.message.reply_voice(voice=voice_file, caption=caption, parse_mode=ParseMode.HTML)
    except Exception as e:
        logger.error(f"Error sending voice message: {e}")
        await update.message.reply_text("Meow", parse_mode=ParseMode.HTML)


def run_bot() -> None:
    print(config.telegram_token)
    application = (
        ApplicationBuilder()
        .token(config.telegram_token)
        .concurrent_updates(True)
        .http_version("1.1")
        .get_updates_http_version("1.1")
        .read_timeout(30)
        .write_timeout(30)
        .connect_timeout(30)
        .pool_timeout(30)
        .connection_pool_size(1024)
        .build()
    )

    # Add handlers
    application.add_handler(CommandHandler("meow", meow_handler))
    application.add_error_handler(error_handler)

    # Start the bot
    application.run_polling()
