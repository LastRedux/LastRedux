import QtQuick
Item {
  property alias name:regular.name
  FontLoader{
    id:regular
    source:'qrc:/Inter-Regular.ttf'
  }
  FontLoader {
    source:'qrc:/Inter-Medium.ttf'
  }
  FontLoader {
    source:'qrc:/Inter-SemiBold.ttf'
  }
  FontLoader {
    source:'qrc:/Inter-Bold.ttf'
  }
}