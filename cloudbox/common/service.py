# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

# YAMl
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from twisted.application.internet import TCPClient, TCPServer
from twisted.application.service import MultiService

from cloudbox.common.loops import LoopRegistry
from cloudbox.constants.common import *


class cloudBoxService(MultiService):
    """
    The central hub of all services.
    """

    def __init__(self, whoami):
        """
        Initializes the service.
        Whoami contains the server identifier.
        """
        MultiService.__init__(self)
        if whoami not in SERVER_TYPES:
            raise ValueError("Server not in valid SERVER_TYPE")
        self.serverType = SERVER_TYPES[whoami]
        # Make our loop registry
        self.loops = LoopRegistry()
        self.factories = {}
        self.settings = {}
        self.loadConfig()
        self.initComponents()

    def loadConfig(self, reload=False):
        """
        Loads the configuration file, depending on the SERVER_TYPE of the server.
        Specify reload to make the function reload the configuration. Note that by specifying reload, the function
        assumes that the related factories exist.
        """
        if self.serverType == SERVER_TYPES["HubServer"]:
            with open("config/hub.yaml", "r") as f:
                s = f.read()
            self.settings["hub"] = yaml.load(s, Loader)
        elif self.serverType == SERVER_TYPES["DatabaseServer"]:
            with open("config/database.yaml", "r") as f:
                s = f.read()
            self.settings["db"] = yaml.dump(yaml.load(s, Loader))
        elif self.serverType == SERVER_TYPES["DatabaseServer"]:
            with open("config/world.yaml", "r") as f:
                s = f.read()
            self.settings["world"] = yaml.dump(yaml.load(s, Loader))
        if reload:
            self.rehashConfig()

    def rehashConfig(self):
        # Send the configuration to the respective factories
        if self.serverType == SERVER_TYPES["HubServer"]:
            self.factories["MinecraftHubServerFactory"].settings = self.settings["hub"]
            self.factories["WorldServerCommServerFactory"].settings = self.settings["hub"]

    def initComponents(self):
        """
        Initializes components as needed.
        """
        if self.serverType == SERVER_TYPES["HubServer"]:
            from cloudbox.hub.run import init as hubInit
            hubInit(self)
        elif self.serverType == SERVER_TYPES["DatabaseServer"]:
            from cloudbox.database.server.run import init as dbInit
            dbInit(self)