from skeletons.connection_mgr import IConnectionManager
from ..DataProviderSDK import DataProviderSDK
from ..crossGameUtils import readClientServerVersion
from helpers import dependency, getClientLanguage
from constants import AUTH_REALM


class GameProvider(object):
  
  connectionMgr = dependency.descriptor(IConnectionManager) # type: IConnectionManager
  
  def __init__(self, sdk):
    # type: (DataProviderSDK) -> None
    self.version = sdk.createState(['game', 'version'], readClientServerVersion()[1])
    self.region = sdk.createState(['game', 'region'], AUTH_REALM)
    self.language = sdk.createState(['game', 'language'], getClientLanguage())
    self.server = sdk.createState(['game', 'server'], None)
    
    self.connectionMgr.onConnected += self.__onConnected
    
  def __onConnected(self, *args, **kwargs):
    self.server.setValue(self.connectionMgr.serverUserName)
    
  
    