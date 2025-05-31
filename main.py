#!/usr/bin/env python3
"""
Telegram Synonym/Antonym Bot - Main Entry Point (PythonAnywhere Version)
"""
import logging
from flask import Flask, request
from telegram.ext import (
    Dispatcher, CommandHandler, MessageHandler, Filters,
    CallbackQueryHandler, ConversationHandler
)
from telegram import Update, Bot
from config import BOT_TOKEN
from modules.bot_handlers import (
    start_command, help_command, synonym_command, antonym_command,
    both_command, save_word_command, show_saved_command, text_handler, 
    button_handler, setup_save_path_command,
    AWAITING_WORD, AWAITING_SAVE_PATH
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)

# Create conversation handler
conv_handler = ConversationHandler(
    entry_points=[
        CommandHandler("start", start_command),
        CommandHandler("help", help_command),
        CommandHandler("synonym", synonym_command),
        CommandHandler("antonym", antonym_command),
        CommandHandler("both", both_command),
        CommandHandler("setup_path", setup_save_path_command),
        CommandHandler("save", save_word_command),
        CommandHandler("saved", show_saved_command),
        CallbackQueryHandler(button_handler)
    ],
    states={
        AWAITING_WORD: [
            MessageHandler(Filters.text & ~Filters.command, text_handler),
            CallbackQueryHandler(button_handler)
        ],
        AWAITING_SAVE_PATH: [
            MessageHandler(Filters.text & ~Filters.command, text_handler),
            CallbackQueryHandler(button_handler)
        ]
    },
    fallbacks=[
        CommandHandler("start", start_command),
        CommandHandler("help", help_command),
        CallbackQueryHandler(button_handler)
    ]
)

# Add conversation handler
dispatcher.add_handler(conv_handler)

@app.route('/webhook_path', methods=['POST'])
def webhook():
    """Handle incoming webhook updates."""
    update = Update.de_json(request.get_json(), bot)
    dispatcher.process_update(update)
    return 'ok'

def set_webhook():
    """Set webhook for the bot."""
    # Replace USERNAME with your PythonAnywhere username
    webhook_url = 'https://YOUR_USERNAME.pythonanywhere.com/webhook_path'
    bot.set_webhook(webhook_url)
    logger.info(f"Webhook set to {webhook_url}")

if __name__ == '__main__':
    # Set the webhook when running the script
    set_webhook()
    # Run the Flask application
    app.run()