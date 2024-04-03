import telebot
import os
from database_manager import DatabaseManager
from json_formatter import JSONFormatter


class TelegramManager:
    def __init__(self, episodes_path, chapters_path, OVAs_path, films_path):
        self.bot = telebot.TeleBot('TOKEN', parse_mode=None)
        self.episodes_path = episodes_path
        self.chapters_path = chapters_path
        self.OVAs_path = OVAs_path
        self.films_path = films_path

    def send_welcome(self, message):
        chat_id = message.chat.id
        self.bot.send_message(chat_id, "Коноха Компаньон - Бот для удобного просмотра информации о Наруто\n"
                                       "Для получения полного списка доступных команд введите /help")

    def send_help(self, message):
        chat_id = message.chat.id
        help_message = ("Доступные команды:\n"
                        "/c {номер главы} - Отправляет главу по номеру\n"
                        "/e {номер эпизода} - Отправляет эпизод по номеру\n"
                        "/f {номер фильма} - Отправляет фильм по номеру\n"
                        "/OVA {номер OVA} - Отправляет OVA по номеру\n"
                        "/character {имя персонажа} - Отправляет информацию о персонаже")
        self.bot.send_message(chat_id, help_message)

    def send_document_or_message(self, message, file_path, not_found_message):
        chat_id = message.chat.id
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                self.bot.send_document(chat_id, file)
        else:
            self.bot.send_message(chat_id, not_found_message)

    def send_chapter(self, message, chapter_number):
        chapter_filename = f"{chapter_number}.pdf"
        chapter_file_path = os.path.join(self.chapters_path, chapter_filename)
        self.send_document_or_message(message, chapter_file_path, f"Глава {chapter_number} не найдена.")

    def send_episode(self, message, episode_number):
        episode_filename = f"{episode_number}.mkv"
        episode_file_path = os.path.join(self.episodes_path, episode_filename)
        self.send_document_or_message(message, episode_file_path, f"Эпизод {episode_number} не найден.")

    def send_OVA(self, message, OVA_number):
        OVA_filename = f"{OVA_number}.mkv"
        OVA_file_path = os.path.join(self.OVAs_path, OVA_filename)
        self.send_document_or_message(message, OVA_file_path, f"OVA {OVA_number} не найдено.")

    def send_film(self, message, film_number):
        film_filename = f"{film_number}.mkv"
        film_file_path = os.path.join(self.films_path, film_filename)
        self.send_document_or_message(message, film_file_path, f"Фильм {film_number} не найден.")

    def send_character_info(self, message, name):
        chat_id = message.chat.id
        DB = DatabaseManager('https://narutodb.xyz/api/character/search')
        data = DB.get_character_info_by_name(name)
        if data:
            formatted_info = JSONFormatter().get_character_personal(data)
            self.bot.send_message(chat_id, formatted_info)
        else:
            self.bot.send_message(chat_id, f"Персонаж {name} не найден.")

    def start_bot(self):
        @self.bot.message_handler(commands=['start'])
        def handle_start(message):
            self.send_welcome(message)

        @self.bot.message_handler(commands=['help'])
        def handle_help(message):
            self.send_help(message)

        @self.bot.message_handler(commands=['c'])
        def handle_chapter(message):
            try:
                chapter_number = message.text.split()[1]
                self.send_chapter(message, chapter_number)
            except IndexError:
                self.bot.reply_to(message, "Пожалуйста, укажите номер главы.")

        @self.bot.message_handler(commands=['e'])
        def handle_episode(message):
            try:
                episode_number = message.text.split()[1]
                self.send_episode(message, episode_number)
            except IndexError:
                self.bot.reply_to(message, "Пожалуйста, укажите номер эпизода.")

        @self.bot.message_handler(commands=['OVA'])
        def handle_OVA(message):
            try:
                OVA_number = message.text.split()[1]
                self.send_OVA(message, OVA_number)
            except IndexError:
                self.bot.reply_to(message, "Пожалуйста, укажите номер OVA.")

        @self.bot.message_handler(commands=['f'])
        def handle_film(message):
            try:
                film_number = message.text.split()[1]
                self.send_film(message, film_number)
            except IndexError:
                self.bot.reply_to(message, "Пожалуйста, укажите номер фильма.")

        @self.bot.message_handler(commands=['character'])
        def handle_character(message):
            try:
                name = ' '.join(message.text.split()[1:])
                self.send_character_info(message, name)
            except IndexError:
                self.bot.reply_to(message, "Пожалуйста, введите имя персонажа.")

        self.bot.polling()
