# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from twisted.application import service
from twisted.application.internet import TCPServer

from cloudbox.hub.minecraft.server import MinecraftHubServerFactory
from cloudbox.hub.world.server import WorldServerCommServerFactory

def init(serv):
    # Minecraft part of the Hub
    mcHubServerFactory = MinecraftHubServerFactory(serv)
    TCPServer(serv.settings["ports"]["clients"], mcHubServerFactory).setServiceParent(serv)

    # WorldServer part of the Hub
    wsCommServerFactory = WorldServerCommServerFactory(serv)
    TCPServer(serv.settings["ports"]["worldservers"], wsCommServerFactory).setServiceParent(serv)

    # cloudBox, the variable that binds everything together.
    cloudBox = service.Application("cloudBox")

    # Connect our MultiService to the application
    serv.setServiceParent(cloudBox)