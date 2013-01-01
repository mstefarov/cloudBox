# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from twisted.application.internet import TCPClient, TCPServer
from twisted.application.service import Application, MultiService
from twisted.python import log

from cloudbox.common.constants import * 
from cloudbox.common.loops import LoopRegistry

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
            raise ValueError, "Server not in valid SERVER_TYPE"
        self.serverType = SERVER_TYPES[whoami]
        # Make our loop registry
        self.loops = LoopRegistry()
        self.factories = list()
        self.loadConfig()
        self.initComponents()

    def addService(self, service):
        MultiService.addService(self, service)

    def removeService(self, service):
        MultiService.removeService(self, service)

    def loadConfig(self):
        """
        Loads the configuration.
        """
        pass

    def initComponenet(self):
        """
        Initializes components as needed.
        """
        if self.serverType == SERVER_TYPES["HubServer"]:
            from cloudbox.hub import run
