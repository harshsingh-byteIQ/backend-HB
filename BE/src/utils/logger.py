import logging
import os

class Logger:
    def __init__(self, log_file="logs/app.log"):
        os.makedirs(os.path.dirname(log_file), exist_ok=True)  # Ensure directory exists

        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger(__name__)

    def log_info(self, message: str):
        """Logs an INFO message."""
        self.logger.info(message)

    def log_error(self, message: str):
        """Logs an ERROR message."""
        self.logger.error(message)

logger = Logger() #creates an instance

