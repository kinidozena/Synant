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
from pathlib import Path
from config import DEFAULT_LANGUAGE, CALLBACK_DATA, SAVE_PATHS_FILE

# States for conversation handler
AWAITING_WORD = 1
AWAITING_SAVE_PATH = 2

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

def load_save_paths() -> Dict[str, str]:
    """Load save paths for all users."""
    try:
        os.makedirs(os.path.dirname(SAVE_PATHS_FILE), exist_ok=True)
        with open(SAVE_PATHS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_save_paths(paths: Dict[str, str]) -> None:
    """Save the save paths for all users."""
    os.makedirs(os.path.dirname(SAVE_PATHS_FILE), exist_ok=True)
    with open(SAVE_PATHS_FILE, 'w') as f:
        json.dump(paths, f, indent=2)

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

def get_user_save_path(user_id: int) -> str:
    """Get user's save file path."""
    paths = load_save_paths()
    return paths.get(str(user_id), '')

def set_user_save_path(user_id: int, save_path: str) -> None:
    """Set user's save file path."""
    paths = load_save_paths()
    paths[str(user_id)] = save_path
    save_save_paths(paths)

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
    elif query.data == CALLBACK_DATA['SETUP_PATH']:
        query.edit_message_text(
            get_message('enter_save_path', lang),
            reply_markup=get_back_keyboard(lang),
            parse_mode=ParseMode.MARKDOWN
        )
        return AWAITING_SAVE_PATH
    elif query.data == CALLBACK_DATA['SAVE_WORD']:
        save_path = get_user_save_path(user_id)
        if not save_path:
            query.edit_message_text(
                get_message('setup_path_first', lang),
                reply_markup=get_main_keyboard(lang),
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            context.user_data['mode'] = 'save'
            query.edit_message_text(
                get_message('enter_word_save', lang),
                reply_markup=get_back_keyboard(lang),
                parse_mode=ParseMode.MARKDOWN
            )
            return AWAITING_WORD
    elif query.data == CALLBACK_DATA['VIEW_SAVED']:
        # Create a message object for show_saved_command
        message = type('Message', (), {})()
        message.reply_text = query.edit_message_text
        update.message = message
        show_saved_command(update, context)
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
    elif query.data == CALLBACK_DATA['BACK']:
        query.edit_message_text(
            get_message('welcome', lang),
            reply_markup=get_main_keyboard(lang),
            parse_mode=ParseMode.MARKDOWN
        )
    
    return ConversationHandler.END

def text_handler(update: Update, context: CallbackContext) -> None:
    """Handle regular text messages."""
    text = update.message.text.strip()
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    
    logger.info(f"Received text: {text}")
    
    # Check if we're waiting for a save path
    if context.user_data.get('awaiting_path'):
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(text), exist_ok=True)
            
            # Try to create/open the file
            with open(text, 'a+', encoding='utf-8') as f:
                if f.tell() == 0:  # If file is empty
                    json.dump([], f)
            
            # Save the path in persistent storage
            set_user_save_path(user_id, text)
            
            update.message.reply_text(
                f"✅ Save location has been set to:\n`{text}`\n\n"
                "You can now use the /save command to save words!\n"
                "This path will be remembered even if the bot restarts.",
                reply_markup=get_main_keyboard(lang),
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception as e:
            logger.error(f"Error setting up save path: {e}")
            update.message.reply_text(
                "❌ Error: Could not set up the save location. Please make sure:\n"
                "• The path is valid\n"
                "• You have write permissions\n"
                "• The directory exists or can be created",
                reply_markup=get_main_keyboard(lang),
                parse_mode=ParseMode.MARKDOWN
            )
        
        del context.user_data['awaiting_path']
        return ConversationHandler.END
    
    # Handle word input
    if len(text.split()) > 1:
        update.message.reply_text(
            get_message('one_word_only', lang),
            reply_markup=get_main_keyboard(lang),
            parse_mode=ParseMode.MARKDOWN
        )
        return ConversationHandler.END
    
    # Set the word as an argument for the command handlers
    context.args = [text]
    
    # Get the current mode, defaulting to 'both' if not set
    mode = context.user_data.get('mode', 'both')
    logger.info(f"Processing word '{text}' with mode: {mode}")
    
    # Process the word based on the current mode
    if mode == 'save':
        save_word_command(update, context)
    else:
        process_word_command(update, context, mode)
    
    # Clear the mode after processing
    if 'mode' in context.user_data:
        del context.user_data['mode']
    
    return ConversationHandler.END

def setup_save_path_command(update: Update, context: CallbackContext) -> int:
    """Set up the save path for words."""
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    
    if not context.args:
        update.message.reply_text(
            "Please provide the full path where you want to save your words.\n"
            "Example: /setup_path C:/Users/YourName/Documents/saved_words.json\n"
            "Make sure you have write permissions for this location.",
            reply_markup=get_main_keyboard(lang),
            parse_mode=ParseMode.MARKDOWN
        )
        return ConversationHandler.END

    save_path = ' '.join(context.args)
    
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # Try to create/open the file
        with open(save_path, 'a+', encoding='utf-8') as f:
            if f.tell() == 0:  # If file is empty
                json.dump([], f)
        
        # Save the path in persistent storage
        set_user_save_path(user_id, save_path)
        
        update.message.reply_text(
            f"✅ Save location has been set to:\n`{save_path}`\n\n"
            "You can now use the /save command to save words!\n"
            "This path will be remembered even if the bot restarts.",
            reply_markup=get_main_keyboard(lang),
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        logger.error(f"Error setting up save path: {e}")
        update.message.reply_text(
            "❌ Error: Could not set up the save location. Please make sure:\n"
            "• The path is valid\n"
            "• You have write permissions\n"
            "• The directory exists or can be created",
            reply_markup=get_main_keyboard(lang),
            parse_mode=ParseMode.MARKDOWN
        )
    
    return ConversationHandler.END

def save_word_command(update: Update, context: CallbackContext) -> None:
    """Save a word to the user's save file."""
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    save_path = get_user_save_path(user_id)
    
    if not save_path:
        update.message.reply_text(
            "⚠️ You need to set up a save location first!\n\n"
            "Use the /setup_path command followed by your desired save location.\n"
            "Example: `/setup_path C:/Users/YourName/Documents/saved_words.json`",
            reply_markup=get_main_keyboard(lang),
            parse_mode=ParseMode.MARKDOWN
        )
        return

    if not context.args:
        update.message.reply_text(
            get_message('provide_word', lang).format('save'),
            reply_markup=get_main_keyboard(lang),
            parse_mode=ParseMode.MARKDOWN
        )
        return

    word = context.args[0].lower()
    info = get_word_info(word)
    
    if info is None:
        update.message.reply_text(
            get_message('word_not_found', lang),
            reply_markup=get_main_keyboard(lang),
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    try:
        # Read existing words
        try:
            with open(save_path, 'r', encoding='utf-8') as f:
                saved_words = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            saved_words = []
            
        # Check if word already exists
        if word not in [item['word'] for item in saved_words]:
            saved_words.append({
                'word': word,
                'synonyms': info['synonyms'],
                'antonyms': info['antonyms']
            })
            
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(saved_words, f, indent=2, ensure_ascii=False)
            
            update.message.reply_text(
                f"✅ The word '{word}' has been saved!",
                reply_markup=get_main_keyboard(lang),
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            update.message.reply_text(
                f"ℹ️ The word '{word}' is already in your saved list.",
                reply_markup=get_main_keyboard(lang),
                parse_mode=ParseMode.MARKDOWN
            )
            
    except Exception as e:
        logger.error(f"Error saving word: {e}")
        update.message.reply_text(
            "❌ Error saving the word. Please check if your save location is still accessible.",
            reply_markup=get_main_keyboard(lang),
            parse_mode=ParseMode.MARKDOWN
        )

def show_saved_command(update: Update, context: CallbackContext) -> None:
    """Show user's saved words from their save file."""
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    save_path = get_user_save_path(user_id)
    
    if not save_path:
        update.message.reply_text(
            "⚠️ You need to set up a save location first!\n\n"
            "Use the /setup_path command followed by your desired save location.\n"
            "Example: `/setup_path C:/Users/YourName/Documents/saved_words.json`",
            reply_markup=get_main_keyboard(lang),
            parse_mode=ParseMode.MARKDOWN
        )
        return
        
    try:
        if not os.path.exists(save_path):
            update.message.reply_text(
                "You don't have any saved words yet.",
                reply_markup=get_main_keyboard(lang),
                parse_mode=ParseMode.MARKDOWN
            )
            return
            
        with open(save_path, 'r', encoding='utf-8') as f:
            saved_words = json.load(f)
            
        if not saved_words:
            update.message.reply_text(
                "You don't have any saved words yet.",
                reply_markup=get_main_keyboard(lang),
                parse_mode=ParseMode.MARKDOWN
            )
            return
            
        response = ["📚 *Your saved words:*\n"]
        for item in saved_words:
            word = item['word']
            syn_count = len(item['synonyms'])
            ant_count = len(item['antonyms'])
            response.append(f"• *{word}* - {syn_count} synonyms, {ant_count} antonyms")
        
        update.message.reply_text(
            '\n'.join(response),
            reply_markup=get_main_keyboard(lang),
            parse_mode=ParseMode.MARKDOWN
        )
            
    except Exception as e:
        logger.error(f"Error reading saved words: {e}")
        update.message.reply_text(
            "❌ Error reading your saved words. Please check if your save location is still accessible.",
            reply_markup=get_main_keyboard(lang),
            parse_mode=ParseMode.MARKDOWN
        )