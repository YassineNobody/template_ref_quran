

import json
from pathlib import Path
from src.folder_builder import FolderBuilder
from src.interfaces import VerseDict
from src.verses import Verses


class Folder(FolderBuilder):
    def __init__(self) -> None:
        super().__init__()
        self.verses_class = Verses()

    def modify_verses_audio_url(self, verses:VerseDict):
        audio_url = verses['audio']["url"]
        verses["audio"]["url"] = Verses().url_verses_audio + audio_url
        return verses
    
    def modify_verses_words_url(self, verses:VerseDict):
        words = verses.get("words")
        for word in words:
            url = word["audio_url"]
            if (url is None): 
                pass
            else:
                word['audio_url'] = self.verses_class.url_verses_audio + url
        verses["words"] = words
        return verses
    
    def modify(self, dirname:Path):
        verses_json = self.readVerses(dirname)
        def modify_sub(v:VerseDict):
            verses = self.modify_verses_audio_url(v)
            return self.modify_verses_words_url(verses)
        vvs = map(modify_sub, verses_json)
        self.writeVerses(dirname, list(vvs))
            

    def readVerses(self, dirname:Path) -> list[VerseDict]:
        with open(dirname, "r") as f:
            return json.load(f)
        
    def writeVerses(self, dirname:Path, verses:list[VerseDict]) -> None:
        with open(dirname, "w") as f:
            json.dump(verses, f, ensure_ascii=False, indent=4)

        
    def modify_verses(self, verses:VerseDict) -> VerseDict:
        verses_mod = self.modify_verses_audio_url(verses)
        return self.modify_verses_words_url(verses_mod)
    

    def exeception(self, dirname:Path):
        self.readVerses(dirname)
        self.writeVerses(dirname,self.readVerses(dirname))