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
MAX_SAVED_WORDS = 50      # Maximum number of words to save in file

# Data storage
USER_DATA_PATH = "data/user_data.json"
SAVE_PATHS_FILE = "data/save_paths.json"  # File to store user save paths

# Keyboard callback data
CALLBACK_DATA = {
    'SYNONYMS': 'get_synonyms',
    'ANTONYMS': 'get_antonyms',
    'BOTH': 'get_both',
    'SAVE_WORD': 'save_word',
    'VIEW_SAVED': 'view_saved',
    'DOWNLOAD_SAVED': 'download_saved',  # New callback for downloading saved words
    'SWITCH_LANG': 'switch_language',
    'BACK': 'back_to_menu'
}

# Supported languages
SUPPORTED_LANGUAGES = ['en', 'ru']
