# Version
version = '0.0.1'

from .utils import Dump
from .settings import Setting
setting = Setting()
dump = Dump(setting=setting).run
