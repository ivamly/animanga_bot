from telegram_manager import TelegramManager

episodes_path = "episodes"
chapters_path = "chapters"
OVAs_path = "OVAs"
films_path = "films"


def main():
    bot = TelegramManager(episodes_path, chapters_path, OVAs_path, films_path)
    bot.start_bot()


if __name__ == "__main__":
    main()
