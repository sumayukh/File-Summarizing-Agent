import logging
import os
from datetime import datetime
from app.config import LOG_DIR
    
class Logger:
    def __init__(self, LOG_DIR=LOG_DIR):
        self.log_dir = LOG_DIR
        os.makedirs(self.log_dir, exist_ok=True)
        self.log_file = os.path.join(self.log_dir, f"agent_log_{datetime.now().date()}.log")
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
    
    def log(self, message: str):
        logging.info(message)