# -*- coding: utf-8 -*-
import json
import logging
import logging.handlers
import os
import sys
import signal
import time

from PyQt5.QtCore import QUrl, QThread, QObject, Qt#, SIGNAL
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtWidgets import QApplication, QMainWindow, QShortcut, QWidget, QVBoxLayout

_config = json.load(open(os.path.join(os.path.dirname(__file__), 'config.json')))
_logger = logging.getLogger("gui")

class Thread(QThread):
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        time.sleep(3)
        #self.emit(SIGNAL('some_signal'))

class Gui:
    def __init__(self):
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        signal.signal(signal.SIGCHLD, signal.SIG_DFL)
        signal.signal(signal.SIGHUP, signal.SIG_DFL)
        
        self.init_logger()
        _logger.debug("Logger Ititialized")
        
        # Create an application
        self.app = QApplication([])
        
        #Create the Window
        self.win = QWidget()
        self.win.setContentsMargins(0,0,0,0)
        self.win.setGeometry(self.app.desktop().availableGeometry())
        self.win.show()
        
        QShortcut(QKeySequence("Ctrl+Alt+Backspace"), self.win).activated.connect(self.quit)
        # And give it a layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        self.win.setLayout(layout)

        # Create and fill a QWebView
        self.view = QWebView()
        
        # Add the QWebViewto the layout
        layout.addWidget(self.view)
        self.go_to("http://localhost:8080/")
        _logger.info("GUI Started and show localhost")
        #t = self.t = Thread()
        #QObject.connect(t, SIGNAL('some_signal'), self.signalHandler, Qt.QueuedConnection)

    def go_to(self, url):
        self.view.load(QUrl(url))
        self.win.showMaximized()

    def quit(self):
        QApplication.quit()
    
    def init_logger(self):
        # create a format for log messages and dates
        format = '%(Name)s %(levelName)s %(asctime)s: %(message)s'
        rootLogger = logging.getLogger()
        rootLogger.setLevel(getattr(logging, _config.get("general", {}).get("mode", "info").upper(), "INFO"))
        
        dirname = os.path.join(os.path.dirname(__file__), "log")
        try:
            if dirname and not os.path.isdir(dirname):
                os.makedirs(dirname)
                
            fileHandler = logging.handlers.TimedRotatingFileHandler(filename=os.path.join(dirname, 'server.log'), when='D', interval=1, backupCount=5)
            fileHandler.setFormatter(DBFormatter(format))
            rootLogger.addHandler(fileHandler)
        except Exception, e:
            sys.stderr.write("ERROR: couldn't create the logfile directory. Logging to the standard output.\n" + e + "\n")
        
        # Normal Handler on stderr
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(ColoredFormatter(format))
        logging.getLogger().addHandler(streamHandler)
        
    def run(self):
        self.app.exec_()

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, _NOTHING, DEFAULT = range(10)
#The background is set with 40 plus the number of the color, and the foreground with 30
#These are the sequences need to get colored ouput
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[%dm"
BOLD_SEQ = "\033[1m"
COLOR_PATTERN = "%s%s%%s%s" % (COLOR_SEQ, COLOR_SEQ, RESET_SEQ)
LEVEL_COLOR_MAPPING = {
    logging.DEBUG: (BLUE, DEFAULT),
    logging.INFO: (GREEN, DEFAULT),
    logging.WARNING: (YELLOW, DEFAULT),
    logging.ERROR: (RED, DEFAULT),
    logging.CRITICAL: (WHITE, RED),
}

class DBFormatter(logging.Formatter):
    def format(self, record):
        record.pid = os.getpid()
        if not hasattr(record, "levelName"):
            record.levelName = "%-10s" % ("["+record.levelname+"]")
        if not hasattr(record, "Name"):
            record.Name = "[%s]" % record.name.upper()
        return logging.Formatter.format(self, record)

class ColoredFormatter(DBFormatter):
    def format(self, record):
        fg_color, bg_color = LEVEL_COLOR_MAPPING.get(record.levelno, (GREEN, DEFAULT))
        record.levelName = COLOR_PATTERN % (30 + fg_color, 40 + bg_color, "%-10s" % ("["+record.levelname+"]"))
        record.Name = COLOR_PATTERN % (30 + CYAN, 40 + DEFAULT, "[%s]" % record.name.upper())
        return DBFormatter.format(self, record)

        
if __name__ == "__main__":
    sys.exit(Gui().run())