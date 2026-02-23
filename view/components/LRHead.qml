import QtQuick
import QtQuick.Layouts
Item{
	property alias content:title.content
	property alias child:slot.sourceComponent
	Layout.fillWidth:parent
	width:parent.width
	height:31
	LRLabel{
		id:title
		anchors.left:parent.left
		anchors.leftMargin:16
		anchors.verticalCenter:parent.verticalCenter
		size:"h4"
	}
	Loader{
		id:slot
		anchors.right:parent.right
		anchors.rightMargin:15
		anchors.verticalCenter:parent.verticalCenter
	}
}