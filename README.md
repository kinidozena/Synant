# Synant - Telegram Synonym/Antonym Bot
# Synant - Телеграм-бот для поиска синонимов и антонимов

[English](#english) | [Русский](#russian)

---

<a name="english"></a>
## English

### Description
Synant is a Telegram bot that helps users find synonyms and antonyms for English words. The bot provides an intuitive interface with both English and Russian language support for the user interface, while working with English vocabulary.

### Features
- Search for synonyms and antonyms
- Save favorite words
- Switch between English and Russian interface
- View history of saved words
- Get both synonyms and antonyms at once

### Requirements
- Python 3.7+
- Telegram Bot Token (obtained from [@BotFather](https://t.me/BotFather))
- PythonAnywhere account (for hosting) or your own server

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/synant.git
cd synant
```

2. Create and activate virtual environment:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your Telegram Bot Token:
```
BOT_TOKEN=your_bot_token_here
```

5. Configure the webhook URL in `main.py`:
```python
webhook_url = 'https://YOUR_USERNAME.pythonanywhere.com/webhook_path'
```

### Usage
1. Start the bot using:
```bash
python main.py
```

2. In Telegram, find your bot by username and start interaction with `/start` command
3. Send any English word to get its synonyms or antonyms
4. Use available commands:
   - `/synonym` - get synonyms
   - `/antonym` - get antonyms
   - `/both` - get both synonyms and antonyms
   - `/save` - save a word
   - `/saved` - view saved words
   - `/help` - get help

---

<a name="russian"></a>
## Русский

### Описание
Synant - это Telegram-бот, помогающий пользователям находить синонимы и антонимы английских слов. Бот предоставляет интуитивно понятный интерфейс с поддержкой английского и русского языков интерфейса, при работе с английской лексикой.

### Возможности
- Поиск синонимов и антонимов
- Сохранение избранных слов
- Переключение между английским и русским интерфейсом
- Просмотр истории сохраненных слов
- Получение синонимов и антонимов одновременно

### Требования
- Python 3.7+
- Токен Telegram бота (получается у [@BotFather](https://t.me/BotFather))
- Аккаунт PythonAnywhere (для хостинга) или собственный сервер

### Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/synant.git
cd synant
```

2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/MacOS
source venv/bin/activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` в корне проекта и добавьте токен вашего Telegram бота:
```
BOT_TOKEN=ваш_токен_бота
```

5. Настройте URL вебхука в `main.py`:
```python
webhook_url = 'https://ВАШ_ЛОГИН.pythonanywhere.com/webhook_path'
```

### Использование
1. Запустите бота командой:
```bash
python main.py
```

2. В Telegram найдите вашего бота по имени и начните взаимодействие командой `/start`
3. Отправьте любое английское слово, чтобы получить его синонимы или антонимы
4. Используйте доступные команды:
   - `/synonym` - получить синонимы
   - `/antonym` - получить антонимы
   - `/both` - получить синонимы и антонимы
   - `/save` - сохранить слово
   - `/saved` - просмотреть сохраненные слова
   - `/help` - получить помощь 