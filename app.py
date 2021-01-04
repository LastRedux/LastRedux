import os
import signal
import sys

import sentry_sdk
from loguru import logger
from PySide2 import QtCore, QtGui, QtQml, QtNetwork

# Initialize Sentry in production
if getattr(sys, 'frozen', False) or os.environ.get('ENABLE_SENTRY'):
  sentry_sdk.init(
    "https://d0fef6e3cd3c411a90fe61532982140e@o496413.ingest.sentry.io/5570752",
    traces_sample_rate=1.0
  )

# Configure loguru
logger.configure(
  handlers=[{
    'sink': sys.stderr,
    'format': '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>'
  }]
)

from platform_integrations.WindowStyle import WindowStyle
from ApplicationViewModel import ApplicationViewModel
from OnboardingViewModel import OnboardingViewModel
# from HistoryViewModel import HistoryViewModel
# from HistoryListModel import HistoryListModel
# from ProfileViewModel import ProfileViewModel
# from FriendsViewModel import FriendsViewModel
# from FriendsListModel import FriendsListModel
# from DetailsViewModel import DetailsViewModel
from shared.components.NetworkImage import NetworkImage

# Get the built application path
if getattr(sys, 'frozen', False):
  # If the application is run as a bundle, the PyInstaller bootloader extends the sys module by a flag frozen=True and sets the app path into variable _MEIPASS
  application_path = os.path.dirname(sys.executable) # sys._MEIPASS
else:
  application_path = os.path.dirname(os.path.abspath(__file__))

# Enable Ctrl-C to kill app
signal.signal(signal.SIGINT, signal.SIG_DFL)

# Store constants for registering types
MODULE_NAME = 'Kale'
MAJOR_VERSION = 1
MINOR_VERSION = 0

if __name__ == '__main__':
  # Create QML components from Python classes
  # major_version and minor_version represent major and minor version numbers for when we import it in QML
  QtQml.qmlRegisterType(ApplicationViewModel, MODULE_NAME, MAJOR_VERSION, MINOR_VERSION, 'ApplicationViewModel')
  QtQml.qmlRegisterType(OnboardingViewModel, MODULE_NAME, MAJOR_VERSION, MINOR_VERSION, 'OnboardingViewModel')
  # QtQml.qmlRegisterType(HistoryViewModel, MODULE_NAME, MAJOR_VERSION, MINOR_VERSION, 'HistoryViewModel')
  # QtQml.qmlRegisterType(HistoryListModel, MODULE_NAME, MAJOR_VERSION, MINOR_VERSION, 'HistoryListModel')
  # QtQml.qmlRegisterType(ProfileViewModel, MODULE_NAME, MAJOR_VERSION, MINOR_VERSION, 'ProfileViewModel')
  # QtQml.qmlRegisterType(FriendsViewModel, MODULE_NAME, MAJOR_VERSION, MINOR_VERSION, 'FriendsViewModel')
  # QtQml.qmlRegisterType(FriendsListModel, MODULE_NAME, MAJOR_VERSION, MINOR_VERSION, 'FriendsListModel')
  # QtQml.qmlRegisterType(DetailsViewModel, MODULE_NAME, MAJOR_VERSION, MINOR_VERSION, 'DetailsViewModel')
  QtQml.qmlRegisterType(NetworkImage, MODULE_NAME, MAJOR_VERSION, MINOR_VERSION, 'NetworkImage')

  # Enable retina support
  QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

  # Use render loop that supports persistent 60fps
  os.environ['QSG_RENDER_LOOP'] = 'windows'

  # Create system app
  app = QtGui.QGuiApplication(sys.argv)

  # Create network access manager for custom network image view to use to request image URLs
  network_manager = QtNetwork.QNetworkAccessManager()
  NetworkImage.NETWORK_MANAGER = network_manager

  # Initialize QML rendering engine
  engine = QtQml.QQmlApplicationEngine(parent=app)

  # Get the main QML file path and load it  
  file = os.path.join(application_path, 'main.qml')
  engine.load(QtCore.QUrl.fromLocalFile(file))

  # Apply macOS-specific code which changes the main window to a seamless appearance
  WindowStyle.applyMacOsWindowTreatment()
  
  # Use the app's status as an exit code
  sys.exit(app.exec_()) # exec_ to avoid collision with built in exec function
