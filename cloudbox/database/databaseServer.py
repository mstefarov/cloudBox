# cloudBox is copyright 2012 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from twisted.enterprise import adbapi
from twisted.internet import Factory
from zope.interface import implements

from cloudbox.database.interfaces import IDatabaseServerFactory

class DatabaseServerFactory(Factory):
    """I am a database server that takes requests from nodes."""

    implements(IDatabaseServerFactory)