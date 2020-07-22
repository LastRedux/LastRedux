import os
import sys

from PySide2 import QtCore, QtGui, QtQml

from PlatformIntegrations import *
from ApplicationViewModel import *
from ScrobbleDetailsViewModel import *
from ScrobbleHistoryListModel import *

if __name__ == '__main__':
  # Register models
  QtQml.qmlRegisterType(ApplicationViewModel, 'Kale', 1, 0, 'ApplicationViewModel')
  QtQml.qmlRegisterType(ScrobbleDetailsViewModel, 'Kale', 1, 0, 'ScrobbleDetailsViewModel')
  QtQml.qmlRegisterType(ScrobbleHistoryListModel, 'Kale', 1, 0, 'ScrobbleHistoryListModel')

  # Init QtQuick application context
  os.environ['QSG_RENDER_LOOP'] = 'windows' # Use render loop that supports persistent 60fps
  app = QtGui.QGuiApplication(sys.argv)
  engine = QtQml.QQmlApplicationEngine(parent=app)
  engine.load('main.qml')
  PlatformIntegrations.applyMacOsWindowTreatment()
  sys.exit(app.exec_())
