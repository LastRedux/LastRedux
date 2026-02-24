import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
Item{
	ColumnLayout{
		anchors.fill:parent
		spacing:0
		LRProfileLink{
			name:vm.name
			user:vm.user
			z:2
		}
		Rectangle{
			Layout.fillWidth:true
			color:'#1b1b1b'
			height:xOverview.height
			z:1
			ColumnLayout{
				id:xOverview
				width:parent.width
				spacing:5
				ColumnLayout{
					Layout.fillWidth:true
					Layout.topMargin:10
					Layout.rightMargin:15
					Layout.leftMargin:15
					LRLine{res:'song';content:"5,119 scrobbles"}
					LRLine{res:'clock';content:"58 plays today"}
					LRLine{res:'date';content:"24 plays per day"}
					LRLine{res:'artist';content:"656 artists in library"}
					LRLine{res:'heart';content:"0 loved tracks"}
				}
				Item{
					Layout.fillWidth:true
					height:34
					RowLayout{
						anchors.centerIn:parent
						LRTab{content:"Artists"}
						LRTab{content:"Tracks";active:true}
						LRTab{content:"Albums"}
					}
				}
			}
			LRShadow{}
		}
		Item{
			id:xTracks
			Layout.fillWidth:true
			Layout.fillHeight:true
			Flickable{
				id:xTracksFlick
				anchors.fill:parent
				contentHeight:xTracksColumn.height
				clip:true
				ColumnLayout{
					id:xTracksColumn
					width:parent.width
					spacing:0
					LRHead{
						content:'TOP THIS WEEK'
					}
					LREntry{
						content:'song'
						sub:'artist'
						plays:5
					}
					LREntry{
						content:'song'
						sub:'artist'
						plays:2
					}
					LREntry{
						content:'song'
						sub:'artist'
						plays:1
					}
					LRHead{
						content:'TOP THIS MONTH'
					}
					LREntry{
						content:'song'
						sub:'artist'
						plays:5
					}
					LREntry{
						content:'song'
						sub:'artist'
						plays:2
					}
					LREntry{
						content:'song'
						sub:'artist'
						plays:1
					}
				}
			}
			LRScroll{
				anchors.fill:xTracksFlick
				hook:xTracksFlick
			}
		}
	}
}
