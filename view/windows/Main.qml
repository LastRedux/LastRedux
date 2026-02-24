import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import LastRedux
ApplicationWindow{
	LRFonts{id:xFonts}
	property int section:2
	id:xApp
	visible:true
	title:'LastRedux'
	color:'#0c0c0c'
	width:957
	height:600


	LRViewModel{id:vm}
	Rectangle{
		id:xSidebar
		anchors.top:parent.top
		anchors.left:parent.left
		anchors.bottom:parent.bottom
		color:"#111"
		width:250

		Image{
			id:nav
			width:parent.width
			height:44
			source:'qrc:/sk_bar.png'
			z:1
			RowLayout{
				anchors.centerIn:parent
				spacing:0
				LRNavBtn{res:'tab_history';resActive:'tab_history_active';active:section===1;onClicked:section=1}
				LRNavBtn{res:'tab_profile';resActive:'tab_profile_active';active:section===2;onClicked:section=2}
				LRNavBtn{res:'tab_friends';resActive:'tab_friends_active';active:section===3;onClicked:section=3}
			}
			LRShadow{}
		}
		Item{
			id:body
			width:parent.width
			anchors.top:nav.bottom
			anchors.bottom:parent.bottom
			LRHistory{
				anchors.fill:parent
				visible:section===1
			}
			LRProfile{
				anchors.fill:parent
				visible:section===2
			}
			LRFriends{
				anchors.fill:parent
				visible:section===3
			}
		}
	}
	LRDetails{
		anchors.top:parent.top
		anchors.left:xSidebar.right
		anchors.bottom:parent.bottom
		anchors.right:parent.right
		anchors.leftMargin:1
	}
}