import QtQuick 2.14

import Kale 1.0

import 'Details'
import '../shared/components'

Item {
  id: root
  
  // Store reference to view model counterpart that can be set from main.qml
  property DetailsViewModel viewModel

  // Don't do just viewModel && viewModel.scrobble because we need to return a bool value instead of an undefined viewModel.scrobble
  property bool canDisplayScrobble: !!(viewModel && viewModel.scrobble)

  // Check if all remote scrobble data from Last.fm has loaded
  property bool hasLastfmTrackData: (
    canDisplayScrobble && !!viewModel.scrobble.lastfm_track
  )
  property bool hasLastfmArtistData: (
    canDisplayScrobble && !!viewModel.scrobble.lastfm_artist
  )
  property bool isTrackNotFound: (
    canDisplayScrobble && !viewModel.scrobble.lastfm_track && !viewModel.scrobble.is_loading
  )
  property bool hasTrackLoadingError: (
    canDisplayScrobble && viewModel.scrobble.has_error
  )

  signal switchToCurrentScrobble

  // --- No Scrobble Selected Page ---

  Item {
    visible: !canDisplayScrobble

    anchors.fill: parent

    Column {
      anchors.centerIn: parent

      Label {
        opacity: 0.5
        style: kTitleSecondary
        horizontalAlignment: Qt.AlignHCenter
        
        text: `No Scrobble Selected\n\n${viewModel.mediaPlayerName} is currently selected as your media player.`
      }
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
          visible: isTrackNotFound || hasTrackLoadingError

          fillMode: Image.TileHorizontally
          source: '../shared/resources/effects/bannerGradient.png'

          width: parent.width
          height: 30

          Label {
            text: (
              isTrackNotFound ? 
              'This track isn’t in Last.fm\'s database yet' :
              'Could not load track data from Last.fm, most likely a server outage'
            )
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
          property bool hasLastfmAlbum: (
            canDisplayScrobble
            && !!viewModel.scrobble.lastfm_track
            && !!viewModel.scrobble.lastfm_album
          )
          
          id: trackDetails

          isCurrentlyScrobbling: canDisplayScrobble && viewModel.isCurrentScrobble
          title: canDisplayScrobble && viewModel.scrobble.track_title
          lastfmUrl: hasLastfmTrackData && viewModel.scrobble.lastfm_track.url
          lastfmGlobalListeners: hasLastfmTrackData && viewModel.scrobble.lastfm_track.global_listeners
          lastfmGlobalPlays: hasLastfmTrackData && viewModel.scrobble.lastfm_track.global_plays
          lastfmPlays: hasLastfmTrackData && viewModel.scrobble.lastfm_track.plays
          lastfmTags: hasLastfmTrackData && viewModel.scrobble.lastfm_track.tags
          artistName: canDisplayScrobble && viewModel.scrobble.artist_name
          artistLastfmUrl: hasLastfmTrackData && viewModel.scrobble.lastfm_track.artist_link.url
          albumTitle: canDisplayScrobble && viewModel.scrobble.album_title
          albumLastfmUrl: hasLastfmAlbum && viewModel.scrobble.lastfm_album.url
          albumImageUrl: (
            canDisplayScrobble
            && !!viewModel.scrobble.image_set
            && viewModel.scrobble.image_set.medium_url
          )
          isTrackNotFound: root.isTrackNotFound
          isPlayerPaused: viewModel.isPlayerPaused
          isInMiniMode: viewModel.isInMiniMode

          width: column.width
        }

        ArtistDetails {
          // visible: !isTrackNotFound

          name: canDisplayScrobble && viewModel.scrobble.artist_name
          bio: hasLastfmArtistData && viewModel.scrobble.lastfm_artist.bio
          lastfmUrl: hasLastfmArtistData && viewModel.scrobble.lastfm_artist.url
          lastfmGlobalListeners: (
            hasLastfmArtistData && viewModel.scrobble.lastfm_artist.global_listeners
          )
          lastfmGlobalPlays: (
            hasLastfmArtistData && viewModel.scrobble.lastfm_artist.global_plays
          )
          lastfmPlays: hasLastfmArtistData && viewModel.scrobble.lastfm_artist.plays
          lastfmTags: hasLastfmArtistData ? viewModel.scrobble.lastfm_artist.tags : []
          spotifyArtists: canDisplayScrobble && viewModel.scrobble.spotify_artists
          isReadMoreLinkVisible: hasLastfmArtistData && viewModel.scrobble.lastfm_artist.bio
          hasLastfmData: hasLastfmArtistData
          isInMiniMode: viewModel.isInMiniMode

          width: column.width
        }

        // --- Similar Artists ---

        Item {
          visible: (
            !isInMiniMode
            && hasLastfmArtistData
            && viewModel.scrobble.lastfm_artist.similar_artists.length
          )

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
              model: hasLastfmArtistData && viewModel.scrobble.lastfm_artist.similar_artists

              delegate: Tag {
                name: modelData.name
                address: modelData.url
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
