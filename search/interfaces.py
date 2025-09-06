from typing import Any, Literal, TypedDict, List

class TranslatedName(TypedDict):
    language_name: str
    name: str


class ChapterDict(TypedDict):
    id: int
    revelation_place: Literal["makkah", "madinah"]  # ⚠️ "makkah", pas "mekka"
    revelation_order: int
    bismillah_pre: bool
    name_simple: str
    name_complex: str
    name_arabic: str
    verses_count: int
    pages: List[int]
    translated_name: TranslatedName


class ChapterDictIncludePath(ChapterDict):
    path: str

class ChaptersProps(TypedDict):
    chapters: List[ChapterDict]


class StyleReciter(TranslatedName): ...


class QiratReciter(TranslatedName): ...


class ReciterDict(TypedDict):
    id: int
    name: str
    style: StyleReciter
    qirat: QiratReciter
    translated_name: TranslatedName


class Reciters(TypedDict):
    reciters: List[ReciterDict]


class AudioDataAyah(TypedDict):
    verse_key: str
    url: str


class TranslationVerse(TypedDict):
    text: str
    language_name: str


class WordVerse(TypedDict):
    id: int
    position: int
    audio_url: str
    char_type_name: str
    text_uthmani: str
    page_number: int
    line_number: str
    text: str
    translation: TranslationVerse
    transliteration: TranslationVerse


class AudioVerse(TypedDict):
    url: str
    segments: list


class VerseDict(TypedDict):
    id: int
    verse_number: int
    verse_key: str
    hizb_number: int
    rub_el_hizb_number: int
    ruku_number: int
    manzil_number: int
    sajda_number: None | Any
    text_uthmani: str
    page_number: int
    juz_number: int
    words: list[WordVerse]
    audio: AudioVerse


class TajweedDict(TypedDict):
    id:int
    verse_key:str
    text_uthmani_tajweed:str


class TranslationItem(TypedDict):
    id: int
    resource_id: int
    text: str

class TranslationDict(TypedDict):
    id: int
    verse_number: int
    verse_key: str
    hizb_number: int
    rub_el_hizb_number: int
    ruku_number: int
    manzil_number: int
    sajdah_number: None | Any
    page_number: int
    juz_number: int
    translations: list[TranslationItem]

