# cloudBox is copyright 2012 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

import urllib

from zope.interface import implements

from twisted.internet import reactor
from twisted.internet.defer import succeed
from twisted.web.client import Agent
from twisted.web.http_headers import Headers

class HeartbeatService(object):
    """I send heartbeats to Minecraft.net/WorldOfMinecraft every so often."""

    def __init__(self, factory):
        self.factory = factory
        self.logger = factory.logger.getLogger(
        self.agent = Agent(reactor)

    def sendHeartbeat(self):
        """Sends Heartbeat."""
        
    def _sendHeartbeat(self, overrideurl=False):
        hburl = "http://direct.worldofminecraft.com/hb.php" if (self.factory.wom_heartbeat and not overrideurl) else "http://www.minecraft.net/heartbeat.jsp"
        getPage(hburl, method="POST", postdata=self.hbdata,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}, timeout=30).addCallback(
            self.heartbeatSentCallback, 0).addErrback(self.heartbeatFailedCallback, 0)