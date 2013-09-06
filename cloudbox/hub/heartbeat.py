# cloudBox is copyright 2012 - 2013 the cloudBox team.
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
    """I send heartbeats to Minecraft.net/ClassiCube every so often."""

    def __init__(self, factory, hburl):
        self.factory = factory
        self.hburl = hburl
        self.logger = factory.logger
        self.agent = Agent(reactor)

    @property
    def hbdata(self):
        return urllib.urlencode({
            "port": self.factory.server_port,
            "users": len(self.factory.clients),
            "max": self.factory.max_clients,
            "name": self.factory.server_name,
            "public": self.factory.public,
            "version": 7,
            "salt": self.factory.salt,
        })

    def sendHeartbeat(self):
        """Sends Heartbeat."""
        
    def _sendHeartbeat(self, overrideurl=False):
        getPage(hburl, method="POST", postdata=self.hbdata,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}, timeout=30).addCallback(
            self.heartbeatSentCallback, 0).addErrback(self.heartbeatFailedCallback, 0)

    def heartbeatSentCallback(self):
        pass

    def heartbeatFailedCallback(self):
        pass
