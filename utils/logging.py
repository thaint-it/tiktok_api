import logging


class CommonLogger:
    def __init__(self, prefix=""):
        self.logger = logging.getLogger("common_logger")

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)
        self.logger.setLevel(logging.INFO)
        self.prefix = prefix

    def info(self, message):
        self.logger.info(f"{self.prefix} - {message}")

    def error(self, message):
        self.logger.error(f"{self.prefix} - {message}")

    def warning(self, message):
        self.logger.warning(f"{self.prefix} - {message}")

    def debug(self, message):
        self.logger.debug(f"{self.prefix} - {message}")
