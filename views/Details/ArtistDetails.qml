import QtQuick 2.14

import '../Profile'
import '../../shared/components'

Item {
  id: root

  property bool isInMiniMode
  property string name
  property bool isReadMoreLinkVisible
  property bool hasLastfmData

  // var to support undefined
  property var lastfmUrl
  property var lastfmGlobalListeners
  property var lastfmGlobalPlays
  property var lastfmPlays
  property var spotifyArtists
  property var bio

  property bool hasMultipleArtists: !!spotifyArtists && spotifyArtists.length > 1

  // var to support lists
  property var lastfmTags

  height: (
    hasMultipleArtists ? 
      Math.max(
        column.y + column.height + 30,
        multipleArtistImagesView.y + multipleArtistImagesView.height + 30
      ) :
      Math.max(
        column.y + column.height + 30,
        friendArtistLeaderboard.y + friendArtistLeaderboard.height + 30
        // singularArtistImageView.y + singularArtistImageView.height + 30
      )
  )
  
  // --- Artist Information ---

  Column {
    id: column

    spacing: 15

    anchors {
      top: hasMultipleArtists ? multipleArtistImagesView.top : singularArtistImageView.top
      right: hasMultipleArtists ? multipleArtistImagesView.left : parent.right
      left: !!spotifyArtists ? (hasMultipleArtists ? parent.left : singularArtistImageView.right) : parent.left

      topMargin: (!!spotifyArtists && !isInMiniMode) ? (hasMultipleArtists ? 0 : 10) : 0
      leftMargin: !!spotifyArtists ? (hasMultipleArtists ? 30 : 20) : 30
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
        value: lastfmGlobalListeners === 0 ? 0 : (lastfmGlobalListeners || null)
      }

      Statistic {
        title: 'Plays'
        value: lastfmGlobalPlays === 0 ? 0 : (lastfmGlobalPlays || null)
      }

      Statistic {
        title: lastfmPlays === 1 ? 'Play in Library' : 'Plays in Library'
        value: lastfmPlays === 0 ? 0 : (lastfmPlays || null)
        
        shouldAbbreviate: false
      }
    }

    // --- Tags ---

    Flow {
      visible: !isInMiniMode
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
      visible: !isInMiniMode

      width: parent.width

      SelectableText {
        text: bio || 'No bio available.'
        visible: hasLastfmData

        width: parent.width
      }

      Link {
        elide: Text.ElideRight
        text: 'Read more on Last.fm...'
        address: lastfmUrl
        visible: isReadMoreLinkVisible // Only show if bio exists

        width: parent.width
      }

      // --- Bio Placeholder ---

      Column {
        spacing: 2
        visible: !hasLastfmData

        width: parent.width

        Placeholder {
          width: parent.width
        }

        Placeholder {
          width: parent.width - 40
        }
        
        Placeholder {
          width: parent.width
        }

        Placeholder {
          width: parent.width - 20
        }

        Placeholder {
          width: parent.width
        }

        Placeholder {
          width: Math.floor(parent.width / 4)
        }
      }
    }

    // --- Friend Artist Leaderboard ---

    Column {
      id: friendArtistLeaderboard
      spacing: 8
      visible: !isInMiniMode

      width: parent.width

      Label {
        text: 'Friend Leaderboard'
        style: kTitleTertiary
      }

      Column {
        spacing: 10

        width: parent.width
        visible: (
          hasLastfmData
          && !!viewModel.scrobble.friend_artist_leaderboard
          && viewModel.scrobble.friend_artist_leaderboard.length
        )

        Repeater {
          model: (
            hasLastfmData
            && !!viewModel.scrobble.friend_artist_leaderboard
            && viewModel.scrobble.friend_artist_leaderboard
          )

          delegate: ProfileStatistic {
            imageSource: modelData.image_url
            lastfmUrl: modelData.lastfm_url
            title: modelData.title
            plays: modelData.plays
            playsPercentage: modelData.percentage

            width: parent.width
          }
        }
      }

      // --- Leaderboard Placeholder ---

      Column {
        spacing: 2
        visible: !hasLastfmData || !viewModel.scrobble.friend_artist_leaderboard

        width: parent.width

        Placeholder {
          width: parent.width
        }

        Placeholder {
          width: parent.width - 40
        }
        
        Placeholder {
          width: parent.width - 60
        }

        Placeholder {
          width: parent.width - 80
        }
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
          shouldBlankOnNewSource: true
          
          source: modelData.image_url || ''

          width: 52
          height: 52
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

          address: modelData.url
          
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
    visible: !!spotifyArtists && !hasMultipleArtists
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

      source: !!spotifyArtists ? spotifyArtists[0].image_url : ''

      width: isInMiniMode ? 107 : 139
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

      text: !!spotifyArtists ? spotifyArtists[0].name : ''
      address: !!spotifyArtists ? spotifyArtists[0].url : ''
    
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