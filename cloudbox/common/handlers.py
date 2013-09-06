# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

import random

import msgpack
from zope.interface import implements

from cloudbox.common.interfaces import IDataHandler


class KeepAliveDataHandler(object):
    """
    DataHandler for keep-alive.
    """

    implements(IDataHandler)

    def __init__(self, parent):
        self.parent = parent

    def packData(self, data):
        return {"randomID": random.randint(1, 999999)}


class InitHandshakeDataHandler(object):
    """
    DataHandler for packet HandshakeRequest.
    """

    implements(IDataHandler)

    def __init__(self, parent):
        self.parent = parent

    def packData(self, data):
        return self.parent.packer.pack({
            "clientName": self.parent.parent.NAME,
            "clientType": self.parent.parent.TYPE
        })

    def parseData(self, data):
        return self.parent.unpacker.unpack(data)


class DisconnectDataHandler(object):
    """
    DataHandler for disconnection.
    """

    implements(IDataHandler)

    def __init__(self, parent):
        self.parent = parent

    def pack(self, data):
        return self.parent.packer.pack({
            "disconnectReason": data["reason"]
        })