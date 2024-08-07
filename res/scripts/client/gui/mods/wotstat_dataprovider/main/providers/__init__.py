import BigWorld

from ..ILogger import ILogger

logger = None # type: ILogger | None

def setup(dataProviderSDK, loggerInstance):

  global logger 
  logger = loggerInstance
  
  from KeyboardProvider import KeyboardProvider
  from PlayerProvider import PlayerProvider
  from GameProvider import GameProvider
  from AccountProvider import AccountProvider
  from HangarProvider import HangarProvider
  from PlatoonProvider import PlatoonProvider
  from BattleProvider import BattleProvider
  from AimingProvider import AimingProvider
  
  # KeyboardProvider(dataProviderSDK, logger)
  PlayerProvider(dataProviderSDK)
  GameProvider(dataProviderSDK)
  AccountProvider(dataProviderSDK)
  HangarProvider(dataProviderSDK)
  PlatoonProvider(dataProviderSDK)
  BattleProvider(dataProviderSDK)
  AimingProvider(dataProviderSDK)
