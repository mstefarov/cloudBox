# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from twisted.internet.protocol import Protocol

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
        self.id = self.factory.claimId(self)
        if self.id is None:
            self.sendError("The server is full.")
            return

    def dataReceived(self, data):
        """
        Called when data is received.
        """
        # First, add the data we got onto our internal buffer
        self.buffer += data
        # While there's still data there...
        while self.buffer:
            # Examine the first byte, to see what the command is
            type = ord(self.buffer[0])
            try:
                format = TYPE_FORMATS[type]
            except KeyError:
                # it's a weird data packet, probably a ping.
                reactor.callLater(0.2, self.transport.loseConnection)
                return
            # See if we have all its data
            if len(self.buffer) - 1 < len(format):
                # Nope, wait a bit
                break
            # OK, decode the data
            parts = list(format.decode(self.buffer[1:]))
            self.buffer = self.buffer[len(format) + 1:]

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