import QtQuick
import QtQuick.Layouts
Item{
	property alias content:xLabel1.content
	property alias sub:xLabel2.content
	property alias date:xLabel3.content
	property bool active:false
	property int plays:-1
	property int playsMax:10
	signal clicked
	id:xRoot
	Layout.fillWidth:parent
	width:parent.width
	height:Math.max(44,xColumn.height+5*2)
	opacity:xMouse.containsPress?0.5:1
	LRTexture{
		res:'active'
		visible:active
		opacity:0.375
	}
	LRCover{
		id:xCover
		anchors.top:parent.top
		anchors.left:parent.left
		anchors.topMargin:5
		anchors.leftMargin:16
	}
	ColumnLayout{
		id:xColumn
		anchors.top:parent.top
		anchors.right:parent.right
		anchors.left:xCover.right
		anchors.topMargin:5
		anchors.leftMargin:10
		anchors.rightMargin:15
		spacing:2
		LRElide{
			id:xLabel1
			size:"h3"
		}
		LRElide{
			id:xLabel2
			visible:content!==""
		}
		LRElide{
			Layout.topMargin:1
			id:xLabel3
			visible:content!==""
			size:"h4"
		}
		LRProgress{
			visible:plays!==-1
			content:"▶︎ "+plays
			value:plays/playsMax
			cw:40
		}
	}
	MouseArea{
		id:xMouse
		anchors.fill:parent
		onClicked:xRoot.clicked
	}
}