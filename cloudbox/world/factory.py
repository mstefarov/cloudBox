# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from twisted.internet import reactor
from twisted.internet.protocol import ReconnectingClientFactory

from cloudbox.common.logger import Logger
from cloudbox.world.protocol import WorldServerProtocol


class WorldServerFactory(ReconnectingClientFactory):
    """
    I am the world server. I host some worlds, and do calculations about them.
    """
    protocol = WorldServerProtocol
    retryConnection = False

    def __init__(self, parentService):
        self.parentService = parentService
        self.logger = Logger()
        self.worlds = []
        self.retryConnection = True

    ### Twisted functions

    def startedConnecting(self, connector):
        self.logger.info("Connecting to %s:%s...")

    def buildProtocol(self, addr):
        self.resetDelay()
        proto = WorldServerProtocol()
        return proto

    def quit(self, msg):
        self.retryConnection = False
        # Tell the HubServer we are breaking up
        self.instance.sendServerShutdown()

    def clientConnectionLost(self, connector, reason):
        """
        If we get disconnected, reconnect to server.
        """
        self.instance = None
        if self.rebootFlag:
            connector.connect()

    def clientConnectionFailed(self, connector, reason):
       self.logger.crtical("Connection to HubServer failed: %s" % reason)
       connector.connect()

    def loadWorld(self, worldId):
       pass

    def unloadWorld(self, worldId):
       pass

    def packWorld(self, worldId):
       """
       Packs the world as a world stream to be sent to Hub Server.
       """
       pass

    def unpackWorld(self, worldStream):
       """
       Unpacks the world stream sent from the Hub server.
       """
       pass