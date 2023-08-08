
import logging
import os

@dataclass 
class WBLogLevel:
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

class WBFormatter(logging.Formatter):
  "[{severity} {time}] [{name}]: {message} ({function_name}() at {file_name}:{line_number})"
  grey = "\x1b[38;20m"
  yellow = "\x1b[33;20m"
  red = "\x1b[31;20m"
  bold_red = "\x1b[31;1m"
  reset = "\x1b[0m"
  format = "[%(levelname)s %(asctime)s] [%(name)s]: %(message)s (%(funcName)s() at %(filename)s:%(lineno)d)"

  FORMATS = {
      logging.DEBUG: grey + format + reset,
      logging.INFO: grey + format + reset,
      logging.WARNING: yellow + format + reset,
      logging.ERROR: red + format + reset,
      logging.CRITICAL: bold_red + format + reset
  }

  def format(self, record):
      log_fmt = self.FORMATS.get(record.levelno)
      formatter = logging.Formatter(log_fmt)
      return formatter.format(record)
  
def create_logger(log_level: WBLogLevel = WBLogLevel.DEBUG) -> logging.Logger:
    # create logger with filename as name
    logger = logging.getLogger(os.path.basename(__file__))
    logger.setLevel(log_level)

    # create console handler with specified log level
    ch = logging.StreamHandler()
    ch.setLevel(log_level)

    # set formatter of the console stream handler
    ch.setFormatter(WBFormatter())

    # add the handlers to the logger
    logger.addHandler(ch)

    return logger