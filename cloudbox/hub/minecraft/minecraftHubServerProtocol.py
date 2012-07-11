# cloudBox is copyright 2012 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from twisted.internet.protocol import Protocol

class MinecraftHubServerProtocol(Protocol):
    """
    Main protocol class for communicating with clients.
    """

    def connectionMade(self):
        """Initial set-up of the protocol"""
        self.buffer = ""
        # Get an ID for ourselves
        self.id = self.factory.claimId(self)
        if self.id == None:
            self.sendError("The server is full.")
            return

