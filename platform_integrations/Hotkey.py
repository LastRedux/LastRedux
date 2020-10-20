from PySide2 import QtCore, QtGui

class Hotkey(QtCore.QObject):
  activated = QtCore.Signal()
  released = QtCore.Signal()
  isRegisteredChanged = QtCore.Signal(bool)

  def __init__(shortcut, should_register=False, application=None):
    pass
  
  def set_shortcut_from_key_code(self, key_code, modifiers, should_register, application):
    pass
  
  def set_native_shortcut(self, shortcut, should_register, application):
    pass

  def get_key_code(self):
    pass

  def get_modifiers(self):
    pass

  def get_current_native_shortcut(self):
    pass
  
  # --- Qt Property Getters and Setters ---

  def get_is_registered(self):
    pass

  def get_shortcut(self):
    pass

  def set_is_registered(self):
    pass

  def set_shortcut(new_shortcut, should_register):
    if new_shortcut is None:
      return reset_shortcut()
    elif new_shortcut.count() > 1:
      print('Shortcuts with chords cannot be used')
    
    self.set_shortcut_from_key_code(QtGui.Key)

  # --- Qt Properties ---

  isRegistered = QtCore.Property(bool, get_is_registered, set_registered, notify=is_registered_change)
  shortcut = QtCore.Property(QtGui.QKeySequence, get_shortcut, set_shortcut, reset=reset_shortcut)