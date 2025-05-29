#!/usr/bin/env python3
"""
Telegram Synonym/Antonym Bot - Main Entry Point
"""
import logging
from telegram.ext import (
    Updater, CommandHandler, MessageHandler, Filters,
    CallbackQueryHandler, ConversationHandler
)
from config import BOT_TOKEN
from modules.bot_handlers import (
    start_command, help_command, synonym_command, antonym_command,
    both_command, saved_command, text_handler, button_handler,
    AWAITING_WORD
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token
    updater = Updater(BOT_TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Create conversation handler
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start_command),
            CommandHandler("help", help_command),
            CommandHandler("synonym", synonym_command),
            CommandHandler("antonym", antonym_command),
            CommandHandler("both", both_command),
            CommandHandler("saved", saved_command),
            CallbackQueryHandler(button_handler)
        ],
        states={
            AWAITING_WORD: [
                MessageHandler(Filters.text & ~Filters.command, text_handler),
                CallbackQueryHandler(button_handler)
            ]
        },
        fallbacks=[
            CommandHandler("start", start_command),
            CallbackQueryHandler(button_handler)
        ]
    )

    # Add conversation handler
    dp.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()
    logger.info("Bot started. Press Ctrl+C to stop.")

    # Run the bot until you press Ctrl-C
    updater.idle()


if __name__ == '__main__':
    main()