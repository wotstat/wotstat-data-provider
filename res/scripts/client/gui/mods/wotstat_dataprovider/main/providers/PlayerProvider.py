from Account import PlayerAccount
import BigWorld
from PlayerEvents import g_playerEvents
from ..hook import registerEvent
from Event import Event

from ..DataProviderSDK import DataProviderSDK

class PlayerProvider(object):
  
  def __init__(self, sdk):
    # type: (DataProviderSDK) -> None
    
    self.playerName = sdk.createState(['player', 'name'], None)
    self.playerId = sdk.createState(['player', 'id'], None)
    
    g_playerEvents.onAccountBecomePlayer += self.__onAccountBecomePlayer
    
    global onPlayerId
    onPlayerId += self.__onPlayerId
    
  
  def __onAccountBecomePlayer(self):
    player = BigWorld.player() # type: PlayerAccount
    self.playerName.setValue(player.name)
    print('PlayerProvider: Player name is %s' % player.name)
    
  def __onPlayerId(self, playerId):
    self.playerId.setValue(playerId)
    print('PlayerProvider: Player id is %s' % playerId)
  

onPlayerId = Event()

@registerEvent(PlayerAccount, 'showGUI')
def playerAccount_showGUI(self, *a, **k):
  onPlayerId(self.databaseID)

  
    