import os
import signal
import sys

from PySide2 import QtCore, QtGui, QtQml

from PlatformIntegrations import *
from ScrobbleHistoryViewModel import *
from ScrobbleDetailsViewModel import *
from ScrobbleHistoryListModel import *

# Get the built application path
if getattr(sys, 'frozen', False):
  # If the application is run as a bundle, the PyInstaller bootloader
  # extends the sys module by a flag frozen=True and sets the app 
  # path into variable _MEIPASS'.
  application_path = sys._MEIPASS
else:
  application_path = os.path.dirname(os.path.abspath(__file__))

# Enable Ctrl-C to kill
signal.signal(signal.SIGINT, signal.SIG_DFL)

# Store constants for registering types
MODULE_NAME = 'Kale'
MAJOR_VERSION = 1
MINOR_VERSION = 0

if __name__ == '__main__':
  # Register models
  QtQml.qmlRegisterType(ScrobbleHistoryViewModel, MODULE_NAME, MAJOR_VERSION, MINOR_VERSION, 'ScrobbleHistoryViewModel')
  QtQml.qmlRegisterType(ScrobbleDetailsViewModel, MODULE_NAME, MAJOR_VERSION, MINOR_VERSION, 'ScrobbleDetailsViewModel')
  QtQml.qmlRegisterType(ScrobbleHistoryListModel, MODULE_NAME, MAJOR_VERSION, MINOR_VERSION, 'ScrobbleHistoryListModel')

  # Enable retina support
  QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

  # Init QtQuick application context
  os.environ['QSG_RENDER_LOOP'] = 'windows' # Use render loop that supports persistent 6MINOR_VERSIONfps
  app = QtGui.QGuiApplication(sys.argv)
  engine = QtQml.QQmlApplicationEngine(parent=app)
  file = os.path.join(application_path, "main.qml")
  engine.load(QtCore.QUrl.fromLocalFile(file))
  PlatformIntegrations.applyMacOsWindowTreatment()
  sys.exit(app.exec_())
