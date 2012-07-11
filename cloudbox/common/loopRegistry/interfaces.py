# cloudBox is copyright 2012 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from zope.interface import Interface, Attribute

class ILoopRegistry(Interface):
    """
    Interface for a Loop Registry.
    """

    loops = Attribute("The dictionary that contains all the loops.")

    def registerLoop(name, obj):
        """
        Registers a loop.
        """

    def unregisterLoop(name):
        """
        Unregisters a loop.
        """