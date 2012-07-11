# cloudBox is copyright 2012 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from twisted.internet.protocol import ClientFactory
from zope.interface import implements

from cloudbox.common.centralLogger import CentralLoggerPipeProtocol

class CentralLoggerPipeFactory(ClientFactory):
    """
    I am a pipe that connects an object to the Central Logger.
    """

    protocol = centralLoggerPipeProtocol

    def __init__(self, main_factory):
        self.main_factory = main_factory
        self.instance = None
        self.rebootFlag = True

    def quit(self, msg):
        self.rebootFlag = False
        self.instance.sendLine("QUIT :" + msg)

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        self.instance = None
        if self.rebootFlag:
            connector.connect()

    def clientConnectionFailed(self, connector, reason):
        self.main_factory.logger.critical("IRC connection failed: %s" % reason)
        self.instance = None