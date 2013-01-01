# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

import logging

from twisted.internet.protocol import ClientFactory

from cloudbox.common.centralLogger.protocol import CentralLoggerPipeProtocol

class CentralLoggerPipeFactory(ClientFactory):
    """
    I am a pipe that connects an object to the Central Logger.
    """

    protocol = CentralLoggerPipeProtocol

    def __init__(self, parent):
        self.parent = parent
        self.instance = None
        self.rebootFlag = True

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        self.instance = None
        if self.rebootFlag:
            connector.connect()

    def clientConnectionFailed(self, connector, reason):
        self.parent.logger.critical("CentralLogger connection failed: %s" % reason)
        self.instance = None

    def send(self, message, level=logging.INFO):    
        self.instance.send(message, level)
