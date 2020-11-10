import QtQuick 2.14

import '../../shared/components'

Item {
  id: root

  property url imageUrl
  property string name
  property bool isReadMoreLinkVisible

  // var to support undefined
  property var lastfmUrl
  property var lastfmGlobalListeners
  property var lastfmGlobalPlays
  property var lastfmPlays
  property var spotifyArtists
  property var bio

  property bool hasMultipleArtists: spotifyArtists.length > 1

  // var to support lists
  property var lastfmTags

  height: hasMultipleArtists ? Math.max(column.y + column.height + 30, multipleArtistImagesView.y + multipleArtistImagesView.height + 30) : Math.max(column.y + column.height + 30, singularArtistImageView.y + singularArtistImageView.height + 30)
  
  Column {
    id: column

    spacing: 15

    anchors {
      top: hasMultipleArtists ? multipleArtistImagesView.top : singularArtistImageView.top
      right: hasMultipleArtists ? multipleArtistImagesView.left : parent.right
      left: spotifyArtists.length ? (hasMultipleArtists ? parent.left : singularArtistImageView.right) : parent.left

      topMargin: spotifyArtists.length ? (hasMultipleArtists ? 0 : 10) : 0
      leftMargin: spotifyArtists.length ? (hasMultipleArtists ? 30 : 20) : 30
      rightMargin: hasMultipleArtists ? 20 : 30
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
      width: parent.width
      
      Statistic {
        title: 'Listeners'
        value: lastfmGlobalListeners === 0 ? 0 : (lastfmGlobalListeners || '---')
      }

      Statistic {
        title: 'Plays'
        value: lastfmGlobalPlays === 0 ? 0 : (lastfmGlobalPlays || '---')
      }

      Statistic {
        title: lastfmPlays === 1 ? 'Play in Library' : 'Plays in Library'
        value: lastfmPlays === 0 ? 0 : (lastfmPlays || '---')
        
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

    Column {
      spacing: 5

      width: parent.width

      SelectableText {
        text: bio || 'No bio available'

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

  // --- Multiple Artist Images ---

  Column {
    id: multipleArtistImagesView
    visible: hasMultipleArtists

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

  // --- Singular Artist Image ---

  Item {
    id: singularArtistImageView
    visible: spotifyArtists.length && !hasMultipleArtists
    width: singularArtistImage.width
    height: spotifyName.y + spotifyName.height

    anchors {
      top: parent.top
      left: parent.left

      margins: 30
    }

    Picture {
      id: singularArtistImage

      type: kArtist

      fillMode: Image.PreserveAspectCrop // Fill image instead of stretch
      source: spotifyArtists.length ? spotifyArtists[0].image_url : ''

      width: 139
      height: width

      anchors {
        top: parent.top
      }
    }

    Image {
      id: spotifyIcon
      
      source: '../../shared/resources/spotifyIconGreen.png'
      
      width: 21
      height: width

      anchors {
      top: singularArtistImage.bottom
        topMargin: 15

        left: parent.left
      }
    }

    Link {
      id: spotifyName

      text: spotifyArtists.length ? spotifyArtists[0].name : ''
      address: spotifyArtists.length ? spotifyArtists[0].spotify_url : ''
    
      wrapMode: Text.Wrap

      anchors {
        top: spotifyIcon.top
        right: parent.right
        left: spotifyIcon.right
        
        topMargin: 3
        leftMargin: 8
      } 
    }
  }
}