# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

import array
import cStringIO

from twisted.internet.threads import deferToThread
from zope.interface import implements

from cloudbox.world.formats.cw import CloudBoxWorldFormat
from cloudbox.world.interfaces import IWorld


class ClassicWorld(object):
    """
    I am a Minecraft Classic world.
    """
    implements(IWorld)

    def __init__(self, factory):
        self.factory = factory
        self.worldReady = False
        self.blockData = array.array("B")
        self.metadata = []
        self.blockMetadata = []
        self.physics = None  # Physics engine here

    def loadWorld(self):
        deferToThread(self._loadWorld).addCallback(lambda: self.__setattr__("worldReady", True))  # Laziness calls :D

    def _loadWorld(self):
        pass

    def saveWorld(self):
        deferToThread(self._saveWorld)

    def _saveWorld(self):
        pass
