"""
Telegram bot command handlers
"""
from telegram import Update, ParseMode
from telegram.ext import CallbackContext, ConversationHandler
from .wordnet_utils import get_word_info, format_word_info
from .languages import get_message
from .keyboards import get_main_keyboard, get_back_keyboard
import json
import os
import logging
from typing import Dict, Any
from config import DEFAULT_LANGUAGE, CALLBACK_DATA

# States for conversation handler
AWAITING_WORD = 1

logger = logging.getLogger(__name__)

# Load user data
def load_user_data() -> Dict[str, Any]:
    try:
        with open('data/user_data.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Save user data
def save_user_data(data: Dict[str, Any]) -> None:
    os.makedirs('data', exist_ok=True)
    with open('data/user_data.json', 'w') as f:
        json.dump(data, f, indent=2)

def get_user_language(user_id: int) -> str:
    """Get user's preferred language."""
    user_data = load_user_data()
    return user_data.get(str(user_id), {}).get('language', DEFAULT_LANGUAGE)

def set_user_language(user_id: int, language: str) -> None:
    """Set user's preferred language."""
    user_data = load_user_data()
    if str(user_id) not in user_data:
        user_data[str(user_id)] = {}
    user_data[str(user_id)]['language'] = language
    save_user_data(user_data)

def start_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    
    update.message.reply_text(
        get_message('welcome', lang),
        reply_markup=get_main_keyboard(lang),
        parse_mode=ParseMode.MARKDOWN
    )

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    
    update.message.reply_text(
        get_message('help', lang),
        reply_markup=get_main_keyboard(lang),
        parse_mode=ParseMode.MARKDOWN
    )

def process_word_command(update: Update, context: CallbackContext, mode: str) -> None:
    """Process word-related commands (synonym, antonym, both)."""
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    
    logger.info(f"Processing word command with mode: {mode}")
    
    if not context.args:
        update.message.reply_text(
            get_message('provide_word', lang).format(mode),
            reply_markup=get_main_keyboard(lang),
            parse_mode=ParseMode.MARKDOWN
        )
        return

    word = context.args[0].lower()
    logger.info(f"Looking up word: {word}")
    
    info = get_word_info(word)
    response = format_word_info(word, info, mode, lang)
    
    # Save to user history
    if info is not None:
        user_data = load_user_data()
        user_id_str = str(user_id)
        
        if user_id_str not in user_data:
            user_data[user_id_str] = {'history': [], 'language': lang}
        elif 'history' not in user_data[user_id_str]:
            user_data[user_id_str]['history'] = []
            
        if word not in [item['word'] for item in user_data[user_id_str]['history']]:
            user_data[user_id_str]['history'].append({
                'word': word,
                'info': info
            })
            user_data[user_id_str]['history'] = user_data[user_id_str]['history'][-10:]
            save_user_data(user_data)
    
    logger.info(f"Sending response for word: {word}")
    update.message.reply_text(
        response,
        reply_markup=get_main_keyboard(lang),
        parse_mode=ParseMode.MARKDOWN
    )

def synonym_command(update: Update, context: CallbackContext) -> None:
    """Handle the /synonym command."""
    process_word_command(update, context, 'synonym')

def antonym_command(update: Update, context: CallbackContext) -> None:
    """Handle the /antonym command."""
    process_word_command(update, context, 'antonym')

def both_command(update: Update, context: CallbackContext) -> None:
    """Handle the /both command."""
    process_word_command(update, context, 'both')

def saved_command(update: Update, context: CallbackContext) -> None:
    """Show user's saved words."""
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    user_data = load_user_data()
    
    if str(user_id) not in user_data or not user_data[str(user_id)]['history']:
        update.message.reply_text(
            get_message('saved_words_empty', lang),
            reply_markup=get_main_keyboard(lang),
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    response = [get_message('saved_words_title', lang)]
    for item in user_data[str(user_id)]['history']:
        word = item['word']
        syn_count = len(item['info']['synonyms'])
        ant_count = len(item['info']['antonyms'])
        response.append(get_message('word_stats', lang).format(word, syn_count, ant_count))
    
    update.message.reply_text(
        '\n'.join(response),
        reply_markup=get_main_keyboard(lang),
        parse_mode=ParseMode.MARKDOWN
    )

def button_handler(update: Update, context: CallbackContext) -> None:
    """Handle button presses."""
    query = update.callback_query
    user_id = query.from_user.id
    lang = get_user_language(user_id)
    
    logger.info(f"Button pressed with data: {query.data}")
    query.answer()  # Acknowledge the button press
    
    if query.data == CALLBACK_DATA['SWITCH_LANG']:
        new_lang = 'en' if lang == 'ru' else 'ru'
        set_user_language(user_id, new_lang)
        query.edit_message_text(
            get_message('welcome', new_lang),
            reply_markup=get_main_keyboard(new_lang),
            parse_mode=ParseMode.MARKDOWN
        )
    elif query.data == CALLBACK_DATA['SYNONYMS']:
        context.user_data['mode'] = 'synonym'
        query.edit_message_text(
            get_message('enter_word', lang),
            reply_markup=get_back_keyboard(lang),
            parse_mode=ParseMode.MARKDOWN
        )
        return AWAITING_WORD
    elif query.data == CALLBACK_DATA['ANTONYMS']:
        context.user_data['mode'] = 'antonym'
        query.edit_message_text(
            get_message('enter_word', lang),
            reply_markup=get_back_keyboard(lang),
            parse_mode=ParseMode.MARKDOWN
        )
        return AWAITING_WORD
    elif query.data == CALLBACK_DATA['BOTH']:
        context.user_data['mode'] = 'both'
        query.edit_message_text(
            get_message('enter_word', lang),
            reply_markup=get_back_keyboard(lang),
            parse_mode=ParseMode.MARKDOWN
        )
        return AWAITING_WORD
    elif query.data == CALLBACK_DATA['SAVED']:
        # Create a message object for saved_command
        message = type('Message', (), {})()
        message.reply_text = query.edit_message_text
        update.message = message
        saved_command(update, context)
    elif query.data == CALLBACK_DATA['BACK']:
        query.edit_message_text(
            get_message('welcome', lang),
            reply_markup=get_main_keyboard(lang),
            parse_mode=ParseMode.MARKDOWN
        )
    
    return ConversationHandler.END

def text_handler(update: Update, context: CallbackContext) -> None:
    """Handle regular text messages."""
    word = update.message.text.strip().lower()
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    
    logger.info(f"Received text: {word}")
    logger.info(f"Current mode: {context.user_data.get('mode', 'both')}")
    
    if len(word.split()) > 1:
        update.message.reply_text(
            get_message('one_word_only', lang),
            reply_markup=get_main_keyboard(lang),
            parse_mode=ParseMode.MARKDOWN
        )
        return ConversationHandler.END
    
    # Set the word as an argument for the command handlers
    context.args = [word]
    
    # Get the current mode, defaulting to 'both' if not set
    mode = context.user_data.get('mode', 'both')
    logger.info(f"Processing word '{word}' with mode: {mode}")
    
    # Process the word based on the current mode
    process_word_command(update, context, mode)
    
    # Clear the mode after processing
    if 'mode' in context.user_data:
        del context.user_data['mode']
    
    return ConversationHandler.END