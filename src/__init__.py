import dotenv

dotenv.load_dotenv()
from src.api import call_quran_api
from src.constantes import CLIENT_ID, CLIENT_SECRET, URL_OAUTH2, TOKEN_FILE
from src.utils import readJSON, file_exists, writeJSON
from src.chapters import Chapters
from src.audio import Audio
from src.folder_builder import FolderBuilder
from src.builder import BuilderSurah
from src.tajweed import Tajweed
from src.quran import Quran
