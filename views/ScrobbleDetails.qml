import QtQuick 2.14

import Kale 1.0

import 'ScrobbleDetails'
import '../shared/components'

Item {
  // Store reference to view model counterpart that can be set from main.qml
  property ScrobbleDetailsViewModel viewModel

  property bool canDisplayScrobble: {
    // Don't do just viewModel && viewModel.scrobbleData because we need to return a bool value instead of an undefined viewModel.scrobbleData
    if (viewModel && viewModel.scrobbleData) {
      return true
    }

    return false
  }

  // Check if all remote scrobble data from Last.fm has loaded
  property bool canDisplayEntireScrobble: canDisplayScrobble && viewModel.scrobbleData.is_additional_data_downloaded

  // No scrobble selected page
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

  // Song info page (always keep in memory - just hide when no scrobble is selected)
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
          trackName: canDisplayScrobble && viewModel.scrobbleData.name
          trackLastFmUrl: canDisplayEntireScrobble && viewModel.scrobbleData.lastfm_url
          trackPlays: canDisplayEntireScrobble ? viewModel.scrobbleData.plays : undefined

          artistName: canDisplayScrobble && viewModel.scrobbleData.artist.name
          artistLastFmUrl: canDisplayEntireScrobble && viewModel.scrobbleData.artist.lastfm_url

          albumName: canDisplayScrobble && viewModel.scrobbleData.album.name
          albumLastFmUrl: canDisplayEntireScrobble && viewModel.scrobbleData.album.lastfm_url

          albumImageUrl: {
            if (canDisplayEntireScrobble) {
              return viewModel.scrobbleData.album.image_url
            }
            
            return ''
          }

          width: column.width
        }

        ArtistDetails {
          name: canDisplayScrobble && viewModel.scrobbleData.artist.name
          lastFmUrl: canDisplayEntireScrobble && viewModel.scrobbleData.artist.lastfm_url
          bio: canDisplayEntireScrobble ? viewModel.scrobbleData.artist.bio : 'Loading Bio...'
          globalListeners: canDisplayEntireScrobble ? viewModel.scrobbleData.artist.global_listeners : ''
          globalPlays: canDisplayEntireScrobble ? viewModel.scrobbleData.artist.global_plays : ''
          plays: canDisplayEntireScrobble ? viewModel.scrobbleData.artist.plays : ''

          imageUrl: {
            if (canDisplayEntireScrobble) {
              return viewModel.scrobbleData.artist.image_url
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
