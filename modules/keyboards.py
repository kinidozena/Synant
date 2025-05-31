"""
Keyboard layouts for the Telegram Synonym/Antonym Bot
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import CALLBACK_DATA
from .languages import get_message

def get_main_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Create the main menu keyboard."""
    keyboard = [
        [
            InlineKeyboardButton(get_message('find_synonyms', lang), 
                               callback_data=CALLBACK_DATA['SYNONYMS']),
            InlineKeyboardButton(get_message('find_antonyms', lang), 
                               callback_data=CALLBACK_DATA['ANTONYMS'])
        ],
        [
            InlineKeyboardButton(get_message('find_both', lang), 
                               callback_data=CALLBACK_DATA['BOTH'])
        ],
        [
            InlineKeyboardButton(get_message('setup_path', lang), 
                               callback_data=CALLBACK_DATA['SETUP_PATH']),
            InlineKeyboardButton(get_message('save_word', lang), 
                               callback_data=CALLBACK_DATA['SAVE_WORD'])
        ],
        [
            InlineKeyboardButton(get_message('view_saved', lang), 
                               callback_data=CALLBACK_DATA['VIEW_SAVED']),
            InlineKeyboardButton(get_message('switch_language', lang), 
                               callback_data=CALLBACK_DATA['SWITCH_LANG'])
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Create a keyboard with just a back button."""
    keyboard = [[
        InlineKeyboardButton("⬅️ " + get_message('back', lang), 
                           callback_data=CALLBACK_DATA['BACK'])
    ]]
    return InlineKeyboardMarkup(keyboard) 