import logging
import asyncio
from uuid import uuid4
from telegram.ext import (
    ApplicationBuilder,
    AIORateLimiter,
    filters,
)

# telegram imports
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackContext,
)
from telegram.ext.filters import BaseFilter
from telegram.constants import ParseMode

from bot.config import config


logger = logging.getLogger(__name__)


async def error_handler(update: Update, context: CallbackContext) -> None:
    error_id = str(uuid4())[:8]
    logger.error(msg=f"Exception while handling an update ({error_id}):", exc_info=context.error)


async def meow_handler(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Meow", parse_mode=ParseMode.MARKDOWN)



def run_bot() -> None:
    application = (
        ApplicationBuilder()
        .token(config.telegram_token)
        .concurrent_updates(True)
        # .rate_limiter(AIORateLimiter(max_retries=3))
        .http_version("1.1")
        .get_updates_http_version("1.1")
        .read_timeout(30)
        .write_timeout(30)
        .connect_timeout(30)
        .pool_timeout(30)
        .connection_pool_size(1024)
        .build()
    )

    # add handlers
    application.add_handler(CommandHandler("meow", meow_handler))
    application.add_error_handler(error_handler)

    # start the bot
    application.run_polling()
