# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from twisted.application import service
from twisted.application.internet import TCPServer

from cloudbox.hub.heartbeat import HeartbeatService
from cloudbox.hub.minecraft.server import MinecraftHubServerFactory
from cloudbox.hub.world.server import WorldServerCommServerFactory

def init(serv):
    # Minecraft part of the Hub
    serv.factories["MinecraftHubServerFactory"] = MinecraftHubServerFactory(serv, serv.settings["hub"])
    TCPServer(serv.settings["hub"]["main"]["ports"]["clients"], serv.factories["MinecraftHubServerFactory"]).setServiceParent(serv)

    # WorldServer part of the Hub
    serv.factories["WorldServerCommServerFactory"] = WorldServerCommServerFactory(serv, serv.settings["hub"])
    TCPServer(serv.settings["hub"]["main"]["ports"]["worldservers"],
              serv.factories["WorldServerCommServerFactory"]).setServiceParent(serv)

    # Heartbeat Service
    if serv.settings["hub"]["heartbeat"]["send-heartbeat"]:
        if serv.settings["hub"]["heartbeat"]["minecraft-heartbeat"]:
            serv.factories["HeartbeatService-Minecraft"] = HeartbeatService(serv,
                "http://minecraft.net/heartbeat.jsp").start()

        if serv.settings["hub"]["heartbeat"]["classicube-heartbeat"]:
            serv.factories["HeartbeatService-ClassiCube"] = HeartbeatService(serv,
                "http://www.classicube.net/server/heartbeat").start()
    # cloudBox, the variable that binds everything together.
    cloudBox = service.Application("cloudBox")

    # Connect our MultiService to the application
    serv.setServiceParent(cloudBox)