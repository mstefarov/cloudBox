# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

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
        self.factories = list()
        self.loadConfig()
        self.initComponents()

    def loadConfig(self):
        """
        Loads the configuration.
        """
        pass

    def initComponents(self):
        """
        Initializes components as needed.
        """
        if self.serverType == SERVER_TYPES["HubServer"]:
            from cloudbox.hub.run import init as hubInit
            hubInit(self)
