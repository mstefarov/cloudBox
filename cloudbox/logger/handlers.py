# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from cloudbox.common.interfaces import IDataHandler

class logDataDataHandler(object):
    """
    I am a log data packet.
    """

    implements(IDataHandler)

    def __init__(self, parent):
        self.parent = parent

    def packData(self, data):
        return {"message": data["message"], "from": data["from"]}

    def parseData(self, data):
        return self.parent.unpacker.unpack(data)