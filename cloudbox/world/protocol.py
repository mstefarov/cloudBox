# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from twisted.internet.protocol import Protocol

from cloudbox.common.gpp import MSGPackPacketProcessor
from cloudbox.common.constants.handlers import *


class WorldServerProtocol(Protocol):
    """
    I am a Protocol for the World Server.
    """

    ### Twisted-related functions ###

    def connectionMade(self):
        self.available = True  # Set to False to prevent new connections
        self.gpp = MSGPackPacketProcessor(self, self.handlers)

    def dataReceived(self, data):
        self.gpp.feed(data)
        self.gpp.parseFirstPacket()

    def sendPacket(self, packetID, packetData):
        self.transport.write(self.handlers[packetID].packData(packetData))

    def sendServerShutdown(self):
        self.sendPacket(TYPE_SERVERDISCONNECT, {})