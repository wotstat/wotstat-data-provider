from BattleFeedbackCommon import BATTLE_EVENT_TYPE
from gui.battle_control.arena_info.arena_vos import VehicleArenaInfoVO
from skeletons.gui.game_control import IGameSessionController
from skeletons.gui.shared import IItemsCache
from ..DataProviderSDK import DataProviderSDK
from Account import PlayerAccount
from PlayerEvents import g_playerEvents
from items import vehicles as itemsVehicles
from constants import PREMIUM_TYPE, ROLE_TYPE_TO_LABEL
from helpers import dependency
from gui.battle_control.battle_constants import PERSONAL_EFFICIENCY_TYPE
from skeletons.gui.battle_session import IBattleSessionProvider, IArenaDataProvider
from gui.battle_control.controllers.feedback_events import _CritsExtra, _DamageExtra, _MultiStunExtra, _VisibilityExtra, PlayerFeedbackEvent
from typing import List

from . import logger



class PlayerFeedbackProvider(object):
  sessionProvider = dependency.descriptor(IBattleSessionProvider) # type: IBattleSessionProvider

  def __init__(self, sdk):
    # type: (DataProviderSDK) -> None
    
    self.onPlayerFeedback = sdk.createTrigger(['battle', 'onPlayerFeedback'])
    
    self.sessionProvider.onBattleSessionStart += self.__onBattleSessionStart
    self.sessionProvider.onBattleSessionStop += self.__onBattleSessionStop
    
    self.battleEventProcessors = {
      BATTLE_EVENT_TYPE.SPOTTED: self.processSpotted,
      BATTLE_EVENT_TYPE.RADIO_ASSIST: self.processRadioAssist,
      BATTLE_EVENT_TYPE.TRACK_ASSIST: self.processTrackAssist,
      BATTLE_EVENT_TYPE.BASE_CAPTURE_POINTS: self.processBaseCapturePoints,
      BATTLE_EVENT_TYPE.BASE_CAPTURE_DROPPED: self.processBaseCaptureDropped,
      BATTLE_EVENT_TYPE.TANKING: self.processTanking,
      BATTLE_EVENT_TYPE.CRIT: self.processCrit,
      BATTLE_EVENT_TYPE.DAMAGE: self.processDamage,
      BATTLE_EVENT_TYPE.KILL: self.processKill,
      BATTLE_EVENT_TYPE.RECEIVED_CRIT: self.processReceivedCrit,
      BATTLE_EVENT_TYPE.RECEIVED_DAMAGE: self.processReceivedDamage,
      BATTLE_EVENT_TYPE.STUN_ASSIST: self.processStunAssist,
      BATTLE_EVENT_TYPE.TARGET_VISIBILITY: self.processTargetVisibility,
      BATTLE_EVENT_TYPE.ENEMY_SECTOR_CAPTURED: self.processEnemySectorCaptured,
      BATTLE_EVENT_TYPE.DESTRUCTIBLE_DAMAGED: self.processDestructibleDamaged,
      BATTLE_EVENT_TYPE.DESTRUCTIBLE_DESTROYED: self.processDestructibleDestroyed,
      BATTLE_EVENT_TYPE.DESTRUCTIBLES_DEFENDED: self.processDestructiblesDefended,
      BATTLE_EVENT_TYPE.DEFENDER_BONUS: self.processDefenderBonus,
      BATTLE_EVENT_TYPE.SMOKE_ASSIST: self.processSmokeAssist,
      BATTLE_EVENT_TYPE.INSPIRE_ASSIST: self.processInspireAssist,
      BATTLE_EVENT_TYPE.BASE_CAPTURE_BLOCKED: self.processBaseCaptureBlocked,
      BATTLE_EVENT_TYPE.MULTI_STUN: self.processMultiStun,
      BATTLE_EVENT_TYPE.DETECTED: self.processDetected,
      BATTLE_EVENT_TYPE.EQUIPMENT_TIMER_EXPIRED: self.processEquipmentTimerExpired,
    }
    
  def __onBattleSessionStart(self):
    self.sessionProvider.shared.feedback.onPlayerFeedbackReceived += self.__onPlayerFeedbackReceived
    self.arenaDataProvider = self.sessionProvider.getArenaDP() # type: IArenaDataProvider
    
  def __onBattleSessionStop(self):
    self.sessionProvider.shared.feedback.onPlayerFeedbackReceived += self.__onPlayerFeedbackReceived

  def __onPlayerFeedbackReceived(self, events):
    # type: (List[PlayerFeedbackEvent]) -> None
  
    for event in events:
      eventType = event.getBattleEventType()
      if eventType not in self.battleEventProcessors:
        logger.error('Unknown battle event type: %d', eventType)
        continue
      
      processed = self.battleEventProcessors[eventType](event)
      eventName = processed[0]
      data = processed[1] if len(processed) > 1 else None
      self.onPlayerFeedback.trigger({'type': eventName, 'data': data})
      
  def vehicleById(self, vehicleID):
    targetVehicle = self.arenaDataProvider.getVehicleInfo(vehicleID) # type: VehicleArenaInfoVO
    if targetVehicle is None: return None
    
    typeInfo = targetVehicle.vehicleType
    return {
      'tag': itemsVehicles.getItemByCompactDescr(typeInfo.compactDescr).name,
      'localizedName': typeInfo.shortName,
      'localizedShortName': typeInfo.name,
      'level': typeInfo.level,
      'class': typeInfo.classTag,
      'role': ROLE_TYPE_TO_LABEL.get(typeInfo.role, 'None'),
      'team': targetVehicle.team,
      'playerName': targetVehicle.player.name if targetVehicle.player else None,
      'playerId': targetVehicle.player.accountDBID if targetVehicle.player else None,
    }
      
  def processSpotted(self, event):
    # type: (PlayerFeedbackEvent) -> any
    extra = event.getExtra() # type: _VisibilityExtra
    veh = self.vehicleById(event.getTargetID())
    
    return ('spotted', {
      'vehicle': veh,
      'isVisible': bool(extra.isVisible()),
      'isDirect': bool(extra.isDirect()),
      'isRoleAction': bool(extra.isRoleAction())
    })
    
  def processRadioAssist(self, event):
    # type: (PlayerFeedbackEvent) -> any
    extra = event.getExtra() # type: _DamageExtra
    
    return ('radioAssist',)

  def processTrackAssist(self, event):
    # type: (PlayerFeedbackEvent) -> any
    extra = event.getExtra() # type: _DamageExtra
    
    return ('trackAssist',)

  def processBaseCapturePoints(self, event):
    # type: (PlayerFeedbackEvent) -> any
    extra = event.getExtra() # type: int
    
    return ('baseCapturePoints',)

  def processBaseCaptureDropped(self, event):
    # type: (PlayerFeedbackEvent) -> any
    extra = event.getExtra() # type: int
    
    return ('baseCaptureDropped',)

  def processBaseCaptureBlocked(self, event):
    # type: (PlayerFeedbackEvent) -> any
    extra = event.getExtra() # type: int
    
    return ('baseCaptureBlocked',)

  def processTanking(self, event):
    # type: (PlayerFeedbackEvent) -> any
    extra = event.getExtra() # type: int
    
    return ('tanking',)

  def processCrit(self, event):
    # type: (PlayerFeedbackEvent) -> any
    extra = event.getExtra() # type: _CritsExtra
    
    return ('crit',)

  def processDamage(self, event):
    # type: (PlayerFeedbackEvent) -> any
    extra = event.getExtra() # type: _DamageExtra
    
    return ('damage',)

  def processKill(self, event):
    # type: (PlayerFeedbackEvent) -> any
    
    return ('kill',)

  def processReceivedCrit(self, event):
    # type: (PlayerFeedbackEvent) -> any
    extra = event.getExtra() # type: _CritsExtra
    
    return ('receivedCrit',)

  def processReceivedDamage(self, event):
    # type: (PlayerFeedbackEvent) -> any
    extra = event.getExtra() # type: _DamageExtra
    
    return ('receivedDamage',)

  def processStunAssist(self, event):
    # type: (PlayerFeedbackEvent) -> any
    extra = event.getExtra() # type: _DamageExtra
    
    return ('stunAssist',)

  def processTargetVisibility(self, event):
    # type: (PlayerFeedbackEvent) -> any
    extra = event.getExtra() # type: _VisibilityExtra
    
    return ('targetVisibility',)

  def processEnemySectorCaptured(self, event):
    # type: (PlayerFeedbackEvent) -> any
    
    return ('enemySectorCaptured',)

  def processDestructibleDamaged(self, event):
    # type: (PlayerFeedbackEvent) -> any
    extra = event.getExtra() # type: int
    
    return ('destructibleDamaged',)

  def processDestructibleDestroyed(self, event):
    # type: (PlayerFeedbackEvent) -> any
    
    return ('destructibleDestroyed',)

  def processDestructiblesDefended(self, event):
    # type: (PlayerFeedbackEvent) -> any
    extra = event.getExtra() # type: int
    
    return ('destructiblesDefended',)

  def processDefenderBonus(self, event):
    # type: (PlayerFeedbackEvent) -> any
    
    return ('defenderBonus',)

  def processSmokeAssist(self, event):
    # type: (PlayerFeedbackEvent) -> any
    extra = event.getExtra() # type: _DamageExtra
    
    return ('smokeAssist',)

  def processInspireAssist(self, event):
    # type: (PlayerFeedbackEvent) -> any
    extra = event.getExtra() # type: _DamageExtra
    
    return ('inspireAssist',)

  def processMultiStun(self, event):
    # type: (PlayerFeedbackEvent) -> any
    extra = event.getExtra() # type: _MultiStunExtra
    
    return ('multiStun',)

  def processDetected(self, event):
    # type: (PlayerFeedbackEvent) -> any
    extra = event.getExtra() # type: _VisibilityExtra
    
    return ('detected',)

  def processEquipmentTimerExpired(self, event):
    # type: (PlayerFeedbackEvent) -> any
    return ('equipmentTimerExpired',)


        
        