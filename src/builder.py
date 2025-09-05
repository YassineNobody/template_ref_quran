import os
from pathlib import Path
import time
import requests
from src.audio import Audio
from src.interfaces import (
    AudioDataAyah,
    ChapterDict,
    ReciterDict,
    TajweedDict,
    VerseDict,
)
from src.tajweed import Tajweed
from src.utils import readJSON, writeJSON
from src.verses import Verses


class BuilderSurah:
    def __init__(self, pathdirname: str) -> None:
        self.pathdirname = Path(pathdirname)
        self.infos = self.readinfos()
        self.audio_reciters: list[ReciterDict] = []
        self.delay_step: int = 60
        # flags pour savoir si un fetch API a eu lieu
        self.fetched_audio_verse = False
        self.fetched_verses = False
        self.fetched_tajweed = False

    def readinfos(self) -> ChapterDict:
        chapter = readJSON(self.pathdirname.joinpath("infos.json").as_posix(), True)
        if chapter is None:
            raise Exception("Le fichier infos.json est introuvable")
        return chapter

    def set_audio_reciter(self, reciter: ReciterDict) -> None:
        self.audio_reciters.append(reciter)

    def create_dir_audio(self) -> Path:
        path = self.pathdirname.joinpath("audio")
        path.mkdir(exist_ok=True)
        return path

    def _fetch_audio(self) -> None:
        if not self.audio_reciters:
            raise Exception("Vous devez inclure des recitateurs")
        audio = Audio()
        dirname = self.create_dir_audio()
        for reciter in self.audio_reciters:
            self._fetch_single_audio(dirname, reciter, audio)
            try:
                data_brut = audio.get_ayah_audio(reciter["id"], self.infos["id"])
                if data_brut:
                    data = self._parse_audio(data_brut, audio)
                    self._save_reciter_audio(dirname, reciter, data)
                    self.fetched_audio_verse = True
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    print(f"⚠️ {reciter['name']} n’a pas d’audio verset par verset")
                else:
                    raise

    def _fetch_single_audio(
        self, dirname: Path, reciter: ReciterDict, audio: Audio
    ) -> None:
        filename = dirname.joinpath(
            f"{reciter['name'].lower()}-{reciter['id']}-single.json"
        )
        if filename.exists():
            return
        data = audio.get_chapter(reciter["id"], self.infos["id"])
        writeJSON(filename.as_posix(), data, complete=True)

    def _parse_audio(
        self, data: list[AudioDataAyah], audio: Audio
    ) -> list[AudioDataAyah]:
        def p(d_audio: AudioDataAyah):
            url_complete = audio.url_verses_audio + d_audio["url"]
            d_audio["url"] = url_complete
            return d_audio

        return [p(d) for d in data]

    def _save_reciter_audio(
        self, path: Path, reciter: ReciterDict, data: list[AudioDataAyah]
    ) -> None:
        filename = f"{reciter['name'].lower().strip()}-{reciter['id']}-verses.json"
        writeJSON(path.joinpath(filename).as_posix(), data, complete=True)

    def _fetch_verses(self) -> None:
        filename = self.pathdirname.joinpath("verses.json")
        if filename.exists():
            return
        data = Verses().get_verses(self.infos["id"])
        self._save_verses(data)
        self.fetched_verses = True

    def _save_verses(self, data: list[VerseDict]):
        writeJSON(
            self.pathdirname.joinpath("verses.json").as_posix(), data, complete=True
        )

    def _fetch_tajweed(self) -> None:
        filename = self.pathdirname.joinpath("tajweed.json")
        if filename.exists():
            return
        data = Tajweed().get(self.infos["id"])
        self._save_tajweed(data)
        self.fetched_tajweed = True

    def _save_tajweed(self, data: list[TajweedDict]) -> None:
        writeJSON(self.pathdirname.joinpath("tajweed.json").as_posix(), data, True)

    def create(self) -> bool:
        print("Builder in progress " + self.infos.get("name_simple"))
        self._fetch_audio()
        self._fetch_verses()
        self._fetch_tajweed()
        print(f"Builder finish for {self.infos.get('name_simple')}")
        return self.have_fetch()

    def have_fetch(self) -> bool:
        """Retourne True si au moins un appel API a été fait"""
        return any(
            [
                self.fetched_tajweed,
                self.fetched_audio_verse,
                self.fetched_verses,
            ]
        )
