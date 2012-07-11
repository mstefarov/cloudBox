# cloudBox is copyright 2012 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

import logging, sys, time

class Logger(object):
    """A logger."""

    def __init__(self, name, file, centralLogger, level=logging.INFO):
        self.name = name
        self.file = file
        self.level = level
        self.centralLogger = centralLogger # Instance of CentralLoggerPipe

    def stdout(self, data):
        "Output to stdout."
        try:
            sys.stdout.write(data + "\n")
        except Exception as e:
            print("Unable to write directly to stdout! Data: %s" % data)
            print(str(e))

    def stderr(self, data):
        "Output to stderr."
        try:
            sys.stderr.write(data + "\n")
        except Exception as e:
            self.stdout(data)

    def log(self, data, file):
        "Outputs to the main log file."
        with open(self.file, "a") as f:
            f.write(data + "\n")
            f.flush()
            f.close()

    def logWithLevel(self, level, data):
        if level < self.level: 
            pass # Discard the data
        towrite = "%s - %s - %s" % (time.strftime("%d %b (%H:%M:%S)"), logging.getLevelName(level), data)
        self.log(towrite)
        self.stdout(towrite)
        # Send it to central logger pipe
        self.centralLogger.log(self.name, logging.getLevelName(level), data)

    def debug(self, data):
        """DEBUG level output"""
        self.logWithLevel(logging.DEBUG, data)
        
    def info(self, data):
        """INFO level output"""
        self.logWithLevel(logging.INFO, data)

    def warn(self, data):
        """WARN level output"""
        self.logWithLevel(logging.WARN, data)

    warning = warn

    def error(self, data):
        """ERROR level output"""
        self.logWithLevel(logging.ERROR, data)

    def critical(self, data):
        """CRITICAL level output"""
        self.logWithLevel(logging.CRITICAL, data)
