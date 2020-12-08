import QtQuick 2.14

import Kale 1.0

import 'Details'
import '../shared/components'

Item {
  id: root
  
  // Store reference to view model counterpart that can be set from main.qml
  property DetailsViewModel viewModel
  property alias isInMiniMode: trackDetails.isInMiniMode

  // Don't do just viewModel && viewModel.scrobbleTrackData because we need to return a bool value instead of an undefined viewModel.scrobbleTrackData
  property bool canDisplayScrobble: (viewModel && viewModel.scrobbleTrackData) ? true : false

  // Check if all remote scrobble data from Last.fm has loaded
  property bool hasLastfmData: canDisplayScrobble && viewModel.scrobbleTrackData.loading_state === 'LASTFM_TRACK_LOADED'
  property bool isTrackNotFound: canDisplayScrobble && viewModel.scrobbleTrackData.loading_state === 'LASTFM_TRACK_NOT_FOUND'

  signal switchToCurrentScrobble

  // --- No Scrobble Selected Page ---

  Item {
    visible: !canDisplayScrobble

    anchors.fill: parent

    Label {
      opacity: 0.5
      style: kTitleSecondary
      
      text: 'No Scrobble Selected'

      anchors.centerIn: parent
    }
  }

  // --- Song Info Page (always keep in memory - just hide when no scrobble is selected) ---

  Item {
    visible: canDisplayScrobble

    anchors.fill: parent
    
    // Allow content to overflow and be scrolled
    Flickable {
      id: scrollArea
      
      contentHeight: column.height // Define scrollable area as tall as the content within

      anchors.fill: parent

      // Automatically position each component below the previous one
      Column {
        id: column

        width: scrollArea.width
        
        // --- First time scrobble banner ---
  
        Image {
          visible: isTrackNotFound

          fillMode: Image.TileHorizontally
          source: '../shared/resources/effects/bannerGradient.png'

          width: parent.width
          height: 30

          Label {
            text: 'This track isn’t in Last.fm\'s database yet'
            isShadowEnabled: false
            color: 'black'
            elide: Text.ElideRight

            anchors {
              right: parent.right
              left: parent.left

              verticalCenter: parent.verticalCenter

              leftMargin: 15
              rightMargin: 15
            }
          }
        }

        TrackDetails {
          id: trackDetails

          property bool hasAlbum: canDisplayScrobble && !!viewModel.scrobbleTrackData.album.title

          isCurrentlyScrobbling: canDisplayScrobble && viewModel.isCurrentScrobble
          title: canDisplayScrobble && viewModel.scrobbleTrackData.title
          lastfmUrl: hasLastfmData && viewModel.scrobbleTrackData.lastfm_url
          lastfmGlobalListeners: hasLastfmData && viewModel.scrobbleTrackData.lastfm_global_listeners
          lastfmGlobalPlays: hasLastfmData && viewModel.scrobbleTrackData.lastfm_global_plays
          lastfmPlays: hasLastfmData && viewModel.scrobbleTrackData.lastfm_plays
          lastfmTags: hasLastfmData ? viewModel.scrobbleTrackData.lastfm_tags : []

          artistName: canDisplayScrobble && viewModel.scrobbleTrackData.artist.name
          artistLastfmUrl: hasLastfmData && viewModel.scrobbleTrackData.artist.lastfm_url

          albumTitle: hasAlbum ? viewModel.scrobbleTrackData.album.title : '' // Use blank string as fallback because the Text element used to render the album title won't accept undefined
          albumLastfmUrl: hasAlbum && hasLastfmData && viewModel.scrobbleTrackData.album.lastfm_url
          albumImageUrl: canDisplayScrobble ? (viewModel.scrobbleTrackData.album.image_url || '') : '' // Fall back to empty string if loading or if there is no image_url (Not tied to hasAlbum because we can still show art for tracks that aren't on Last.fm)
          isTrackNotFound: root.isTrackNotFound

          width: column.width
        }

        ArtistDetails {
          visible: !isTrackNotFound

          name: canDisplayScrobble && viewModel.scrobbleTrackData.artist.name
          bio: root.hasLastfmData ? viewModel.scrobbleTrackData.artist.lastfm_bio : null
          imageUrl: root.hasLastfmData ? viewModel.scrobbleTrackData.artist.image_url : ''
          
          lastfmUrl: root.hasLastfmData && viewModel.scrobbleTrackData.artist.lastfm_url
          lastfmGlobalListeners: root.hasLastfmData && viewModel.scrobbleTrackData.artist.lastfm_global_listeners
          lastfmGlobalPlays: root.hasLastfmData && viewModel.scrobbleTrackData.artist.lastfm_global_plays
          lastfmPlays: root.hasLastfmData && viewModel.scrobbleTrackData.artist.lastfm_plays
          lastfmTags: root.hasLastfmData ? viewModel.scrobbleTrackData.artist.lastfm_tags : []
          
          spotifyArtists: root.hasLastfmData ? viewModel.scrobbleTrackData.spotify_artists : []
          
          isReadMoreLinkVisible: root.hasLastfmData && viewModel.scrobbleTrackData.artist.lastfm_bio
          hasLastfmData: root.hasLastfmData

          width: column.width
        }

        // --- Similar Artists ---

        Item {
          visible: hasLastfmData && viewModel.scrobbleTrackData.artist.lastfm_similar_artists.length

          width: column.width
          height: similarArtists.y + similarArtists.height + 30

          // Background inside container because excess background height shouldn't count towards section height in column
          Rectangle {
            color: '#222'

            width: parent.width
            
            height: {
              if (scrollArea.contentHeight < scrollArea.height) {
                return 0 - parent.y + scrollArea.height
              }

              return parent.height
            }
          }

          Label {
            id: similarArtistsTitle

            style: kTitleTertiary
            text: 'Similar Artists'

            anchors {
              top: parent.top
              right: parent.right
              left: parent.left

              topMargin: 20
              rightMargin: 30
              leftMargin: 30
            }
          }

          Flow {
            id: similarArtists

            spacing: 8

            anchors {
              top: similarArtistsTitle.bottom
              right: parent.right
              left: parent.left

              topMargin: 15
              rightMargin: 30
              leftMargin: 30
            }

            Repeater {
              model: hasLastfmData ? viewModel.scrobbleTrackData.artist.lastfm_similar_artists : []

              delegate: Tag {
                name: modelData.name
                address: modelData.lastfm_url
              }
            }
          }
        }
      }
    }

    // Add native scrolling physics to scroll area
    WheelScrollArea {
      flickable: scrollArea

      anchors.fill: scrollArea
    }
  }

  Shortcut {
    sequence: 'Ctrl+J'
    context: Qt.ApplicationShortcut
    onActivated: switchToCurrentScrobble()
  }
}
