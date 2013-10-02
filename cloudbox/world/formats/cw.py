# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

import cStringIO

import nbt
from zope.interface import implements

from cloudbox.constants.world import *
from cloudbox.world.interfaces import IWorldFormat


class ClassicWorldWorldFormat(object):
    implements(IWorldFormat)

    name = "ClassicWorld Format"
    supportsLoading = True
    supportsSaving = True

    CURRENT_LEVEL_VERSION = 0
    ACCEPTABLE_LEVEL_VERSIONS = [0]

    requiredFields = ["WorldName", "WorldGUID", "X", "Y", "Z", "Spawn", "BlockArray" "Metadata"]
    optionalFields = ["CreatedBy", "MapGeneratorUsed", "TimeCreated", "LastAccessed", "LastModified"]

    @classmethod
    def loadWorld(cls, filepath):
        returnDict = {}
        with open(filepath, "r") as fo:
            _nbtFile = fo.read()
        nbtObject = nbt.NBTFile(cStringIO.StringIO(_nbtFile))
        if nbtObject.name != "CLASSIC_WORLD":
            return {"error": ERROR_HEADER_MISMATCH}  # Not using exceptions due to performance
        if nbtObject["WORLD_VERSION"] not in cls.ACCEPTABLE_LEVEL_VERSIONS:
            return {"error": ERROR_UNSUPPORTED_LEVEL_VERSION}
        for r in cls.requiredFields:
            if not nbtObject[r]:
                return {"error": ERROR_REQUIRED_FIELDS_MISSING, "missingField": r}
            returnDict[r] = nbtObject[r]
        for r in cls.optionalFields:
            if nbtObject[r]:
                returnDict[r] = nbtObject[r]
            else:
                returnDict[r] = None
        return returnDict

    @classmethod
    def saveWorld(cls, filepath, data):
        pass