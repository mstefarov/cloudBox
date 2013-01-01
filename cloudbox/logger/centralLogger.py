# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

import os

from twisted.internet.protocol import ServerFactory, Protocol
from twisted.internet.reactor import callLater
from twisted.internet.task import LoopingCall
from twisted.internet.threads import deferToThread
from twisted.python.logfile import DailyLogFile

from cloudbox.common.constants import *
from cloudbox.common.gpp import MSGPackPacketProcessor
from cloudbox.logger.constants import *

class CentralLoggerProtocol(Protocol):
    """
    I am a central logger that handles event logging by all services.
    """

    def __init__(self):
        self.serverType = None
        self.gpp = MSGPackPacketProcessor(self, self.factory.handlers)

    def dataReceived(self, data):
        """Triggered when data is received."""
        # First, add the data we got onto our internal buffer
        self.gpp.feed(data)
        while True:
            try:
                # Ask the GPP to decode the data, if possible
                response = self.gpp.parseFirstPacket()
                # Check the response
                if response == ERR_METHOD_NOT_FOUND:
                    # Warn the user that we have an unhandlable packet
                    self.factory.logger.warning("Received unparsable data. Dropping connection.")
                    callLater(0.2, self.transport.loseConnection)
                    return
            except StopIteration:
                # No more data
                break

class CentralLoggerFactory(ServerFactory):
    """
    The Central Logger Factory.
    Contains methods for file I/O.
    """

    protocol = CentralLoggerProtocol

    def __init__(self, file="server.log", directory="../", hubFactory=None):
        # Are we in standalone mode?
        self.hubFactory = hubFactory
        self.isStandalone = False
        if self.hubFactory is None:
            self.isStandalone = True
        self.handlers = HANDLERS_CENTRALLOGGER_SERVER
        # Initialize the log file
        self.logfile = DailyLogFile(file, directory)
        self.cache = []
        self.wfcLoop = LoopingCall(self.writeFromCache)
        if not self.isStandalone:
            self.wfcLoop = self.hubFactory.service.loops.registerLoop(self.wfcLoop, "logger.centralLogger.writeFromCache")
        self.wfcLoop.start(2)
        self.logger = self.hubFactory.logger if not self.isStandalone else Logger()

    def writeFromCache(self):
        """Grabs data from cache and write them."""
        # If nothing's in the cache, return
        if not self.cache: return
        deferToThread(self._writeFromCache) # Because File I/O blocks

    def _writeFromCache(self):
        _cache = self.cache
        self.cache = []
        towrite = ""
        for i in _cache:
            towrite += "\n" + i
        self.logfile.write(towrite)
        self.logfile.flush()