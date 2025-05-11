import logging
from pathlib import Path

class LoggerConfig:
    ROOT_DIR = Path(__file__).parent.parent
    LOG_DIR = ROOT_DIR / 'logs'
    LOG_LEVEL = logging.INFO
    LOG_NAME = 'MyLogger'

print(LoggerConfig.ROOT_DIR)