import time
from src.api import call_quran_api


class Quran:
    def __init__(self, translation_id: int = 31, max_req_per_minute: int = 30) -> None:
        # 149 = traduction en français (Muhammad Hamidullah)
        self.translation_id = translation_id
        self.max_req_per_minute = max_req_per_minute
        # calcul du délai minimum entre deux requêtes
        self.delay = 60 / max_req_per_minute


    def get(self, chapter_number: int):
        """
        Récupère tous les versets d'une sourate avec traduction FR.
        """
        page=1
        data=[]
        endpoint = f"/verses/by_chapter/{chapter_number}?translations={self.translation_id}&page={page}&per_page=50"
        resp = call_quran_api(endpoint)
        data.extend(resp["verses"])
        total_pages = resp["pagination"]["total_pages"]
        print(f"⏳ VERSES ->  {total_pages} pages à récupérer pour chapitre {chapter_number}")

        while resp["pagination"]["next_page"]:
            page+= 1
            print(f"→ Récupération page {page}/{total_pages}...")
            time.sleep(self.delay)
            endpoint = f"/verses/by_chapter/{chapter_number}?translations={self.translation_id}&page={page}&per_page=50"
            resp = call_quran_api(endpoint)      
            data.extend(resp["verses"])
        print(f"✔ Terminé ({len(data)} versets récupérés)")
        return data

