class JSONFormatter:
    @staticmethod
    def get_character_debut(data):
        debut_info = data.get("debut", {})
        manga_debut = debut_info.get("manga", "N/A")
        anime_debut = debut_info.get("anime", "N/A")
        return f"Дебют в манге: {manga_debut}\nДебют в аниме: {anime_debut}"

    @staticmethod
    def get_character_personal(data):
        personal_info = data.get("personal", {})
        return f"Информация о персонаже: {personal_info}\n"