from typing import List, Tuple, Optional
from search.search import Search
from search.interfaces import VerseDict, TranslationDict, ChapterDictIncludePath


class MultiTemplate:
    def __init__(self, refs: List[Tuple[int, int, Optional[int]]]):
        """
        refs = liste de tuples (id_surah, start_v, end_v)
        ex: [(1, 1, 2), (50, 33, None)]
        """
        self.search = Search()
        self.blocks = []

        # SVG play/pause
        self.icon_play = """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 5a2 2 0 0 1 3-2l12 7a2 2 0 0 1 0 4l-12 7a2 2 0 0 1-3-2z"/></svg>"""
        self.icon_pause = """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="14" y="3" width="5" height="18" rx="1"/><rect x="5" y="3" width="5" height="18" rx="1"/></svg>"""

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
        # insérer directement les SVG play dans le HTML
        html = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Quran References</title>
<link href="https://fonts.cdnfonts.com/css/kfgqpc-hafs-uthmanic-script" rel="stylesheet">

<style>
body {{
  font-family: 'KFGQPC HAFS Uthmanic Script', serif;
  margin: 0;
  padding: 20px;
  background: #fff;
  text-align: center;
}}
.quran-container {{
  max-width: 900px;
  margin: auto;
  display: flex;
  flex-direction: column;
  gap: 6px;
}}
.verse {{
  margin: 0;
  direction: rtl;
}}
.arabic {{
  font-size: 22px;
}}
.play-verse {{
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  margin-left: 8px;
  vertical-align: middle;
}}
.translation-block {{
  font-size: 15px;
  color: #333;
  text-align: center;
  margin-top: 0.5rem;
}}
.reference {{
  font-size: 14px;
  color: #555;
  font-style: italic;
  margin-bottom: 1.5rem;
}}
</style>
</head>
<body>

<div class="quran-container">
"""

        for info, verses, translation in self.blocks:
            html += '<div class="reference-block">\n'

            for verse in verses:
                html += '<div class="verse">\n'
                html += '  <div class="arabic">\n'
                html += f"    {verse['text_uthmani']}\n"

                if verse.get("audio", {}).get("url"):
                    html += (
                        f'    <span class="play-verse" data-audio="{verse["audio"]["url"]}">'
                        f"{self.icon_play}</span>\n"
                    )

                html += "  </div>\n</div>\n"

            html += '<div class="translation-block">\n'
            for tr in translation:
                html += f'  <div class="translation-verse">{tr["translations"][0]["text"]}</div>\n'
            html += "</div>\n"

            start_v = verses[0]["verse_number"]
            end_v = verses[-1]["verse_number"]
            if start_v == end_v:
                ref = f"Sourate {info['name_simple']} ({info['translated_name']['name']}), v.{start_v}"
            else:
                ref = f"Sourate {info['name_simple']} ({info['translated_name']['name']}), v.{start_v}–{end_v}"
            html += f'<div class="reference">{ref}</div>\n</div>\n'

        # JS : gestion play/pause
        html += f"""
</div>
<script>
(function(){{
    let player = new Audio();
    let currentBtn = null;
    const iconPlay = `{self.icon_play}`;
    const iconPause = `{self.icon_pause}`;

    document.querySelectorAll(".play-verse").forEach(btn => {{
        btn.addEventListener("click", () => {{
            const url = btn.getAttribute("data-audio");
            if (!url) return;

            if (currentBtn === btn && !player.paused) {{
                player.pause();
                btn.innerHTML = iconPlay;
            }} else {{
                if (currentBtn) currentBtn.innerHTML = iconPlay;
                player.src = url;
                player.play();
                btn.innerHTML = iconPause;
                currentBtn = btn;
            }}
        }});
    }});

    player.addEventListener("ended", () => {{
        if (currentBtn) currentBtn.innerHTML = iconPlay;
        currentBtn = null;
    }});
}})();
</script>
</body>
</html>
"""
        return html
