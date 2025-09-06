from typing import List, Tuple, Optional
from search.search import Search
from search.interfaces import VerseDict, TranslationDict, ChapterDictIncludePath


class PartsTemplate:
    def __init__(self, refs: List[Tuple[int, int, Optional[int]]]):
        """
        refs = liste de tuples (id_surah, start_v, end_v)
        ex: [(1, 1, 2), (50, 33, None)]
        """
        self.search = Search()
        self.blocks = []

        for id_surah, start_v, end_v in refs:
            verses: list[VerseDict] = self.search.get_verses(id_surah, start_v, end_v, "verses")  # type: ignore
            translation: list[TranslationDict] = self.search.get_verses(id_surah, start_v, end_v, "translation")  # type: ignore
            info: ChapterDictIncludePath | None = self.search.find_complete_surah_info(
                "id", id_surah
            )

            if not verses or not translation or not info:
                raise Exception(f"Sourate {id_surah} introuvable")

            self.blocks.append((info, verses, translation))

    def get_template(self) -> str:
        return self._write_html()

    def _write_html(self) -> str:
        html = """
<style>
@import url("https://fonts.cdnfonts.com/css/kfgqpc-hafs-uthmanic-script");

.quran-container { max-width: 900px; margin: auto; font-family: 'KFGQPC HAFS Uthmanic Script', serif; }
.verse { margin: 0; direction: rtl; }
.arabic { font-size: 22px; }
.word { cursor: pointer; transition: background 0.2s ease; }
.word:hover { background: #f0f0f0; }
.play-verse { cursor: pointer; margin-right: 6px; color: #007BFF; font-size: 16px; vertical-align: middle; }
.translation-block { font-size: 15px; color: #333; text-align: center; }
.reference { font-size: 14px; color: #555; font-style: italic;  }
</style>

<div class="quran-container">
"""

        # 🔹 Boucle sur chaque bloc (sourate demandée)
        # 🔹 Boucle sur chaque bloc (sourate demandée)
        for info, verses, translation in self.blocks:
            html += '<div class="reference-block">\n'  # 🔹 conteneur pour une référence

            # Partie arabe
            for verse in verses:
                html += '<div class="verse">\n'
                html += '  <div class="arabic">\n'

                for w in verse["words"]:
                    translit = w.get("transliteration", {}).get("text") or ""
                    audio = w.get("audio_url")
                    if audio:
                        html += (
                            f'    <span class="word" data-audio="{audio}" title="{translit}">'
                            f'{w["text_uthmani"]}</span>\n'
                        )
                    else:
                        html += f'    <span class="word" title="{translit}">{w["text_uthmani"]}</span>\n'

                if verse.get("audio", {}).get("url"):
                    html += f'    <span class="play-verse" data-audio="{verse["audio"]["url"]}">▶</span>\n'

                html += "  </div>\n"
                html += "</div>\n"

            # Traductions
            html += '<div class="translation-block">\n'
            for tr in translation:
                html += f'  <div class="translation-verse">({tr["verse_number"]}) {tr["translations"][0]["text"]}</div>\n'
            html += "</div>\n"

            # Référence
            start_v = verses[0]["verse_number"]
            end_v = verses[-1]["verse_number"]
            if start_v == end_v:
                ref = f"— Sourate {info['name_simple']} ({info['translated_name']['name']}), v.{start_v}"
            else:
                ref = f"— Sourate {info['name_simple']} ({info['translated_name']['name']}), v.{start_v}–{end_v}"
            html += f'<div class="reference">{ref}</div>\n'

            html += "</div>\n"  # 🔹 fin du bloc

        # --- JS ---
        html += """
</div>
<script>
(function(){
    let player = new Audio();
    document.querySelectorAll(".word[data-audio]").forEach(span => {
        span.addEventListener("click", () => {
            const url = span.getAttribute("data-audio");
            if (url) { player.src = url; player.play(); }
        });
    });
    document.querySelectorAll(".play-verse[data-audio]").forEach(btn => {
        btn.addEventListener("click", () => {
            const url = btn.getAttribute("data-audio");
            if (url) { player.src = url; player.play(); }
        });
    });
})();
</script>
"""
        return html
