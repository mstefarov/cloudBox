# cloudBox is copyright 2012 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from twisted.internet.task import LoopingCall
from zope.interface import implements

from cloudbox.common.loopRegistry.interfaces import ILoopRegistry

class LoopRegistry(object):
    """
    I am the loop Registry. I keep all LoopingCalls together, allowing plugin authors
    to easily keep track of them.
    I can be used from anywhere.
    """

    implements(ILoopRegistry)

    loops = {}

    def registerLoop(self, name, obj):
        self.loops[name] = obj

    def unregisterLoop(self, name):
        del self.loops[name]
