# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from twisted.internet.protocol import Factory

from cloudbox.database.databaseServerProtocol import DatabaseServerProtocol

class DatabaseServerFactory(Factory):
    """I am a database server that takes requests from nodes."""

    protocol = DatabaseServerProtocol

    def __init__(self, dbProvider):
        self.loadConfig()
        self.dbProvider = dbProvider(self)

    def loadConfig(self):
        """
        Loads the configuration.
        """