# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from zope.interface import Attribute, Interface

#noinspection PyMethodParameters,PyMethodParameters,PyMethodParameters
class IDatabaseProvider(Interface):
    """
    The interface to the Database Providers
    """

    dbConnection = Attribute("The database connection")

    #noinspection PyMethodParameters
    def dbConnect():
        """
        Connects to the database.
        """

    def dbDisconnect():
        """
        Disconnects to the database, flushing any data if we need to.
        """