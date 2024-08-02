import BigWorld

from KeyboardProvider import KeyboardProvider
from Player import PlayerProvider

def setup(dataProviderSDK):
  KeyboardProvider(dataProviderSDK)
  PlayerProvider(dataProviderSDK)
