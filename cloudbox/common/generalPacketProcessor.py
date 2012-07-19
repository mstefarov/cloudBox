# cloudBox is copyright 2012 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from google.protobuf import descriptor, descriptor_pb2, message, reflection
from zope.interface import implements

from cloudbox.common.interfaces import IGeneralPacketParser
from cloudbox.common.protodef import Header

ERR_NOT_ENOUGH_DATA = 0
ERR_UNABLE_TO_PARSE_HEADER = 1
ERR_UNABLE_TO_PARSE_DATA = 2

class ProtobufPacketProcessor(object):
    """
    A General Packet Parser designed for protobuf packets.
    Automatically splits packets, reads the header then dispatches data to registered handlers.
    """
    implements(IGeneralPacketProcessor)

    def __init__(self, parent, handlers, buffer):
        """
        Initializes the class.
        handlers: A dict of the format {packetTypeID: [ParsingHandler, DataHandler]}
        parent: The parent that is using the parser.
        buffer:; The buffer string.
        """
        self.handlers = handlers
        self.parent = parent
        self.buffer = buffer

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

