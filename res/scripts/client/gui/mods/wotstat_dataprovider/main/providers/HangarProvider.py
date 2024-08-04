import HangarVehicle
from constants import ROLE_TYPE_TO_LABEL
from helpers import dependency
from ..DataProviderSDK import DataProviderSDK
from PlayerEvents import g_playerEvents
from skeletons.gui.shared.utils import IHangarSpace
from CurrentVehicle import g_currentVehicle
from shared_utils import first
from items import vehicles
from . import logger

from ..ExceptionHandling import withExceptionHandling


class HangarProvider(object):
  
  hangarsSpace = dependency.descriptor(IHangarSpace) # type: IHangarSpace
  
  def __init__(self, sdk):
    # type: (DataProviderSDK) -> None
    
    self.vehicle = sdk.createState(['hangar', 'vehicle', 'info'])
    self.crew = sdk.createState(['hangar', 'vehicle', 'crew'])
    self.optDevices = sdk.createState(['hangar', 'vehicle', 'optDevices'])
    self.shells = sdk.createState(['hangar', 'vehicle', 'shells'])
    self.consumables = sdk.createState(['hangar', 'vehicle', 'consumables'])
    self.boosters = sdk.createState(['hangar', 'vehicle', 'boosters'])
    self.isInBattle = sdk.createState(['hangar', 'vehicle', 'isInBattle'], False)
    self.isBroken = sdk.createState(['hangar', 'vehicle', 'isBroken'], False)
    self.postProgression = sdk.createState(['hangar', 'vehicle', 'postProgression'])
    self.xp = sdk.createState(['hangar', 'vehicle', 'xp'])
    
    self.hangarsSpace.onVehicleChanged += self.__onVehicleChanged
    g_playerEvents.onAccountBecomePlayer += self.__onAccountBecomePlayer
    g_playerEvents.onAccountBecomeNonPlayer += self.__onAccountBecomeNonPlayer
    
  
  def __onAccountBecomePlayer(self):
    g_currentVehicle.onChanged += self.__onCurrentVehicleChanged
    self.__onCurrentVehicleChanged()
    
  def __onAccountBecomeNonPlayer(self):
    g_currentVehicle.onChanged -= self.__onCurrentVehicleChanged
  
  @withExceptionHandling(logger)
  def __onVehicleChanged(self, *args, **kwargs):
    vehicle = self.hangarsSpace.getVehicleEntity() # type: HangarVehicle
    self.vehicle.setValue({
      'tag': vehicle.typeDescriptor.name,
      'class': vehicle.typeDescriptor.type.classTag,
      'role': ROLE_TYPE_TO_LABEL.get(vehicle.typeDescriptor.type.role, 'None'),
      'level': vehicle.typeDescriptor.level,
      'localizedName': vehicle.typeDescriptor.type.userString,
      'localizedShortName': vehicle.typeDescriptor.type.shortUserString,
    })
    
  @withExceptionHandling(logger)
  def __onCurrentVehicleChanged(self, *args, **kwargs):
    logger.info('HangarProvider: Current vehicle changed')
    
    item = g_currentVehicle.item
    
    if not item:
      return
    
    self.isBroken.setValue(item.isBroken)
    self.isInBattle.setValue(item.isInBattle)
    
    self.crew.setValue([{
        'isFemale': t[1].isFemale,
        'efficiencyRoleLevel': t[1].efficiencyRoleLevel,
        'vehicleTag': t[1].getVehicle().name,
        'roles': t[1].roles(),
        'skills': [{
          'tag': s.name,
          'level': s.level,
        } for s in t[1].skills]
      } if t[1] else None for t in item.crew
    ])
    
    slots = [first(t.categories) for t in item.optDevices.slots]
    if item.optDevices.dynSlotTypeIdx < len(item.optDevices.slots) and item.optDevices.dynSlotType:
      slots[item.optDevices.dynSlotTypeIdx] = first(item.optDevices.dynSlotType.categories)
      
    installed = [vehicles.getItemByCompactDescr(t).name if t else None for t in item.optDevices.installed.getStorage]
    
    self.optDevices.setValue([{
        'tag': installed[i] if i < len(installed) else None,
        'specialization': slots[i],
      } for i in range(len(slots))
    ])
    
    self.shells.setValue([{
        'tag': t.type,
        'count': t.count,
      } for t in item.shells.installed.getItems()
    ])
    
    self.consumables.setValue([vehicles.getItemByCompactDescr(t).name if t else None for t in item.consumables.installed.getStorage])
    self.boosters.setValue([vehicles.getItemByCompactDescr(t).name if t else None for t in item.battleBoosters.installed.getStorage])
    
    postProgressionCache = vehicles.g_cache.postProgression()
    postProgressionState = item.postProgression.getState()
    
    levels = filter(lambda t: t <= 10, postProgressionState.unlocks)
    level = max(levels) if len(levels) else 0
    features = {
      'optSwitchEnabled': 1 not in postProgressionState.disabledSwitches,
      'shellsSwitchEnabled': 2 not in postProgressionState.disabledSwitches,
    }
    
    
    unlockedModifications = filter(lambda t: t > 10, postProgressionState.unlocks)
    rawTree = item.postProgression.getRawTree()
    possibleModifications = sorted(filter(lambda t: t > 10, rawTree.steps.keys())) if rawTree else []
    unlockedModificationsName = [postProgressionCache.modifications[t].name for t in unlockedModifications]
    selectedModificationsName = [postProgressionCache.modifications[t[0] * 10 + t[1]].name if t[1] else None for t in [(t, postProgressionState.getPair(t)) for t in possibleModifications]]
    
    self.postProgression.setValue({
      'level': level,
      'features': features,
      'unlockedModifications': unlockedModificationsName,
      'selectedModifications': selectedModificationsName,
    })
    
    self.xp.setValue(item.xp)