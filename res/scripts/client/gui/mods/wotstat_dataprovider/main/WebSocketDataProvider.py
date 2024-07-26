import BigWorld

class ILogger(object):
  def debug(self, log): pass
  def info(self, log): pass
  def warn(self, log): pass
  def error(self, log): pass
  def critical(self, log): pass
  

class WebSocketDataProvider(object):

  def __init__(self, logger):
    # type: (ILogger) -> None
    logger.info("Starting WebSocketDataProvider")