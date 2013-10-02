# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.platform.twisted import TwistedIOLoop
from twisted.internet import reactor

from cloudbox.web.application import WebServerApplication


def init(serv):
    TwistedIOLoop().install()

    serv.factories["WebServerApplicationHTTPServer"] = WebServerApplication(serv)
    serv.factories["WebHTTPServer"] = HTTPServer(serv.factories["WebServerApplicationHTTPServer"])
    serv.factories["WebHTTPServer"].listen(serv.settings["web"]["port"])
    IOLoop.instance().run()

    reactor.run()