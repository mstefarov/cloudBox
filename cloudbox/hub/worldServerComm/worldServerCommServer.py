# cloudBox is copyright 2012 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from twisted.internet.protocol import ServerFactory

from cloudbox.common.logger import Logger
from cloudbox.hub.worldServerComm import WorldCommServerProtocol

class WorldServerCommServer(ServerFactory):
    """
    I listen to World Servers and interact with them, acting as a proxy.
    """

    def __init__(self, mchub):
        self.mcHub = mchub
        self.worldServers = {}
        