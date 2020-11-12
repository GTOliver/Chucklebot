from datetime import datetime


class Logger:
    @staticmethod
    def log_message(message):
        print(datetime.now(), message)
