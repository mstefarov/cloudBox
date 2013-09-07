# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

import msgpack
from zope.interface import implements

from cloudbox.common.interfaces import IGeneralPacketProcessor


class MSGPackPacketProcessor(object):
    """
    A General Packet Processor for MSGPack packets.
    """
    implements(IGeneralPacketProcessor)

    def __init__(self, parent, handlers):
        """
        Initialization.
        """
        self.parent = parent
        self.handlers = handlers
        self.unpacker = msgpack.Unpacker()

    def feed(self, data):
        self.unpacker.feed(data)

    def parseFirstPacket(self):
        """
        Parses the first packet received in the buffer and pass it onto the handler.
        """
        # Try to decode the data
        data = self.unpacker.unpack()
        if not data:
            return ERR_NOT_ENOUGH_DATA # Try again later
        # Read the handler
        handler = data[0]
        if handler not in self.handlers.keys():
            return ERR_METHOD_NOT_FOUND
        # Pass it on to the handler to handle this request
        ret = self.handlers[handler].parseData(data[1])
        return ret