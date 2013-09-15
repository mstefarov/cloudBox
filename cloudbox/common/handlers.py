# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

import random

from zope.interface import implements

from cloudbox.common.interfaces import IPacketHandler
from cloudbox.constants import common, handlers

class BasePacketHandler(object):
    """
    Base packet handler.
    """

    implements(IPacketHandler)

    @staticmethod
    def packData(data):
        pass

    @staticmethod
    def handleData(data):
        pass


class KeepAlivePacketHandler(BasePacketHandler):
    """
    A Handler class for keep-alive.
    """

    @staticmethod
    def packData(data):
        return data["_packer"].pack([])


class HandshakePacketHandler(BasePacketHandler):
    """
    A Handler class for packet HandshakeRequest.
    """

    @staticmethod
    def handleData(data):
        if data["remoteServerType"] == common.SERVER_TYPES["WorldServer"]:
            if data["_serverType"] == common.SERVER_TYPES["HubServer"]:
                # See if they are in our allowed list
                if not data["parent"].transport.getPeer().host in data["parent"].settings["main"]["allowed-ips"]:
                    # Refuse connection
                    data["parent"].sendError("You are not connecting from an authorized IP.")
                    data["parent"].loseConnection()

    # TODO: What the hell is this?
    @staticmethod
    def packData(data):
        return data["_packer"].pack({
            "clientName": data["parent"].NAME,
            "clientType": data["parent"].TYPE
        })

class DisconnectPacketHandler(BasePacketHandler):
    """
    A Handler class for disconnection.
    """

    @staticmethod
    def packData(data):
        return self.data["_packer"].pack({
            "disconnectReason": data["reason"]
        })

class ServerShutdownPacketHandler(BasePacketHandler):
    """
    A Handler class for Server Shutdown.
    """

    @staticmethod
    def parseData(data):
        if data["remoteServerType"] == common.SERVER_TYPES["HubServer"]:
            # Hub Server is closing our connection, why oh why
            if data["_serverType"] == common.SERVER_TYPES["WorldServer"]:
                data["parent"].saveAllWorlds()
                data["parent"].closeAllWorlds()
            elif data["_serverType"] == common.SERVER_TYPES["DatabaseServer"]:
                return
        elif data["remoteServerType"] == common.SERVER_TYPES["WorldServer"]:
            # World Server is closing our connection, probably shutting down
            data["parent"].available = False

    @staticmethod
    def packData(data):
        return data["packer"].pack([
            handlers.TYPE_SERVERSHUTDOWN,
            data["_serverType"]
        ]
        )