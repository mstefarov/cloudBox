# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from twisted.internet import Factory
from cloudbox.common.logger import Logger
from cloudbox.common.centralLogger.pipe import CentralLoggerPipe


class WorldServerFactory(Factory):
    """
    I am the world server. I host some worlds, and do calculations about them.
    """

    def __init__(self, parent):
        self.parent = parent
        self.worlds = set()

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