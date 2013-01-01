# cloudBox is copyright 2012 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from yaml import load, dump
import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from twisted.internet.protocol import ServerFactory

from cloudbox.common.logger import Logger
from cloudbox.hub.hubServerProtocol import MinecraftHubServerProtocol

class MinecraftHubServerFactory(ServerFactory):
    """
    I am the Minecraft side of the hub. I handle Minecraft client requests and pass them on to World Servers.
    """
    protocol = MinecraftHubServerProtocol

    def __init__(self, service):
        self.mainService = service
        self.databaseServer = None
        self.loggingServer = None
        self.settings = {}
        self.clients = {}
        self.loadConfig()

    def loadConfig(self, reload=False):
        """Loads the config from the configuration file."""
        self.settings = yaml.load("../config/hub.yaml", Loader)

    def claimId(self, proto):
        """
        Fetches ID for a client protocol instance.
        """
        for i in range(1, self.settings["main"]["max_clients"] + 1):
            if i not in self.clients:
                self.clients[i] = {"username": proto.username, "protocol": proto}
                # TODO - Hook Call Here
                return i
        # Server is full, claim ID only for staff
        if proto.isHelper():
            i = len(self.clients.keys()) + 1
            self.clients[i] = {"username": proto.username, "protocol": proto}
            # TODO - Hook Call Here
            return i
        raise ServerFull

    def assignServer(self, proto):
        """
        Assign a WorldServer to a user.
        Load Balancing magic happens here.
        """
        # Get the current load from servers


    def buildUsernames(self, wsID):
        """
        Builds a list of {username: client object} by the client list, or
        specify a WorldServer ID to filter.
        """
        theList = dict()
        for client, proto in self.clients:
            if wsID:
                if proto.wsID == wsID:
                    theList[proto.username] = proto
            else:
                theList[proto.username] = proto
        return theList