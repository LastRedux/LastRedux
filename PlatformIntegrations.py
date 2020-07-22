from PySide2 import QtCore, QtGui

class PlatformIntegrations(QtCore.QObject):
  def applyMacOsWindowTreatment():
    # Import macOS-specific libraries
    import AppKit
    import ctypes
    import objc

    window_id = QtGui.QGuiApplication.allWindows()[0].winId()
    window_view = objc.objc_object(c_void_p=ctypes.c_void_p(window_id))
    window = window_view.window()
    window.setAppearance_(AppKit.NSAppearance.appearanceNamed_(AppKit.NSAppearanceNameVibrantDark)) # Force dark mode
    window.setTitlebarAppearsTransparent_(True)
    window.setTitleVisibility_(AppKit.NSWindowTitleHidden)
    window.setStyleMask_(window.styleMask() | AppKit.NSFullSizeContentViewWindowMask) # Enable seamless window