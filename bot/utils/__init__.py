from .logger import logger, info, warning, debug, success, error, critical
from . import launcher

from os import path, mkdir

if not path.exists(path="sessions"):
    mkdir(path="sessions")
