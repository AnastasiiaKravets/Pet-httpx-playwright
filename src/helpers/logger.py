import sys

from loguru import logger

logger.remove(0)
logger.add(sys.stderr, format="{level} - {time} - {message} - {process}")
