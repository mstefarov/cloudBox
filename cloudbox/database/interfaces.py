# cloudBox is copyright 2012 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from zope.interface import Attribute, Interface

class IDatabaseServerFactory(Interface):
    """
    An object that provides the DatabaseServerFactory interface.
    """

    dbConnection = Attribute("The database connection")

    def dbConnect():
        """
        Connects to the database.
        """

    def dbDisconnect():
        """
        Disconnects to the database, flushing any data if we need to.
        """