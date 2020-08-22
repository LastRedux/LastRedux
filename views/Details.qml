import QtQuick 2.14

import Kale 1.0

import 'Details'
import '../shared/components'

Item {
  // Store reference to view model counterpart that can be set from main.qml
  property DetailsViewModel viewModel

  property bool canDisplayScrobble: {
    // Don't do just viewModel && viewModel.scrobbleTrackData because we need to return a bool value instead of an undefined viewModel.scrobbleTrackData
    if (viewModel && viewModel.scrobbleTrackData) {
      return true
    }

    return false
  }

  // Check if all remote scrobble data from Last.fm has loaded
  property bool canDisplayEntireScrobble: canDisplayScrobble && viewModel.scrobbleTrackData.has_lastfm_data

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

        TrackDetails {
          title: canDisplayScrobble ? viewModel.scrobbleTrackData.title : ''
          lastfmUrl: canDisplayEntireScrobble && viewModel.scrobbleTrackData.lastfm_url
          lastfmGlobalListeners: canDisplayEntireScrobble ? viewModel.scrobbleTrackData.lastfm_global_listeners : undefined
          lastfmGlobalPlays: canDisplayEntireScrobble ? viewModel.scrobbleTrackData.lastfm_global_plays : undefined
          lastfmPlays: canDisplayEntireScrobble ? viewModel.scrobbleTrackData.lastfm_plays : undefined
          lastfmTags: canDisplayEntireScrobble ? viewModel.scrobbleTrackData.lastfm_tags : []

          artistName: canDisplayScrobble && viewModel.scrobbleTrackData.artist.name
          artistLastfmUrl: canDisplayEntireScrobble && viewModel.scrobbleTrackData.artist.lastfm_url

          albumName: canDisplayScrobble && viewModel.scrobbleTrackData.album.title
          albumLastfmUrl: canDisplayEntireScrobble && viewModel.scrobbleTrackData.album.lastfm_url

          albumImageUrl: {
            if (canDisplayEntireScrobble) {
              return viewModel.scrobbleTrackData.album.image_url
            }
            
            return ''
          }

          width: column.width
        }

        ArtistDetails {
          name: canDisplayScrobble ? viewModel.scrobbleTrackData.artist.name : ''
          lastfmUrl: canDisplayEntireScrobble && viewModel.scrobbleTrackData.artist.lastfm_url
          bio: canDisplayEntireScrobble ? viewModel.scrobbleTrackData.artist.bio : 'Loading Bio...'
          isReadMoreLinkVisible: canDisplayEntireScrobble && viewModel.scrobbleTrackData.artist.bio
          lastfmGlobalListeners: canDisplayEntireScrobble ? viewModel.scrobbleTrackData.artist.lastfm_global_listeners : undefined
          lastfmGlobalPlays: canDisplayEntireScrobble ? viewModel.scrobbleTrackData.artist.lastfm_global_plays : undefined
          lastfmPlays: canDisplayEntireScrobble ? viewModel.scrobbleTrackData.artist.lastfm_plays : undefined
          lastfmTags: canDisplayEntireScrobble ? viewModel.scrobbleTrackData.artist.lastfm_tags : []

          imageUrl: {
            if (canDisplayEntireScrobble) {
              return viewModel.scrobbleTrackData.artist.image_url
            }
            
            return ''
          }

          width: column.width
        }

        // --- Similar Artists ---

        Item {
          visible: canDisplayEntireScrobble && viewModel.scrobbleTrackData.artist.similar_artists.length

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

            spacing: 20

            anchors {
              top: similarArtistsTitle.bottom
              right: parent.right
              left: parent.left

              topMargin: 15
              rightMargin: 30
              leftMargin: 30
            }

            Repeater {
              model: canDisplayEntireScrobble ? viewModel.scrobbleTrackData.artist.similar_artists : []

              delegate: SimilarArtist {
                name: modelData.name
                imageSource: modelData.image_url
                lastfmUrl: modelData.lastfm_url

                width: ((similarArtists.width + 20) / Math.floor(similarArtists.width / 170)) - 20
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
}
