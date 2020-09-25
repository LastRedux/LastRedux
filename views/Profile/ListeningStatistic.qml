Item {
  property alias title: titleLabel.text
  property alias subtitle: subtitleLabel.text
  property alias scrobbleCount: scrobbleCountLabel.text
  property alias scrobbleCountPercentage: scrobbleCountProgressBar.percentage

  height: scrobbleCountLabel.y + scrobbleCountLabel.height + 5

  anchors {
    top: parent.top
    left: parent.left

    margins: 30
  }

  // --- Picture ---

  Picture {
    id: picture

    anchors {
      top: parent.top
      left: parent.left

      topMargin: 5
      leftMargin: 15
    }
  }

  /// --- Title ---

  Label {
    id: titleLabel

    elide: Text.ElideRight
    maximumLineCount: 2

    style: kTitleSecondary
    text: 'Experience'
    wrapMode: Text.Wrap

    y: 5

    anchors {
      right: parent.right
      left: picture.right

      rightMargin: 15
      leftMargin: 10
    }
  }

  // --- Subtitle ---

  Label {
    id: subtitleLabel
    
    elide: Text.ElideRight
    maximumLineCount: 2

    text: 'Victoria Monét, Khalid & SG Lewis'
    wrapMode: Text.Wrap

    y: titleLabel.y + titleLabel.height + 1

    anchors {
      right: titleLabel.right
      left: titleLabel.left
    }
  }

  // --- Scrobble Count ---

  ProgressBar {
    id: scrobbleCountProgressBar

    percentage: 1

    y: {
      let topMargin = 7

      if (subtitleLabel.visible) {
        return subtitleLabel.y + subtitleLabel.height + topMargin
      }

      return titleLabel.y + titleLabel.height + topMargin
    }

    anchors {
      right: scrobbleCountLabel.left
      left: titleLabel.left

      rightMargin: 8
    }
  }

  Label {
    id: scrobbleCountLabel

    horizontalAlignment: Qt.AlignRight
    style: kTitleTertiary
    text: '000 plays'

    width: 62

    anchors {
      verticalCenter: scrobbleCountProgressBar.verticalCenter

      right: titleLabel.right
    }
  }
}