import BigWorld
from WebSocketDataProvider import WebSocketDataProvider
from DataProviderSDK import DataProviderSDK, PublicDataProviderSDK

from providers import setup as setupProviders


def setup(logger):

  def createSDK():
    dataProviderSDK = DataProviderSDK(WebSocketDataProvider(logger), logger)
    publicDataProviderSDK = PublicDataProviderSDK(dataProviderSDK.registerExtension)
    BigWorld.wotstat_dataProvider = publicDataProviderSDK
    BigWorld.callback(0, lambda: setupProviders(dataProviderSDK) if publicDataProviderSDK == BigWorld.wotstat_dataProvider else None)
    
  
  if hasattr(BigWorld, 'wotstat_dataProvider'):
    version = BigWorld.wotstat_dataProvider.version
    if version < PublicDataProviderSDK.version:
      BigWorld.wotstat_dataProvider.dispose()
      createSDK()
      logger.info("DataProviderSDK updated from version %s to %s" % (version, PublicDataProviderSDK.version))
    else:
      logger.info("DataProviderSDK already exists with version %s" % version)
      
  else:
    createSDK()
    logger.info("DataProviderSDK created with version %s" % PublicDataProviderSDK.version)
  