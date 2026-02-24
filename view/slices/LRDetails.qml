import QtQuick
import QtQuick.Layouts
Rectangle{
	property string song:'song'
	property string artist:'artist'
	property string album:'album'
	property string songListeners:'0'
	property string songScrobbles:'0'
	property string songPlays:'0'
	property string artistListeners:'0'
	property string artistScrobbles:'0'
	property string artistPlays:'0'
	property string artistDesc:''
	color:"#111"
	ColumnLayout{
		width:parent.width
		Button{
			text:'Fetch Track'
			onClicked:vm.fetchTrack()
		}
		Rectangle{
			id:xSong
			Layout.fillWidth:true
			height:Math.max(xCover.height+30*2,xSongInfo.height+40*2)
			color:'#06ffffff'
			LRShadow{}
			Item{
				id:xCover
				width:181
				height:181
				x:30
				y:30
				LRTexture{res:'cover_lg'}
				LRIcon{
					anchors.centerIn:parent
					res:'song_lg'
					size:161
				}
			}
			ColumnLayout{
				id:xSongInfo
				spacing:15
				y:40
				anchors.right:parent.right
				anchors.left:xCover.right
				anchors.rightMargin:30
				anchors.leftMargin:20
				ColumnLayout{
					spacing:5
					RowLayout{
						LRPlaying{
							big:true
						}
						LRLabel{
							LRLink{}
							wrapMode:Text.Wrap
							content:song
							size:'h2'
						}
					}
					LRElide{LRLink{}content:artist;size:'h3'}
					LRElide{LRLink{}content:album}
				}
				RowLayout{
					spacing:20
					LRStat{content:'LISTENERS';value:songListeners}
					LRStat{content:'SCROBBLES';value:songScrobbles}
					LRStat{content:'PLAYS IN LIBRARY';value:songPlays}
				}
				RowLayout{
					spacing:8
					LRTag{content:'electronic'}
					LRTag{content:'j-pop'}
					LRTag{content:'electropop'}
				}
			}
		}
		Item{
			id:xArtist
			Layout.fillWidth:true
			height:Math.max(xArtistImage.height+30*2,xArtistInfo.height+40*2)
			Rectangle{
				id:xArtistImage
				width:139
				height:139
				x:30
				y:30
				LRTexture{res:'cover_m'}
				LRIcon{
					anchors.centerIn:parent
					res:'artist_lg'
					size:119
				}
			}
			ColumnLayout{
				id:xArtistInfo
				spacing:15
				y:40
				anchors.right:parent.right
				anchors.left:xArtistImage.right
				anchors.rightMargin:30
				anchors.leftMargin:20
				LRElide{content:artist;size:'h2'}
				RowLayout{
					spacing:20
					LRStat{content:'LISTENERS';value:artistListeners}
					LRStat{content:'SCROBBLES';value:artistScrobbles}
					LRStat{content:'PLAYS IN LIBRARY';value:artistPlays}
				}
				RowLayout{
					spacing:8
					LRTag{content:'electronic'}
					LRTag{content:'japanese'}
					LRTag{content:'j-pop'}
					LRTag{content:'electropop'}
				}
				ColumnLayout{
					Layout.fillWidth:parent
					spacing:8
					LRLabel{
						Layout.fillWidth:parent
						content:artistDesc
						wrapMode:Text.Wrap
					}
				}
			}
		}
	}
}
