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
from config import DEFAULT_LANGUAGE, CALLBACK_DATA, SAVE_PATHS_FILE, MAX_SAVED_WORDS

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
    """Send a welcome message when the command /start is issued."""
    user = update.effective_user
    user_id = user.id
    
    # Detect user's language from Telegram settings
    user_lang_code = update.effective_user.language_code
    # Map common language codes to our supported languages
    lang = 'ru' if user_lang_code and user_lang_code.lower().startswith('ru') else 'en'
    
    # Save the detected language preference
    set_user_language(user_id, lang)
    
    # Create a personalized welcome message
    first_name = user.first_name or "there"
    personal_greeting = f"Hi {first_name}! " if lang == 'en' else f"Привет, {first_name}! "
    
    # Send the welcome message
    update.message.reply_text(
        personal_greeting + get_message('welcome', lang),
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
        try:
            update.message.reply_text(
                get_message('provide_word', lang).format(mode),
                reply_markup=get_main_keyboard(lang),
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception as e:
            logger.error(f"Error sending prompt message: {str(e)}")
        return

    word = context.args[0].lower()
    logger.info(f"Looking up word: {word}")
    
    try:
        info = get_word_info(word)
        logger.info(f"Got word info for '{word}': {'Found' if info else 'Not found'}")
        
        response = format_word_info(word, info, mode, lang)
        logger.info(f"Formatted response for '{word}' (length: {len(response)})")
        
        # Split response if it's too long
        MAX_MESSAGE_LENGTH = 4096
        if len(response) > MAX_MESSAGE_LENGTH:
            logger.info(f"Response too long ({len(response)} chars), splitting into multiple messages")
            chunks = [response[i:i + MAX_MESSAGE_LENGTH] for i in range(0, len(response), MAX_MESSAGE_LENGTH)]
            for chunk in chunks:
                try:
                    update.message.reply_text(
                        chunk,
                        reply_markup=get_main_keyboard(lang),
                        parse_mode=ParseMode.MARKDOWN
                    )
                except Exception as e:
                    logger.error(f"Error sending response chunk: {str(e)}")
        else:
            try:
                update.message.reply_text(
                    response,
                    reply_markup=get_main_keyboard(lang),
                    parse_mode=ParseMode.MARKDOWN
                )
                logger.info(f"Successfully sent response for '{word}'")
            except Exception as e:
                logger.error(f"Error sending response: {str(e)}")
                # Try sending without markdown if there might be a markdown formatting issue
                try:
                    update.message.reply_text(
                        "Sorry, there was an error formatting the response. Here it is without formatting:\n\n" + 
                        response.replace('*', '').replace('_', '').replace('`', ''),
                        reply_markup=get_main_keyboard(lang)
                    )
                except Exception as e2:
                    logger.error(f"Error sending plain text response: {str(e2)}")
                    # Last resort - send a simple error message
                    try:
                        update.message.reply_text(
                            get_message('error_occurred', lang),
                            reply_markup=get_main_keyboard(lang)
                        )
                    except Exception as e3:
                        logger.error(f"Failed to send error message: {str(e3)}")
        
        # Save to user history
        if info is not None:
            try:
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
            except Exception as e:
                logger.error(f"Error saving to user history: {str(e)}")
    
    except Exception as e:
        logger.error(f"Error processing word '{word}': {str(e)}")
        try:
            update.message.reply_text(
                get_message('error_occurred', lang),
                reply_markup=get_main_keyboard(lang)
            )
        except Exception as e2:
            logger.error(f"Failed to send error message: {str(e2)}")

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

def button_handler(update: Update, context: CallbackContext) -> int:
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
    elif query.data == CALLBACK_DATA['SAVE_WORD']:
        context.user_data['mode'] = 'save'
        query.edit_message_text(
            get_message('provide_word', lang).format('save'),
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
    elif query.data == CALLBACK_DATA['DOWNLOAD_SAVED']:
        # For download, we need to send a new message instead of editing
        temp_file = f'data/temp/saved_words_{user_id}.json'
        
        try:
            if not os.path.exists(temp_file):
                query.message.reply_text(
                    get_message('saved_words_empty', lang),
                    reply_markup=get_main_keyboard(lang),
                    parse_mode=ParseMode.MARKDOWN
                )
                return ConversationHandler.END
                
            with open(temp_file, 'r', encoding='utf-8') as f:
                try:
                    saved_words = json.load(f)
                    if not isinstance(saved_words, list):
                        saved_words = []
                except json.JSONDecodeError:
                    saved_words = []
                
            if not saved_words:
                query.message.reply_text(
                    get_message('saved_words_empty', lang),
                    reply_markup=get_main_keyboard(lang),
                    parse_mode=ParseMode.MARKDOWN
                )
                return ConversationHandler.END
                
            # Send the file as a new message
            with open(temp_file, 'rb') as f:
                query.message.reply_document(
                    document=f,
                    filename=f'saved_words.json',
                    caption=get_message('download_ready', lang)
                )
                
        except Exception as e:
            logger.error(f"Error downloading saved words: {e}")
            query.message.reply_text(
                f"❌ Error downloading your saved words. Please try again later.\nError details: {str(e)}",
                reply_markup=get_main_keyboard(lang),
                parse_mode=ParseMode.MARKDOWN
            )
    elif query.data == CALLBACK_DATA['SYNONYMS']:
        context.user_data['mode'] = 'synonym'
        query.edit_message_text(
            get_message('provide_word', lang).format('synonym'),
            reply_markup=get_back_keyboard(lang),
            parse_mode=ParseMode.MARKDOWN
        )
        return AWAITING_WORD
    elif query.data == CALLBACK_DATA['ANTONYMS']:
        context.user_data['mode'] = 'antonym'
        query.edit_message_text(
            get_message('provide_word', lang).format('antonym'),
            reply_markup=get_back_keyboard(lang),
            parse_mode=ParseMode.MARKDOWN
        )
        return AWAITING_WORD
    elif query.data == CALLBACK_DATA['BOTH']:
        context.user_data['mode'] = 'both'
        query.edit_message_text(
            get_message('provide_word', lang).format('both'),
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

def text_handler(update: Update, context: CallbackContext) -> int:
    """Handle regular text messages."""
    text = update.message.text.strip()
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    
    logger.info(f"Received text: {text}")
    
    # Handle word input
    if len(text.split()) > 1:
        update.message.reply_text(
            get_message('one_word_only', lang),
            reply_markup=get_main_keyboard(lang),
            parse_mode=ParseMode.MARKDOWN
        )
        return ConversationHandler.END
    
    # Set the word as an argument for the command handlers
    context.args = [text.lower()]  # Ensure word is lowercase
    
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

def save_word_command(update: Update, context: CallbackContext) -> None:
    """Save a word to the temporary file."""
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    
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
        # Create data directory if it doesn't exist
        os.makedirs('data/temp', exist_ok=True)
        
        # Create a temporary file for this user
        temp_file = f'data/temp/saved_words_{user_id}.json'
        
        # Read existing words or create new list
        try:
            if os.path.exists(temp_file):
                with open(temp_file, 'r', encoding='utf-8') as f:
                    saved_words = json.load(f)
                    if not isinstance(saved_words, list):
                        saved_words = []
            else:
                saved_words = []
        except json.JSONDecodeError:
            saved_words = []
            
        # Check if word already exists
        if any(item.get('word') == word for item in saved_words):
            update.message.reply_text(
                get_message('word_exists', lang).format(word),
                reply_markup=get_main_keyboard(lang),
                parse_mode=ParseMode.MARKDOWN
            )
            return
            
        # Check if maximum limit reached
        if len(saved_words) >= MAX_SAVED_WORDS:
            update.message.reply_text(
                get_message('max_words_reached', lang).format(MAX_SAVED_WORDS),
                reply_markup=get_main_keyboard(lang),
                parse_mode=ParseMode.MARKDOWN
            )
            return
            
        # Extract synonyms and antonyms from all parts of speech
        all_synonyms = []
        all_antonyms = []
        
        # Iterate through each part of speech
        for pos_data in info.values():
            # Add synonyms
            for syn in pos_data.get('synonyms', []):
                if isinstance(syn, dict) and 'word' in syn:
                    all_synonyms.append(syn['word'])
                elif isinstance(syn, str):
                    all_synonyms.append(syn)
            
            # Add antonyms
            for ant in pos_data.get('antonyms', []):
                if isinstance(ant, dict) and 'word' in ant:
                    all_antonyms.append(ant['word'])
                elif isinstance(ant, str):
                    all_antonyms.append(ant)
        
        # Add the new word with unique synonyms and antonyms
        saved_words.append({
            'word': word,
            'synonyms': list(dict.fromkeys(all_synonyms)),
            'antonyms': list(dict.fromkeys(all_antonyms))
        })
        
        # Save the updated list
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(saved_words, f, indent=2, ensure_ascii=False)
        
        update.message.reply_text(
            get_message('word_saved', lang).format(word),
            reply_markup=get_main_keyboard(lang),
            parse_mode=ParseMode.MARKDOWN
        )
            
    except Exception as e:
        logger.error(f"Error saving word: {e}")
        error_msg = (
            "❌ Error saving the word. Please try again later.\n"
            f"Error details: {str(e)}"
        )
        update.message.reply_text(
            error_msg,
            reply_markup=get_main_keyboard(lang),
            parse_mode=ParseMode.MARKDOWN
        )

def show_saved_command(update: Update, context: CallbackContext) -> None:
    """Show user's saved words and offer to download them."""
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    temp_file = f'data/temp/saved_words_{user_id}.json'
    
    try:
        if not os.path.exists(temp_file):
            update.message.reply_text(
                get_message('saved_words_empty', lang),
                reply_markup=get_main_keyboard(lang),
                parse_mode=ParseMode.MARKDOWN
            )
            return
            
        with open(temp_file, 'r', encoding='utf-8') as f:
            try:
                saved_words = json.load(f)
                if not isinstance(saved_words, list):
                    saved_words = []
            except json.JSONDecodeError:
                saved_words = []
            
        if not saved_words:
            update.message.reply_text(
                get_message('saved_words_empty', lang),
                reply_markup=get_main_keyboard(lang),
                parse_mode=ParseMode.MARKDOWN
            )
            return
            
        # First send the list as a message
        response = ["📚 *Your saved words:*\n"]
        for item in saved_words:
            word = item['word']
            syn_count = len(item.get('synonyms', []))
            ant_count = len(item.get('antonyms', []))
            response.append(f"• *{word}* - {syn_count} synonyms, {ant_count} antonyms")
        
        update.message.reply_text(
            '\n'.join(response),
            reply_markup=get_main_keyboard(lang),
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Then send the file
        with open(temp_file, 'rb') as f:
            update.message.reply_document(
                document=f,
                filename=f'saved_words.json',
                caption="📥 Here's your saved words file. You can save it anywhere on your computer!"
            )
            
    except Exception as e:
        logger.error(f"Error reading saved words: {e}")
        error_msg = (
            "❌ Error reading your saved words. Please try again later.\n"
            f"Error details: {str(e)}"
        )
        update.message.reply_text(
            error_msg,
            reply_markup=get_main_keyboard(lang),
            parse_mode=ParseMode.MARKDOWN
        )