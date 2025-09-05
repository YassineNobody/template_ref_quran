import time
from urllib.parse import urlencode

from src.api import call_quran_api
from src.interfaces import VerseDict


class Verses:
    def __init__(self, max_req_per_minute: int = 10) -> None:
        self.max_req_per_minute = max_req_per_minute
        # calcul du délai minimum entre deux requêtes
        self.delay = 60 / max_req_per_minute
        self.url_verses_audio = "https://verses.quran.com/"

    def get_verses(
        self,
        id_chapter: int,
        language: str = "fr",
        words: bool = True,
        id_reciter: int = 3,
        translations: str = "fr",
        word_fields: str = "text_uthmani",
        fields: str = "text_uthmani",
    ) -> list[VerseDict]:
        page = 1
        verses = []
        url_base = f"/verses/by_chapter/{id_chapter}"

        # première requête pour initialiser
        query = {
            "language": language,
            "words": str(words).lower(),  # True -> "true"
            "translations": translations,
            "word_fields": word_fields,
            "fields": fields,
            "audio": id_reciter,
            "page": page,
            "per_page": 50,
        }
        url = f"{url_base}?{urlencode(query)}"
        data = call_quran_api(url)
        verses.extend(data["verses"])
        total_pages = data["pagination"]["total_pages"]
        print(f"⏳ VERSES ->  {total_pages} pages à récupérer pour chapitre {id_chapter}")

        # boucle sur les pages suivantes
        while data["pagination"]["next_page"]:
            page += 1
            print(f"→ Récupération page {page}/{total_pages}...")
            time.sleep(self.delay)  # pause pour limiter les requêtes
            query["page"] = page
            url = f"{url_base}?{urlencode(query)}"
            data = call_quran_api(url)
            verses.extend(data["verses"])

        print(f"✔ Terminé ({len(verses)} versets récupérés)")
        return verses
