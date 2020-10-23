import QtQuick 2.14

import '../../shared/components'

Item {
  id: root

  property url imageUrl
  property string name
  property string lastfmUrl
  property string bio
  property bool isReadMoreLinkVisible
  property bool isNotInLastfmDatabase

  // var to support undefined
  property var lastfmGlobalListeners
  property var lastfmGlobalPlays
  property var lastfmPlays
  property var spotifyArtists

  // var to support lists
  property var lastfmTags

  height: Math.max(column.y + column.height + 30, artistImageView.y + artistImageView.height + 30)
  
  Column {
    id: column

    spacing: 15

    anchors {
      top: artistImageView.top
      right: artistImageView.left
      left: parent.left

      topMargin: 10
      rightMargin: 30
      leftMargin: 30
    }

    // --- Name ---

    Link {
      style: kTitlePrimary
      text: name
      address: lastfmUrl
      wrapMode: Text.Wrap

      width: parent.width
    }

    // --- Statistics ---
    
    Flow {
      id: statistics
      
      spacing: 20
      visible: lastfmPlays !== undefined

      width: parent.width
      
      Statistic {
        title: 'Listeners'
        value: lastfmGlobalListeners
      }

      Statistic {
        title: 'Plays'
        value: lastfmGlobalPlays
      }

      Statistic {
        title: lastfmPlays === 1 ? 'Play in Library' : 'Plays in Library'
        value: lastfmPlays
        shouldAbbreviate: false
      }
    }

    // --- Tags ---

    Flow {
      spacing: 8
      
      width: parent.width
      
      Repeater {
        model: lastfmTags

        delegate: Tag {
          name: modelData.name
          address: modelData.url
        }
      }
    }

    // --- Bio ---

    Rectangle {
      color: '#ffff00'
      width: parent.width
      height: 25
      visible: isNotInLastfmDatabase
      
      Text {
        text: 'This is the first time anybody has scrobbled this track!'
      }
    }

    Column {
      spacing: 5
      visible: !isNotInLastfmDatabase

      width: parent.width

      SelectableText {
        text: bio

        width: parent.width
      }

      Link {
        elide: Text.ElideRight
        text: 'Read more on Last.fm'
        address: lastfmUrl
        visible: isReadMoreLinkVisible // Only show if bio exists

        width: parent.width
      }
    }
  }

  // --- Artist Image ---

  Column {
    id: artistImageView

    width: 220
    spacing: 15

    anchors {
      top: parent.top
      right: parent.right

      margins: 30
    }

    Repeater {
      model: spotifyArtists

      delegate: Item {
        width: parent.width
        height: 52

        Picture {
          id: spotifyArtistImage

          type: kArtist
          
          fillMode: Image.PreserveAspectCrop // Fill image instead of stretch
          source: modelData.image_url

          width: 52
          height: width
        }

        Image {
          id: spotifyIcon
          
          source: '../../shared/resources/spotifyIconGreen.png'
          
          width: 21
          height: width

          anchors {
            left: spotifyArtistImage.right
            
            verticalCenter: spotifyArtistImage.verticalCenter
            
            leftMargin: 15
          }
        }

        Link {
          text: modelData.name

          address: modelData.spotify_url
          
          maximumLineCount: 2
          wrapMode: Text.Wrap
          elide: Text.ElideRight

          anchors {
            left: spotifyIcon.right
            right: parent.right

            verticalCenter: spotifyArtistImage.verticalCenter

            leftMargin: 8
          } 
        }
      }
    }
  }
}