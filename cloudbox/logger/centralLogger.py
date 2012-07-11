# cloudBox is copyright 2012 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

import os

from twisted.internet.protocol import ServerFactory
from twisted.internet.basic import LineReceiver
from twisted.internet.task import LoopingCall
from twisted.python.logfile import DailyLogFile

class CentralLoggerProtocol(LineReceiver):
    """I am a central logger that handles event logging by all services."""

    def connectionMade(self):
        peer = self.transport.getPeer()
        logging.log(logging.INFO, "Control connection made from %s:%s" % (peer.host, peer.port))
        self.factory, self.controller_factory = self.factory.main_factory, self.factory

    def lineReceived(self, line):
        """Triggered when a line is received."""
  

class CentralLoggerFactory(ServerFactory):
    """
    The Central Logger Factory.
    Contains methods for file I/O.
    """

    protocol = CentralLoggerProtocol

    def __init__(self, file, directory="../", hubFactory=None):
        # Are we in standalone mode?
        self.hubFactory = hubFactory
        self.isStandalone = False
        if self.hubFactory == None:
            self.isStandalone = True
        # Initialize the log file
        self.logfile = DailyLogFile(file, directory)
        self.cache = []
        self.wfcLoop = LoopingCall(self.writeFromCache)
        if not self.isStandalone:
            self.hubFactory.registerLoop(self.
        self.wfcLoop.start(2)

    def writeFromCache(self):
        """Grabs data from cache and write them."""
        # If nothing's in the cache, return
        if self.cache == []: return
        _cache = self.cache
        self.cache = []
        towrite = ""
        for i in _cache:
            towrite + "\n" += i
        self.logfile.write(towrite)
        self.logfile.flush()
        os.fsync(fObj.fileno())
        if self.factory.settings["useFSync"]: os.fsync()