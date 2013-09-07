# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from twisted.internet.protocol import Protocol, connectionDone as _connDone
from cloudbox.constants.cpe import * # Classic things plus CPE things


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
        # First, add the data we got onto our internal buffer
        self.buffer += data
        # While there's still data there...
        while self.buffer:
            # Examine the first byte, to see what the command is
            packetType = ord(self.buffer[0])
            try:
                packetFormat = TYPE_FORMATS[packetType]
            except KeyError:
                # Out of range - unknown packet.
                break
            # See if we have all its data
            if len(self.buffer) - 1 < len(packetFormat):
                # Nope, wait a bit
                return
            # OK, decode the data
            parts = list(packetFormat.decode(self.buffer[1:]))
            self.buffer = self.buffer[len(packetFormat) + 1:]

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
