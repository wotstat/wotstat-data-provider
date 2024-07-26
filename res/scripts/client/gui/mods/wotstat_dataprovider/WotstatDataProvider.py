
from .common.ServerLoggerBackend import ServerLoggerBackend
from .common.Logger import Logger, SimpleLoggerBackend
from .common.Config import Config

from .main.WebSocketDataProvider import WebSocketDataProvider


DEBUG_MODE = '{{DEBUG_MODE}}'
CONFIG_PATH = './mods/configs/wotstat.dataprovider/config.cfg'

logger = Logger.instance()

class WotstatDataProvider(object):
  
  def __init__(self):
    logger.info("Starting WotStatWidget")
    
    self.config = Config(CONFIG_PATH)
    version = self.config.get("version")
    
    logger.setup([
      SimpleLoggerBackend(prefix="[MOD_WOTSTAT_DP]", minLevel="INFO" if not DEBUG_MODE else "DEBUG"),
      ServerLoggerBackend(url=self.config.get('lokiURL'),
                          prefix="[MOD_WOTSTAT_DP]",
                          source="mod_dataprovider",
                          modVersion=version,
                          minLevel="INFO")
    ])
    
    webSocketDataProvider = WebSocketDataProvider(logger)