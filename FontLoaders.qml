import QtQuick 2.14

Item {
  property alias name: regular.name

  FontLoader {
    id: regular

    source: 'shared/resources/fonts/Inter-Regular.ttf'
  }

  FontLoader {
    source: 'shared/resources/fonts/Inter-Medium.ttf'
  }

  FontLoader {
    source: 'shared/resources/fonts/Inter-SemiBold.ttf'
  }

  FontLoader {
    source: 'shared/resources/fonts/Inter-Bold.ttf'
  }
}
