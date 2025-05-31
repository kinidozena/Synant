"""
Language support for the Telegram Synonym/Antonym Bot
"""
from typing import Dict, Any

MESSAGES = {
    'ru': {
        'welcome': (
            "*👋 Добро пожаловать в бот синонимов и антонимов!*\n\n"
            "Я помогу вам найти синонимы и антонимы для английских слов. "
            "Для каждого слова я покажу его тип (существительное, глагол и т.д.) "
            "и примеры использования.\n\n"
            "📚 *Доступные команды:*\n"
            "• /synonym <слово> - Найти синонимы\n"
            "• /antonym <слово> - Найти антонимы\n"
            "• /both <слово> - Показать синонимы и антонимы\n"
            "• /setup_path <путь> - Указать путь для сохранения\n"
            "• /save <слово> - Сохранить слово\n"
            "• /saved - Показать сохранённые слова\n"
            "• /help - Показать это сообщение\n\n"
            "*💾 Сохранение слов:*\n"
            "1. Сначала укажите путь командой /setup_path\n"
            "2. Этот путь сохранится даже после перезапуска бота"
        ),
        'help': (
            "*🤖 Команды бота:*\n\n"
            "• /synonym <слово> - Найти синонимы\n"
            "• /antonym <слово> - Найти антонимы\n"
            "• /both <слово> - Показать всё\n"
            "• /setup_path <путь> - Настроить сохранение\n"
            "• /save <слово> - Сохранить слово\n"
            "• /saved - Сохранённые слова\n"
            "• /help - Помощь\n\n"
            "Пример: Попробуйте '/both happy'\n\n"
            "Для каждого слова вы получите:\n"
            "• Тип слова (существительное, глагол и т.д.)\n"
            "• Синонимы/антонимы\n"
            "• Примеры использования\n\n"
            "*💾 Сохранение слов:*\n"
            "1. Используйте /setup_path чтобы указать путь для сохранения\n"
            "   Пример: `/setup_path C:/Users/ИмяПользователя/Documents/saved_words.json`\n"
            "2. Этот путь сохранится даже после перезапуска бота\n"
            "3. После этого используйте /save для сохранения слов\n"
            "4. Просматривайте сохранённые слова через /saved"
        ),
        'provide_word': "Пожалуйста, укажите слово после команды. Пример: /{} happy",
        'synonyms_title': "*📚 Синонимы для {}:*\n",
        'antonyms_title': "*⚡️ Антонимы для {}:*\n",
        'no_results': "Извините, не удалось найти информацию для слова '{}'",
        'no_synonyms': "Синонимы не найдены",
        'no_antonyms': "Антонимы не найдены",
        'saved_words_empty': "У вас пока нет сохранённых слов!",
        'saved_words_title': "*📝 Ваши сохранённые слова:*",
        'word_stats': "• {} ({} синонимов, {} антонимов)",
        'current_language': "Текущий язык",
        'language_changed': "✅ Язык интерфейса изменён на русский",
        'choose_action': "Выберите действие:",
        'find_synonyms': "🔍 Найти синонимы",
        'find_antonyms': "🔄 Найти антонимы",
        'find_both': "📚 Синонимы и антонимы",
        'setup_path': "⚙️ Настроить путь",
        'save_word': "💾 Сохранить слово",
        'view_saved': "📋 Сохранённые слова",
        'switch_language': "🌐 Switch to English",
        'enter_word': "Введите слово для поиска:",
        'enter_word_save': "Введите слово для сохранения:",
        'enter_save_path': "Введите путь для сохранения слов:",
        'back': "Назад",
        'one_word_only': "Пожалуйста, отправьте только одно слово",
        'example_title': "\n_Пример использования:_",
        'no_examples': "Примеры не найдены",
        'setup_path_first': (
            "⚠️ Сначала нужно настроить путь для сохранения!\n\n"
            "Используйте команду /setup_path и укажите путь, куда сохранять слова.\n"
            "Пример: `/setup_path C:/Users/ИмяПользователя/Documents/saved_words.json`"
        )
    },
    'en': {
        'welcome': (
            "*👋 Welcome to the Synonym/Antonym Bot!*\n\n"
            "I can help you find synonyms and antonyms for words. "
            "For each word, I'll show its type (noun, verb, etc.) "
            "and usage examples.\n\n"
            "📚 *Available Commands:*\n"
            "• /synonym <word> - Find synonyms\n"
            "• /antonym <word> - Find antonyms\n"
            "• /both <word> - Show both synonyms and antonyms\n"
            "• /setup_path <path> - Set save location\n"
            "• /save <word> - Save a word\n"
            "• /saved - View saved words\n"
            "• /help - Show this help message\n\n"
            "*💾 Saving Words:*\n"
            "1. First set your save path with /setup_path\n"
            "2. This path will be remembered even after bot restarts"
        ),
        'help': (
            "*🤖 Bot Commands:*\n\n"
            "• /synonym <word> - Find synonyms\n"
            "• /antonym <word> - Find antonyms\n"
            "• /both <word> - Show both\n"
            "• /setup_path <path> - Setup saving\n"
            "• /save <word> - Save word\n"
            "• /saved - View saved\n"
            "• /help - Show help\n\n"
            "Example: Try '/both happy'\n\n"
            "For each word you'll get:\n"
            "• Word type (noun, verb, etc.)\n"
            "• Synonyms/antonyms\n"
            "• Usage examples\n\n"
            "*💾 Saving Words:*\n"
            "1. Use /setup_path to set your save location\n"
            "   Example: `/setup_path C:/Users/YourName/Documents/saved_words.json`\n"
            "2. This path will be remembered even after bot restarts\n"
            "3. Then use /save to save words\n"
            "4. View your saved words with /saved"
        ),
        'provide_word': "Please provide a word after the command. Example: /{} happy",
        'synonyms_title': "*📚 Synonyms for {}:*\n",
        'antonyms_title': "*⚡️ Antonyms for {}:*\n",
        'no_results': "Sorry, couldn't find any information for '{}'",
        'no_synonyms': "No synonyms found",
        'no_antonyms': "No antonyms found",
        'saved_words_empty': "You don't have any saved words yet!",
        'saved_words_title': "*📝 Your saved words:*",
        'word_stats': "• {} ({} synonyms, {} antonyms)",
        'current_language': "Current language",
        'language_changed': "✅ Interface language changed to English",
        'choose_action': "Choose an action:",
        'find_synonyms': "🔍 Find Synonyms",
        'find_antonyms': "🔄 Find Antonyms",
        'find_both': "📚 Synonyms & Antonyms",
        'setup_path': "⚙️ Setup Path",
        'save_word': "💾 Save Word",
        'view_saved': "📋 Saved Words",
        'switch_language': "🌐 Сменить на русский",
        'enter_word': "Enter a word to search:",
        'enter_word_save': "Enter a word to save:",
        'enter_save_path': "Enter the path to save words:",
        'back': "Back",
        'one_word_only': "Please send only one word",
        'example_title': "\n_Example usage:_",
        'no_examples': "No examples found",
        'setup_path_first': (
            "⚠️ You need to set up a save location first!\n\n"
            "Use the /setup_path command followed by where you want to save words.\n"
            "Example: `/setup_path C:/Users/YourName/Documents/saved_words.json`"
        )
    }
}

def get_message(key: str, lang: str = 'ru') -> str:
    """Get a message in the specified language."""
    return MESSAGES.get(lang, MESSAGES['en']).get(key, MESSAGES['en'][key]) 