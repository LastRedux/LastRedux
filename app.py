import os
import sys

from PySide2 import QtCore, QtGui, QtQml

from PlatformIntegrations import *
from ApplicationViewModel import *
from ScrobbleDetailsViewModel import *
from ScrobbleHistoryListModel import *

application_path = (
  sys._MEIPASS
  if getattr(sys, "frozen", False)
  else os.path.dirname(os.path.abspath(__file__))
)

if __name__ == '__main__':
  # Register models
  QtQml.qmlRegisterType(ApplicationViewModel, 'Kale', 1, 0, 'ApplicationViewModel')
  QtQml.qmlRegisterType(ScrobbleDetailsViewModel, 'Kale', 1, 0, 'ScrobbleDetailsViewModel')
  QtQml.qmlRegisterType(ScrobbleHistoryListModel, 'Kale', 1, 0, 'ScrobbleHistoryListModel')

  # Enable retina support
  QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

  # Init QtQuick application context
  os.environ['QSG_RENDER_LOOP'] = 'windows' # Use render loop that supports persistent 60fps
  app = QtGui.QGuiApplication(sys.argv)
  engine = QtQml.QQmlApplicationEngine(parent=app)
  file = os.path.join(application_path, "main.qml")
  engine.load(QtCore.QUrl.fromLocalFile(file))
  PlatformIntegrations.applyMacOsWindowTreatment()
  sys.exit(app.exec_())
