from PySide2 import QtCore, QtGui, QtQuick, QtQml, QtNetwork

class NetworkImage(QtQuick.QQuickItem):
  has_image_changed = QtCore.Signal()
  should_blank_on_new_source_changed = QtCore.Signal()
  source_changed = QtCore.Signal()
  
  NETWORK_MANAGER = None
  RAM_IMAGE_CACHE = {}
  
  def __init__(self, parent=None):
    QtQuick.QQuickItem.__init__(self, parent)

    self._image = None
    self._reply = None

    # Store Qt Scene Graph node that will display texture
    self._node = None

    # This is set after _image is replaced with another source, and causes _image to be reconverted to a texture on the next updatePaintNode call
    self._should_refresh_node_texture = False

    # Internal variables for Qt Properties
    self._has_image = False # Trying to check _image for None causes unintended behavior because of Python to C++ translation, so a separate variable is needed to check whether an image exists
    self._should_blank_on_new_source = False
    self._source = None

    # Tell Qt that this component should render onscreen
    self.setFlag(QtQuick.QQuickItem.ItemHasContents, True)
  
  def updatePaintNode(self, old_node, data):
    if self._has_image:
      if self._node is None:
        self._node = QtQuick.QSGNode()
        new_texture_node = QtQuick.QSGSimpleTextureNode()
        self._node.appendChildNode(new_texture_node)
      
      texture_node = self._node.firstChild()
      
      if self._should_refresh_node_texture:
        new_texture = self.window().createTextureFromImage(self._image)
        texture_node.setFiltering(QtQuick.QSGTexture.Linear)
        texture_node.setTexture(new_texture)
        self._should_refresh_node_texture = False
      
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
    
    return self._node

  """Refresh the paint node with new image"""
  def update_image(self, image):
    self._image = image
    self._has_image = True
    self._should_refresh_node_texture = True
    self.has_image_changed.emit()

    # Request update of paint node
    self.update()
  
  """Convert recieved network data into QImage and update"""
  def handle_reply(self):
    if self._reply:
      if self._reply.error() == QtNetwork.QNetworkReply.NetworkError.NoError:
        image = QtGui.QImage.fromData(self._reply.readAll())

        # Add image to cache if not in cache
        if self._source not in NetworkImage.RAM_IMAGE_CACHE:
          NetworkImage.RAM_IMAGE_CACHE[self._source] = image
        
        self.update_image(image)
    
    # Delete reply as it's not needed anymore
    self._reply = None
  
  def set_should_blank_on_new_source(self, value):
    self._should_blank_on_new_source = value
    self.should_blank_on_new_source_changed.emit()
  
  def set_source(self, value):
    # Don't do anything if source is changed to the same value
    if not NetworkImage.NETWORK_MANAGER or value == self._source:
      return
    
    if value:
      self._source = value

      if self._should_blank_on_new_source:
        self._has_image = False
        self.has_image_changed.emit()
      
      # Cancel previous ongoing request if exists
      if self._reply:
        self._reply.abort()

      if self._source in NetworkImage.RAM_IMAGE_CACHE:
        # Immediately set image to cached version if exists
        self.update_image(NetworkImage.RAM_IMAGE_CACHE[self._source])
      else:
        # If cached image doesn't exist, tell network manager to request from source
        self._reply = NetworkImage.NETWORK_MANAGER.get(QtNetwork.QNetworkRequest(self._source))
        self._reply.finished.connect(self.handle_reply)
  
  hasImage = QtCore.Property(bool, lambda self: self._has_image, notify=has_image_changed)
  
  # Controls whether the view should immediately blank or keep showing cached content when a new URL is set. Should be true when the view needs to swap between entirely different images. (e.g. album art view in track details) Needs additional view to cover image view like in Picture component.
  shouldBlankOnNewSource = QtCore.Property(bool, lambda self: self._should_blank_on_new_source, set_should_blank_on_new_source, notify=should_blank_on_new_source_changed)

  # Set the source of the view. QUrl doesn't allow blank string - only None/undefined.
  source = QtCore.Property('QUrl', lambda self: self._source, set_source, notify=source_changed)