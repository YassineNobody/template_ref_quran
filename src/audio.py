import time
from src.interfaces import AudioDataAyah, Reciters
from src.utils import writeJSON, readJSON, file_exists
from src.api import call_quran_api


class Audio:
    def __init__(self, max_req_per_minute: int = 10) -> None:
        self.max_req_per_minute = max_req_per_minute
        # calcul du délai minimum entre deux requêtes
        self.delay = 60 / max_req_per_minute
        self.url_verses_audio = "https://verses.quran.com/"

    def get_list_all_reciters(self) -> Reciters:
        if file_exists("reciters.json"):
            reciters = readJSON("reciters.json")
            if reciters:
                return reciters
            else:
                raise Exception("Erreur lors de la lecture de reciters.json")
        else:
            reciters = call_quran_api("/resources/recitations")
            writeJSON("reciters.json", reciters)
            return reciters

    def get_chapter(self, id_reciter: int, id_chapter: int) -> dict:
        return call_quran_api(f"/chapter_recitations/{id_reciter}/{id_chapter}")

    def get_ayah_audio(self, id_reciter: int, id_chapter: int) -> list[AudioDataAyah]:
        audios = []
        page = 1

        # première requête pour voir combien de pages au total
        data = call_quran_api(
            f"/recitations/{id_reciter}/by_chapter/{id_chapter}?per_page=50&page={page}"
        )
        audios.extend(data["audio_files"])
        total_pages = data["pagination"]["total_pages"]
        print(f"⏳ {total_pages} pages à récupérer pour chapitre {id_chapter}")

        # boucle sur les pages restantes
        while data["pagination"]["next_page"]:
            page += 1
            print(f"→ Récupération page {page}/{total_pages}...")
            time.sleep(self.delay)  # pause pour limiter les requêtes

            data = call_quran_api(
                f"/recitations/{id_reciter}/by_chapter/{id_chapter}?per_page=50&page={page}"
            )
            audios.extend(data["audio_files"])

        print(f"✔ Terminé ({len(audios)} fichiers audio)")
        return audios

    def getbyid(self, id: int):
        for reciter in self.get_list_all_reciters()["reciters"]:
            if reciter["id"] == id:
                return reciter
        raise Exception("Recitateur introuvable")
