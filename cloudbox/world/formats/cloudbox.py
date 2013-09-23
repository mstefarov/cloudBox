# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

import cStringIO

import nbt
from zope.interface import implements

from cloudbox.constants.world import *
from cloudbox.world.formats.base import BaseWorldFormat


class CloudBoxWorldFormat(BaseWorldFormat):
    name = "cloudBox Classic Format"
    supportsLoading = True
    supportsSaving = True

    CURRENT_LEVEL_VERSION = 0
    ACCEPTABLE_LEVEL_VERSIONS = [0]

    @staticmethod
    def loadWorld(filepath):
        with open(filepath, "r") as fo:
            _nbtFile = fo.read()
        nbtObject = nbt.NBTFile(cStringIO.StringIO(_nbtFile))
        if nbtObject.name != "CLOUDBOX_LEVEL":
            return {"error": ERROR_HEADER_MISMATCH}  # Not using exceptions due to performance
        if nbtObject["LEVEL_VERSION"] not in CloudBoxWorldFormat.ACCEPTABLE_LEVEL_VERSIONS:
            return {"error": ERROR_UNSUPPORTED_LEVEL_VERSION}
        for r in CloudBoxWorldFormat.requiredFields:
            if not nbtObject["r"]:
                return {"error": ERROR_REQUIRED_FIELDS_MISSING, "missingField": r}
        return nbtObject  # The NBT lib seems to translate the object pretty well... passing it directly