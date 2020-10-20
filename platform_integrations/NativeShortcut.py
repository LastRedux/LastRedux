class NativeShortcut:
  def __init__(key, modifier=0):
    self.key = key
    self.modifier = modifier
    self.__is_valid = False
  
  def is_valid(self):
    pass

  # TODO: Add is_equal function