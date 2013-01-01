# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from twisted.internet.protocol import Protocol

from cloudbox.common.gpp import MSGPackPacketProcessor
from cloudbox.common.centralLogger.constants import *

class CentralLoggerPipeProtocol(Protocol):
    """
    Protocol for the Central Logger.
    """

    def __init__(self, factory):
        self.factory = factory
        self.handlers = [
            HANDLERS_CLIENT_BASIC + HANDLERS_CLIENT, # Send
            HANDLERS_SERVER_BASIC + HANDLERS_SERVER, # Receive
        ]
        self.gpp = MSGPackPacketProcessor(self, self.handlers)

    def connectionMade(self):
        """Triggered when a connection is made."""
        self.logger = self.factory.parent.logger
        self.factory.instance = self

    def dataReceived(self, data):
        """Triggered when data is received."""
        self.gpp.feed(data)
        while True:
            unpacked = self.gpp.parseFirstPacket()
            if unpacked == ERR_NOT_ENOUGH_DATA:
                # Wait a bit
                break
            if unpacked == ERR_METHOD_NOT_FOUND:
                # Warn the user that we have an unhandlable packet
                self.factory.logger.warning("Received unparsable data. Dropping connection.")
                callLater(0.2, self.transport.loseConnection)
                return