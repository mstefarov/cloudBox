# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from twisted.internet.protocol import Protocol, connectionDone as _connDone

from cloudbox.constants.cpe import * # Classic things plus CPE things
from cloudbox.common.gpp import MinecraftClassicPacketProcessor


class MinecraftHubServerProtocol(Protocol):
    """
    Main protocol class for communicating with clients.
    """

    def __init__(self):
        """
        Initial set-up of the protocol
        """
        self.buffer = ""
        self.id = None
        self.username = None
        self.wsID = None # World Server this user belongs to
        self.identified = False
        self.gpp = MinecraftClassicPacketProcessor(self, self.handlers, self.buffer)

    ### Twisted Methods ###

    def connectionMade(self):
        """
        Called when a connection is made.
        """

        # Get an ID for ourselves
        self.id = self.factory.claimID(self)
        if self.id is None:
            self.sendError("The server is full.")
            return
        # Assign a server for ourselves
        self.wsID = self.factory.assignServer(self)
        if self.wsID is None:
            self.sendError("The connector could not find a server that is open.")
            return

    def connectionLost(self, reason=_connDone):
        # Leave the world
        self.factory.leaveWorldServer(self, wsID)
        # Release our ID
        self.factory.releaseID(self.id)

    def dataReceived(self, data):
        """
        Called when data is received.
        """
        # Add the data we got onto our internal buffer
        self.buffer += data
        self.gpp.parseFirstPacket()

    ### Message Handling ###

    def send(self, msg):
        """
        Sends a message to the client.
        """

    def sendError(self, error):
        """
        Sends an error the client.
        """

    def sendMessage(self, message):
        """
        Sends a message to the client.
        """
