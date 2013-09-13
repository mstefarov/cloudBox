# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

import random

import msgpack
from zope.interface import implements

from cloudbox.common.interfaces import IPacketHandler


class BasePacketHandler(object):
    """
    Base packet handler.
    """

    implements(IPacketHandler)

    def __init__(self, parent):
        self.parent = parent

    def packData(self, data):
        pass

    def handleData(self, data):
        pass


class KeepAliveDataPacketHandler(BasePacketHandler):
    """
    DataHandler for keep-alive.
    """

    def packData(self, data):
        return {"randomID": random.randint(1, 999999)}


class InitHandshakeDataPacketHandler(BasePacketHandler):
    """
    DataHandler for packet HandshakeRequest.
    """

    def packData(self, data):
        return self.parent.packer.pack({
            "clientName": self.parent.parent.NAME,
            "clientType": self.parent.parent.TYPE
        })

    def handleData(self, data):
        return self.parent.unpacker.unpack(data)


class DisconnectDataPacketHandler(BasePacketHandler):
    """
    DataHandler for disconnection.
    """

    def packData(self, data):
        return self.parent.packer.pack({
            "disconnectReason": data["reason"]
        })