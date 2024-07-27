import BigWorld
from WebSocketDataProvider import WebSocketDataProvider
from DataProviderSDK import DataProviderSDK

from .providers.KeyboardProvider import KeyboardProvider


def setup(logger):
  webSocketDataProvider = WebSocketDataProvider(logger)
  dataProviderSDK = DataProviderSDK(webSocketDataProvider, logger)
  
  KeyboardProvider(dataProviderSDK)
  
  