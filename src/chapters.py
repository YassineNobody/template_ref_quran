from tkinter import N
from src.interfaces import ChapterDict, ChaptersProps
from src.utils import file_exists, writeJSON, readJSON
from src.api import call_quran_api


class Chapters:
    def __init__(self) -> None:
        self._chapters: ChaptersProps = self._get_chapters()

    def _get_chapters(self) -> ChaptersProps:
        if file_exists("chapters.json"):
            chapters = readJSON("chapters.json")
            if chapters:
                return chapters
            else:
                raise Exception(
                    "Une erreur est survenue lors de la lecture du fichier chapters.json"
                )
        else:
            chapters = call_quran_api("/chapters?language=fr")
            writeJSON("chapters.json", chapters)
            return chapters

    def get_chapter_infos(self, id: int) -> dict:
        return call_quran_api(f"/chapters/{id}/info?language=fr")

    @property
    def chapters(self) -> ChaptersProps:
        return self._chapters

    def find(
        self,
        name: str | None = None,
        id: int | None = None,
        name_translation: str | None = None,
    ) -> ChapterDict | None:
        chapters = self.chapters["chapters"]
        for chapter in chapters:
            if name and chapter["name_simple"].lower() == name.lower():
                return chapter
            elif id and chapter["id"] == id:
                return chapter
            elif (
                name_translation
                and chapter["translated_name"]["name"].lower()
                == name_translation.lower()
            ):
                return chapter
        return None
