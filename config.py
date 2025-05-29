import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration settings
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Default language (WordNet is English-only, but interface can be in Russian)
DEFAULT_LANGUAGE = "ru"  # Changed to Russian as default

# Response settings
MAX_SYNONYMS_DISPLAY = 10  # Maximum number of synonyms to show at once
MAX_SAVED_WORDS = 10      # Maximum number of words to save in history

# Data storage
USER_DATA_PATH = "data/user_data.json"

# Keyboard callback data
CALLBACK_DATA = {
    'SYNONYMS': 'get_synonyms',
    'ANTONYMS': 'get_antonyms',
    'BOTH': 'get_both',
    'SAVED': 'view_saved',
    'SWITCH_LANG': 'switch_language',
    'BACK': 'back_to_menu'
}

# Supported languages
SUPPORTED_LANGUAGES = ['en', 'ru']
