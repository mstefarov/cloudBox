# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from cloudbox.common.handlers import BasePacketHandler
from cloudbox.constants.cpe import *

class ExtInfoPacketHandler(BasePacketHandler):
    """
    A Handler class for handling extension information.
    """

    @staticmethod
    def handleData(data):
        pass

    @staticmethod
    def packData(data):
        pass

class ExtEntryPacketHandler(BasePacketHandler):
    """
    A Handler class for handling extension entries.
    """

    @staticmethod
    def handleData(data):
        pass

    @staticmethod
    def packData(data):
        pass
