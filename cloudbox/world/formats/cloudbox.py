# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

import nbt
from zope.interface import implements

from cloudbox.world.formats.interfaces import IWorldFormat


class CloudBoxWorldFormat(object):
    implements(IWorldFormat)

    name = "cloudBox Classic Format"
    supportsLoading = True
    supportsSaving = True