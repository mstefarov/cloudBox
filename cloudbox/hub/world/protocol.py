# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from twisted.internet.protocol import Protocol

class WorldServerCommServerProtocol(Protocol):
    """
    The protocol class for the WorldServer communicator factory.
    """

    def __init__(self):
        self.usernames = []

    def connectionMade(self):
        """
        Triggered when connection is established.
        """
        pass

    def dataReceived(self):
        """
        Triggered when data is received.
        """
        pass

    def doLeaveServer(self, proto):
        """
        Makes the protocol leave the server.
        """
        pass