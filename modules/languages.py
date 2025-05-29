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
            "• /saved - Просмотреть сохранённые слова\n"
            "• /help - Показать это сообщение"
        ),
        'help': (
            "*🤖 Команды бота:*\n\n"
            "• /synonym <слово> - Найти синонимы\n"
            "• /antonym <слово> - Найти антонимы\n"
            "• /both <слово> - Показать всё\n"
            "• /saved - История поиска\n"
            "• /help - Помощь\n\n"
            "Пример: Попробуйте '/both happy'\n\n"
            "Для каждого слова вы получите:\n"
            "• Тип слова (существительное, глагол и т.д.)\n"
            "• Синонимы/антонимы\n"
            "• Примеры использования"
        ),
        'provide_word': "Пожалуйста, укажите слово после команды. Пример: /{} happy",
        'synonyms_title': "*📚 Синонимы для {}:*\n",
        'antonyms_title': "*⚡️ Антонимы для {}:*\n",
        'no_results': "Извините, не удалось найти информацию для слова '{}'",
        'no_synonyms': "Синонимы не найдены",
        'no_antonyms': "Антонимы не найдены",
        'saved_words_empty': "Вы ещё не искали слова!",
        'saved_words_title': "*📝 Ваши недавние поиски:*",
        'word_stats': "• {} ({} синонимов, {} антонимов)",
        'current_language': "Текущий язык",
        'language_changed': "✅ Язык интерфейса изменён на русский",
        'choose_action': "Выберите действие:",
        'find_synonyms': "🔍 Найти синонимы",
        'find_antonyms': "🔄 Найти антонимы",
        'find_both': "📚 Синонимы и антонимы",
        'view_saved': "📋 История поиска",
        'switch_language': "🌐 Switch to English",
        'enter_word': "Введите слово для поиска:",
        'back': "Назад",
        'one_word_only': "Пожалуйста, отправьте только одно слово",
        'example_title': "\n_Пример использования:_",
        'no_examples': "Примеры не найдены"
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
            "• /saved - View your saved words\n"
            "• /help - Show this help message"
        ),
        'help': (
            "*🤖 Bot Commands:*\n\n"
            "• /synonym <word> - Find synonyms\n"
            "• /antonym <word> - Find antonyms\n"
            "• /both <word> - Show both\n"
            "• /saved - View history\n"
            "• /help - Show help\n\n"
            "Example: Try '/both happy'\n\n"
            "For each word you'll get:\n"
            "• Word type (noun, verb, etc.)\n"
            "• Synonyms/antonyms\n"
            "• Usage examples"
        ),
        'provide_word': "Please provide a word after the command. Example: /{} happy",
        'synonyms_title': "*📚 Synonyms for {}:*\n",
        'antonyms_title': "*⚡️ Antonyms for {}:*\n",
        'no_results': "Sorry, couldn't find any information for '{}'",
        'no_synonyms': "No synonyms found",
        'no_antonyms': "No antonyms found",
        'saved_words_empty': "You haven't looked up any words yet!",
        'saved_words_title': "*📝 Your recently looked up words:*",
        'word_stats': "• {} ({} synonyms, {} antonyms)",
        'current_language': "Current language",
        'language_changed': "✅ Interface language changed to English",
        'choose_action': "Choose an action:",
        'find_synonyms': "🔍 Find Synonyms",
        'find_antonyms': "🔄 Find Antonyms",
        'find_both': "📚 Synonyms & Antonyms",
        'view_saved': "📋 View History",
        'switch_language': "🌐 Сменить на русский",
        'enter_word': "Enter a word to search:",
        'back': "Back",
        'one_word_only': "Please send only one word",
        'example_title': "\n_Example usage:_",
        'no_examples': "No examples found"
    }
}

def get_message(key: str, lang: str = 'ru') -> str:
    """Get a message in the specified language."""
    return MESSAGES.get(lang, MESSAGES['en']).get(key, MESSAGES['en'][key]) 