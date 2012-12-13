# cloudBox is copyright 2012 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

import msgpack
from zope.interface import implements

from cloudbox.common.constants import *
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
        Parses the first packet received in the buffer and return it.
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

class ProtobufPacketProcessor(object):
    """
    A General Packet Processor designed for protobuf packets.
    Automatically splits packets, reads the header then dispatches data to registered handlers.
    Currently unused.
    """
    implements(IGeneralPacketProcessor)

    def __init__(self, parent, handlers):
        """
        Initializes the class.
        """
        self.handlers = handlers
        self.parent = parent
        self.buffer = ""

    def parseFirstPacket(self):
        """
        Parses the first packet received.
        """
        headerInstance = Header()
        # Have we received all the bytes for header yet?
        if len(self.buffer) < headerInstance.LENGTH:
            # Nope, wait a bit
            return ERR_NOT_ENOUGH_DATA
        # Header is here, let's parse it
        headerData = self.buffer[0:(headerInstance.LENGTH - 1)]
        try:
            headerInstance.ParseFromString(headerData)
        except message.DecodeError: # Something is wrong, possibly corrupt packet?
            return ERR_UNABLE_TO_PARSE_HEADER
        # Grab the data's information
        dataType = headerInstance.messageType
        dataLen = headerInstance.messageSize
        # Do we have all the bytes to parse the data?
        if len(self.buffer[headerInstance.LENGTH:]) < dataLen:
            return ERR_NOT_ENOUGH_DATA
        # OK, parse the data according to the handler given
        dataPacketData = self.buffer[headerInstance.LENGTH:(dataLen - 1)]
        dataParserInstance = self.handlers[dataType][0]
        try:
            dataParserInstance.ParseFromString(headerData)
        except message.DecodeError: # Something is wrong, possibly corrupt packet?
            # Drop the whole packet
            self.buffer = self.buffer[(headerInstance.LENGTH + dataLen + 1):]
            return ERR_UNABLE_TO_PARSE_DATA
        # Now that we are sure that we have everything, pop the parsed data
        self.buffer = self.buffer[(headerInstance.LENGTH + dataLen + 1):]
        # Pass on the data Parser Instance to the Data Handler
        self.handlers[dataType][1].parseData(dataParserInstance)
        return True

