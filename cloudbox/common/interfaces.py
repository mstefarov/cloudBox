# cloudBox is copyright 2012 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from zope.interface import Interface, Attribute

#noinspection PyMethodParameters,PyMethodParameters
class IDataHandler(Interface):
    """
    Interface for all DataHandlers.
    """

    parent = Attribute("The parent the DataHandler belongs to.")

    def parseData(data):
        """
        Unserializes data given, and act upon it.
        """

    def packData(data):
        """
        Packs the data to the desired wire-transfer format.
        """

class IGeneralPacketProcessor(Interface):
    """
    Interface for all GeneralPacketProcessors.
    """
    buffer = Attribute("""Buffer for data received.""")

    def parseFirstPacket():
        """
        Parses the first packet in the buffer.
        """

    def packPacket(handler, data):
        """
        Packs a packet using the given handler..
        """