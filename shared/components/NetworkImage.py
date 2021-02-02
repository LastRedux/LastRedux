from PySide2 import QtCore, QtGui, QtQuick, QtQml, QtNetwork

class NetworkImage(QtQuick.QQuickItem):
  has_image_changed = QtCore.Signal()
  should_blank_on_new_source_changed = QtCore.Signal()
  source_changed = QtCore.Signal()
  
  NETWORK_MANAGER = None
  RAM_IMAGE_CACHE = {}
  
  def __init__(self, parent=None):
    QtQuick.QQuickItem.__init__(self, parent)

    self.__image = None
    self.__reply = None

    # Store Qt Scene Graph node that will display texture
    self.__node = None

    # This is set after _image is replaced with another source, and causes _image to be reconverted to a texture on the next updatePaintNode call
    self.__should_refresh_node_texture = False

    # Internal variables for Qt Properties
    self.__has_image = False # Trying to check _image for None causes unintended behavior because of Python to C++ translation, so a separate variable is needed to check whether an image exists
    self.__should_blank_on_new_source = False
    self.__source: str = None

    # Tell Qt that this component should render onscreen
    self.setFlag(QtQuick.QQuickItem.ItemHasContents, True)
  
  def updatePaintNode(self, old_node, data):
    if self.__has_image:
      if self.__node is None:
        self.__node = QtQuick.QSGNode()
        new_texture_node = QtQuick.QSGSimpleTextureNode()
        self.__node.appendChildNode(new_texture_node)
      
      texture_node = self.__node.firstChild()
      
      if self.__should_refresh_node_texture:
        new_texture = self.window().createTextureFromImage(self.__image)
        texture_node.setFiltering(QtQuick.QSGTexture.Linear)
        texture_node.setTexture(new_texture)
        self.__should_refresh_node_texture = False
      
      # Get size values for aspect ratio calculation
      bounding_rect = self.boundingRect()
      texture_size = texture_node.texture().textureSize()

      # Make the texture node (which is a child of the main node) fill the full component bounds
      texture_node.setRect(bounding_rect)

      if (texture_size.width() > texture_size.height()): # Account for Spotify images that are wider than their container
        # Calculate portion of texture to use to correct for container's aspect ratio
        slice_width = (bounding_rect.width() / bounding_rect.height()) * texture_size.height()
        slice_x = (texture_size.width() / 2) - (slice_width / 2)

        # Use calculated slice as area of texture to apply to the texture node
        texture_node.setSourceRect(slice_x, 0, slice_width, texture_size.height())
      else: # Account for album images being applied to a wider container
        slice_height = (bounding_rect.height() / bounding_rect.width()) * texture_size.width()
        slice_y = (texture_size.height() / 2) - (slice_height / 2)
        texture_node.setSourceRect(0, slice_y, texture_size.width(), slice_height)
    
    return self.__node

  def update_image(self, image):
    '''Refresh the paint node with new image'''

    self.__image = image
    self.__has_image = True
    self.__should_refresh_node_texture = True
    self.has_image_changed.emit()

    # Request update of paint node
    self.update()
  
  def handle_reply(self):
    '''Convert recieved network data into QImage and update'''

    if self.__reply:
      if self.__reply.error() == QtNetwork.QNetworkReply.NoError:
        image = QtGui.QImage.fromData(self.__reply.readAll())

        # Add image to cache if not in cache
        if self.__source not in NetworkImage.RAM_IMAGE_CACHE:
          NetworkImage.RAM_IMAGE_CACHE[self.__source] = image
        
        self.update_image(image)
    
    # Delete reply as it's not needed anymore
    self.__reply = None
  
  def set_should_blank_on_new_source(self, value):
    self.__should_blank_on_new_source = value
    self.should_blank_on_new_source_changed.emit()
  
  def set_source(self, value):
    # Don't do anything if source is changed to the same value
    if not NetworkImage.NETWORK_MANAGER or value == self.__source:
      return
    
    if not value:
      return
    
    self.__source = value

    if self.__should_blank_on_new_source:
      self.__has_image = False
      self.has_image_changed.emit()
    
    # Cancel previous ongoing request if exists
    if self.__reply:
      self.__reply.abort()

    if self.__source in NetworkImage.RAM_IMAGE_CACHE:
      # Immediately set image to cached version if exists
      self.update_image(NetworkImage.RAM_IMAGE_CACHE[self.__source])
    else:
      # If cached image doesn't exist, tell network manager to request from source
      self.__reply = NetworkImage.NETWORK_MANAGER.get(QtNetwork.QNetworkRequest(self.__source))
      self.__reply.finished.connect(self.handle_reply)
  
  # Qt Properties

  hasImage = QtCore.Property(bool, lambda self: self.__has_image, notify=has_image_changed)
  
  shouldBlankOnNewSource = QtCore.Property(bool, lambda self: self.__should_blank_on_new_source, set_should_blank_on_new_source, notify=should_blank_on_new_source_changed) # Controls whether the view should immediately blank or keep showing cached content when a new URL is set. Should be true when the view needs to swap between entirely different images. (e.g. album art view in track details) Needs additional view to cover image view like in Picture component.

  # Set the source of the view. QUrl doesn't allow blank string - only None/undefined.
  source = QtCore.Property('QUrl', lambda self: self.__source, set_source, notify=source_changed)