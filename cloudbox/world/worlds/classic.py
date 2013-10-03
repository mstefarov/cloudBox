# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

import array
import importlib

from twisted.internet.threads import deferToThread
from zope.interface import implements

from cloudbox.common.constants.world import SUPPORTED_LEVEL_FORMATS
from cloudbox.world.interfaces import IWorld


class ClassicWorld(object):
    """
    I am a Minecraft Classic world.
    """
    implements(IWorld)

    def __init__(self, factory, **worldParams):
        self.factory = factory
        self.worldReady = False
        self.worldParams = worldParams
        self.blockData = array.array("B")
        self.metadata = {}
        self.blockMetadata = {}
        self.physics = None  # Physics engine here

    def loadWorld(self):
        # TODO File IO needs own process?
        deferToThread(self._loadWorld).addCallback(lambda: self.__setattr__("worldReady", True))  # Laziness calls :D

    def _loadWorld(self):
        # Get the handler
        cls = getattr(importlib.import_module(SUPPORTED_LEVEL_FORMATS[self.worldParams["worldType"][0]]),
                      SUPPORTED_LEVEL_FORMATS[self.worldParams["worldType"][1]])
        data = cls.loadWorld(self.worldParams["filePath"])
        # Unpack data

    def saveWorld(self):
        deferToThread(self._saveWorld)

    def _saveWorld(self):
        # Get the handler
        cls = getattr(importlib.import_module(SUPPORTED_LEVEL_FORMATS[self.worldParams["worldType"][0]]),
                      SUPPORTED_LEVEL_FORMATS[self.worldParams["worldType"][1]])
        # Prepare data
        data = {
            "Name": self.worldName,
            "GUID": self.GUID,
            "BlockArray": self.blockData
            "Metadata": {
                "cloudBox": self.metadata
            },
            "BlockMetadata": {
                "cloudBox": self.blockMetadata
            },
        }
        cls.saveWorld(self.worldParams["filePath"])
