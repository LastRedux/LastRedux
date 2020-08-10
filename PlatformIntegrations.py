from PySide2 import QtCore, QtGui

class PlatformIntegrations(QtCore.QObject):
  def applyMacOsWindowTreatment(self):
    '''Apply settings to the macOS window object to make it seamless and force dark mode'''

    # Import macOS-specific libraries inside the function to avoid importing them on all platforms
    import AppKit
    import ctypes
    import objc

    # Get the system window ID of the first window
    # Other windows like preferences and onboarding should have the standard window style
    window_id = QtGui.QGuiApplication.allWindows()[0].winId()

    # Convert system window ID into Objective-C NSView object and get the NSWindow of the view
    window_view = objc.objc_object(c_void_p=ctypes.c_void_p(window_id))
    window = window_view.window()
    
    # Force dark mode to avoid the dreaded white line when light mode is active
    window.setAppearance_(AppKit.NSAppearance.appearanceNamed_(AppKit.NSAppearanceNameVibrantDark)) 
    
    # Remove the window titlebar background
    window.setTitlebarAppearsTransparent_(True)

    # Hide title from window titlebar
    window.setTitleVisibility_(AppKit.NSWindowTitleHidden)
    
    # Allow window content to overlap the titlebar, creating a seamless window appearance
    window.setStyleMask_(window.styleMask() | AppKit.NSFullSizeContentViewWindowMask)