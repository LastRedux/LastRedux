import QtQuick 2.14

import Kale 1.0

import 'ScrobbleDetails'
import '../shared/components'

Item {
  // Store reference to view model counterpart that can be set from main.qml
  property ScrobbleDetailsViewModel viewModel

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
          trackName: canDisplayScrobble && viewModel.scrobbleTrackData.title
          trackLastFmUrl: canDisplayEntireScrobble && viewModel.scrobbleTrackData.lastfm_url
          trackPlays: canDisplayEntireScrobble ? viewModel.scrobbleTrackData.lastfm_plays : undefined

          artistName: canDisplayScrobble && viewModel.scrobbleTrackData.artist.name
          artistLastFmUrl: canDisplayEntireScrobble && viewModel.scrobbleTrackData.artist.lastfm_url

          albumName: canDisplayScrobble && viewModel.scrobbleTrackData.album.title
          albumLastFmUrl: canDisplayEntireScrobble && viewModel.scrobbleTrackData.album.lastfm_url

          albumImageUrl: {
            if (canDisplayEntireScrobble) {
              return viewModel.scrobbleTrackData.album.image_url
            }
            
            return ''
          }

          width: column.width
        }

        ArtistDetails {
          name: {
            console.log(viewModel.scrobbleTrackData.artist)
            
            return canDisplayScrobble && viewModel.scrobbleTrackData.artist.name
          }
          lastFmUrl: canDisplayEntireScrobble && viewModel.scrobbleTrackData.artist.lastfm_url
          bio: canDisplayEntireScrobble ? viewModel.scrobbleTrackData.artist.bio : 'Loading Bio...'
          isReadMoreLinkVisible: canDisplayEntireScrobble && viewModel.scrobbleTrackData.artist.bio
          globalListeners: canDisplayEntireScrobble ? viewModel.scrobbleTrackData.artist.lastfm_global_listeners : undefined
          globalPlays: canDisplayEntireScrobble ? viewModel.scrobbleTrackData.artist.lastfm_global_plays : undefined
          plays: canDisplayEntireScrobble ? viewModel.scrobbleTrackData.artist.lastfm_plays : undefined

          imageUrl: {
            if (canDisplayEntireScrobble) {
              return viewModel.scrobbleTrackData.artist.image_url
            }
            
            return ''
          }

          width: column.width
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
