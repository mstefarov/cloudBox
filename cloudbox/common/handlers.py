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

    @staticmethod
    def packData(data):
        pass

    @staticmethod
    def handleData(data):
        pass


class KeepAliveDataPacketHandler(BasePacketHandler):
    """
    DataHandler for keep-alive.
    """

    @staticmethod
    def packData(data):
        return {"randomID": random.randint(1, 999999)}


class InitHandshakeDataPacketHandler(BasePacketHandler):
    """
    DataHandler for packet HandshakeRequest.
    """

    # TODO: What the hell is this?
    @staticmethod
    def packData(data):
        return self.data["_packer"].pack({
            "clientName": self.data["parent"].NAME,
            "clientType": self.data["parent"].TYPE
        })

    @staticmethod
    def handleData(data):
        return self.data["_packer"].unpack(data)


class DisconnectDataPacketHandler(BasePacketHandler):
    """
    DataHandler for disconnection.
    """

    @staticmethod
    def packData(data):
        return self.data["_packer"].pack({
            "disconnectReason": data["reason"]
        })