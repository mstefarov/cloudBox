# cloudBox is copyright 2012 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from twisted.internet.protocol import Protocol

class CentralLoggerPipeProtocol(Protocol):
    """
    Protocol for the Central Logger.
    """

    buffer = "" # Buffer

    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        """Triggered when a connection is made."""
        self.logger = self.factory.parent.logger
        self.factory.instance = self

    def dataReceived(self, data):
        """Triggered when data is received."""
    
