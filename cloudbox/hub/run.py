# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from twisted.application import internet, service

from cloudbox.hub import minecraft, world

def init(serv):
    # Minecraft part of the Hub
    mcHubServerFactory = minecraft.MinecraftHubServerFactory(serv)
    internet.TCPServer(mcHubServerFactory.settings["ports"]["clients"], mcHubServerFactory).setServiceParent(serv)

    # WorldServer part of the Hub
    worldCommServerFactory = world.WorldServerCommServer(mcHubServerFactory)
    internet.TCPServer(mcHubServerFactory.settings["ports"]["worldservers"], worldCommServerFactory).\
    setServiceParent(serv)

    # Initialize optional servers, if they are a part of the hub server

    if "loggerserver" in mcHubServerFactory.settings["main"]["ports"]:
        import cloudbox.logger.centralLogger
        loggerServerFactory = centralLogger.CentralLoggerFactory()
        internet.TCPServer()

    # cloudBox, the variable that binds everything together.
    cloudBox = service.Application("cloudBox")

    # Connect our MultiService to the application
    serv.setServiceParent(cloudBox)