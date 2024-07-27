
import json
from typing import List

from .WebSocketDataProvider import WebSocketDataProvider
from .ILogger import ILogger

def canSerializeValue(value):
  try:
    str = json.dumps(value)
    return True
  except Exception as e:
    return e

class State(object):
  def __init__(self, path, wsDataProvider, initialValue = None):
    # type: (List[str], WebSocketDataProvider, any) -> None
    self.__path = path
    self.__wsDataProvider = wsDataProvider
    self.__value = initialValue
    
  def getValue(self):
    return self.__value
  
  def setValue(self, value):
    e = canSerializeValue(value)
    if e != True:
      raise Exception("Failed to serialize value: %s" % e)
    
    self.__value = value
    self.__wsDataProvider.sendMessage(json.dumps({ "type": "state", "path": '.'.join(self.__path), "value": value }))
  
class Trigger(object):
  def __init__(self, path, wsDataProvider):
    # type: (List[str], WebSocketDataProvider) -> None
    self.__path = path
    self.__wsDataProvider = wsDataProvider
    
  def trigger(self, value):
    e = canSerializeValue(value)
    if e != True:
      raise Exception("Failed to serialize value: %s" % e)
    
    self.__wsDataProvider.sendMessage(json.dumps({ "type": "trigger", "path": '.'.join(self.__path), "value": value }))

class DPExtension(object):
  def __init__(self, name, wsDataProvider):
    # type: (str, WebSocketDataProvider) -> None
    self.__wsDataProvider = wsDataProvider
    self.__name = name
    
  def createState(self, path):
    # type: (List[str]) -> State
    return State(['extensions', self.__name] + path, self.__wsDataProvider)
  
  def createTrigger(self, path):
    # type: (List[str]) -> Trigger
    return Trigger(['extensions', self.__name] + path, self.__wsDataProvider)

class DataProviderSDK(object):
  
  def __init__(self, wsDataProvider, logger):
    # type: (WebSocketDataProvider, ILogger) -> None
    self.__wsDataProvider = wsDataProvider
    self.__logger = logger
    
  def createState(self, path, initialValue = None):
    # type: (List[str], any) -> State
    return State(path, self.__wsDataProvider, initialValue)
  
  def createTrigger(self, path):
    # type: (List[str]) -> Trigger
    return Trigger(path, self.__wsDataProvider)
  
  def registerExtension(self, extension):
    return DPExtension(extension, self.__wsDataProvider)