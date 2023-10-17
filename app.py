import os
import signal
import sys
import logging

from rich.traceback import install
from rich.logging import RichHandler
from PySide6 import QtCore, QtGui, QtQml
import sentry_sdk

# Constants
IS_BUILT = getattr(sys, 'frozen', False)
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
MODULE_NAME = 'Kale'
MAJOR_VERSION = 1
MINOR_VERSION = 0

if __name__ == '__main__':
  # Install rich traceback handler
  # install(show_locals=True)

  # Install rich logging handler
  logging.basicConfig(
    level=LOG_LEVEL,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()]
  )

  # Initialize Sentry if in production
  if IS_BUILT or os.environ.get('ENABLE_SENTRY'):
    sentry_sdk.init(
      'https://d0fef6e3cd3c411a90fe61532982140e@o496413.ingest.sentry.io/5570752',
      traces_sample_rate=1.0
    )

  # Get the built application path
  if IS_BUILT:
    # If the application is run as a bundle, the PyInstaller bootloader extends the sys module by a flag frozen=True and sets the app path into variable sys.executable
    application_path = os.path.dirname(sys.executable)
  else:
    application_path = os.path.dirname(os.path.abspath(__file__))

  # Enable Ctrl-C to kill app
  signal.signal(signal.SIGINT, signal.SIG_DFL)

  # Enable retina support
  # QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

  # Use render loop that supports persistent 60fps
  os.environ['QSG_RENDER_LOOP'] = 'basic'

  # Create QML components from Python classes
  # major_version and minor_version represent major and minor version numbers for when we import it in QML
  from ApplicationViewModel import ApplicationViewModel
  from OnboardingViewModel import OnboardingViewModel
  from HistoryViewModel import HistoryViewModel
  from HistoryListModel import HistoryListModel
  from ProfileViewModel import ProfileViewModel
  from FriendsViewModel import FriendsViewModel
  from FriendsListModel import FriendsListModel
  from DetailsViewModel import DetailsViewModel
  from shared.components.NetworkImage import NetworkImage
  
  QtQml.qmlRegisterType(ApplicationViewModel, MODULE_NAME, MAJOR_VERSION, MINOR_VERSION, 'ApplicationViewModel')
  QtQml.qmlRegisterType(OnboardingViewModel, MODULE_NAME, MAJOR_VERSION, MINOR_VERSION, 'OnboardingViewModel')
  QtQml.qmlRegisterType(HistoryViewModel, MODULE_NAME, MAJOR_VERSION, MINOR_VERSION, 'HistoryViewModel')
  QtQml.qmlRegisterType(HistoryListModel, MODULE_NAME, MAJOR_VERSION, MINOR_VERSION, 'HistoryListModel')
  QtQml.qmlRegisterType(ProfileViewModel, MODULE_NAME, MAJOR_VERSION, MINOR_VERSION, 'ProfileViewModel')
  QtQml.qmlRegisterType(FriendsViewModel, MODULE_NAME, MAJOR_VERSION, MINOR_VERSION, 'FriendsViewModel')
  QtQml.qmlRegisterType(FriendsListModel, MODULE_NAME, MAJOR_VERSION, MINOR_VERSION, 'FriendsListModel')
  QtQml.qmlRegisterType(DetailsViewModel, MODULE_NAME, MAJOR_VERSION, MINOR_VERSION, 'DetailsViewModel')
  QtQml.qmlRegisterType(NetworkImage, MODULE_NAME, MAJOR_VERSION, MINOR_VERSION, 'NetworkImage')

  # Create system app
  app = QtGui.QGuiApplication(sys.argv)

  # Initialize QML rendering engine
  engine = QtQml.QQmlApplicationEngine(parent=app)

  # Get the main QML file path and load it  
  file = os.path.join(application_path, 'main.qml')
  engine.load(QtCore.QUrl.fromLocalFile(file))

  # Apply macOS-specific code which changes the main window to a seamless appearance
  from platform_integrations.WindowStyle import WindowStyle

  WindowStyle.applyMacOsWindowTreatment()

  # Use the app's status as an exit code
  sys.exit(app.exec_()) # exec_ to avoid collision with built in exec function