from sys import version_info
from .modulemanage.module_update import check_and_update_module
# ------------------------------
from .main.videosmanager import VideosManager
from .main.videos import Videos
from .main.rich_VD4 import my_console as con
from .main import formatstr

from .richtext import ask_prompt as ask
from .richtext.read_script import print_code

from .newtypes import new_sum

from rich.text import Text
from rich.style import Style

# 파이썬 버전 확인
if not version_info >= (3, 11):
    raise ImportError("Only Python versions 3.11 and above are supported")

# yt-dlp 확인
check_and_update_module('yt-dlp', "ask")

__all__ = ["VideosManager", "Videos", "con", "formatstr", "ask", "print_code", "new_sum", "Text", "Style"]

__version__ = "2.0.0"
