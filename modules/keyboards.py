"""
Telegram bot keyboard layouts
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import CALLBACK_DATA
from .languages import get_message

def get_main_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Get the main menu keyboard."""
    keyboard = [
        [
            InlineKeyboardButton(get_message('synonyms_btn', lang), callback_data=CALLBACK_DATA['SYNONYMS']),
            InlineKeyboardButton(get_message('antonyms_btn', lang), callback_data=CALLBACK_DATA['ANTONYMS'])
        ],
        [
            InlineKeyboardButton(get_message('both_btn', lang), callback_data=CALLBACK_DATA['BOTH']),
            InlineKeyboardButton(get_message('save_btn', lang), callback_data=CALLBACK_DATA['SAVE_WORD'])
        ],
        [
            InlineKeyboardButton(get_message('view_saved_btn', lang), callback_data=CALLBACK_DATA['VIEW_SAVED']),
            InlineKeyboardButton(get_message('download_saved_btn', lang), callback_data=CALLBACK_DATA['DOWNLOAD_SAVED'])
        ],
        [
            InlineKeyboardButton(get_message('switch_lang_btn', lang), callback_data=CALLBACK_DATA['SWITCH_LANG'])
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Get the back button keyboard."""
    keyboard = [[
        InlineKeyboardButton(get_message('back_btn', lang), callback_data=CALLBACK_DATA['BACK'])
    ]]
    return InlineKeyboardMarkup(keyboard) 