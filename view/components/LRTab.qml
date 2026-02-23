import QtQuick
Item{
	property bool active:false
	property alias content:xLabel.content
	signal clicked
	id:root
	width:xLabel.width+10*2
	height:20
	opacity:xMouse.containsPress?0.5:1
	Rectangle{
		anchors.fill:parent
		color:Qt.rgba(1,1,1,0.15)
		radius:999
		visible:active||xMouse.containsMouse
	}
	LRLabel{
		id:xLabel
		anchors.verticalCenter:parent.verticalCenter
		//style:active||xMouse.containsMouse?Text.Normal:Text.Sunken
		size:"h3"
		x:10
	}
	MouseArea{
		id:xMouse
		anchors.fill:parent
		onClicked:root.clicked()
		hoverEnabled:true
	}
}