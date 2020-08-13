import QtQuick 2.14

Column {
  property string title
  property string value
  
  spacing: 3

  Label {
    style: kNumber
    text: value
  }

  Label {
    style: kTitleTertiary
    text: title
  }
}