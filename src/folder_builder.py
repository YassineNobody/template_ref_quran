from pathlib import Path
import json

from src.chapters import Chapters
from src.interfaces import ChapterDict
from src.utils import writeJSON


class FolderBuilder:
    def __init__(self) -> None:
        self.folder_database = Path(__file__).parent.parent / "quran"
        self.chapters = Chapters()

    def _create_database(self) -> None:
        if self.folder_database.exists():
            return
        self.folder_database.mkdir()

    def constructor(self) -> list[Path]:
        self._create_database()
        folders: list[Path] = []
        for chapter in self.chapters.chapters["chapters"]:
            dirname_chapter = self.folder_database.joinpath(
                f"{chapter['id']}-{chapter["name_simple"].lower()}"
            )
            if dirname_chapter.exists():
                pass

            else:
                dirname_chapter.mkdir()
                pass
            folders.append(dirname_chapter)
            self.check_files_in_folder(dirname_chapter, chapter)
        return folders

    def check_files_in_folder(
        self, dirname_folder: Path, chapter_infos: ChapterDict
    ) -> None:
        # on verifie si les infos de la sourates existe -> ChapterDict
        if (dirname_folder.joinpath("infos.json")).exists():
            pass
        else:
            print(f"Création du fichier infos.json pour {dirname_folder.name}")
            writeJSON(
                dirname_folder.joinpath("infos.json").as_posix(), chapter_infos, True
            )

        # d'autre verif ici plus tards

    def find_folder(self, name_folder: str) -> str:
        for folder in self.folder_database.iterdir():
            if folder.is_dir():
                if folder.name.lower == name_folder.lower():
                    return folder.as_posix()
        raise Exception("dossier introuvable : function find_folder")
