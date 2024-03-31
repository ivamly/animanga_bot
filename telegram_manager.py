import telebot
import os


class TelegramManager:
    def __init__(self, episodes_path, chapters_path, OVAs_path, films_path):
        self.bot = telebot.TeleBot('TOKEN', parse_mode=None)
        self.episodes_path = episodes_path
        self.chapters_path = chapters_path
        self.OVAs_path = OVAs_path
        self.films_path = films_path

    def send_welcome(self, message):
        chat_id = message.chat.id
        self.bot.send_message(chat_id, "Welcome to the bot! How can I assist you?")

    def send_help(self, message):
        chat_id = message.chat.id
        help_message = ("Available commands:\n"
                        "/help - Display available commands\n"
                        "/ch {chapter_number} - Choose chapter\n"
                        "/ep {episode_number} - Choose episode")
        self.bot.send_message(chat_id, help_message)

    def send_chapter(self, message, chapter_number):
        chat_id = message.chat.id
        chapter_filename = f"{chapter_number}.pdf"
        chapter_file_path = os.path.join(self.chapters_path, chapter_filename)

        if os.path.isfile(chapter_file_path):
            with open(chapter_file_path, 'rb') as file:
                self.bot.send_document(chat_id, file)
        else:
            self.bot.send_message(chat_id, f"Chapter {chapter_number} not found.")

    def send_episode(self, message, episode_number):
        chat_id = message.chat.id
        episode_filename = f"{episode_number}.mkv"
        episode_file_path = os.path.join(self.episodes_path, episode_filename)

        if os.path.isfile(episode_file_path):
            with open(episode_file_path, 'rb') as file:
                self.bot.send_document(chat_id, file)
        else:
            self.bot.send_message(chat_id, f"Episode {episode_number} not found.")

    def send_OVA(self, message, OVA_number):
        chat_id = message.chat.id
        OVA_filename = f"{OVA_number}.mkv"
        OVA_file_path = os.path.join(self.OVAs_path, OVA_filename)

        if os.path.isfile(OVA_file_path):
            with open(OVA_file_path, 'rb') as file:
                self.bot.send_document(chat_id, file)
        else:
            self.bot.send_message(chat_id, f"OVA {OVA_number} not found.")

    def send_film(self, message, film_number):
        chat_id = message.chat.id
        film_filename = f"{film_number}.mkv"
        film_file_path = os.path.join(self.films_path, film_filename)

        if os.path.isfile(film_file_path):
            with open(film_file_path, 'rb') as file:
                self.bot.send_document(chat_id, file)
        else:
            self.bot.send_message(chat_id, f"Film {film_number} not found.")

    def start_bot(self):
        @self.bot.message_handler(commands=['start'])
        def handle_start(message):
            self.send_welcome(message)

        @self.bot.message_handler(commands=['help'])
        def handle_help(message):
            self.send_help(message)

        @self.bot.message_handler(commands=['ch'])
        def handle_chapter(message):
            try:
                chapter_number = message.text.split()[1]
                self.send_chapter(message, chapter_number)
            except IndexError:
                self.bot.reply_to(message, "Please provide chapter number")

        @self.bot.message_handler(commands=['ep'])
        def handle_episode(message):
            try:
                episode_number = message.text.split()[1]
                self.send_episode(message, episode_number)
            except IndexError:
                self.bot.reply_to(message, "Please provide episode number")

        @self.bot.message_handler(commands=['OVA'])
        def handle_episode(message):
            try:
                OVA_number = message.text.split()[1]
                self.send_OVA(message, OVA_number)
            except IndexError:
                self.bot.reply_to(message, "Please provide OVA number")

        @self.bot.message_handler(commands=['film'])
        def handle_episode(message):
            try:
                film_number = message.text.split()[1]
                self.send_film(message, film_number)
            except IndexError:
                self.bot.reply_to(message, "Please provide film number")

        self.bot.polling()
