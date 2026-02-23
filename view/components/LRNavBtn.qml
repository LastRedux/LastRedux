import QtQuick
Item{
	property alias res:xInactive.res
	property alias resActive:xActive.res
	property bool active:false
	signal clicked
	id:root
	width:54
	height:44
	opacity:xMouse.containsPress?0.5:1
	LRIcon{
		id:xInactive
		anchors.centerIn:parent
		visible:!active
		size:24
	}
	LRIcon{
		id:xActive
		anchors.centerIn:parent
		visible:active
		size:24
	}
	MouseArea{
		id:xMouse
		anchors.fill:parent
		onClicked:root.clicked()
	}
}