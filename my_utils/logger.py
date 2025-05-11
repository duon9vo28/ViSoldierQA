import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent.parent))

from config.LoggerConfig import LoggerConfig

import logging

class Logger:
    def __init__(self, name: str = None, log_file: str = None):
        if name is None:
            self.name = LoggerConfig.LOG_NAME
        else:
            self.name = name
        self.log = logging.getLogger(self.name)
        self.log_level = LoggerConfig.LOG_LEVEL
        self.log_dir = LoggerConfig.LOG_DIR
        if log_file is None:
            self.log_file = LoggerConfig.LOG_DIR / 'logging.log'
        else:
            self.log_file = LoggerConfig.LOG_DIR / log_file
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.create_handler()
    
    def create_handler(self):
        self.handler = logging.FileHandler(self.log_file)
        self.handler.setFormatter(self.formatter)
        self.log.addHandler(self.handler)
        self.log.setLevel(self.log_level)
    
    def add_formatter(self, format: str):
        if not format:
            raise ValueError(f'add_formatter() missing 1 required positional argument: format')
        else:
            self.formatter = format
            self.create_handler()
            
    def add_file_handler(self, filename: str):
        if not format:
            raise ValueError(f'add_file_handler() missing 1 required positional argument: filename')
        else:
            self.log_file = LoggerConfig.ROOT_DIR / filename
        self.create_handler()
    
    def log_model(self, model_name):
        self.log.info(f"LLM model: {model_name}")
