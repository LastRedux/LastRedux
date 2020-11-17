import QtQuick 2.15

Label {
  id: root

  property var address
  
  signal clicked

  style: kTitleSecondary

  // Don't show underline for links that don't have an address loaded
  font.underline: address ? pointerHandlers.hovered : false 

  LinkPointerHandlers {
    id: pointerHandlers
    
    address: root.address
    text: root.text

    onClicked: root.clicked()

    // Limit area of pointer handlers to visible text
    width: root.contentWidth
    height: root.contentHeight
  }
}
