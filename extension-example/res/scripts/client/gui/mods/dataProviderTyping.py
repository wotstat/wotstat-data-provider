
from typing import List

# typing for intellisense
class ITrigger(object):
  def trigger(self, value=None): pass
  
class IState(object):
  def getValue(self): pass
  def setValue(self, value): pass
  
class IExtension(object):
  def createState(self, path, initialValue = None):
    # type: (List[str], any) -> IState
    pass
  
  def createTrigger(self, path):
    # type: (List[str]) -> ITrigger
    pass
  
class IDataProviderSDK(object):
  version = None # type: int
  def registerExtension(self, name):
    # type: (str) -> IExtension
    pass
  