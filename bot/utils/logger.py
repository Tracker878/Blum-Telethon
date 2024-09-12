import sys
from loguru import logger
from bot.config import settings
from datetime import date

logger.remove()

logger.add(sink=sys.stdout, format="<white>{time:YYYY-MM-DD HH:mm:ss}</white>"
                                   " | <level>{level}</level>"
                                   " | <white><b>{message}</b></white>",
           filter=lambda record: record["level"].name != "TRACE")

logger = logger.opt(colors=True)

if settings.DEBUG_LOGGING:
    logger.add(f"logs/err_tracebacks_{date.today()}.txt",
               format="{time:DD.MM.YYYY HH:mm:ss} - {level} - {message}",
               level="TRACE",
               backtrace=True,
               diagnose=True,
               filter=lambda record: record["level"].name == "TRACE")


def info(text):
    return logger.info(text)


def debug(text):
    return logger.debug(text)


def warning(text):
    return logger.warning(text)


def error(text):
    if settings.DEBUG_LOGGING:
        logger.opt(exception=True, colors=True).trace(text)
    return logger.error(text)


def critical(text):
    return logger.critical(text)


def success(text):
    return logger.success(text)
