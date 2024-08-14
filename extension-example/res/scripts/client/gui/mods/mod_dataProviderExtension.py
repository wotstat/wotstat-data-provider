import BigWorld
import Keys
from gui import InputHandler

from dataProviderTyping import IDataProviderSDK, IState, ITrigger

demoState = None # type: IState
demoTrigger = None # type: ITrigger

def setupExtension():
  global demoState, demoTrigger
  
  if not hasattr(BigWorld, 'wotstat_dataProvider'):
    return
  
  provider = BigWorld.wotstat_dataProvider # type: IDataProviderSDK
  
  providerVersion = provider.version
  extension = provider.registerExtension('demoExtension')
  demoState = extension.createState(['demo', 'state'], 0)
  demoTrigger = extension.createTrigger(['demo', 'trigger'])
  
  print('Extension setup complete. Data provider version: %s' % str(providerVersion))


def onKeyDown(event):
  # type: (BigWorld.KeyEvent) -> None
  if not demoState or not demoTrigger:
    return
  
  if event.key == Keys.KEY_T:
    demoTrigger.trigger(BigWorld.time())
  
  if event.key == Keys.KEY_SPACE:
    demoState.setValue(demoState.getValue() + 1)

def init():
  # Wait next frame after game start
  BigWorld.callback(0, setupExtension)
  InputHandler.g_instance.onKeyDown += onKeyDown