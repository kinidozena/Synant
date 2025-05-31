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
            "• /save <слово> - Сохранить слово\n"
            "• /saved - Показать сохранённые слова\n"
            "• /help - Показать это сообщение\n\n"
            "*💾 Сохранение слов:*\n"
            "1. Используйте /save для сохранения слова\n"
            "2. Бот отправит вам файл со всеми сохранёнными словами\n"
            "3. Сохраните файл в любом месте на вашем компьютере"
        ),
        'help': (
            "*🤖 Команды бота:*\n\n"
            "• /synonym <слово> - Найти синонимы\n"
            "• /antonym <слово> - Найти антонимы\n"
            "• /both <слово> - Показать всё\n"
            "• /save <слово> - Сохранить слово\n"
            "• /saved - Сохранённые слова\n"
            "• /help - Помощь\n\n"
            "Пример: Попробуйте '/both happy'\n\n"
            "Для каждого слова вы получите:\n"
            "• Тип слова (существительное, глагол и т.д.)\n"
            "• Синонимы/антонимы\n"
            "• Примеры использования\n\n"
            "*💾 Сохранение слов:*\n"
            "1. Используйте /save для сохранения слова\n"
            "2. Бот отправит вам файл JSON со всеми сохранёнными словами\n"
            "3. Сохраните файл в любом месте на вашем компьютере\n"
            "4. Просматривайте сохранённые слова через /saved"
        ),
        'synonyms_btn': "🔄 Синонимы",
        'antonyms_btn': "⚡️ Антонимы",
        'both_btn': "🔍 Оба варианта",
        'save_btn': "💾 Сохранить",
        'view_saved_btn': "📋 Просмотр",
        'download_saved_btn': "📥 Скачать",
        'switch_lang_btn': "🌐 EN/RU",
        'back_btn': "⬅️ Назад",
        'provide_word': "Введите слово для {}:",
        'word_not_found': "❌ Слово не найдено. Проверьте правильность написания.",
        'one_word_only': "❌ Пожалуйста, введите только одно слово.",
        'saved_words_empty': "📭 У вас пока нет сохранённых слов.",
        'saved_words_title': "📚 *Ваши сохранённые слова:*",
        'word_stats': "• *{}* - {} синонимов, {} антонимов",
        'word_saved': "✅ Слово '{}' сохранено!",
        'word_exists': "ℹ️ Слово '{}' уже в списке сохранённых.",
        'max_words_reached': "⚠️ Достигнут лимит в {} слов. Скачайте текущий список, чтобы начать новый.",
        'download_ready': "📥 Ваш файл с сохранёнными словами готов к скачиванию!"
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
            "• /save <word> - Save a word\n"
            "• /saved - View saved words\n"
            "• /help - Show this help message\n\n"
            "*💾 Saving Words:*\n"
            "1. Use /save to save a word\n"
            "2. Bot will send you a file with all saved words\n"
            "3. Save the file anywhere on your computer"
        ),
        'help': (
            "*🤖 Bot Commands:*\n\n"
            "• /synonym <word> - Find synonyms\n"
            "• /antonym <word> - Find antonyms\n"
            "• /both <word> - Show both\n"
            "• /save <word> - Save word\n"
            "• /saved - View saved\n"
            "• /help - Show help\n\n"
            "Example: Try '/both happy'\n\n"
            "For each word you'll get:\n"
            "• Word type (noun, verb, etc.)\n"
            "• Synonyms/antonyms\n"
            "• Usage examples\n\n"
            "*💾 Saving Words:*\n"
            "1. Use /save to save a word\n"
            "2. Bot will send you a JSON file with all saved words\n"
            "3. Save the file anywhere on your computer\n"
            "4. View your saved words with /saved"
        ),
        'synonyms_btn': "🔄 Synonyms",
        'antonyms_btn': "⚡️ Antonyms",
        'both_btn': "🔍 Both",
        'save_btn': "💾 Save",
        'view_saved_btn': "📋 View",
        'download_saved_btn': "📥 Download",
        'switch_lang_btn': "🌐 EN/RU",
        'back_btn': "⬅️ Back",
        'provide_word': "Enter a word to {}:",
        'word_not_found': "❌ Word not found. Please check the spelling.",
        'one_word_only': "❌ Please enter only one word.",
        'saved_words_empty': "📭 You don't have any saved words yet.",
        'saved_words_title': "📚 *Your saved words:*",
        'word_stats': "• *{}* - {} synonyms, {} antonyms",
        'word_saved': "✅ Word '{}' has been saved!",
        'word_exists': "ℹ️ Word '{}' is already in your saved list.",
        'max_words_reached': "⚠️ Maximum limit of {} words reached. Download current list to start a new one.",
        'download_ready': "📥 Your saved words file is ready for download!"
    }
}

def get_message(key: str, lang: str = 'ru') -> str:
    """Get a message in the specified language."""
    return MESSAGES.get(lang, MESSAGES['en']).get(key, MESSAGES['en'][key]) 