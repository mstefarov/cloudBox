# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

import tornado.web


class WebServerApplication(tornado.web.Application):
    """
    I am the WebServer application.
    """

    def __init__(self, parentService):
        self.parentService = parentService
        self.handlers = []
        tornado.web.Application.__init__(self, self.handlers, self.parentService.settings["web"])