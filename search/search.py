import json
from pathlib import Path
from typing import Literal, Any

from search.interfaces import ChapterDictIncludePath, VerseDict, TranslationDict


class Search:
    FILE_VERSES = "verses.json"
    FILE_TRANSLATION = "translation.json"

    def __init__(self) -> None:
        self.index_json_path = Path(__file__).parent.parent / "index.json"
        self.index_json: list[ChapterDictIncludePath] = self._read_index()

    def _read_index(self) -> list[ChapterDictIncludePath]:
        with open(self.index_json_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def find_complete_surah_info(
        self, key: Literal["id", "name_simple", "name_fr"], value: Any
    ) -> ChapterDictIncludePath | None:
        """Recherche un chapitre dans l’index"""
        for chapter in self.index_json:
            if key == "id" and chapter["id"] == value:
                return chapter
            if (
                key == "name_simple"
                and chapter["name_simple"].lower() == str(value).lower()
            ):
                return chapter
            if (
                key == "name_fr"
                and chapter["translated_name"]["name"].lower() == str(value).lower()
            ):
                return chapter
        return None

    def read_file(
        self, info: ChapterDictIncludePath, t: Literal["verses", "translation"]
    ) -> list[VerseDict] | list[TranslationDict]:
        """Lit le fichier JSON (verses ou translation) d’une sourate"""
        if t == "verses":
            path = Path(info["path"]) / Search.FILE_VERSES
        else:
            path = Path(info["path"]) / Search.FILE_TRANSLATION
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def resources(self, ptype: Literal["array", "column"] = "column") ->  list[ChapterDictIncludePath]:
        if ptype == "column":
            for chapter in self.index_json:
                print(
                    f"{chapter['id']:>3} - {chapter['name_simple']:<20} - {chapter['translated_name']['name']}"
                )

        elif ptype == "array":
            i = 0
            while i < len(self.index_json):
                chapter = self.index_json[i]
                if i + 1 < len(self.index_json):
                    next_chapter = self.index_json[i + 1]
                    print(
                        f"{chapter['id']:>3} - {chapter['name_simple']:<20} - {chapter['translated_name']['name']:<25}"
                        f" | "
                        f"{next_chapter['id']:>3} - {next_chapter['name_simple']:<20} - {next_chapter['translated_name']['name']:<25}"
                    )
                else:
                    print(
                        f"{chapter['id']:>3} - {chapter['name_simple']:<20} - {chapter['translated_name']['name']}"
                    )
                i += 2
        return self.index_json
    def get_verses(
        self,
        id_surah: int,
        start_v: int,
        end_v: int | None = None,
        t: Literal["verses", "translation"] = "verses",
    ):
        """
        Récupère un ou plusieurs versets.
        Toujours renvoie une liste.
        """
        info = self.find_complete_surah_info("id", id_surah)
        if not info:
            raise ValueError(f"Sourate {id_surah} introuvable")

        data = self.read_file(info, t)

        if end_v is None:
            verse = next((v for v in data if v["verse_number"] == start_v), None)
            return [verse] if verse else []

        return [v for v in data if start_v <= v["verse_number"] <= end_v]

        def resources(self, ptype: Literal["array", "column"] = "column") -> None:
            if ptype == "column":
                for chapter in self.index_json:
                    print(
                        f"{chapter['id']:>3} - {chapter['name_simple']:<20} - {chapter['translated_name']['name']}"
                    )

            elif ptype == "array":
                i = 0
                while i < len(self.index_json):
                    chapter = self.index_json[i]
                    if i + 1 < len(self.index_json):
                        next_chapter = self.index_json[i + 1]
                        print(
                            f"{chapter['id']:>3} - {chapter['name_simple']:<20} - {chapter['translated_name']['name']:<25}"
                            f" | "
                            f"{next_chapter['id']:>3} - {next_chapter['name_simple']:<20} - {next_chapter['translated_name']['name']:<25}"
                        )
                    else:
                        print(
                            f"{chapter['id']:>3} - {chapter['name_simple']:<20} - {chapter['translated_name']['name']}"
                        )
                    i += 2
