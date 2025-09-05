from typing import Any
from src.api import call_quran_api
from src.interfaces import TajweedDict


class Tajweed:
    def __init__(self) -> None:
        pass

    def get(self, id_chapter: int) -> list[TajweedDict]:
        data = call_quran_api(
            f"/quran/verses/uthmani_tajweed?chapter_number={id_chapter}"
        )
        verses = data.get("verses", [])
        print(f"TAJWEED -> Terminé ({len(verses)} versets récupérés pour chapitre {id_chapter})")
        return verses
