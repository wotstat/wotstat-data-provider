import BigWorld

from threading import Thread, Lock

from typing import List

from .simple_websocket_server import WebSocket, WebSocketServer
from .ILogger import ILogger
from .ExceptionHandling import withExceptionHandling


logger = None # type: ILogger
clients = [] # type: List[WebSocket]

class WSClient(WebSocket):
  @withExceptionHandling(logger)
  def handle(self):
    logger.debug("Received message: %s" % str(self.data))
    self.send_message(self.data)
    
  @withExceptionHandling(logger)
  def connected(self):
    logger.info("Connected %s" % str(self.address))
    clients.append(self)
    
  @withExceptionHandling(logger)
  def handle_close(self):
    logger.info("Disconnected %s"% str(self.address))
    clients.remove(self)


class WebSocketDataProvider(object):

  def __init__(self, loggerInstance):
    # type: (ILogger) -> None
    
    global logger
    logger = loggerInstance
    logger.info("Starting WebSocketDataProvider")
    
    self.server = WebSocketServer('', 38200, WSClient)
    
    self.serverThread = Thread(target=self._requestLoop, args=(self.server,))
    self.serverThread.daemon = True
    self.serverThread.start()
    
    logger.info("WebSocketDataProvider started")
    
  def _requestLoop(self, server):
    # type: (WebSocketServer) -> None
    while True:
      try:
        server.handle_request()
      except Exception as e:
        logger.error("Error in requestLoop: %s" % e)
        
  def sendMessage(self, message):
    # type: (str) -> None
    logger.debug("Sending message to %s clients: %s" % (len(clients), message))
    for client in clients:
      client.send_message_text(message)
